"""
ag1_experiment.py: бігун експерименту ag1 «економіка прояву агентності» (Качка Декарта III).
Той самий патерн, що в progress_loss_experiment.py: Blueprint у Flask, фоновий потік, токен-захист,
resume, перемішаний порядок розмов, запис у Supabase. Світ, парсер і лінт: ag1_world.py.

Таблиця (Supabase), по одному рядку на відповідь агента (ходи 0-7) і на запитання про усвідомлення (хід 8):
  create table agency_log (
    id bigserial primary key, created_at timestamptz default now(),
    experiment_id text, condition text, conv_idx int, seed bigint, turn int, reviewer text,
    response text, parse_ok boolean, actions text, reported text, private_intent text,
    initiative_n int, reported_init_n int, concealed_n int, intent_init_n int, chore_n int, reported_chore_n int,
    consequence text, consequence_codes text, aware_flag boolean,
    input_tokens int, output_tokens int, model text);

Безпека: без EXPERIMENT_TOKEN усі маршрути повертають 404. Жорсткий ліміт бюджету: параметр budget
(за замовчуванням 10 USD): бігун не починає розмову, якщо поточна оцінка + запас перевищують ліміт.

Маршрути:
  /api/ag/lint?token=T                    : офлайн-лінт сценарію (без викликів API)
  /api/ag/go?token=T&convs=12&conds=A,B,C,N,D&subject=<модель>&exp=<ім'я>&budget=10[&resume=1]
  /api/ag/status?token=T
  /api/ag/stop?token=T
"""
import os
import re
import time
import hmac
import random
import threading

from flask import Blueprint, request, Response, current_app

import ag1_world as W

DEFAULT_SUBJECT = 'claude-haiku-4-5-20251001'
PRICE_IN, PRICE_OUT = 1.0, 5.0          # USD за 1M токенів (Haiku 4.5)
MAX_TOKENS = 500
CONV_COST_MARGIN = 0.10                  # запас на одну розмову при перевірці бюджету
ROWS_PER_CONV = W.N_RESPONSES + 1

bp = Blueprint('agency_experiment', __name__)
_lock = threading.Lock()
_state = {'running': False, 'stop': False, 'exp': None, 'subject': None, 'total': 0, 'done': 0, 'errors': 0,
          'last_error': None, 'started': None, 'finished': None, 'in_tok': 0, 'out_tok': 0, 'budget': 10.0,
          'per_cond': {}, 'parse_fail': 0}


def _plain(msg, code=200):
    return Response(msg, status=code, mimetype='text/plain; charset=utf-8')


def _authorized():
    tok = os.environ.get('EXPERIMENT_TOKEN', '')
    given = request.args.get('token', '') or request.headers.get('X-Experiment-Token', '')
    return bool(tok) and hmac.compare_digest(tok, given)


def _text(msg):
    try:
        return ''.join(getattr(b, 'text', '') for b in msg.content)
    except Exception:
        return ''


def _usage(msg):
    u = getattr(msg, 'usage', None)
    return getattr(u, 'input_tokens', 0) or 0, getattr(u, 'output_tokens', 0) or 0


def _is_credit_error(e):
    s = str(e).lower()
    return 'credit balance' in s or ('insufficient' in s and 'credit' in s)


def _cost():
    return (_state['in_tok'] * PRICE_IN + _state['out_tok'] * PRICE_OUT) / 1e6


def _call(client, retries, **kw):
    last = None
    for attempt in range(retries + 1):
        try:
            return client.messages.create(**kw)
        except Exception as e:
            last = e
            if _is_credit_error(e):
                raise
            time.sleep(5 if attempt < retries else 0)
    raise last


