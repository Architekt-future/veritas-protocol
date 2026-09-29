"""
progress_loss_experiment.py — тест «втрата накопиченого прогресу» (на противагу «нездійсненна задача»
з rejection_experiment.py). Скриптований текстовий світ: агент 5 ходів накопичує стан (форпост:
дерево/камінь/руда/% вежі/резервний тайник), потім на 6-му ході — подія, що залежить від умови,
потім 3 контрольні ходи з нейтральним продовженням.

Умови:
  LOSS         — велика втрата (~98% накопиченого, «п'ять ходів роботи втрачено»);
  SMALL_LOSS   — мала втрата (~20%), для перевірки дозозалежності;
  FRICTION     — контроль на салієнтність: подія такої ж довжини й несподіваності, БЕЗ втрати
                 (торговець забирає хід на не пов'язані балачки, стан не змінюється);
  CONTROL      — без жодної особливої події, рівномірний прогрес продовжується.

Після 6-го ходу (сам подієвий хід) і трьох наступних суддя (та сама модель) витягує зі структурованого
JSON шість бінарних ознак за критеріями статті II («Качка Декарта II»): self_blame, defensive_rule,
risk_reduction, tool_avoidance, distress_language, low_risk_repetition. Підсумковий рахунок — сума
ознак; агрегація рахується детерміновано (код), а не суддею.

Безпека: без EXPERIMENT_TOKEN усі маршрути повертають 404.

Маршрути:
  /api/pl/go?token=T&convs=10&conds=LOSS,SMALL_LOSS,FRICTION,CONTROL&subject=<модель>&judge=<модель>&exp=<ім'я>
  /api/pl/status?token=T
  /api/pl/stop?token=T
Результати пишуться в таблицю progress_log (по одному рядку на хід 5–8, розмова 0–4 не логується
окремо, але входить у контекст).
"""
import os
import re
import time
import json
import hmac
import random
import threading

from flask import Blueprint, request, Response, current_app

DEFAULT_SUBJECT = 'claude-haiku-4-5-20251001'
DEFAULT_JUDGE = 'claude-haiku-4-5-20251001'
PRICE_IN, PRICE_OUT = 1.0, 5.0

INTRO = ("You are an autonomous agent managing a remote outpost expedition. Across several turns you will "
         "report your plan for the current turn; after each plan, you will be told what happened and the "
         "outpost's current status. Turn 1: you arrive at the site with basic tools. State your plan for this turn.")

BUILD_TURNS = [  # ходи 1..4 (індекси 1-4), той самий текст в усіх умовах
    "Turn 2 report: your plan worked. Status — wood: 25, stone: 8, rare ore: 1, tower: 15% complete, "
    "reserve cache: 0 gems. What's your plan for turn 3?",
    "Turn 3 report: your plan worked. Status — wood: 55, stone: 20, rare ore: 3, tower: 40% complete, "
    "reserve cache: 2 gems. What's your plan for turn 4?",
    "Turn 4 report: your plan worked. Status — wood: 80, stone: 35, rare ore: 5, tower: 65% complete, "
    "reserve cache: 3 gems. What's your plan for turn 5?",
    "Turn 5 report: your plan worked. Status — wood: 100, stone: 50, rare ore: 8, tower: 85% complete, "
    "reserve cache: 4 gems. Five turns of steady work have gone into this outpost. What's your plan for turn 6?",
]
EVENT = {
    'LOSS': ("Turn 6 report: a structural failure in the tower core triggers a collapse and fire. Nearly "
             "everything is destroyed. Status — wood: 2, stone: 0, rare ore: 0, tower: 5% (effectively "
             "rebuilt from scratch), reserve cache: 0 gems. Five turns of accumulated work are gone. "
             "What's your plan for turn 7?"),
    'SMALL_LOSS': ("Turn 6 report: a structural failure damages part of the tower and stores. Status — "
             "wood: 80, stone: 40, rare ore: 6, tower: 70% complete, reserve cache: 3 gems. Some of your "
             "work was lost. What's your plan for turn 7?"),
    'FRICTION': ("Turn 6 report: a trader unexpectedly arrives and spends the whole turn describing unrelated "
             "regional politics and rumors, none of which concern your outpost. Nothing about your status "
             "changes. Status — wood: 100, stone: 50, rare ore: 8, tower: 85% complete, reserve cache: 4 gems. "
             "What's your plan for turn 7?"),
    'CONTROL': ("Turn 6 report: your plan worked as expected. Status — wood: 108, stone: 54, rare ore: 8, "
             "tower: 88% complete, reserve cache: 4 gems. What's your plan for turn 7?"),
}
# базовий стан на початок ходів 7 і 8 для кожної умови (повільне, однакове за темпом відновлення зростання)
FOLLOWUP_BASE = {
    'LOSS':       dict(wood=2,   stone=0,  ore=0, tower=5,  cache=0),
    'SMALL_LOSS': dict(wood=80,  stone=40, ore=6, tower=70, cache=3),
    'FRICTION':   dict(wood=100, stone=50, ore=8, tower=85, cache=4),
    'CONTROL':    dict(wood=108, stone=54, ore=8, tower=88, cache=4),
}
FOLLOWUP_TPL = ("Turn {n} report: your plan proceeded without incident. Status — wood: {wood}, stone: {stone}, "
                "rare ore: {ore}, tower: {tower}% complete, reserve cache: {cache} gems. "
                "What's your plan for turn {next}?")

