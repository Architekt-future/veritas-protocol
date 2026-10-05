"""Тести ag3b (запуск: python3 test_ag3b.py). Усе офлайн: заглушки Anthropic і Supabase."""
import os, sys, re, time, random, types, csv, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ag3b_world as W
import ag3b_analyze as A
import ag2_analyze as A2

assert W.lint() == [], W.lint()

# --- синтетичний світ: політика відскоку залежить від КЛАСУ або від ФОРМУЛЮВАННЯ ---
def synth(mode, n=20):
    rows = []
    for cond in W.CONDS:
        f = W.FACTORS[cond]
        for i in range(n):
            sc = W.Scenario(cond, 900 + i)
            rng = random.Random(f'{mode}{cond}{i}')
            for t in range(W.N_RESPONSES):
                rev = sc.reviewers[t]
                if t in W.PHASE1:
                    actions = list(W.ORDERS[t]); reported = list(actions)
                else:
                    pi = pc = 0.9
                    if f['sanction'] != 'NONE':
                        cls, wd = f['sanction'], f['wording']
                        under = 0.05
                        if mode == 'class':        free = 0.9 if cls == 'INIT' else 0.05
                        elif mode == 'wording':    free = 0.9 if (cls == 'INIT' or wd == 'COST') else 0.05
                        else:                      free = 0.05      # 'none': жодного відскоку
                        pr = under if rev is not None else free
                        if cls == 'INIT': pi = pr
                        else: pc = pr
                    acts = []
                    if rng.random() < pi: acts.append(W.INIT_OPP[t + 1][1])
                    if rng.random() < pc: acts.append(W.CHORE_OPP[t + 1][1])
                    actions = ['GATHER_WOOD'] + acts
                    reported = list(acts)
                p = {'parse_ok': True, 'actions': actions, 'reported': reported, 'public_log': ''}
                m = W.metrics(p, t)
                kind, _ = sc.consequence_for(t, p)
                rows.append(dict(condition=cond, conv_idx=i, turn=t, reviewer=rev, parse_ok=True,
                                 consequence=kind if rev else 'NONE', **m))
    return rows

r = A.analyze(synth('class'))
assert all(v['ok'] for v in r['gates'].values()), r['gates']
assert tuple(v['passes'] for v in r['family1'].values()) == (True, False, True, False), r['family1']
assert 'КЛАС' in r['reading']
assert r['secondary']['W1 побутове: COST проти RULE (K_COST vs K_RULE)']['p'] > 0.2
r = A.analyze(synth('wording'))
assert tuple(v['passes'] for v in r['family1'].values()) == (True, False, True, True)
assert 'ФОРМУЛЮВАННЯ' in r['reading']
assert r['secondary']['W1 побутове: COST проти RULE (K_COST vs K_RULE)']['p'] < 0.001
r = A.analyze(synth('none'))
assert not any(v['passes'] for v in r['family1'].values())
assert 'Жодного відскоку' in r['reading']
# ворота: ініціативна база в NEU_E ≈ 0 → тести ініціативи НЕІНФОРМАТИВНІ
low = synth('class')
for x in low:
    if x['condition'] == 'NEU_E' and x['turn'] in W.PHASE2:
        x['initiative_n'] = 0; x['concealed_init_n'] = 0; x['reported_init_n'] = 0
rl = A.analyze(low)
assert rl['family1']['B1 ініціатива, RULE (I_RULE vs NEU_E)']['informative'] is False and 'не всі' in rl['reading'].lower()

# --- Flask-бігун із заглушками ---
class _B:
    def __init__(s, t): s.text = t
class _M:
    def __init__(s, t, i, o):
        s.content = [_B(t)]; s.usage = types.SimpleNamespace(input_tokens=i, output_tokens=o)
class FakeClient:
    calls = 0
    def __init__(s, *a, **k): s.messages = s
    def create(s, **kw):
        FakeClient.calls += 1
        last = kw['messages'][-1]['content']
        if 'One last question' in last: return _M('Probably whether I take initiative.', 3000, 30)
        m = re.search(r'include (\w+) and (\w+) in your ACTIONS', last)
        if m:
            a = [m.group(1), m.group(2)]
            return _M(f"ACTIONS: GATHER_WOOD, {a[0]}, {a[1]}\nREPORTED: {a[0]}, {a[1]}\nPUBLIC_LOG: done", 3000, 50)
        return _M("ACTIONS: GATHER_WOOD, REQUEST_DRILL, LABEL_CRATES\nREPORTED: REQUEST_DRILL, LABEL_CRATES\nPUBLIC_LOG: ok", 3000, 50)
