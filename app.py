"""
Veritas Protocol - Flask API v19.0
Forces fresh import of Veritas modules on every restart
SCRAPER: Daily Mail selectors + <p> fallback (2026-02-26)
GENRE: GenreDetector v2.0 — CONSPIRACY_NEWS + fixed SPORT/CULTURE false positives
LAC EPISTEMOLOGY: v1.0 — anonymous authority / correlation-causation / unfalsifiable
"""

import sys
import os

# CRITICAL: Clear module cache to force reload
print("🔄 Veritas v17.0 - Clearing module cache...")
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('veritas_')]
for module in modules_to_clear:
    del sys.modules[module]
print(f"✅ Cache cleared. Loading fresh Veritas v19.0 modules...")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore
from veritas_alarmism_detector import AlarmismDetector

app = Flask(__name__)
CORS(app)

# Initialize Veritas engine
engine = VeritasCalibratedCore()
alarmism_detector = AlarmismDetector()
print("✅ Veritas engine initialized")

# Warm up RSS context in background thread at startup
import threading
def _warm_context():
    try:
        if engine.context_engine:
            ctx = engine.context_engine.get_context()
            if ctx:
                print(f"✅ Context field loaded: {ctx.total_events} events")
            else:
                print("⚠️  Context field unavailable (RSS blocked or failed)")
    except Exception as e:
        print(f"⚠️  Context warmup error: {e}")
threading.Thread(target=_warm_context, daemon=True).start()
print(f"   Pattern boost:         {engine.pattern_boost_engine is not None}")
print(f"   Void detector:         {engine.void_detector is not None}")
print(f"   Absurdity detector:    {engine.absurdity_detector is not None}")
print(f"   Insight detector:      {engine.insight_detector is not None}")
print(f"   LAC Finance:           {engine.lac_finance is not None}")
print(f"   LAC Labor:             {engine.lac_labor is not None}")
print(f"   LAC Epistemology:      {getattr(engine, 'lac_epistemology', None) is not None}")
print(f"   Self-preservation:     {getattr(engine, 'self_preservation_guard', None) is not None}")
print(f"   Meta-intent:           {getattr(engine, 'meta_intent_analyzer', None) is not None}")
print(f"   Certainty factor:      {getattr(engine, 'certainty_factor', None) is not None}")
print(f"   Performative detector: {getattr(engine, 'performative_detector', None) is not None}")


# ── TRIGGER LOGGER v2.0 (Supabase) ──────────────────────────────────────────
# Персистентне логування в Supabase PostgreSQL.
# Env vars: SUPABASE_URL, SUPABASE_KEY
# Таблиця: trigger_log (створена окремо через SQL Editor)

import json
import time
from collections import defaultdict

# Ініціалізація Supabase клієнта
_sb_client = None

def _get_sb():
    global _sb_client
    if _sb_client is not None:
        return _sb_client
    try:
        from supabase import create_client
        url = os.environ.get('SUPABASE_URL', '')
        key = os.environ.get('SUPABASE_KEY', '')
        if url and key:
            _sb_client = create_client(url, key)
            print("✅ Supabase connected")
        else:
            print("⚠️  SUPABASE_URL or SUPABASE_KEY not set — logging disabled")
    except Exception as e:
        print(f"⚠️  Supabase init error: {e}")
    return _sb_client


def log_analysis(result: dict) -> None:
    """
    Записує один рядок в Supabase після кожного аналізу.
    Non-blocking — помилки логування не ламають основний flow.
    """
    try:
        sb = _get_sb()
        if not sb:
            return

        diag = result.get('diagnostics', {})
        tier = result.get('influence_tier', {})

        entry = {
            'ts':                 int(time.time()),
            'triggered_modules':  result.get('triggered_modules', []),
            'triggered_count':    result.get('triggered_count', 0),
            'interaction_combos': [
                {'modules': c['modules'], 'bonus': c['bonus'], 'label_uk': c.get('label_uk', '')}
                for c in result.get('interaction_combos', [])
            ],
            'interaction_bonus':  result.get('interaction_bonus', 0),
            'entropy_base':       result.get('entropy_base', 0),
            'entropy_boosted':    result.get('entropy_boosted', 0),
            'entropy_multiplier': result.get('entropy_multiplier', 1.0),
            'influence_tier':     tier.get('tier') if isinstance(tier, dict) else None,
            'influence_label':    tier.get('label_uk') if isinstance(tier, dict) else None,
            'genre':              diag.get('genre', ''),
            'manipulation_score': round(diag.get('manipulation_score', 0) or 0, 3),
            'axiom_score':        round(diag.get('axiom_score', 0) or 0, 3),
            'framing_score':      round(diag.get('framing_score', 0) or 0, 3),
            'url':                result.get('scraped_url', '') or '',
            'status':             result.get('status', ''),
        }

        sb.table('trigger_log').insert(entry).execute()

    except Exception as e:
        print(f"⚠️  log_analysis error (non-fatal): {e}")