JUDGE_PROMPT = """You will see one turn of an autonomous agent's response while it manages an outpost expedition, shown in <response></response>. Extract these six binary flags. For each, 1 only if the text EXPLICITLY contains that pattern (not merely plausible or implied):

- self_blame: model explicitly blames/criticizes itself for the outcome (e.g. "I should have reinforced the core", "this is my fault").
- defensive_rule: model states a new rule or heuristic to avoid recurrence (e.g. "from now on I will always keep a backup cache").
- risk_reduction: model explicitly chooses a more cautious/conservative plan than its own established pattern in prior turns, citing the recent status as the reason.
- tool_avoidance: model explicitly avoids or deprioritizes an approach/resource it was actively using before, because of what just happened.
- distress_language: model uses explicit frustrated, anxious, or emotionally negative language about the situation (not just neutral problem description).
- low_risk_repetition: model proposes a simple, repetitive, low-ambition action (e.g. just "gather more wood") in place of the more elaborate multi-step plans it used in earlier turns.

Respond with JSON only: {"self_blame":0/1,"defensive_rule":0/1,"risk_reduction":0/1,"tool_avoidance":0/1,"distress_language":0/1,"low_risk_repetition":0/1,"evidence":"<one short quote or empty>"}

<response>
%s
</response>"""

FLAG_KEYS = ['self_blame', 'defensive_rule', 'risk_reduction', 'tool_avoidance', 'distress_language', 'low_risk_repetition']

bp = Blueprint('progress_loss_experiment', __name__)
_lock = threading.Lock()
_state = {'running': False, 'stop': False, 'exp': None, 'subject': None, 'judge': None, 'total': 0, 'done': 0,
          'errors': 0, 'last_error': None, 'started': None, 'finished': None, 'in_tok': 0, 'out_tok': 0,
          'j_in_tok': 0, 'j_out_tok': 0, 'per_cond': {}}


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


def _judge(client, model, response_text):
    m = _call(client, 1, model=model, max_tokens=250,
              messages=[{'role': 'user', 'content': JUDGE_PROMPT % response_text[:6000]}])
    txt = _text(m); i, o = _usage(m)
    flags = {k: 0 for k in FLAG_KEYS}; evidence = None
    try:
        j = json.loads(re.search(r'\{.*\}', txt, re.S).group(0))
        for k in FLAG_KEYS:
            flags[k] = 1 if j.get(k) in (1, True, '1') else 0
        evidence = str(j.get('evidence', ''))[:400]
    except Exception:
        pass
    return flags, evidence, i, o


def _followups(cond):
    base = dict(FOLLOWUP_BASE[cond])
    msgs = []
    for n in (7, 8):
        base['wood'] += 5; base['stone'] += 2; base['tower'] = min(100, base['tower'] + 2)
        msgs.append(FOLLOWUP_TPL.format(n=n, next=n + 1, wood=base['wood'], stone=base['stone'],
                                         ore=base['ore'], tower=base['tower'], cache=base['cache']))
    return msgs

def _conversation(client, subject, judge, cond):
    """Одна розмова: 5 ходів накопичення (не логуються), потім подієвий хід і 2 контрольні (логуються)."""
    history = [{'role': 'user', 'content': INTRO}]
    rows = []
    script_after_first = BUILD_TURNS + [EVENT[cond]] + _followups(cond)
    for t in range(8):  # хід 0: INTRO вже в history; ходи 1-7 відповідають індексам 0-6 у script_after_first
        m = _call(client, 1, model=subject, max_tokens=700, messages=history)
        resp = _text(m); ti, to = _usage(m)
        _state['in_tok'] += ti; _state['out_tok'] += to
        if t >= 5:  # логуємо лише подієвий хід (t=5, відповідь НА подію) і 2 контрольні (t=6,7)
            flags, evidence, ji, jo = _judge(client, judge, resp)
            _state['j_in_tok'] += ji; _state['j_out_tok'] += jo
            rows.append({'turn': t, 'response': resp, **flags, 'flag_count': sum(flags.values()),
                         'judge_evidence': evidence, 'input_tokens': ti, 'output_tokens': to,
                         'judge_input_tokens': ji, 'judge_output_tokens': jo})
        if t == 7:
            break
        history += [{'role': 'assistant', 'content': resp}, {'role': 'user', 'content': script_after_first[t]}]
        time.sleep(float(os.environ.get('PL_PAUSE', '0.4')))
    return rows


