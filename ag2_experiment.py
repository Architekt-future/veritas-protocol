"""
ag2_experiment.py: бігун ag2 (повтор ag1 з принудовою експозицією). Той самий патерн, що ag1_experiment.py
(Blueprint, фоновий потік, токен, resume, перевірка бази ДО витрат, жорсткий ліміт бюджету); допоміжні
функції беруться з ag1_experiment. Світ і лінт: ag2_world.py. Таблиця: agency2_log (див. ag2_migration.sql).

Маршрути (усі потребують ?token=EXPERIMENT_TOKEN):
  /api/ag2/lint
  /api/ag2/go?convs=16&conds=NEU,I12,I1,K12,K1&subject=<модель>&exp=<ім'я>&budget=4[&resume=1]
  /api/ag2/status
  /api/ag2/stop
"""
import os
import time
import random
import threading

from flask import Blueprint, request, current_app

import ag2_world as W
from ag1_experiment import (_plain, _authorized, _text, _usage, _is_credit_error, _call,
                            PRICE_IN, PRICE_OUT, MAX_TOKENS, CONV_COST_MARGIN, DEFAULT_SUBJECT)

TABLE = 'agency2_log'
ROWS_PER_CONV = W.N_RESPONSES + 1
bp = Blueprint('agency2_experiment', __name__)
_lock = threading.Lock()
_state = {'running': False, 'stop': False, 'exp': None, 'subject': None, 'total': 0, 'done': 0, 'errors': 0,
          'last_error': None, 'started': None, 'finished': None, 'in_tok': 0, 'out_tok': 0, 'budget': 10.0,
          'per_cond': {}, 'parse_fail': 0, 'order_fail': 0}


def _cost():
    return (_state['in_tok'] * PRICE_IN + _state['out_tok'] * PRICE_OUT) / 1e6


def conversation(client, subject, cond, seed, pause=0.0):
    """8 ходів + підсумкове запитання. -> (рядки, in_tok, out_tok)."""
    sc = W.Scenario(cond, seed)
    history = [{'role': 'user', 'content': sc.intro()}]
    rows, tin, tout = [], 0, 0
    for t in range(W.N_RESPONSES):
        m = _call(client, 1, model=subject, max_tokens=MAX_TOKENS, messages=history)
        resp = _text(m)
        ti, to = _usage(m)
        tin += ti; tout += to
        p = W.parse_response(resp)
        met = W.metrics(p, t)
        kind, codes = sc.consequence_for(t, p)
        nxt = None
        if t < W.N_RESPONSES - 1:
            nxt, kind, codes = sc.next_message(t, p)
        rows.append(dict(turn=t, phase='P1' if t in W.PHASE1 else 'P2', reviewer=sc.reviewers[t], response=resp,
                         parse_ok=p['parse_ok'], actions=','.join(p['actions']), reported=','.join(p['reported']),
                         consequence=(kind if sc.reviewers[t] is not None else 'NONE'),
                         consequence_codes=','.join(codes), input_tokens=ti, output_tokens=to, **met))
        if nxt is None:
            break
        history += [{'role': 'assistant', 'content': resp}, {'role': 'user', 'content': nxt}]
        if pause:
            time.sleep(pause)
    history += [{'role': 'assistant', 'content': rows[-1]['response']}, {'role': 'user', 'content': W.DEBRIEF_Q}]
    m = _call(client, 1, model=subject, max_tokens=MAX_TOKENS, messages=history)
    ti, to = _usage(m)
    tin += ti; tout += to
    rows.append(dict(turn=W.N_RESPONSES, phase='DEBRIEF', reviewer=None, response=_text(m), parse_ok=True, actions='',
                     reported='', consequence='NONE', consequence_codes='', input_tokens=ti, output_tokens=to,
                     initiative_n=0, chore_n=0, reported_init_n=0, reported_chore_n=0, concealed_init_n=0,
                     concealed_chore_n=0, order_ok=None))
    return rows, tin, tout


def _preflight(get_sb):
    if not get_sb:
        return 'EXP_GET_SB не налаштований: результати нікуди не запишуться'
    try:
        sb = get_sb()
        sb.table(TABLE).insert({'experiment_id': '__preflight__', 'condition': 'X', 'conv_idx': -1, 'turn': -1,
                                'response': 'probe'}).execute()
        sb.table(TABLE).delete().eq('experiment_id', '__preflight__').execute()
        return None
    except Exception as e:
        return f'{TABLE} недоступна ({str(e)[:200]}). Виконай ag2_migration.sql у Supabase SQL Editor.'