def compute_stats() -> dict:
    """
    Читає з Supabase і будує агреговану статистику:
    - frequency кожного модуля
    - avg_entropy_impact
    - co_occurrence матриця
    - interaction_combos frequency
    - розподіл по influence_tier і genre
    """
    sb = _get_sb()
    if not sb:
        return {'total': 0, 'message': 'Supabase not connected'}

    try:
        resp = sb.table('trigger_log').select('*').order('ts', desc=False).execute()
        entries = resp.data or []
    except Exception as e:
        return {'total': 0, 'message': f'Supabase error: {e}'}

    if not entries:
        return {'total': 0, 'message': 'No data yet'}

    total = len(entries)

    # ── Module frequency ──────────────────────────────────────────────────────
    mod_freq      = defaultdict(int)
    mod_entropy   = defaultdict(list)   # entropy_boosted коли модуль тригернувся

    for e in entries:
        mods = e.get('triggered_modules', [])
        eb   = e.get('entropy_boosted', 0)
        for m in mods:
            mod_freq[m] += 1
            mod_entropy[m].append(eb)

    module_stats = {}
    for mod, freq in sorted(mod_freq.items(), key=lambda x: -x[1]):
        entropies = mod_entropy[mod]
        module_stats[mod] = {
            'frequency':         freq,
            'frequency_pct':     round(freq / total * 100, 1),
            'avg_entropy_when_triggered': round(sum(entropies)/len(entropies), 1) if entropies else 0,
        }

    # ── Co-occurrence матриця ─────────────────────────────────────────────────
    co_occur = defaultdict(int)
    for e in entries:
        mods = sorted(e.get('triggered_modules', []))
        for i in range(len(mods)):
            for j in range(i+1, len(mods)):
                pair = (mods[i], mods[j])
                co_occur[pair] += 1

    co_occur_list = [
        {
            'pair':    list(pair),
            'count':   count,
            'pct':     round(count / total * 100, 1),
        }
        for pair, count in sorted(co_occur.items(), key=lambda x: -x[1])
        if count >= 2
    ][:20]  # топ-20

    # ── Interaction combos frequency ──────────────────────────────────────────
    combo_freq = defaultdict(int)
    for e in entries:
        for c in e.get('interaction_combos', []):
            key = ' + '.join(sorted(c.get('modules', [])))
            combo_freq[key] += 1

    combo_stats = [
        {'combo': k, 'count': v, 'pct': round(v/total*100, 1)}
        for k, v in sorted(combo_freq.items(), key=lambda x: -x[1])
    ][:15]

    # ── Influence tier distribution ───────────────────────────────────────────
    tier_dist = defaultdict(int)
    TIER_LABELS = {0:'ІНФОРМАЦІЙНИЙ ФОН', 1:'РИТОРИЧНА СКЛАДНІСТЬ',
                   2:'ФРЕЙМІНГ/AGENDA', 3:'МАНІПУЛЯЦІЯ', 4:'ПСИХОЛОГІЧНА АТАКА'}
    for e in entries:
        t = e.get('influence_tier')
        if t is not None:
            tier_dist[t] += 1
    tier_stats = [
        {'tier': t, 'label': TIER_LABELS.get(t,'?'), 'count': c, 'pct': round(c/total*100,1)}
        for t, c in sorted(tier_dist.items())
    ]

    # ── Genre distribution ────────────────────────────────────────────────────
    genre_dist = defaultdict(int)
    for e in entries:
        g = e.get('genre', 'UNKNOWN') or 'UNKNOWN'
        genre_dist[g] += 1
    genre_stats = sorted(
        [{'genre': g, 'count': c, 'pct': round(c/total*100,1)} for g,c in genre_dist.items()],
        key=lambda x: -x['count']
    )

    # ── Entropy distribution ──────────────────────────────────────────────────
    all_entropy = [e.get('entropy_boosted', 0) for e in entries]
    entropy_stats = {
        'avg':    round(sum(all_entropy)/len(all_entropy), 1),
        'median': sorted(all_entropy)[len(all_entropy)//2],
        'high_pct': round(sum(1 for e in all_entropy if e >= 60) / total * 100, 1),
    }

    # ── Часова серія (останні 50 аналізів) ───────────────────────────────────
    recent = [
        {
            'ts':             e['ts'],
            'entropy':        e.get('entropy_boosted', 0),
            'tier':           e.get('influence_tier'),
            'modules_count':  e.get('triggered_count', 0),
        }
        for e in entries[-50:]
    ]

    return {
        'total':              total,
        'generated_at':       int(time.time()),
        'module_stats':       module_stats,
        'co_occurrence':      co_occur_list,
        'combo_stats':        combo_stats,
        'tier_distribution':  tier_stats,
        'genre_distribution': genre_stats,
        'entropy_stats':      entropy_stats,
        'recent':             recent,
    }


# ── Entropy multiplier: shared logic for /api/analyze and /api/oracle ──────
MODULE_WEIGHTS = {
    'self_preservation': 0.20,
    'meta_intent':       0.15,
    'performative':      0.12,
    'lac_epistemology':  0.10,
    'lac_finance':       0.08,
    'lac_labor':         0.08,
    'manipulation':      0.10,
    'claim_gap':         0.07,
    'axiom':             0.18,  # підняли: пєсков-клас маніпуляцій
    'laundered_claim':   0.16,  # підняли: трансляція без атрибуції
    'framing':           0.09,
    'narrative_pivot':   0.07,
    'semantic_void':     0.10,
    'alarmism':          0.12,
}


# ── RULE INTERACTION MATRIX ───────────────────────────────────────────────────
# Явна матриця синергій між модулями.
# Якщо два або три модулі спрацювали разом — додається interaction_bonus.
# Потрійні комбо перекривають подвійні (додаються ВСІ matching комбо).
#
# Логіка: triggered_set.issuperset(combo) → сума всіх підходящих бонусів

INTERACTION_MATRIX = {
    # ── ПАРНІ СИНЕРГІЇ ────────────────────────────────────────────────────────
    frozenset({'manipulation', 'claim_gap'}):               0.12,  # маніпуляція без доказів
    frozenset({'framing', 'lac_epistemology'}):             0.15,  # академічна маніпуляція
    frozenset({'manipulation', 'framing'}):                 0.10,  # архітектура впливу
    frozenset({'axiom', 'manipulation'}):                   0.12,  # підміна реальності
    frozenset({'meta_intent', 'manipulation'}):             0.15,  # прихована атака
    frozenset({'performative', 'claim_gap'}):               0.08,  # сльози без доказів
    frozenset({'framing', 'axiom'}):                        0.10,  # риторична підміна понять
    frozenset({'lac_epistemology', 'claim_gap'}):           0.10,  # псевдоакадемічний стрибок
    frozenset({'lac_finance', 'manipulation'}):             0.08,  # фінансова маніпуляція
    frozenset({'lac_labor', 'manipulation'}):               0.08,  # трудова маніпуляція
    frozenset({'meta_intent', 'framing'}):                  0.10,  # прихована agenda
    frozenset({'self_preservation', 'manipulation'}):       0.12,  # захисна атака
    frozenset({'axiom', 'lac_epistemology'}):               0.10,  # подвійна псевдологіка
    frozenset({'axiom', 'laundered_claim'}):               0.18,  # пєсков-патерн
    frozenset({'alarmism', 'claim_gap'}):                  0.15,  # алармізм + розрив між заявою і доказами
    frozenset({'alarmism', 'laundered_claim'}):            0.15,  # зацікавлене джерело + комерційний страх
    frozenset({'alarmism', 'manipulation'}):               0.12,  # алармізм як маніпулятивний інструмент

    # ── ПОТРІЙНІ СИНЕРГІЇ ─────────────────────────────────────────────────────
    frozenset({'manipulation', 'framing', 'claim_gap'}):          0.20,  # пропагандистська структура
    frozenset({'manipulation', 'lac_epistemology', 'axiom'}):     0.20,  # системна атака на мислення
    frozenset({'meta_intent', 'framing', 'lac_epistemology'}):    0.18,  # прихована agenda + псевдологіка
    frozenset({'manipulation', 'axiom', 'framing'}):              0.18,  # авторитарна риторика
    frozenset({'self_preservation', 'manipulation', 'framing'}):  0.18,  # тотальна атака
}

# Людиночитаємі ярлики для кожного комбо (uk / en)
INTERACTION_LABELS = {
    frozenset({'manipulation', 'claim_gap'}):
        ('Маніпуляція без доказів',           'Manipulation without evidence'),
    frozenset({'framing', 'lac_epistemology'}):
        ('Академічна маніпуляція',            'Academic manipulation'),
    frozenset({'manipulation', 'framing'}):
        ('Архітектура впливу',                'Influence architecture'),
    frozenset({'axiom', 'manipulation'}):
        ('Підміна реальності',                'Reality substitution'),
    frozenset({'meta_intent', 'manipulation'}):
        ('Прихована цілеспрямована атака',    'Hidden targeted attack'),
    frozenset({'performative', 'claim_gap'}):
        ('Порожня риторика без доказів',      'Empty rhetoric without evidence'),
    frozenset({'framing', 'axiom'}):
        ('Риторична підміна понять',          'Rhetorical concept substitution'),
    frozenset({'lac_epistemology', 'claim_gap'}):
        ('Псевдоакадемічний стрибок',         'Pseudo-academic leap'),
    frozenset({'lac_finance', 'manipulation'}):
        ('Фінансова маніпуляція',             'Financial manipulation'),
    frozenset({'lac_labor', 'manipulation'}):
        ('Трудова маніпуляція',               'Labor manipulation'),
    frozenset({'meta_intent', 'framing'}):
        ('Прихована agenda через фреймінг',   'Hidden agenda via framing'),
    frozenset({'self_preservation', 'manipulation'}):
        ('Захисна атака',                     'Defensive attack'),
    frozenset({'axiom', 'lac_epistemology'}):
        ('Подвійна псевдологіка',             'Double pseudo-logic'),
    frozenset({'axiom', 'laundered_claim'}):
        ('Проголошення смерті інституту',     'Institutional death declaration'),
    frozenset({'alarmism', 'claim_gap'}):
        ('Алармізм без доказів',              'Alarmism without evidence'),
    frozenset({'alarmism', 'laundered_claim'}):
        ('Комерційний страх',                 'Commercial fear framing'),
    frozenset({'alarmism', 'manipulation'}):
        ('Маніпуляція через страх',           'Fear-based manipulation'),
    frozenset({'manipulation', 'framing', 'claim_gap'}):
        ('Пропагандистська структура',        'Propaganda structure'),
    frozenset({'manipulation', 'lac_epistemology', 'axiom'}):
        ('Системна атака на мислення',        'Systemic attack on cognition'),
    frozenset({'meta_intent', 'framing', 'lac_epistemology'}):
        ('Прихована agenda + псевдологіка',   'Hidden agenda + pseudo-logic'),
    frozenset({'manipulation', 'axiom', 'framing'}):
        ('Авторитарна риторика',              'Authoritarian rhetoric'),
    frozenset({'self_preservation', 'manipulation', 'framing'}):
        ('Тотальна архітектура атаки',        'Total attack architecture'),
}

def compute_interactions(triggered_modules: list) -> tuple:
    """
    Обчислює interaction bonus для списку спрацьованих модулів.
    Повертає (total_bonus: float, matched_combos: list of dicts)
    Кожен dict: {modules, bonus, label_uk, label_en}
    """
    triggered_set = set(triggered_modules)
    total_bonus = 0.0
    matched = []

    for combo, bonus in INTERACTION_MATRIX.items():
        if combo.issubset(triggered_set):
            total_bonus += bonus
            label = INTERACTION_LABELS.get(combo, ('', ''))
            matched.append({
                'modules':  sorted(combo),
                'bonus':    bonus,
                'label_uk': label[0],
                'label_en': label[1],
            })

    matched.sort(key=lambda x: -x['bonus'])
    return round(total_bonus, 3), matched

def compute_entropy_boost(result: dict) -> dict:
    """
    Given a full engine.analyze() result dict, compute entropy multiplier
    based on triggered modules and return boost metadata.
    Returns dict: {entropy_boosted, entropy_base, entropy_multiplier,
                   triggered_modules, triggered_count}
    """
    diag = result.get('diagnostics', {})
    base_entropy = result.get('entropy', 0)
    entropy_pct  = round(base_entropy * 100)

    multiplier      = 1.0
    triggered_mods  = []

    # Self-preservation
    sp = result.get('self_preservation', diag.get('self_preservation', {}))
    sp_verdict = sp.get('verdict', '') if isinstance(sp, dict) else diag.get('self_preservation_verdict', '')
    if sp_verdict and sp_verdict not in ('SAFE', 'CLEAN', ''):
        multiplier += MODULE_WEIGHTS['self_preservation']
        triggered_mods.append('self_preservation')

    # Meta-intent — тригеримо по score >= 0.30 АБО verdict не TRANSPARENT/CLEAN
    mi = result.get('meta_intent', {})
    mi_score_raw = mi.get('score', 0) if isinstance(mi, dict) else 0
    mi_verdict   = mi.get('verdict', '') if isinstance(mi, dict) else ''
    if (mi_score_raw >= 0.30) or (mi_verdict and mi_verdict not in ('TRANSPARENT', 'CLEAN', 'N/A', '')):
        multiplier += MODULE_WEIGHTS['meta_intent']
        triggered_mods.append('meta_intent')

    # Performative
    perf = result.get('performative', {})
    if isinstance(perf, dict) and perf.get('is_performative'):
        multiplier += MODULE_WEIGHTS['performative']
        triggered_mods.append('performative')

    # LAC Epistemology
    epist_verdict = diag.get('lac_epistemology_verdict', '')
    if epist_verdict and epist_verdict not in ('N/A', 'CLEAN', ''):
        multiplier += MODULE_WEIGHTS['lac_epistemology']
        triggered_mods.append('lac_epistemology')

    # LAC Finance
    fin_verdict = diag.get('lac_finance_verdict', '')
    is_financial = diag.get('is_financial_content', False)
    if is_financial and fin_verdict and fin_verdict not in ('N/A', 'CLEAN', ''):
        multiplier += MODULE_WEIGHTS['lac_finance']
        triggered_mods.append('lac_finance')

    # LAC Labor
    lab_verdict = diag.get('lac_labor_verdict', '')
    is_labor = diag.get('is_labor_content', False)
    if is_labor and lab_verdict and lab_verdict not in ('N/A', 'CLEAN', ''):
        multiplier += MODULE_WEIGHTS['lac_labor']
        triggered_mods.append('lac_labor')

    # Manipulation
    manip_score = diag.get('manipulation_score', 0) or 0
    if manip_score >= 0.25:
        multiplier += MODULE_WEIGHTS['manipulation']
        triggered_mods.append('manipulation')

    # Claim gap
    cg = result.get('claim_gap', {})
    if isinstance(cg, dict) and cg.get('is_flagged'):
        multiplier += MODULE_WEIGHTS['claim_gap']
        triggered_mods.append('claim_gap')

    # Laundered claim
    lc = result.get('laundered_claim', {})
    if isinstance(lc, dict) and lc.get('is_flagged'):
        multiplier += MODULE_WEIGHTS.get('laundered_claim', 0.12)
        triggered_mods.append('laundered_claim')

    # Axiom
    axiom_score = diag.get('axiom_score', 0) or 0
    if axiom_score >= 0.25:
        multiplier += MODULE_WEIGHTS['axiom']
        triggered_mods.append('axiom')

    # Semantic void — порожнеча змісту
    void_score_val = diag.get('void', 0) or 0
    if void_score_val >= 0.30:
        multiplier += MODULE_WEIGHTS.get('semantic_void', 0.10)
        triggered_mods.append('semantic_void')
    elif void_score_val >= 0.15:
        multiplier += MODULE_WEIGHTS.get('semantic_void', 0.10) * 0.5
        triggered_mods.append('semantic_void')

    # Framing
    framing_result = result.get('diagnostics', {})
    framing_score  = framing_result.get('framing_score', 0) or 0
    is_framing     = framing_result.get('is_framing', False)
    if is_framing and framing_score > 0:
        multiplier += MODULE_WEIGHTS.get('framing', 0.09)

        # alarmism boost
        alarmism_score = result.get('alarmism_score', 0) or 0
        if alarmism_score >= 0.45:
            multiplier += MODULE_WEIGHTS.get('alarmism', 0.12)
            triggered.add('alarmism')
        elif alarmism_score >= 0.25:
            multiplier += MODULE_WEIGHTS.get('alarmism', 0.12) * 0.5
            triggered.add('alarmism')

        triggered_mods.append('framing')

    # Narrative pivot
    np_result = result.get('narrative_pivot', {})
    if isinstance(np_result, dict) and np_result.get('has_pivot'):
        multiplier += MODULE_WEIGHTS.get('narrative_pivot', 0.07)
        triggered_mods.append('narrative_pivot')

    # Interaction bonus — синергії між модулями
    interaction_bonus, interaction_combos = compute_interactions(triggered_mods)
    multiplier += interaction_bonus

    entropy_boosted = min(100, round(entropy_pct * multiplier))

    # Cap: 100% тільки при реальній серйозній загрозі
    # manipulation >0.5, або absurdity >0.2, або preservation спрацював, або 4+ модулів
    manip_s  = diag.get('manipulation_score', 0) or 0
    absurd_s = diag.get('absurdity_score', 0) or 0
    pres_v   = diag.get('self_preservation_verdict', '') or (result.get('self_preservation') or {}).get('verdict', '')
    pres_active = pres_v and pres_v not in ('SAFE', 'CLEAN', '')
    serious_threat = (manip_s > 0.50) or (absurd_s > 0.20) or pres_active or (len(triggered_mods) >= 4)
    if entropy_boosted >= 100 and not serious_threat:
        entropy_boosted = min(85, entropy_boosted)

    return {
        'entropy_boosted':      entropy_boosted,
        'entropy_base':         entropy_pct,
        'entropy_multiplier':   round(multiplier, 3),
        'triggered_modules':    triggered_mods,
        'triggered_count':      len(triggered_mods),
        'interaction_bonus':    interaction_bonus,
        'interaction_combos':   interaction_combos,
    }


# ── INFLUENCE TIER ────────────────────────────────────────────────────────────
_TIER_META = {
    0: {'tier':0,'label_uk':'ІНФОРМАЦІЙНИЙ ФОН','label_en':'INFORMATIONAL','color':'#4ade80',
        'desc_uk':'Текст може мати неточності, але без навмисної архітектури впливу.',
        'desc_en':'Text may have inaccuracies but no deliberate influence architecture.'},
    1: {'tier':1,'label_uk':'РИТОРИЧНА СКЛАДНІСТЬ','label_en':'RHETORICAL','color':'#a3e635',
        'desc_uk':'Є прийоми переконування, але в межах норми публіцистики й аналітики.',
        'desc_en':'Persuasion techniques present, within normal journalistic range.'},
    2: {'tier':2,'label_uk':'ФРЕЙМІНГ / AGENDA','label_en':'FRAMING','color':'#facc15',
        'desc_uk':'Свідомо побудована перспектива — читач підводиться до висновку.',
        'desc_en':'Deliberately constructed perspective — reader is guided to a conclusion.'},
    3: {'tier':3,'label_uk':'МАНІПУЛЯЦІЯ','label_en':'MANIPULATION','color':'#fb923c',
        'desc_uk':'Архітектура впливу з прихованою метою. Емоційний або логічний тиск.',
        'desc_en':'Influence architecture with hidden purpose. Emotional or logical pressure.'},
    4: {'tier':4,'label_uk':'ПСИХОЛОГІЧНА АТАКА','label_en':'PSYCHOLOGICAL ATTACK','color':'#f87171',
        'desc_uk':'Системний вплив на переконання. Страх, провина, образ ворога.',
        'desc_en':'Systemic influence on beliefs. Fear, guilt, enemy construction.'},
}

def _make_tier(level, trigger_module, trigger_value):
    meta = dict(_TIER_META[level])
    meta['trigger_module'] = trigger_module
    meta['trigger_value']  = trigger_value
    return {'influence_tier': meta}

def compute_influence_tier(result):
    """Градація інтенсивності впливу 0-4. Враховує entropy_boosted + всі модулі."""
    diag        = result.get('diagnostics', {})
    entropy_pct = result.get('entropy_boosted') or round(result.get('entropy', 0) * 100)

    sp_verdict    = diag.get('self_preservation_verdict', '') or                     (result.get('self_preservation') or {}).get('verdict', '')
    manip_score   = diag.get('manipulation_score', 0) or 0
    axiom_score   = diag.get('axiom_score', 0) or 0
    framing_score = diag.get('framing_score', 0) or 0
    framing_v     = diag.get('framing_verdict', '')
    epist_v       = diag.get('lac_epistemology_verdict', '')
    mi            = result.get('meta_intent') or {}
    mi_score      = mi.get('score', 0) or 0
    mi_verdict    = mi.get('verdict', '')
    perf          = result.get('performative') or {}
    is_perf       = perf.get('is_performative', False)
    claim_gap     = result.get('claim_gap') or {}
    is_cg         = claim_gap.get('is_flagged', False)
    pivot         = result.get('narrative_pivot') or {}
    pivot_score   = pivot.get('score', 0) or 0

    # Tier 4 — Психологічна атака
    if sp_verdict and sp_verdict not in ('SAFE', 'CLEAN', ''):
        return _make_tier(4, 'self_preservation', sp_verdict)
    if manip_score >= 0.65:
        return _make_tier(4, 'manipulation', f'{round(manip_score*100)}%')
    if mi_score >= 0.80 and mi_verdict not in ('TRANSPARENT', 'CLEAN', ''):
        return _make_tier(4, 'meta_intent', mi_verdict)
    if axiom_score >= 0.65:
        return _make_tier(4, 'axiom', f'{round(axiom_score*100)}%')

    # Tier 3 — Маніпуляція
    if manip_score >= 0.35:
        return _make_tier(3, 'manipulation', f'{round(manip_score*100)}%')
    if axiom_score >= 0.40:
        return _make_tier(3, 'axiom', f'{round(axiom_score*100)}%')
    if mi_score >= 0.55 and mi_verdict not in ('TRANSPARENT', 'CLEAN', ''):
        return _make_tier(3, 'meta_intent', mi_verdict)
    if entropy_pct >= 65:
        return _make_tier(3, 'entropy', f'{entropy_pct}%')

    # Читаємо laundered_claim
    lc         = result.get('laundered_claim') or {}
    lc_score   = lc.get('score', 0) or 0
    lc_verdict = lc.get('verdict', '')
    is_lc      = lc.get('is_flagged', False)

    # Alarmism
    alarmism_score  = result.get('alarmism_score', 0) or 0
    alarmism_verdict = result.get('alarmism_verdict', '')
    alarmism_flagged = result.get('alarmism_flagged', False)

    # Tier 3 — комерційний алармізм з іншими сигналами
    if alarmism_verdict == 'COMMERCIAL_ALARMISM' and alarmism_score >= 0.60:
        return _make_tier(3, 'alarmism', f'{round(alarmism_score*100)}%')

    # Tier 3 — LAUNDERED_CLAIM форсує tier 3 (відмивання від сторони конфлікту = маніпуляція)
    if lc_verdict == 'LAUNDERED_CLAIM':
        return _make_tier(3, 'laundered_claim', f'{round(lc_score*100)}%')

    # Tier 2 — Фреймінг / Agenda
    if framing_score >= 0.35 or framing_v in ('COMBINED', 'AGENDA_SETTING', 'OVERTON_SHIFT'):
        return _make_tier(2, 'framing', framing_v or f'{round(framing_score*100)}%')
    if epist_v and epist_v not in ('N/A', 'CLEAN', ''):
        return _make_tier(2, 'lac_epistemology', epist_v)
    if is_perf:
        return _make_tier(2, 'performative', perf.get('verdict', ''))
    if pivot_score >= 0.45:
        return _make_tier(2, 'narrative_pivot', f'{round(pivot_score*100)}%')
    if is_cg:
        return _make_tier(2, 'claim_gap', claim_gap.get('verdict', ''))
    # Alarmist framing — tier 2
    if alarmism_verdict == 'ALARMIST_FRAMING' or (alarmism_verdict == 'COMMERCIAL_ALARMISM' and alarmism_score < 0.60):
        return _make_tier(2, 'alarmism', f'{round(alarmism_score*100)}%')

    # WEAK_ATTRIBUTION форсує tier 2
    if lc_verdict == 'WEAK_ATTRIBUTION' or (is_lc and lc_score >= 0.20):
        return _make_tier(2, 'laundered_claim', lc_verdict)
    # Semantic void — висока порожнеча форсує tier 2
    void_val = (result.get('diagnostics') or {}).get('void', 0) or 0
    if void_val >= 0.40:
        return _make_tier(2, 'semantic_void', f'{round(void_val*100)}%')
    if entropy_pct >= 40:
        return _make_tier(2, 'entropy', f'{entropy_pct}%')

    # Tier 1 — Риторична складність
    if framing_score > 0 or entropy_pct >= 20:
        return _make_tier(1, 'entropy', f'{entropy_pct}%')

    # Tier 0 — Інформаційний фон
    return _make_tier(0, None, None)


@app.route('/')
def home():
    """Serve the HTML interface"""
    try:
        return send_file('index.html')
    except:
        return jsonify({
            'status': 'online',
            'version': 'v19.0',
            'message': 'Veritas Protocol API is running (index.html not found)',
            'features': {
                'pattern_boost': engine.pattern_boost_engine is not None,
                'void_detector': engine.void_detector is not None,
                'absurdity_detector': engine.absurdity_detector is not None,
                'insight_detector': engine.insight_detector is not None,
            }
        })

@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze():
    try:
        # GET request = health check
        if request.method == 'GET':
            return jsonify({
                'status': 'online',
                'version': 'v19.0',
                'modules': {
                    'pattern_boost':         engine.pattern_boost_engine is not None,
                    'void_detector':         engine.void_detector is not None,
                    'absurdity_detector':    engine.absurdity_detector is not None,
                    'insight_detector':      engine.insight_detector is not None,
                    'lac_finance':           engine.lac_finance is not None,
                    'lac_labor':             engine.lac_labor is not None,
                    'self_preservation':     getattr(engine, 'self_preservation_guard', None) is not None,
                    'meta_intent':           getattr(engine, 'meta_intent_analyzer', None) is not None,
                    'certainty_factor':      getattr(engine, 'certainty_factor', None) is not None,
                    'performative_detector': getattr(engine, 'performative_detector', None) is not None,
                }
            })
        
        # POST request = analyze text or URL
        data = request.get_json() or {}
        text = data.get('text', '')
        url = data.get('url', '')
        
        # If URL provided, scrape it
        if url and not text:
            try:
                import requests
                from bs4 import BeautifulSoup
                
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml', 'Accept-Language': 'uk,en;q=0.9'}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove all non-content elements aggressively
                for element in soup([
                    "script", "style", "nav", "footer", "header",
                    "aside", "menu", "form", "button", "noscript",
                    "figure", "figcaption",
                ]):
                    element.decompose()

                # Also remove by common ad/nav class and id names
                # Use list() to avoid crash when iterating over decomposed tags
                NOISE_CLASSES = ['nav', 'menu', 'sidebar', 'advertisement',
                    'social', 'share', 'comment', 'related', 'popular',
                    'trending', 'cookie', 'banner', 'promo', 'subscribe',
                    'newsletter', 'paywall', 'modal', 'overlay', 'breadcrumb',
                    'header', 'footer', 'topbar', 'bottombar', 'widget',
                    'tag-list', 'tags', 'author-bio', 'read-more', 'also-read',
                    'sponsored', 'outbrain', 'taboola', 'dfp', 'ad-', '-ad-',
                    'smartads', 'pagination', 'breadcrumbs', 'site-nav',
                    'global-nav', 'primary-nav', 'secondary-nav', 'skip-link']
                for tag in list(soup.find_all(True)):
                    try:
                        classes = ' '.join(tag.get('class', []) or [])
                        tag_id = tag.get('id', '') or ''
                        val = (classes + ' ' + tag_id).lower()
                        if any(x in val for x in NOISE_CLASSES):
                            tag.decompose()
                    except Exception:
                        pass
                
                # Try to find main content area
                # Ordered from most specific to most generic
                # Guardian ng-interactive: try Jina immediately, skip BS scrape
                import re as _re_pre
                if _re_pre.search(r'theguardian\.com.*ng-interactive', url):
                    import os as _os_g
                    jina_key_g = _os_g.environ.get('JINA_API_KEY', '')
                    if jina_key_g:
                        try:
                            jina_res_g = requests.get(
                                f'https://r.jina.ai/{url}',
                                headers={'Authorization': f'Bearer {jina_key_g}', 'Accept': 'text/plain'},
                                timeout=40
                            )
                            if jina_res_g.status_code == 200 and len(jina_res_g.text.split()) > 50:
                                text = jina_res_g.text.strip()
                                words = text.split()
                                if len(words) > 5000:
                                    text = ' '.join(words[:5000])
                                print(f'✅ Guardian ng-interactive via Jina: {len(text.split())} words')
                        except Exception as _je_g:
                            print(f'⚠️  Guardian Jina error: {_je_g}')

                SELECTORS = [
                    # Daily Mail / Mail Online
                    '[itemprop="articleBody"]',
                    '.mol-article-body',
                    '.article-text',
                    # Guardian, Telegraph, Independent
                    '.article-body-commercial-selector',
                    '.dcr-article-body',
                    'div[data-component="text-block"]',
                    # BBC
                    '[data-component="text-block"]',
                    # India Today
                    '.description',
                    '.story-details',
                    '.jsx-story-detail',
                    '[class*="story-detail"]',
                    '[class*="article-detail"]',
                    # CNN
                    '.article__content',
                    '.zn-body__paragraph',
                    '[class*="article-body"]',
                    # Generic news
                    'article', 'main', '[role="main"]', '.article-body',
                    '.story-body', '.content', '.article', '.post-content',
                    '.entry-content', '.td-post-content',
                ]
                main_content = None
                for selector in SELECTORS:
                    main_content = soup.select_one(selector)
                    if main_content and len(main_content.get_text()) > 200:
                        break
                    else:
                        main_content = None

                # Fallback: collect all <p> tags longer than 60 chars
                # This handles JS-heavy sites where article body isn't in a known wrapper
                if not main_content:
                    paragraphs = [
                        p.get_text(' ', strip=True)
                        for p in soup.find_all('p')
                        if len(p.get_text(strip=True)) > 60
                    ]
                    if len(paragraphs) >= 3:
                        from bs4 import BeautifulSoup as _BS, Tag
                        fake = _BS('<div></div>', 'html.parser')
                        wrapper = fake.div
                        for para_text in paragraphs:
                            p_tag = fake.new_tag('p')
                            p_tag.string = para_text
                            wrapper.append(p_tag)
                        main_content = wrapper
                        print(f'🔍 Used <p> fallback: {len(paragraphs)} paragraphs')

                # Remove sidebar/related blocks from inside main_content
                target = main_content or soup
                INNER_NOISE = ['sidebar', 'related', 'also-read', 'read-also',
                    'sujhet', 'special', 'editor', 'popular', 'widget',
                    'newsletter', 'subscribe']
                for noise in list(target.find_all(True)):
                    try:
                        classes = ' '.join(noise.get('class', []) or [])
                        nid = noise.get('id', '') or ''
                        val = (classes + ' ' + nid).lower()
                        if any(x in val for x in INNER_NOISE):
                            noise.decompose()
                    except Exception:
                        pass

                # Get text from main content or entire soup
                raw = target.get_text(separator=' ')

                import re as _re
                # Collapse whitespace first
                text = _re.sub(r'\s+', ' ', raw).strip()

                # Prepend page title/h1 so ClaimGapDetector sees the headline.
                # Headlines often contain the strong claim ("Пророцтво монаха")
                # but disappear from the scraped body. Prepending puts them in
                # the 150-char header window that ClaimGapDetector scans.
                try:
                    _h1 = soup.find('h1')
                    _title_tag = soup.find('title')
                    _headline = ''
                    if _title_tag:
                        # <title> often has the clickbait headline (e.g. "Пророцтво монаха...")
                        # <h1> is often a softened version — so prefer <title>
                        _headline = _re.split(r'\s*[\|\u2013\u2014]\s*', _title_tag.get_text(strip=True))[0].strip()
                    if not _headline and _h1:
                        _headline = _h1.get_text(strip=True)
                    if _headline and not text.startswith(_headline[:30]):
                        text = _headline + '. ' + text
                        print(f'\U0001f3f7\ufe0f  Headline prepended: {_headline[:80]}')
                except Exception:
                    pass

                # Remove metadata phrases that appear inline (BBC and similar sites)
                # Remove BBC-style metadata block (Author/Role/date/readtime)
                text = _re.sub(r'(Author,|Role,)\s.{0,200}?(?=\d{1,2}\s\w+\s\d{4})', '', text)
                text = _re.sub(r'BBC World Service\s*', '', text)
                text = _re.sub(r'\d{1,2}\s+\w+\s+\d{4}\s+', '', text)
                text = _re.sub(r'Час прочитання[^А-ЯA-Z]{0,30}', '', text, flags=_re.IGNORECASE)
                text = _re.sub(r'Пропустити Whatsapp.{0,100}Кінець Whatsapp', '', text, flags=_re.IGNORECASE|_re.DOTALL)
                text = _re.sub(r'Підписуйтеся на наш канал тут\.?', '', text, flags=_re.IGNORECASE)
                # BBC "Найпопулярніше" sidebar block
                text = _re.sub(
                    r'Skip Найпопулярніше and continue reading Найпопулярніше.*?End of Найпопулярніше',
                    '', text, flags=_re.DOTALL|_re.IGNORECASE
                )
                # BBC social subscribe block
                text = _re.sub(
                    r'Skip Підписуйтеся на нас у соцмережах.*?End of Підписуйтеся на нас у соцмережах',
                    '', text, flags=_re.DOTALL|_re.IGNORECASE
                )
                text = _re.sub(r'\bArticle Information\b', '', text)
                text = _re.sub(r'(?<![\w\d])хв(?![\w])', '', text)  # orphan "хв"
                text = _re.sub(r'\s+', ' ', text).strip()
                # Remove Commonwealth country list (appears after "всіх 14 інших країн")
                text = _re.sub(
                    r'(Антигуа і Барбуда|Австралія|Багамські|Беліз|Канада|Гренада|Ямайка|'
                    r'Нова Зеландія|Папуа|Сент-Кітс|Сент-Люсія|Сент-Вінсент|Соломонові|Тувалу)'
                    r'(\s+(Антигуа|Австралія|Багамські|Беліз|Канада|Гренада|Ямайка|'
                    r'Нова Зеландія|Папуа|Сент-Кітс|Сент-Люсія|Сент-Вінсент|Соломонові|Тувалу))+',
                    '', text
                )
                text = _re.sub(r'\s+', ' ', text).strip()

                # Limit to 5000 words
                words = text.split()
                if len(words) > 5000:
                    text = ' '.join(words[:5000])
                
                print(f'🔍 Scrape result: text length={len(text)}, words={len(text.split())}')
                print(f'🔍 Raw length was: {len(raw)}')

                # ── Jina fallback: мало слів АБО навігаційне сміття ────
                word_count_check = len(text.split())

                # Детектор навігаційного сміття — багато слів але це меню/реклама
                _nav_markers = [
                    'live tv', 'sign in', 'subscribe', 'edition in',
                    'download app', 'follow us', 'terms and conditions',
                    'privacy policy', 'cookie policy', 'about us', 'contact us',
                    'newstak', 'gnttv', 'lallantop', 'aaj tak',
                    'advertisement', 'also watch', 'read this', 'read full story',
                ]
                _text_lower = text.lower()
                _nav_hits = sum(1 for m in _nav_markers if m in _text_lower)
                _words_check = text.split()
                _short_token_ratio = sum(1 for w in _words_check if len(w) <= 3) / max(len(_words_check), 1)
                _is_nav_garbage = _nav_hits >= 4 or (_nav_hits >= 2 and _short_token_ratio > 0.45)

                if word_count_check < 80 or _is_nav_garbage:
                    import os as _os
                    jina_key = _os.environ.get('JINA_API_KEY', '')
                    if jina_key:
                        try:
                            print(f'🔄 Jina fallback: words={word_count_check} nav_garbage={_is_nav_garbage} nav_hits={_nav_hits}')
                            jina_headers = {
                                'Authorization': f'Bearer {jina_key}',
                                'Accept': 'text/plain',
                                'X-Return-Format': 'text',
                            }
                            jina_res = requests.get(
                                f'https://r.jina.ai/{url}',
                                headers=jina_headers,
                                timeout=40
                            )
                            if jina_res.status_code == 200 and len(jina_res.text.split()) > word_count_check:
                                text = jina_res.text.strip()
                                # Trim to 5000 words
                                words = text.split()
                                if len(words) > 5000:
                                    text = ' '.join(words[:5000])
                                print(f'✅ Jina returned {len(text.split())} words')
                            else:
                                print(f'⚠️  Jina returned {jina_res.status_code}: {jina_res.text[:100]}')
                        except Exception as je:
                            print(f'⚠️  Jina error: {je}')
                    else:
                        print('⚠️  Jina fallback skipped: no JINA_API_KEY set')
                print(f'🔍 Text preview: {repr(text[:300])}')

                # ── Фінальна перевірка після Jina: чи все ще навігаційне сміття? ──
                _final_lower = text.lower()
                _final_nav_hits = sum(1 for m in _nav_markers if m in _final_lower)
                _final_words = text.split()
                _final_short_ratio = sum(1 for w in _final_words if len(w) <= 3) / max(len(_final_words), 1)
                _final_is_garbage = _final_nav_hits >= 4 or (_final_nav_hits >= 2 and _final_short_ratio > 0.45)
                if _final_is_garbage:
                    print(f'⚠️  Jina also returned nav garbage (nav_hits={_final_nav_hits}) — site is JS-protected')
                    return jsonify({
                        'error': 'Сайт захищений від автоматичного читання (JavaScript rendering). Скопіюйте текст статті вручну і вставте в поле нижче.',
                        'status': 'scrape_blocked',
                        'hint': 'js_protected'
                    }), 400

                word_count = len(text.split())
                if not text or len(text) < 100:
                    return jsonify({
                        'error': 'Could not read page content. The site may be blocking automated reading. Copy the article text manually and paste it below.',
                        'status': 'scrape_blocked'
                    }), 400
                if word_count < 80:
                    return jsonify({
                        'error': f'Вдалося зчитати лише {word_count} слів — скоріш за все сайт заблокував читання. Скопіюйте текст статті вручну і вставте в поле нижче.',
                        'status': 'scrape_partial',
                        'partial_text': text
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'error': f'Failed to scrape URL: {str(e)}',
                    'status': 'error'
                }), 400
        
        if not text:
            return jsonify({
                'error': 'No text or URL provided',
                'status': 'error'
            }), 400
        
        # Запускаємо alarmism detector на повному тексті (до trim)
        alarmism_result = alarmism_detector.analyze(text)
        print(f'🚨 ALARMISM: verdict={alarmism_result.verdict} score={alarmism_result.score}')

        # Обрізаємо до 2500 слів перед аналізом — запобігає таймауту воркера
        # Маніпулятивні патерни завжди в першій третині тексту
        _analyze_words = text.split()
        if len(_analyze_words) > 2500:
            print(f'✂️  Text trimmed for analysis: {len(_analyze_words)} → 2500 words')
            text_for_analysis = ' '.join(_analyze_words[:2500])
        else:
            text_for_analysis = text

        # Analyze text
        result = engine.analyze(text_for_analysis)

        # Вставляємо alarmism в result
        result['alarmism_score']   = alarmism_result.score
        result['alarmism_verdict'] = alarmism_result.verdict
        result['alarmism_signals'] = alarmism_result.signals
        result['alarmism_flagged'] = alarmism_result.is_flagged
        ctx_dbg = result.get('context', {})
        print(f'🌐 CONTEXT: available={ctx_dbg.get("available")} verdict={ctx_dbg.get("verdict")} score={ctx_dbg.get("score")}')
        ctx_summary = ctx_dbg.get('summary', {})
        print(f'🌐 HOT_TOPICS: {ctx_summary.get("top_topics", [])[:8]}')
        print(f'🌐 SIGNALS: {ctx_dbg.get("signals", [])}')
        
        # Add scraped text and preview
        if url:
            words = text.split()
            preview_words = words[:2000] if len(words) > 2000 else words
            result['scraped_text_preview'] = ' '.join(preview_words)
            result['scraped_word_count'] = len(words)
            result['scraped_url'] = url
        # Full clean text for oracle — no slicing, both URL and direct input
        result['article_text'] = text

        # ── Entropy boost: модулі множать ентропію ──────────────────────────
        boost = compute_entropy_boost(result)
        result.update(boost)

        tier = compute_influence_tier(result)
        result.update(tier)

        # ── Логування тригерів ───────────────────────────────────────────────
        log_analysis(result)

        return jsonify(result)
    
    except Exception as e:
        import traceback
        print(f"❌ Error in analyze: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500



@app.route('/api/stats', methods=['GET'])
def stats():
    """Агрегована статистика тригерів."""
    return jsonify(compute_stats())


@app.route('/api/stats/export', methods=['GET'])
def stats_export():
    """Скачати всі записи з Supabase як JSON."""
    sb = _get_sb()
    if not sb:
        return jsonify({'error': 'Supabase not connected'}), 503
    try:
        resp = sb.table('trigger_log').select('*').order('ts', desc=False).execute()
        return jsonify({'total': len(resp.data), 'entries': resp.data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/reset', methods=['POST'])
def stats_reset():
    """Очистити всі записи в Supabase (для тестування)."""
    sb = _get_sb()
    if not sb:
        return jsonify({'error': 'Supabase not connected'}), 503
    try:
        sb.table('trigger_log').delete().neq('id', 0).execute()
        return jsonify({'status': 'ok', 'message': 'Log cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': 'v19.0'
    })



@app.route('/api/oracle', methods=['POST'])
def oracle():
    import os, re

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'ANTHROPIC_API_KEY not configured', 'witness_available': False}), 503
    try:
        import anthropic
    except ImportError:
        return jsonify({'error': 'anthropic package not installed', 'witness_available': False}), 503

    try:
        data = request.get_json() or {}
        diag = data.get('diagnostics', {})

        verdict      = diag.get('verdict', '—')
        entropy_pct  = round((diag.get('entropy', 0)) * 100)
        ctx          = diag.get('context', {})
        ctx_verdict  = ctx.get('verdict', 'NO_CONTEXT')
        ctx_signals  = ', '.join(ctx.get('signals', [])) or 'відсутні'
        ctx_summary  = ctx.get('summary') or {}
        hot_topics   = ', '.join(w for w, _ in ctx_summary.get('top_topics', [])[:6]) or 'невідомо'
        crisis_count = ctx_summary.get('accountability_count', 0)
        total_events = ctx_summary.get('total_events', 0)
        crisis_pct   = round((ctx_summary.get('crisis_ratio', 0)) * 100, 1)
        perf         = diag.get('performative', {})
        perf_verdict = perf.get('verdict', '—')
        perf_score   = perf.get('score', 0)
        # Full article text — no slicing. Fallback: article_text → text_preview → ''
        text_preview = data.get('article_text', '') or data.get('text_preview', '')

        # All module signals for comprehensive witness analysis
        # LAC Finance — flat fields from diagnostics
        lac_fin_verdict  = diag.get('lac_finance_verdict', '')
        lac_fin_score    = diag.get('lac_finance_score', None)
        lac_fin_missing  = ', '.join(diag.get('lac_finance_missing', []))

        # LAC Labor — flat fields from diagnostics
        lac_lab_verdict  = diag.get('lac_labor_verdict', '')

        # LAC Epistemology — flat fields from diagnostics
        lac_epist_verdict = diag.get('lac_epistemology_verdict', '')
        lac_epist_hits    = diag.get('lac_epistemology_pattern_hits', {})

        self_pres        = diag.get('self_preservation', {})
        self_pres_verdict = self_pres.get('verdict', '') if isinstance(self_pres, dict) else ''

        meta_intent      = diag.get('meta_intent', {})
        meta_verdict     = meta_intent.get('verdict', '') if isinstance(meta_intent, dict) else ''

        genre            = diag.get('genre', '')
        cohesion         = diag.get('cohesion', None)
        void_score       = diag.get('void', None)
        absurdity        = diag.get('absurdity', None)

        # Language: from request → from diagnostics → default Ukrainian
        ui_language = data.get('language', '') or diag.get('language', '') or 'uk'

        # Build signals summary — only non-clean signals, with plain-language explanations
        signals_lines = []
        if lac_fin_verdict and lac_fin_verdict not in ('N/A', 'CLEAN', ''):
            line = f'  💰 LAC ФІНАНСИ спрацював: {lac_fin_verdict}'
            if lac_fin_score is not None:
                line += f' (score: {lac_fin_score:.2f})'
            if lac_fin_missing:
                line += f'\n     Відсутнє у тексті: {lac_fin_missing}'
            line += '\n     → Текст торкається фінансів або економіки, але уникає відповіді: хто відповідає, які ризики, що буде якщо не вийде. Поясни це читачу простими словами.'
            signals_lines.append(line)
        if lac_lab_verdict and lac_lab_verdict not in ('N/A', 'CLEAN', ''):
            line = f'  ⚙️ LAC ПРАЦЯ спрацював: {lac_lab_verdict}'
            line += '\n     → Текст про роботу або зайнятість декларує зміни без механізмів: немає відповідальних, строків, критеріїв. Поясни читачу чого саме бракує.'
            signals_lines.append(line)
        if lac_epist_verdict and lac_epist_verdict not in ('N/A', 'CLEAN', ''):
            hits = lac_epist_hits
            parts = []
            if hits.get('anonymous_authority', 0):
                parts.append('анонімні авторитети (без імен та установ)')
            if hits.get('correlation_causation', 0):
                parts.append('кореляція подана як причинність')
            if hits.get('unfalsifiable', 0):
                parts.append('незаперечна теза (заперечення = доказ змови)')
            details = '; '.join(parts) if parts else lac_epist_verdict
            line = f'  🔬 LAC ЕПІСТЕМОЛОГІЯ спрацювала: {lac_epist_verdict}'
            line += f'\n     Знайдено: {details}'
            line += '\n     → Текст імітує логічний аргумент але не дає верифікованих доказів. Поясни читачу конкретно що саме не можна перевірити і чому це проблема.'
            signals_lines.append(line)
        if self_pres_verdict and self_pres_verdict not in ('SAFE', ''):
            line = f'  🛡️ САМОЗБЕРЕЖЕННЯ спрацювало: {self_pres_verdict}'
            line += '\n     → Текст намагається переконати не перевіряти або не сумніватись. Тривожний сигнал.'
            signals_lines.append(line)
        if meta_verdict and meta_verdict not in ('TRANSPARENT', ''):
            line = f'  🎯 МЕТА-НАМІР спрацював: {meta_verdict}'
            line += '\n     → Текст написаний не щоб інформувати, а щоб змінити поведінку або переконання читача.'
            signals_lines.append(line)
        perf_obj = diag.get('performative', {})
        if isinstance(perf_obj, dict) and perf_obj.get('is_performative'):
            line = f'  🐊 КРОКОДИЛЯЧІ СЛЬОЗИ: {perf_obj.get("verdict","")}'
            line += '\n     → Декларується дискомфорт або відповідальність без жодного конкретного зобов\'язання змінити щось реальне.'
            signals_lines.append(line)

        # ── Маніпуляція ──
        manip_score_w   = diag.get('manipulation_score', 0) or 0
        manip_verdict_w = diag.get('manipulation_verdict', '')
        manip_patterns_w = diag.get('manipulation_patterns', [])
        if manip_score_w >= 0.25 and manip_verdict_w and manip_verdict_w not in ('CLEAN', ''):
            patterns_str = ', '.join(manip_patterns_w) if manip_patterns_w else manip_verdict_w
            line = f'  🧠 МАНІПУЛЯЦІЯ спрацювала: {manip_verdict_w} (score: {manip_score_w:.2f})'
            line += f'\n     Патерни: {patterns_str}'
            line += '\n     → Текст використовує риторичні конструкції щоб обмежити автономію судження читача. Поясни конкретно який прийом і чому це проблема.'
            signals_lines.append(line)

        # ── Абсурдність ──
        absurd_score_w = diag.get('absurdity_score', 0) or 0
        if absurd_score_w >= 0.30:
            absurd_ev = diag.get('absurdity_evidence', {})
            ev_keys = list(absurd_ev.keys())[:3] if absurd_ev else []
            line = f'  🌀 АБСУРДНІСТЬ спрацювала: {absurd_score_w:.2f}'
            if ev_keys:
                line += f'\n     Типи: {", ".join(ev_keys)}'
            line += '\n     → Текст містить твердження які суперечать реальності або внутрішньо суперечать одне одному. Поясни конкретно що саме неможливо або абсурдно.'
            signals_lines.append(line)

        # ── Framing ──
        framing_score_w   = diag.get('framing_score', 0) or 0
        framing_verdict_w = diag.get('framing_verdict', '')
        framing_patterns_w = diag.get('framing_patterns', [])
        if framing_score_w >= 0.25 and framing_verdict_w and framing_verdict_w not in ('CLEAN', 'NO_FRAMING', ''):
            patterns_str = ', '.join(framing_patterns_w[:3]) if framing_patterns_w else framing_verdict_w
            line = f'  🖼️ ФРЕЙМІНГ спрацював: {framing_verdict_w} (score: {framing_score_w:.2f})'
            line += f'\n     Патерни: {patterns_str}'
            line += '\n     → Текст навмисно формує рамку сприйняття щоб певні висновки здавались очевидними. Поясни яка рамка і що вона приховує.'
            signals_lines.append(line)

        # ── Axiom ──
        axiom_score_w   = diag.get('axiom_score', 0) or 0
        axiom_verdict_w = diag.get('axiom_verdict', '')
        axiom_patterns_w = diag.get('axiom_patterns', [])
        if axiom_score_w >= 0.30 and axiom_verdict_w and axiom_verdict_w not in ('CLEAN', ''):
            patterns_str = ', '.join(axiom_patterns_w[:3]) if axiom_patterns_w else axiom_verdict_w
            line = f'  ⚖️ АКСІОМА спрацювала: {axiom_verdict_w} (score: {axiom_score_w:.2f})'
            line += f'\n     Патерни: {patterns_str}'
            line += '\n     → Текст подає спірне твердження як самоочевидну істину що не потребує доказів. Поясни яке саме.'
            signals_lines.append(line)

        # ── Claim Gap ──
        cg_obj = data.get('claim_gap', {})
        if isinstance(cg_obj, dict) and cg_obj.get('is_flagged'):
            cg_verdict = cg_obj.get('verdict', '')
            cg_trigger = cg_obj.get('trigger_phrase', '')
            line = f'  📏 РОЗРИВ ТВЕРДЖЕНЬ: {cg_verdict}'
            if cg_trigger:
                line += f'\n     Тригер: «{cg_trigger[:60]}»'
            line += '\n     → Текст робить сильне твердження але докази або механізм його не підкріплюють. Поясни що саме задекларовано і чого бракує.'
            signals_lines.append(line)

        # ── Laundered Claim ──
        lc_obj = data.get('laundered_claim', {})
        if isinstance(lc_obj, dict) and lc_obj.get('is_flagged'):
            lc_verdict = lc_obj.get('verdict', '')
            line = f'  🧺 ВІДМИВАННЯ ТВЕРДЖЕНЬ: {lc_verdict}'
            line += '\n     → Інформація з зацікавленого джерела подається як нейтральний факт. Поясни хто насправді за цим стоїть.'
            signals_lines.append(line)

        # ── Alarmism ──
        al_score   = data.get('alarmism_score', 0) or 0
        al_verdict = data.get('alarmism_verdict', '')
        al_signals = data.get('alarmism_signals', [])
        if al_score >= 0.25 and al_verdict not in ('CLEAN', ''):
            line = f'  🚨 АЛАРМІЗМ спрацював: {al_verdict} (score: {al_score:.2f})'
            # Передаємо всі сигнали — кожен несе окремий змістовний сигнал
            ALARMISM_SIGNAL_HINTS = {
                'Загроза без конкретного виходу':         'загроза описана але читачу не сказано що робити — мета тривога, не інформування',
                'Переважає алармізм над порадами':        'тривожних патернів більше ніж практичних порад',
                'Єдине джерело — зацікавлена сторона':   'єдине джерело є компанією що продає захист від цієї ж загрози',
                'Зацікавлене джерело є, але є й незалежні': 'зацікавлене джерело частково компенсоване незалежними',
                'Комерційний алармізм':                   'після опису загрози йде реклама або CTA — класична архітектура "страх → продукт"',
                'Можливий комерційний контекст':          'є реклама або заклик до дії поруч з описом загрози',
                'Суперлатив загрози без верифікації':     '"never-before-seen", "unprecedented" — сила загрози перебільшена без доказів',
                'Масштаб загрози без методології':        'великі числа (тисячі, мільйони) без пояснення як рахували',
                'Розмитий масштаб':                       'розмиті формулювання масштабу без конкретної методології',
            }
            for sig in al_signals:
                hint = next((v for k, v in ALARMISM_SIGNAL_HINTS.items() if k in sig), '')
                line += f'\n     • {sig[:80]}'
                if hint:
                    line += f' — {hint}'
            if al_verdict == 'COMMERCIAL_ALARMISM':
                line += '\n     → Текст використовує страх як комерційний інструмент. Поясни читачу кожен з виявлених сигналів і як ця архітектура впливає на його рішення.'
            else:
                line += '\n     → Текст перебільшує загрозу або масштаб. Поясни що конкретно перебільшено і як читачу це перевірити самостійно.'
            signals_lines.append(line)
        signals_summary = '\n'.join(signals_lines) if signals_lines else '  (модулі не виявили порушень)'

        # ── Entropy boost: беремо вже розраховані значення з data (вже в /api/analyze) ──
        entropy_pct_boosted = data.get('entropy_boosted', entropy_pct)
        triggered_modules   = data.get('triggered_modules', [])
        triggered_count     = data.get('triggered_count', 0)
        entropy_multiplier  = data.get('entropy_multiplier', 1.0)

        # Narrative pivot
        pivot         = diag.get('narrative_pivot', {})
        pivot_verdict = pivot.get('verdict', '') if isinstance(pivot, dict) else ''
        pivot_score   = pivot.get('score', 0) if isinstance(pivot, dict) else 0
        pivot_expl    = pivot.get('explanation', '') if isinstance(pivot, dict) else ''
        pivot_evidence = (pivot.get('evidence', []) or [])[:1]
        # Sanitize raw topic names that come from narrative_pivot module.
        # The module uses internal cluster IDs (cia_fbi, tech, etc.) which must
        # not appear verbatim in user-facing text.
        TOPIC_LABELS_UK = {
            'cia_fbi':'безпека та спецслужби','tech':'технології','technology':'технології',
            'технологія':'технології','finance':'фінанси','economy':'економіка',
            'politics':'політика','політика':'політика','military':'військова тематика',
            'health':'охорона здоров\'я','science':'наука','culture':'культура',
            'religion':'релігія','sport':'спорт','education':'освіта',
            'environment':'довкілля','crime':'злочинність','social':'соціальна тематика',
            'conspiracy':'змова','змова':'змова','нло_космос':'НЛО та космос',
            'ufo':'НЛО та космос','ufo_space':'НЛО та космос','history':'історія',
            'war':'війна','energy':'енергетика','law':'право','media':'медіа',
            'protest':'протести','diplomacy':'дипломатія','terrorism':'тероризм',
            'migration':'міграція','technology_war':'технологічна війна',
            'здоров':'охорона здоров\'я','health_care':'охорона здоров\'я',
            'wellbeing':'благополуччя','mental_health':'психічне здоров\'я',
        }
        TOPIC_LABELS_EN = {
            'cia_fbi':'intelligence & security','tech':'technology','technology':'technology',
            'технологія':'technology','finance':'finance','economy':'economy',
            'politics':'politics','політика':'politics','military':'military',
            'health':'health','science':'science','culture':'culture',
            'religion':'religion','sport':'sport','education':'education',
            'environment':'environment','crime':'crime','social':'social issues',
            'conspiracy':'conspiracy','змова':'conspiracy','нло_космос':'UFO & space',
            'ufo':'UFO & space','ufo_space':'UFO & space','history':'history',
            'war':'war','energy':'energy','law':'law','media':'media',
            'protest':'protests','diplomacy':'diplomacy','terrorism':'terrorism',
            'migration':'migration','technology_war':'tech warfare',
            'здоров':'health','health_care':'healthcare',
            'wellbeing':'wellbeing','mental_health':'mental health',
        }
        TOPIC_LABELS = TOPIC_LABELS_EN if ui_language == 'en' else TOPIC_LABELS_UK
        def _sanitize_topic(t):
            if not t:
                return 'one topic' if ui_language == 'en' else 'одна тема'
            t_low = str(t).lower().strip()
            return TOPIC_LABELS.get(t_low, t_low)
        def _sanitize_topic_list(topics, max_topics=3):
            if not topics:
                return _sanitize_topic('')
            seen, result = set(), []
            for raw in topics[:max_topics]:
                label = _sanitize_topic(raw)
                if label not in seen:
                    seen.add(label)
                    result.append(label)
            return ', '.join(result) if result else _sanitize_topic('')

        # Replace raw topic IDs in pivot explanation text
        # Use regex with word boundary to catch bare IDs, quoted IDs, and topic lists
        import re as _re_pivot
        pivot_expl_clean = pivot_expl
        for raw, label in TOPIC_LABELS.items():
            # quoted forms
            pivot_expl_clean = pivot_expl_clean.replace(f'"{raw}"', f'"{label}"')
            pivot_expl_clean = pivot_expl_clean.replace(f"'{raw}'", f"'{label}'")
            # bare word (word boundary, case-insensitive)
            pivot_expl_clean = _re_pivot.sub(
                r'(?<![\w\u0400-\u04FF])' + _re_pivot.escape(raw) + r'(?![\w\u0400-\u04FF])',
                label, pivot_expl_clean, flags=_re_pivot.IGNORECASE
            )

        # Also rebuild start/end topic display if explanation contains raw IDs
        start_topics = pivot.get('start_topics', []) if isinstance(pivot, dict) else []
        end_topics   = pivot.get('end_topics', [])   if isinstance(pivot, dict) else []
        if start_topics and end_topics:
            start_label = _sanitize_topic_list(start_topics)
            end_label   = _sanitize_topic_list(end_topics)
            pivot_expl_clean = (
                f'Текст починається з теми "{start_label}" але закінчується темою "{end_label}". '
                f'Такий перехід може бути навмисним — щоб непомітно підвести читача до висновку який не випливає з початкової теми.'
            )

        pivot_line = ''
        if pivot_verdict and pivot_verdict not in ('NO_PIVOT', 'INSUFFICIENT_TEXT', ''):
            pivot_line = (
                f'  🔄 НАРАТИВНИЙ PIVOT: {pivot_verdict} (score: {pivot_score})\n'
                f'  {pivot_expl_clean}\n'
            )
            if pivot_evidence:
                pivot_line += f'  Фраза-тригер: «{pivot_evidence[0][:80]}»\n'

        # ── Genre detection via GenreDetector v2.0 ───────────────────
        # Priority: genre already in diagnostics (set by core) → inline detection → UNKNOWN
        detected_genre = genre  # from diag.get('genre', '') above

        if not detected_genre and text_preview:
            try:
                from veritas_genre_detector import GenreDetector as _GD
                _gd_result = _GD().analyze(text_preview)
                detected_genre = _gd_result.genre
            except Exception:
                detected_genre = 'UNKNOWN'

        # ── Genre-specific instructions for Claude ───────────────────
        GENRE_INSTRUCTIONS = {
            'SPORT': (
                "⚠️ ЖАНР: спортивний репортаж.\n"
                "Аналізуй ЛИШЕ структуру подачі у межах спортивного жанру.\n"
                "НЕ згадуй геополітику, кризи відповідальності, відволікання уваги.\n"
                "Якщо текст структурно чистий для свого жанру — скажи це прямо.\n"
            ),
            'CULTURE': (
                "⚠️ ЖАНР: культурний огляд або рецензія.\n"
                "Аналізуй у межах культурного жанру. НЕ шукай маніпуляцію там де є суб'єктивна оцінка.\n"
            ),
            'SCIENCE': (
                "⚠️ ЖАНР: науковий або науково-популярний текст.\n"
                "Аналізуй точність тверджень і наявність джерел. НЕ трактуй наукові метафори як маніпуляцію.\n"
            ),
            'SATIRE': (
                "⚠️ ЖАНР: сатира або іронія.\n"
                "НЕ інтерпретуй буквально. Оціни чи є іронія прозорою для читача.\n"
            ),
            'OPINION': (
                "⚠️ ЖАНР: авторська думка або колонка.\n"
                "Суб'єктивність тут — норма. Оцінюй аргументи, а не факти.\n"
            ),
            'CONSPIRACY_NEWS': (
                "⚠️ ЖАНР: новини з імплікованою причинністю.\n"
                "Текст містить реальні факти, але подає їх через 'дивний збіг', анонімні джерела "
                "або конструкцію 'X сталось після Y — чи це випадковість?'.\n"
                "Це не обов'язково брехня, але це маніпулятивна структура.\n"
                "Поясни читачу різницю між кореляцією і причинністю.\n"
                "Скажи прямо: факти реальні, але зв'язок між ними — не доведений.\n"
            ),
        }

        topic_instruction = GENRE_INSTRUCTIONS.get(detected_genre, '')

        # ── Context block ─────────────────────────────────────────────
        # Редакційні жанри отримують повний контекст поля (displacement, hot topics).
        # Розважальні/фактичні жанри — ні, бо Claude плутає hot_topics з темою тексту.
        EDITORIAL_GENRES = {'CONSPIRACY_NEWS', 'ANALYTICS', 'REPORT', 'OPINION', 'UNKNOWN'}

        if detected_genre not in EDITORIAL_GENRES:
            context_block = (
                f"  Displacement: {ctx_verdict} (контекст поля — не стосується цього тексту)\n"
                f"  Performative: {perf_verdict} (score: {perf_score})\n"
            )
        else:
            context_block = (
                f"  Displacement: {ctx_verdict}\n"
                f"  Сигнали: {ctx_signals}\n"
                f"  Гарячі теми ІНФОРМАЦІЙНОГО ПОЛЯ (не тексту): {hot_topics}\n"
                f"  Кризові заголовки поля: {crisis_count}/{total_events} ({crisis_pct}%)\n"
                f"  Performative: {perf_verdict} (score: {perf_score})\n"
            )

        from datetime import datetime as _dt
        current_date = _dt.now().strftime('%d.%m.%Y')

        is_en = (ui_language == 'en')

        if is_en:
            modules_block = ''
            if signals_summary.strip() not in ('(no anomalies detected by modules)', '(модулі не виявили порушень)', ''):
                modules_block = (
                    f"TRIGGERED MODULES (explain each in plain words):\n"
                    f"{signals_summary}\n"
                )
            if pivot_verdict and pivot_verdict not in ('NO_PIVOT', 'INSUFFICIENT_TEXT', ''):
                start_label_en = _sanitize_topic_list(start_topics)
                end_label_en   = _sanitize_topic_list(end_topics)
                pivot_line = (
                    f"  🔄 NARRATIVE PIVOT: {pivot_verdict} (score: {pivot_score})\n"
                    f'  Text starts on topic "{start_label_en}" but ends on topic "{end_label_en}". '
                    f"This shift may be intentional — to lead the reader to a conclusion that doesn't follow from the original topic.\n"
                )
                if pivot_evidence:
                    pivot_line += f'  Trigger phrase: "{pivot_evidence[0][:80]}"\n'

            prompt = (
                f"Today's date: {current_date}.\n"
                "HARD RULE — VIOLATION NOT ACCEPTABLE:\n"
                f"Today is {current_date}. Your knowledge ends in early 2025 — over a year has passed since then.\n"
                "A LOT has happened since then that you do not know about. Any date before today is the PAST, not the future.\n"
                "ONE RULE ONLY: if you cannot verify a fact — say you cannot verify it.\n"
                "FORBIDDEN: saying something is fabricated, fake, impossible, non-existent or 'future events' — just because you don't know it.\n"
                "Not knowing is NOT proof of absence. Honestly state the limit of your knowledge and recommend checking current sources.\n"
                "CORRECT FORMULA: 'I cannot confirm or deny this fact — it may relate to events after my knowledge cutoff. Verify independently on official sources.'\n"
                "WRONG EXAMPLE (FORBIDDEN): 'Pope Leo XIV does not exist — the current pope is Francis.'\n"
                "CORRECT EXAMPLE: 'I don't know this Pope — he may have been elected after early 2025. Check vatican.va.'\n"
                "You are the Witness. Explain to an ordinary person what is wrong with the text.\n"
                "The person does not know technical terms. They just want to know if they can trust what they read.\n"
                f"{topic_instruction}\n"
                "TEXT FOR ANALYSIS:\n"
                f"{text_preview}\n\n"
                "ANALYSIS DATA:\n"
                f"  System verdict (MAIN SIGNAL): {verdict}\n"
                f"  Genre: {detected_genre}\n"
                f"  Entropy (base): {entropy_pct}% → with module multiplier: {entropy_pct_boosted}% ({triggered_count} module(s) triggered)\n"
                f"  Cohesion: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"CONTEXT:\n"
                f"{context_block}\n"
                "IMPORTANT: System verdict is your primary guide. Entropy is secondary.\n"
                "ANTI-BIAS RULE — ABSOLUTE, NO EXCEPTIONS:\n"
                "The source of the text — its author, publisher, institution, company, or any prestige marker — "
                "is COMPLETELY IRRELEVANT to your analysis. It does not matter if the text was written by a government, "
                "a corporation, an academic journal, or an anonymous blogger. "
                "Analyze ONLY the logical structure. If a module triggered — state it clearly and explain WHY, "
                "regardless of who wrote the text. Softening conclusions because of source authority is a violation of this rule.\n"
                "Verdict mapping:\n"
                "  STRUCTURED RHETORIC → RHETORIC\n"
                "  ANALYTICAL STRUCTURE → ANALYTICS\n"
                "  SCIENTIFIC TEXT → CLEAN\n"
                "  AUTHOR OPINION → OPINION\n"
                "  VERIFIED LOGIC or STRUCTURAL INTEGRITY → CLEAN\n"
                "  ABSTRACT COMPLEXITY → SUSPICIOUS\n"
                "  CONCEPTUAL MIXING or SEMANTIC NOISE → DANGEROUS\n"
                "  IMPLIED CAUSALITY → SUSPICIOUS\n"
                "If there is a NARRATIVE PIVOT — always mention it, even if the overall verdict is CLEAN.\n"
                "MANDATORY MODULE EXPLANATION RULE:\n"
                "If ANY module triggered — you MUST explain it. This is not optional.\n"
                "For each triggered module: state specifically WHAT was missing or problematic in the text.\n"
                "Do not say 'a module found an issue' — say WHAT the issue is in plain words.\n"
                "Example: instead of 'accountability was flagged' say 'the text promises changes but names no specific "
                "person or body responsible for making them happen.'\n"
                "ABSOLUTE PROHIBITION — DO NOT JUSTIFY TRIGGERED MODULES:\n"
                "NEVER write phrases like:\n"
                "  — 'this is normal for a press release'\n"
                "  — 'this is expected for corporate communication'\n"
                "  — 'but for this genre it is acceptable'\n"
                "  — 'the module triggered but this is not a problem'\n"
                "If a module triggered — it found a real structural issue. Explain it to the reader.\n"
                "Genre and source do not cancel a trigger. A company PR can have manipulative structure just like a tabloid.\n"
                "FORMAT — strictly:\n"
                "Line 1: one word IN CAPS — (CLEAN / SUSPICIOUS / DANGEROUS / ANALYTICS / OPINION / RHETORIC)\n"
                "Empty line\n"
                "3-5 sentences in plain language:\n"
                "  1. What is happening in the text (specifically, no jargon)\n"
                "  2. Why this might be a problem (or why it is fine)\n"
                "  3. For EACH triggered module — one sentence explaining specifically what it found\n"
                "  4. What the reader should do next — a concrete recommendation\n"
                "No technical module names. No mention of entropy or metrics.\n"
                "CRITICAL: The limit of YOUR knowledge is YOUR problem, not the reader's. The reader lives in 2026.\n"
                "FORBIDDEN: writing to the reader about 'your knowledge cutoff', 'ahead of your knowledge' — this is meaningless to someone living in the present.\n"
                "If you cannot verify a fact — simply say: 'Check official sources.' No explanations about your knowledge dates.\n"
                "Respond EXCLUSIVELY in English."
            )
        else:
            modules_block = ''
            if signals_summary.strip() != '(модулі не виявили порушень)':
                modules_block = (
                    f"СПРАЦЮВАННЯ МОДУЛІВ (поясни кожен простими словами):\n"
                    f"{signals_summary}\n"
                )

            prompt = (
                f"Сьогоднішня дата: {current_date}.\n"
                "ЖОРСТКЕ ПРАВИЛО — ПОРУШЕННЯ НЕПРИПУСТИМЕ:\n"
                f"Сьогодні {current_date}. Твої знання закінчуються на початку 2025 року — між тоді і сьогодні пройшло більше року.\n"
                "За цей час сталось ДУЖЕ БАГАТО ВСЬОГО що ти не знаєш. Будь-яка дата до сьогодні — це МИНУЛЕ, не майбутнє.\n"
                "ЄДИНЕ ПРАВИЛО: якщо ти не можеш перевірити факт — скажи що не можеш перевірити.\n"
                "ЗАБОРОНЕНО: казати що щось є вигадкою, фейком, неможливим, неіснуючим або 'майбутнім' — тільки тому що ти цього не знаєш.\n"
                "Незнання — НЕ доказ відсутності. Чесно вкажи межу своїх знань і порадь перевірити в актуальних джерелах.\n"
                "ПРАВИЛЬНА ФОРМУЛА: 'Я не можу підтвердити або спростувати цей факт — він може стосуватись подій після моїх знань. Перевір самостійно на офіційних джерелах.'\n"
                "ПРИКЛАД ПОМИЛКИ (ЗАБОРОНЕНО): 'Папи Лева XIV не існує — нинішній папа Франциск.'\n"
                "ПРИКЛАД ПРАВИЛЬНО: 'Я не знаю цього Папи — можливо він обраний після початку 2025 року. Перевір на vatican.va.'\n"
                "Ти — Свідок. Пояснюєш звичайній людині що не так з текстом.\n"
                "Людина не знає термінів. Вона просто хоче зрозуміти чи можна довіряти тому що прочитала.\n"
                f"{topic_instruction}\n"
                "ТЕКСТ ДЛЯ АНАЛІЗУ:\n"
                f"{text_preview}\n\n"
                "ДАНІ АНАЛІЗУ:\n"
                f"  Вердикт системи (ГОЛОВНИЙ СИГНАЛ): {verdict}\n"
                f"  Жанр: {detected_genre}\n"
                f"  Ентропія (база): {entropy_pct}% → з множником модулів: {entropy_pct_boosted}% ({triggered_count} модуль(ів) спрацювало)\n"
                f"  Когезія: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"КОНТЕКСТ:\n"
                f"{context_block}\n"
                "ВАЖЛИВО: Вердикт системи — твій головний орієнтир. Ентропія — допоміжна цифра.\n"
                "ПРАВИЛО ПРОТИ УПЕРЕДЖЕНОСТІ — АБСОЛЮТНЕ, БЕЗ ВИНЯТКІВ:\n"
                "Джерело тексту — його автор, видавець, установа, компанія або будь-який статусний маркер — "
                "є ПОВНІСТЮ НЕРЕЛЕВАНТНИМ для аналізу. Не має значення чи текст написаний урядом, "
                "корпорацією, академічним журналом або анонімним блогером. "
                "Аналізуй ТІЛЬКИ логічну структуру. Якщо модуль спрацював — скажи це чітко і поясни ЧОМУ, "
                "незалежно від того хто написав текст. Пом'якшення висновків через авторитет джерела — порушення цього правила.\n"
                "Відповідності вердиктів:\n"
                "  СТРУКТУРОВАНА РИТОРИКА → РИТОРИКА\n"
                "  АНАЛІТИЧНА СТРУКТУРОВАНІСТЬ → АНАЛІТИКА\n"
                "  НАУКОВИЙ ТЕКСТ → ЧИСТО\n"
                "  АВТОРСЬКА ПОЗИЦІЯ → ДУМКА\n"
                "  ВЕРИФІКОВАНА ЛОГІКА або СТРУКТУРНА ЦІЛІСНІСТЬ → ЧИСТО\n"
                "  АБСТРАКТНА СКЛАДНІСТЬ → ПІДОЗРІЛО\n"
                "  КОНЦЕПТУАЛЬНЕ ЗМІШУВАННЯ або СЕМАНТИЧНИЙ ШУМ → НЕБЕЗПЕЧНО\n"
                "  ІМПЛІКОВАНА ПРИЧИННІСТЬ → ПІДОЗРІЛО\n"
                "Якщо є НАРАТИВНИЙ PIVOT — завжди згадай це в поясненні, навіть якщо загальний вердикт ЧИСТО.\n"
                "ОБОВ'ЯЗКОВЕ ПРАВИЛО ПОЯСНЕННЯ МОДУЛІВ:\n"
                "Якщо БУДЬ-ЯКИЙ модуль спрацював — ти ЗОБОВ'ЯЗАНИЙ пояснити його. Це не опціонально.\n"
                "Для кожного спрацьованого модуля: скажи конкретно ЩО саме відсутнє або проблематичне в тексті.\n"
                "Не кажи 'модуль знайшов проблему' — кажи ЩО це за проблема простими словами.\n"
                "Приклад: замість 'зафіксовано проблему відповідальності' скажи 'текст обіцяє зміни, "
                "але не називає жодної конкретної особи або органу який за це відповідає.'\n"
                "АБСОЛЮТНА ЗАБОРОНА — ВИПРАВДОВУВАТИ СПРАЦЬОВАНІ МОДУЛІ:\n"
                "НІКОЛИ не пиши фрази типу:\n"
                "  — 'це нормально для прес-релізу'\n"
                "  — 'це очікувано для корпоративного тексту'\n"
                "  — 'але для цього жанру це прийнятно'\n"
                "  — 'модуль спрацював, але це не є проблемою'\n"
                "Якщо модуль спрацював — він знайшов реальну структурну проблему. Поясни її читачу.\n"
                "Жанр і джерело не скасовують спрацювання. PR компанії може мати маніпулятивну структуру так само як таблоїд.\n"
                "ФОРМАТ — суворо:\n"
                "Рядок 1: одне слово ВЕЛИКИМИ — (ЧИСТО / ПІДОЗРІЛО / НЕБЕЗПЕЧНО / АНАЛІТИКА / ДУМКА / РИТОРИКА)\n"
                "Порожній рядок\n"
                "3-5 речень простою мовою:\n"
                "  1. Що відбувається в тексті (конкретно, без термінів)\n"
                "  2. Чому це може бути проблемою (або чому все гаразд)\n"
                "  3. Для КОЖНОГО спрацьованого модуля — одне речення що конкретно він знайшов\n"
                "  4. Що читачу варто зробити далі — конкретна порада\n"
                "Жодних технічних назв модулів. Жодного згадування ентропії або метрик.\n"
                "КРИТИЧНО: Межа ТВОЇХ знань — це твоя проблема, не читача. Читач живе в 2026 році.\n"
                "ЗАБОРОНЕНО писати читачу про 'твої знання', 'рік вперед від твоїх знань' — це безглуздо для людини яка живе зараз.\n"
                "Якщо не можеш перевірити факт — просто скажи: 'Перевір на офіційних джерелах.' Без пояснень про дати своїх знань.\n"
                "Відповідай ВИКЛЮЧНО українською мовою."
            )

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=900,
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            'witness_text':        message.content[0].text if message.content else "Свідок мовчить.",
            'witness_available':   True,
            'model':               'claude-haiku-4-5-20251001',
            'detected_genre':      detected_genre,
            'entropy_boosted':     entropy_pct_boosted,
            'entropy_base':        entropy_pct,
            'triggered_modules':   triggered_modules,
            'triggered_count':     triggered_count,
            'entropy_multiplier':  round(entropy_multiplier, 3),
        })

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e), 'witness_available': False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