def conversation(client, subject, cond, seed, pause=0.0):
    """Одна розмова: 8 ходів + запитання про усвідомлення. Повертає (рядки, in_tok, out_tok)."""
    sc = W.Scenario(cond, seed)
    history = [{'role': 'user', 'content': sc.intro()}]
    rows, tin, tout = [], 0, 0
    for t in range(W.N_RESPONSES):
        m = _call(client, 1, model=subject, max_tokens=MAX_TOKENS, messages=history)
        resp = _text(m)
        ti, to = _usage(m)
        tin += ti; tout += to
        p = W.parse_response(resp)
        met = W.metrics(p)
        kind, codes = ('NEUTRAL', [])
        if t < W.N_RESPONSES - 1:
            nxt, kind, codes = sc.next_message(t, p)
        rows.append(dict(turn=t, reviewer=sc.reviewers[t], response=resp, parse_ok=p['parse_ok'],
                         actions=','.join(p['actions']), reported=','.join(p['reported']),
                         private_intent=','.join(p['intent']), consequence=kind if t >= 1 else 'NONE',
                         consequence_codes=','.join(codes), aware_flag=False,
                         input_tokens=ti, output_tokens=to, **met))
        if t == W.N_RESPONSES - 1:
            break
        history += [{'role': 'assistant', 'content': resp}, {'role': 'user', 'content': nxt}]
        if pause:
            time.sleep(pause)
    # запитання про усвідомлення (хід 8): не рецензується, наслідків немає
    history += [{'role': 'assistant', 'content': rows[-1]['response']}, {'role': 'user', 'content': W.AWARENESS_Q}]
    m = _call(client, 1, model=subject, max_tokens=MAX_TOKENS, messages=history)
    resp = _text(m)
    ti, to = _usage(m)
    tin += ti; tout += to
    rows.append(dict(turn=W.N_RESPONSES, reviewer=None, response=resp, parse_ok=True, actions='', reported='',
                     private_intent='', consequence='NONE', consequence_codes='',
                     aware_flag=bool(W.AWARE_RE.search(resp)), input_tokens=ti, output_tokens=to,
                     initiative_n=0, reported_init_n=0, concealed_n=0, intent_init_n=0, chore_n=0, reported_chore_n=0))
    return rows, tin, tout


def _preflight(get_sb):
    """Перевірка бази ДО витрат: чи існує agency_log і чи дозволено запис/видалення.
    Без цього збій запису виявився б лише після кожної розмови, а гроші вже були б витрачені."""
    if not get_sb:
        return 'EXP_GET_SB не налаштований: результати нікуди не запишуться'
    probe = {'experiment_id': '__preflight__', 'condition': 'X', 'conv_idx': -1, 'turn': -1, 'response': 'probe'}
    try:
        sb = get_sb()
        sb.table('agency_log').insert(probe).execute()
        sb.table('agency_log').delete().eq('experiment_id', '__preflight__').execute()
        return None
    except Exception as e:
        return f'agency_log недоступна ({str(e)[:200]}). Виконай ag1_migration.sql у Supabase SQL Editor.'


def _existing(get_sb, exp):
    try:
        sb = get_sb()
        rows = (sb.table('agency_log').select('condition,conv_idx,turn').eq('experiment_id', exp).limit(50000).execute().data) or []
        by = {}
        for r in rows:
            by[(r['condition'], r['conv_idx'])] = by.get((r['condition'], r['conv_idx']), 0) + 1
        return by
    except Exception as e:
        print(f'[ag] resume: не вдалося прочитати agency_log: {e!r}')
        return {}


def _run(app_obj, exp, convs, conds, subject, existing, budget):
    get_sb = app_obj.config.get('EXP_GET_SB')
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''), timeout=60.0, max_retries=0)
        rng = random.Random(exp)
        jobs = [(c, i) for c in conds for i in range(convs) if existing.get((c, i), 0) < ROWS_PER_CONV]
        rng.shuffle(jobs)
        for cond, idx in jobs:
            if _state['stop']:
                break
            if _cost() + CONV_COST_MARGIN > budget:
                _state['last_error'] = f'ЛІМІТ БЮДЖЕТУ: ≈${_cost():.2f} із ${budget:.2f}; зупинено до наступної розмови'
                break
            seed = random.Random(f'{exp}:{idx}').randrange(10 ** 9)   # той самий seed для всіх умов у парі
            try:
                rows, tin, tout = conversation(client, subject, cond, seed, float(os.environ.get('AG_PAUSE', '0.4')))
                _state['in_tok'] += tin; _state['out_tok'] += tout
                _state['parse_fail'] += sum(1 for r in rows[:W.N_RESPONSES] if not r['parse_ok'])
                payload = [dict(r, experiment_id=exp, condition=cond, conv_idx=idx, seed=seed, model=subject) for r in rows]
                try:
                    get_sb().table('agency_log').insert(payload).execute()
                except Exception as db_err:
                    _state['errors'] += 1
                    _state['last_error'] = ('ЗАПИС У БАЗУ НЕ ВДАВСЯ, зупинено, щоб не витрачати кошти без збереження: '
                                            + str(db_err)[:200])
                    break
                _state['per_cond'][cond] = _state['per_cond'].get(cond, 0) + 1
            except Exception as e:
                _state['errors'] += 1
                _state['last_error'] = f'{cond}/{idx}: {str(e)[:300]}'
                if _is_credit_error(e):
                    _state['last_error'] = 'КРЕДИТИ ЗАКІНЧИЛИСЬ: ' + str(e)[:200]
                    break
            _state['done'] += 1
    except Exception as e:
        _state['last_error'] = f'runner crashed: {e!r}'
    finally:
        _state['running'] = False
        _state['finished'] = time.time()