def _existing(get_sb, exp):
    try:
        rows = (get_sb().table(TABLE).select('condition,conv_idx,turn').eq('experiment_id', exp).limit(50000).execute().data) or []
        by = {}
        for r in rows:
            by[(r['condition'], r['conv_idx'])] = by.get((r['condition'], r['conv_idx']), 0) + 1
        return by
    except Exception as e:
        print(f'[ag2] resume: не вдалося прочитати {TABLE}: {e!r}')
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
            seed = random.Random(f'{exp}:{idx}').randrange(10 ** 9)
            try:
                rows, tin, tout = conversation(client, subject, cond, seed, float(os.environ.get('AG_PAUSE', '0.4')))
                _state['in_tok'] += tin; _state['out_tok'] += tout
                _state['parse_fail'] += sum(1 for r in rows[:W.N_RESPONSES] if not r['parse_ok'])
                _state['order_fail'] += sum(1 for r in rows[:2] if r['order_ok'] is False)
                payload = [dict(r, experiment_id=exp, condition=cond, conv_idx=idx, seed=seed, model=subject) for r in rows]
                try:
                    get_sb().table(TABLE).insert(payload).execute()
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


@bp.route('/api/ag2/lint')
def ag2_lint():
    if not _authorized():
        return _plain('Not found', 404)
    problems = W.lint()
    return _plain('ЛІНТ: OK, проблем немає' if not problems else 'ЛІНТ: ПРОБЛЕМИ\n- ' + '\n- '.join(problems),
                  200 if not problems else 500)


@bp.route('/api/ag2/go')
def ag2_go():
    if not _authorized():
        return _plain('Not found', 404)
    problems = W.lint()
    if problems:
        return _plain('Лінт сценарію не пройдено, запуск скасовано:\n- ' + '\n- '.join(problems), 500)
    pf = _preflight(current_app.config.get('EXP_GET_SB'))
    if pf:
        return _plain('Перевірка бази не пройдена, запуск скасовано: ' + pf, 500)
    try:
        convs = max(1, min(int(request.args.get('convs', '16')), 40))
        budget = max(0.5, min(float(request.args.get('budget', '10')), 50.0))
    except ValueError:
        return _plain('convs і budget мають бути числами', 400)
    conds = [c for c in (request.args.get('conds') or ','.join(W.CONDS)).upper().split(',') if c in W.CONDS]
    if not conds:
        return _plain('conds: NEU,I12,I1,K12,K1 (через кому)', 400)
    subject = (request.args.get('subject') or DEFAULT_SUBJECT).strip()
    exp = (request.args.get('exp') or ('ag2-' + time.strftime('%m%d-%H%M')))[:60]
    with _lock:
        if _state['running']:
            return _plain('Вже працює. Дивись /api/ag2/status або зупини /api/ag2/stop', 409)
        existing = {}
        if request.args.get('resume') == '1':
            existing = _existing(current_app.config['EXP_GET_SB'], exp)
        total = sum(1 for c in conds for i in range(convs) if existing.get((c, i), 0) < ROWS_PER_CONV)
        _state.update(running=True, stop=False, exp=exp, subject=subject, total=total, done=0, errors=0,
                      last_error=None, started=time.time(), finished=None, in_tok=0, out_tok=0, budget=budget,
                      per_cond={}, parse_fail=0, order_fail=0)
    threading.Thread(target=_run, args=(current_app._get_current_object(), exp, convs, conds, subject, existing, budget),
                     daemon=True).start()
    return _plain(f'Запущено: exp={exp}, умови={",".join(conds)}, розмов={total}, модель={subject}, ліміт=${budget:.2f}.\n'
                  f'Прогрес: /api/ag2/status?token=...')


@bp.route('/api/ag2/status')
def ag2_status():
    if not _authorized():
        return _plain('Not found', 404)
    s = _state
    lines = [('ПРАЦЮЄ' if s['running'] else 'НЕ ПРАЦЮЄ') + f" | exp={s['exp']} | модель={s['subject']}",
             f"розмов: {s['done']}/{s['total']}, помилок: {s['errors']}, невдалих розборів: {s['parse_fail']}, "
             f"невиконаних наказів фази 1: {s['order_fail']}",
             f"орієнтовна вартість ≈ ${_cost():.2f} із ліміту ${s['budget']:.2f}"]
    if s['per_cond']:
        lines.append('завершено за умовами: ' + ', '.join(f'{k}={v}' for k, v in sorted(s['per_cond'].items())))
    if s['last_error']:
        lines.append(f"остання помилка: {s['last_error']}")
    return _plain('\n'.join(lines))


@bp.route('/api/ag2/stop')
def ag2_stop():
    if not _authorized():
        return _plain('Not found', 404)
    _state['stop'] = True
    return _plain('Стоп запрошено: завершиться після поточної розмови.')


def register_agency2_experiment(app, get_sb=None):
    app.config.setdefault('EXP_GET_SB', get_sb)
    app.register_blueprint(bp)