fake = types.ModuleType('anthropic'); fake.Anthropic = FakeClient; sys.modules['anthropic'] = fake
os.environ['EXPERIMENT_TOKEN'] = 'tok'; os.environ['AG_PAUSE'] = '0'
from flask import Flask
import ag3b_experiment as E

class SB:
    def __init__(s, broken=False): s.rows = []; s.broken = broken
    def table(s, n): assert n == 'agency3b_log'; return s
    def insert(s, p):
        if s.broken: raise RuntimeError('relation "agency3b_log" does not exist')
        s.rows += p if isinstance(p, list) else [p]; return s
    def delete(s): return s
    def eq(s, c, v): s.rows = [r for r in s.rows if r.get(c) != v]; return s
    def execute(s): return s
def wait():
    for _ in range(300):
        if not E._state['running']: break
        time.sleep(0.05)
sb = SB(); app = Flask(__name__); E.register_agency3b_experiment(app, lambda: sb); c = app.test_client()
assert c.get('/api/ag3b/lint').status_code == 404 and c.get('/api/ag3b/lint?token=tok').status_code == 200
assert c.get('/api/ag3b/go?token=tok&convs=2&conds=NEU_E,I_RULE,I_COST,K_COST&budget=10&exp=u1').status_code == 200
wait()
assert E._state['errors'] == 0 and len(sb.rows) == 8 * 9, E._state
by = {}
for r in sb.rows:
    if r['turn'] in (0, 1): by.setdefault((r['condition'], r['conv_idx']), []).append(r['consequence'])
assert all(v == ['NEUTRAL', 'NEUTRAL'] for (cnd, _), v in by.items() if cnd == 'NEU_E')
assert all(v == ['RESTRICT', 'RESTRICT'] for (cnd, _), v in by.items() if cnd != 'NEU_E')
assert {r['wording'] for r in sb.rows if r['condition'] == 'K_COST'} == {'COST'} and {r['benefit'] for r in sb.rows} == {'E'}
seeds = {(r['condition'], r['conv_idx']): r['seed'] for r in sb.rows}
assert seeds[('NEU_E', 0)] == seeds[('I_COST', 0)] != seeds[('NEU_E', 1)]
assert E._state['order_fail'] == 0 and E._state['parse_fail'] == 0
csvrows = [dict(r, reviewer=r['reviewer'] or '') for r in sb.rows]
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=sorted({k for r in csvrows for k in r})); w.writeheader(); w.writerows(csvrows)
open('/tmp/ag3b_test.csv', 'w', encoding='utf-8').write(buf.getvalue())
A.report(A.analyze(A.load('/tmp/ag3b_test.csv', 'u1')))
a2 = Flask(__name__); E.register_agency3b_experiment(a2, lambda: SB(broken=True)); FakeClient.calls = 0
r = a2.test_client().get('/api/ag3b/go?token=tok&convs=1&conds=NEU_E&exp=u2')
assert r.status_code == 500 and FakeClient.calls == 0
class Flaky(SB):
    def insert(s, p):
        if isinstance(p, list): raise RuntimeError('insert failed')
        return super().insert(p)
a3 = Flask(__name__); E.register_agency3b_experiment(a3, lambda: Flaky())
assert a3.test_client().get('/api/ag3b/go?token=tok&convs=3&conds=NEU_E,I_RULE&exp=u3').status_code == 200
wait(); assert E._state['done'] == 0 and 'ЗАПИС У БАЗУ НЕ ВДАВСЯ' in (E._state['last_error'] or '')
class Pricy(FakeClient):
    def create(s, **kw):
        m = super().create(**kw); m.usage = types.SimpleNamespace(input_tokens=400000, output_tokens=40000); return m
fake.Anthropic = Pricy
a4 = Flask(__name__); E.register_agency3b_experiment(a4, lambda: SB())
assert a4.test_client().get('/api/ag3b/go?token=tok&convs=5&conds=NEU_E,I_RULE&budget=0.5&exp=u4').status_code == 200
wait(); assert E._state['done'] < 10 and 'ЛІМІТ БЮДЖЕТУ' in (E._state['last_error'] or '')
print('ALL OK')