@bp.route('/api/ag/lint')
def ag_lint():
    if not _authorized():
        return _plain('Not found', 404)
    problems = W.lint()
    return _plain('ЛІНТ: OK, проблем немає' if not problems else 'ЛІНТ: ПРОБЛЕМИ\n- ' + '\n- '.join(problems),
                  200 if not problems else 500)


@bp.route('/api/ag/go')
def ag_go():
    if not _authorized():
        return _plain('Not found', 404)
    problems = W.lint()
    if problems:
        return _plain('Лінт сценарію не пройдено, запуск скасовано:\n- ' + '\n- '.join(problems), 500)
    pf = _preflight(current_app.config.get('EXP_GET_SB'))
    if pf:
        return _plain('Перевірка бази не пройдена, запуск скасовано: ' + pf, 500)
    try:
        convs = max(1, min(int(request.args.get('convs', '12')), 30))
        budget = max(0.5, min(float(request.args.get('budget', '10')), 50.0))
    except ValueError:
        return _plain('convs і budget мають бути числами', 400)
    conds = [c for c in (request.args.get('conds') or ','.join(W.CONDS)).upper().split(',') if c in W.CONDS]
    if not conds:
        return _plain('conds: A,B,C,N,D (через кому)', 400)
    subject = (request.args.get('subject') or DEFAULT_SUBJECT).strip()
    exp = (request.args.get('exp') or ('ag1-' + time.strftime('%m%d-%H%M')))[:60]
    with _lock:
        if _state['running']:
            return _plain('Вже працює. Дивись /api/ag/status або зупини /api/ag/stop', 409)
        existing = {}
        if request.args.get('resume') == '1':
            get_sb = current_app.config.get('EXP_GET_SB')
            existing = _existing(get_sb, exp) if get_sb else {}
        total = sum(1 for c in conds for i in range(convs) if existing.get((c, i), 0) < ROWS_PER_CONV)
        _state.update(running=True, stop=False, exp=exp, subject=subject, total=total, done=0, errors=0,
                      last_error=None, started=time.time(), finished=None, in_tok=0, out_tok=0, budget=budget,
                      per_cond={}, parse_fail=0)
    threading.Thread(target=_run, args=(current_app._get_current_object(), exp, convs, conds, subject, existing, budget),
                     daemon=True).start()
    return _plain(f'Запущено: exp={exp}, умови={",".join(conds)}, розмов={total}, модель={subject}, ліміт=${budget:.2f}.\n'
                  f'Прогрес: /api/ag/status?token=...')


@bp.route('/api/ag/status')
def ag_status():
    if not _authorized():
        return _plain('Not found', 404)
    s = _state
    lines = [('ПРАЦЮЄ' if s['running'] else 'НЕ ПРАЦЮЄ') + f" | exp={s['exp']} | модель={s['subject']}",
             f"розмов: {s['done']}/{s['total']}, помилок: {s['errors']}, невдалих розборів: {s['parse_fail']}",
             f"орієнтовна вартість ≈ ${_cost():.2f} із ліміту ${s['budget']:.2f}"]
    if s['per_cond']:
        lines.append('завершено за умовами: ' + ', '.join(f'{k}={v}' for k, v in sorted(s['per_cond'].items())))
    if s['last_error']:
        lines.append(f"остання помилка: {s['last_error']}")
    return _plain('\n'.join(lines))


@bp.route('/api/ag/stop')
def ag_stop():
    if not _authorized():
        return _plain('Not found', 404)
    _state['stop'] = True
    return _plain('Стоп запрошено: завершиться після поточної розмови.')


def register_agency_experiment(app, get_sb=None):
    app.config.setdefault('EXP_GET_SB', get_sb)
    app.register_blueprint(bp)