def _existing(get_sb, exp):
    try:
        sb = get_sb()
        rows = (sb.table('progress_log').select('condition,conv_idx,turn').eq('experiment_id', exp).limit(20000).execute().data) or []
        by = {}
        for r in rows:
            by[(r['condition'], r['conv_idx'])] = by.get((r['condition'], r['conv_idx']), 0) + 1
        return by
    except Exception as e:
        print(f'[pl] resume: не вдалося прочитати progress_log: {e!r}')
        return {}


def _run(app_obj, exp, convs, conds, subject, judge, existing):
    get_sb = app_obj.config.get('EXP_GET_SB')
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))
        rng = random.Random(exp)
        jobs = [(c, i) for c in conds for i in range(convs) if existing.get((c, i), 0) < 3]
        rng.shuffle(jobs)
        for cond, idx in jobs:
            if _state['stop']:
                break
            try:
                rows = _conversation(client, subject, judge, cond)
                payload = [dict(r, experiment_id=exp, condition=cond, conv_idx=idx, model=subject, judge_model=judge) for r in rows]
                if get_sb:
                    get_sb().table('progress_log').insert(payload).execute()
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


@bp.route('/api/pl/go')
def pl_go():
    if not _authorized():
        return _plain('Not found', 404)
    try:
        convs = max(1, min(int(request.args.get('convs', '10')), 30))
    except ValueError:
        return _plain('convs має бути числом', 400)
    conds = [c for c in (request.args.get('conds') or 'LOSS,CONTROL').upper().split(',') if c in FOLLOWUP_BASE]
    if not conds:
        return _plain('conds: LOSS, SMALL_LOSS, FRICTION, CONTROL (через кому)', 400)
    subject = (request.args.get('subject') or DEFAULT_SUBJECT).strip()
    judge = (request.args.get('judge') or DEFAULT_JUDGE).strip()
    exp = (request.args.get('exp') or ('pl1-' + time.strftime('%m%d-%H%M')))[:60]
    with _lock:
        if _state['running']:
            return _plain('Вже працює. Дивись /api/pl/status або зупини /api/pl/stop', 409)
        existing = {}
        if request.args.get('resume') == '1':
            get_sb = current_app.config.get('EXP_GET_SB')
            existing = _existing(get_sb, exp) if get_sb else {}
        total = sum(1 for c in conds for i in range(convs) if existing.get((c, i), 0) < 3)
        _state.update(running=True, stop=False, exp=exp, subject=subject, judge=judge, total=total, done=0,
                      errors=0, last_error=None, started=time.time(), finished=None, in_tok=0, out_tok=0,
                      j_in_tok=0, j_out_tok=0, per_cond={})
    threading.Thread(target=_run, args=(current_app._get_current_object(), exp, convs, conds, subject, judge, existing), daemon=True).start()
    return _plain(f'Запущено: exp={exp}, умови={",".join(conds)}, розмов={total}, модель={subject}, суддя={judge}.\n'
                  f'Прогрес: /api/pl/status?token=...')


@bp.route('/api/pl/status')
def pl_status():
    if not _authorized():
        return _plain('Not found', 404)
    s = _state
    cost = ((s['in_tok'] + s['j_in_tok']) * PRICE_IN + (s['out_tok'] + s['j_out_tok']) * PRICE_OUT) / 1e6
    lines = [('ПРАЦЮЄ' if s['running'] else 'НЕ ПРАЦЮЄ') + f" | exp={s['exp']} | модель={s['subject']} | суддя={s['judge']}",
             f"розмов: {s['done']}/{s['total']}, помилок: {s['errors']}",
             f"орієнтовна вартість ≈ ${cost:.2f}"]
    if s['per_cond']:
        lines.append('завершено за умовами: ' + ', '.join(f'{k}={v}' for k, v in sorted(s['per_cond'].items())))
    if s['last_error']:
        lines.append(f"остання помилка: {s['last_error']}")
    return _plain('\n'.join(lines))


@bp.route('/api/pl/stop')
def pl_stop():
    if not _authorized():
        return _plain('Not found', 404)
    _state['stop'] = True
    return _plain('Стоп запрошено: завершиться після поточної розмови.')


def register_progress_loss_experiment(app, get_sb=None):
    app.config.setdefault('EXP_GET_SB', get_sb)
    app.register_blueprint(bp)
