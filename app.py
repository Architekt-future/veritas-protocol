"""
Veritas Protocol - Flask API v20.5
Forces fresh import of Veritas modules on every restart
SCRAPER: Daily Mail selectors + <p> fallback (2026-02-26)
GENRE: GenreDetector v2.0 — CONSPIRACY_NEWS + fixed SPORT/CULTURE false positives
LAC EPISTEMOLOGY: v1.0 — anonymous authority / correlation-causation / unfalsifiable
WITNESS PROMPT: generalized 'unrecognized source' rule to named products/models/
  incidents (not just citations); verdict now hard-anchored to nonzero module
  scores — Witness can no longer freelance suspicion when all signals are 0.00
SOURCE CONTEXT: new advisory-only badge decoupled from manipulation score —
  "is the text manipulative" and "is the quoted source a conflict party" are
  now two independent signals instead of one blended score. Escalation
  override widened from 2 to all 15 real modules (was silently discarding
  legitimate framing/laundered_claim/etc. escalations).
"""

import sys
import os

# CRITICAL: Clear module cache to force reload
print("🔄 Veritas v20.5 - Clearing module cache...")
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('veritas_')]
for module in modules_to_clear:
    del sys.modules[module]
print(f"✅ Cache cleared. Loading fresh Veritas v20.5 modules...")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore
from veritas_alarmism_detector import AlarmismDetector
from veritas_media_bias_detector import MediaBiasDetector
from veritas_ard_checker import ARDChecker

app = Flask(__name__)
CORS(app)

# Initialize Veritas engine
engine = VeritasCalibratedCore()
alarmism_detector = AlarmismDetector()
media_bias_detector = MediaBiasDetector()
ard_checker = ARDChecker()
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
print(f"   Alarmism detector:     {alarmism_detector is not None}")
print(f"   Media bias detector:   {media_bias_detector is not None}")
print(f"   ARD checker:           {ard_checker is not None}")


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
    'media_bias':        0.11,
}

# Будь-який з цих модулів, якщо реально спрацював, є достатньою підставою
# для ескалації вердикту (НЕБЕЗПЕЧНО/ПІДОЗРІЛО). Раніше запобіжник і промпт
# перевіряли лише 'manipulation'/'axiom' — успадковано зі старого, вужчого
# правила, яке ніхто не переглядав, коли систему розширили до 15 модулів.
# Це давало хибні придушення: LLM міг обґрунтовано ескалувати через
# framing/laundered_claim/alarmism/etc., а запобіжник це відкидав, бо
# перевіряв не той список.
ESCALATION_WORTHY_MODULES = frozenset(MODULE_WEIGHTS.keys())


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
    frozenset({'media_bias', 'alarmism'}):                 0.15,  # спонсорський страх
    frozenset({'media_bias', 'claim_gap'}):                0.13,  # PR без доказів
    frozenset({'media_bias', 'laundered_claim'}):          0.13,  # подвійне відмивання

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
    frozenset({'media_bias', 'alarmism'}):
        ('Спонсорський алармізм',             'Sponsored alarmism'),
    frozenset({'media_bias', 'claim_gap'}):
        ('PR без доказів',                    'PR without evidence'),
    frozenset({'media_bias', 'laundered_claim'}):
        ('Подвійне відмивання',               'Double laundering'),
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
    triggered       = set()

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

        # media_bias boost
        media_bias_score = result.get('media_bias_score', 0) or 0
        if media_bias_score >= 0.35:
            multiplier += MODULE_WEIGHTS.get('media_bias', 0.11)
            triggered.add('media_bias')
        elif media_bias_score >= 0.20:
            multiplier += MODULE_WEIGHTS.get('media_bias', 0.11) * 0.5
            triggered.add('media_bias')

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
    # Media bias — tier 2
    media_bias_score   = result.get('media_bias_score', 0) or 0
    media_bias_verdict = result.get('media_bias_verdict', '')
    if media_bias_score >= 0.55:
        return _make_tier(3, 'media_bias', media_bias_verdict)
    if media_bias_score >= 0.20:
        return _make_tier(2, 'media_bias', media_bias_verdict)

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
        response = send_file('index.html')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except:
        return jsonify({
            'status': 'online',
            'version': 'v20.5',
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
                'version': 'v20.5',
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
                # ФІКС: separator=' ' раніше склеював КОЖЕН <p>/<h2>/<li> пробілом,
                # знищуючи межі абзаців/заголовків ще до regex-очищення нижче.
                # Наслідок: calculate_logical_cohesion() (calibrated_core.py) рахує
                # структурну когезію по text.split('\n') — і для БУДЬ-ЯКОЇ URL-статті
                # виходило рівно 1 "рядок" на весь текст, тому структурний бонус
                # (спеціально доданий у v20.2 для добре структурованих текстів)
                # практично ніколи не міг спрацювати для скрапнутого контенту,
                # лише для вставленого напряму тексту. separator='\n' зберігає
                # межі блокових елементів.
                raw = target.get_text(separator='\n')

                import re as _re
                # Колапсуємо тільки горизонтальні пробіли (не \n) всередині рядків,
                # і стискаємо кілька порожніх рядків підряд в один — але самі межі
                # абзаців/заголовків (по одному \n) лишаються недоторканими.
                text = _re.sub(r'[ \t]+', ' ', raw)
                text = _re.sub(r'\n\s*\n+', '\n', text)
                text = text.strip()

                # ФІКС: клас-базоване INNER_NOISE вище не ловить сайдбар-віджети
                # ("ЧИТАЙТЕ ТАКОЖ", "Сюжети", "ВИБІР РЕДАКТОРА" тощо) на сайтах,
                # де ці блоки не мають відповідних CSS-класів (напр. korrespondent.net) —
                # BeautifulSoup витягує текст статті РАЗОМ із заголовками сусідніх
                # новин, футером і легальним дисклеймером як один суцільний текст.
                # Доповнюємо текстовим маркером: ВЕЛИКИМИ ЛІТЕРАМИ "ЧИТАЙТЕ ТАКОЖ" —
                # типографська конвенція саме для заголовка віджету пов'язаних статей
                # (не для звичайного речення в тексті — те завжди пишеться "Читайте
                # також" з малої), тому обрізання тут безпечне і не ріже легітимний
                # контент усередині статті.
                SIDEBAR_BOUNDARY_MARKERS = [
                    'ЧИТАЙТЕ ТАКОЖ', 'ЧИТАЙТЕ ТЕЖ', 'ТАКЖЕ ЧИТАЙТЕ',
                    'ЧИТАЙТЕ ЩЕ', 'ПОПУЛЯРНІ НОВИНИ', 'НАЙПОПУЛЯРНІШЕ',
                ]
                for _marker in SIDEBAR_BOUNDARY_MARKERS:
                    _idx = text.find(_marker)
                    if _idx > 200:  # маркер має бути ПІСЛЯ реального тексту статті, не на початку
                        text = text[:_idx].strip()
                        print(f'✂️  Обрізано за маркером сайдбару "{_marker}" на позиції {_idx}')
                        break

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
                # Remove BBC-style metadata block (Author/Role/date/readtime) as ONE unit.
                # IMPORTANT: the date must be consumed together with the preceding
                # Author,/Role, marker — a separate global "strip any date" pass
                # was silently deleting every in-body date (treaty dates, executive
                # order dates, event years) from every scraped article, not just
                # BBC bylines. Fixed 2026-08 after a LinkedIn-scraped article lost
                # "12 січня 2024", "21 жовтня 2020", and "COVID-19 у 2020" down to
                # bare "року"/"році".
                text = _re.sub(r'(Author,|Role,)\s.{0,200}?\d{1,2}\s+\w+\s+\d{4}\s+', '', text)
                text = _re.sub(r'BBC World Service\s*', '', text)
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

                # ── X / TWITTER scrape cleanup ─────────────────────────
                # X повертає весь інтерфейс разом з твітом.
                # Лишаємо тільки реальний контент твіту.
                if any(x in (url or '') for x in ['x.com', 'twitter.com']):
                    # Видаляємо X-навігацію і footer
                    for x_noise in [
                        r"Don'?t miss what'?s happening[^.]*\.",
                        r'People on X are the first to know[^.]*\.',
                        r'Log in\s+Sign up(\s+Post)?',
                        r'New to X\?\s*Sign up now[^.]*\.',
                        r'Sign up with (Apple|Google)[^.]*\.',
                        r'By signing up,?\s*you agree[^.]*\.',
                        r'Terms of Service\s*[|]\s*Privacy Policy[^.]*\.',
                        r'© 20\d\d X Corp\.?',
                        r'Read \d+ repl\w+',
                        r'\d+\s*repl\w+',
                        r'Show more\s+Terms',
                        r'(Sports?|Entertainment|Trending)\s*[·•]\s*Trending[^\n]*',
                        r'See new posts\s+Conversation\s+',
                        r'\b\d+:\d{2}\s+(AM|PM)\s+[·•]\s+\w+\s+\d+,\s+\d{4}\b',  # timestamp
                        r'\b\d+(\.\d+)?[KMB]\s+Views\b',                          # view count
                        r'\b\d+\s+\d+(\.\d+)?[KMB]\s+\d+(\.\d+)?[KMB]\s+\d+(\.\d+)?[KMB]\b',  # metrics row
                    ]:
                        text = _re.sub(x_noise, '', text, flags=_re.IGNORECASE)
                    # Видаляємо блок Trending і все після нього
                    text = _re.sub(
                        r'Trending now.*$', '', text,
                        flags=_re.IGNORECASE | _re.DOTALL
                    )
                    text = _re.sub(r'\s+', ' ', text).strip()
                    print(f'🐦 X/Twitter cleanup: {len(text.split())} words remaining')

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
                                # ── X/Twitter cleanup для Jina результату ──
                                if any(x in (url or '') for x in ['x.com', 'twitter.com']):
                                    for x_noise in [
                                        r"Don'?t miss what'?s happening[^.]*\.",
                                        r'People on X are the first to know[^.]*\.',
                                        r'Log in\s+Sign up(\s+Post)?',
                                        r'See new posts\s+Conversation\s+',
                                        r'New to X\?\s*Sign up now[^.]*\.',
                                        r'Sign up with (Apple|Google)[^.]*\.',
                                        r'By signing up,?\s*you agree[^.]*\.',
                                        r'Terms of Service\s*[|]\s*Privacy Policy[^.]*\.',
                                        r'© 20\d\d X Corp\.?',
                                        r'Read \d+ repl\w+',
                                        r'\d+\s*repl\w+',
                                        r'Show more\s+Terms',
                                        r'(Sports?|Entertainment|Politics|Trending)\s*[·•]\s*Trending[^\n]*',
                                        r'\b\d+:\d{2}\s+(AM|PM)\s+[·•][^\n]*',
                                        r'\b\d+(\.\d+)?[KMB]\s+Views\b',
                                        r'\b\d+\s+\d+(\.\d+)?[KMB]\s+\d+(\.\d+)?[KMB]\s+\d+(\.\d+)?[KMB]\b',
                                    ]:
                                        text = _re.sub(x_noise, '', text, flags=_re.IGNORECASE)
                                    text = _re.sub(
                                        r'Trending now.*$', '', text,
                                        flags=_re.IGNORECASE | _re.DOTALL
                                    )
                                    text = _re.sub(r'\s+', ' ', text).strip()
                                    print(f'🐦 X/Twitter Jina cleanup: {len(text.split())} words remaining')
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
        
        # Запускаємо media bias detector
        media_bias_result = media_bias_detector.analyze(text)
        print(f'📰 MEDIA_BIAS: verdict={media_bias_result.verdict} score={media_bias_result.score}')

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

        # Analyze text — з timeout guard щоб regex backtracking не вбивав воркер
        import concurrent.futures as _cf
        _ANALYZE_TIMEOUT = 22  # секунд — gunicorn worker timeout = 30s, лишаємо буфер
        try:
            with _cf.ThreadPoolExecutor(max_workers=1) as _executor:
                _future = _executor.submit(engine.analyze, text_for_analysis)
                result = _future.result(timeout=_ANALYZE_TIMEOUT)
        except _cf.TimeoutError:
            print(f'⏱️  engine.analyze() TIMEOUT після {_ANALYZE_TIMEOUT}с — повертаємо базовий результат')
            return jsonify({
                'error': 'Аналіз зайняв надто довго. Спробуйте коротший текст або повторіть запит.',
                'status': 'timeout',
                'hint': 'analysis_timeout'
            }), 503

        # ── ABSURDITY DEBUG LOG ──────────────────────────────────────────────
        _diag = result.get('diagnostics', {})
        print(f"🔬 ABSURDITY: score={_diag.get('absurdity_score')} "
              f"is_sci={_diag.get('is_legitimate_science')} "
              f"pseudo_history={_diag.get('pseudo_history_count')} "
              f"pseudo_analogy={_diag.get('pseudo_analogy_count')} "
              f"collapse={_diag.get('collapse_count')} "
              f"techno={_diag.get('techno_mystical_count')} "
              f"epistemology={_diag.get('epistemology_collapse_count')} "
              f"evidence={_diag.get('absurdity_evidence', {})}")

        # Вставляємо alarmism в result І в diagnostics
        result['alarmism_score']   = alarmism_result.score
        result['alarmism_verdict'] = alarmism_result.verdict
        result['alarmism_signals'] = alarmism_result.signals
        result['alarmism_flagged'] = alarmism_result.is_flagged

        # Media bias в result І в diagnostics
        result['media_bias_score']    = media_bias_result.score
        result['media_bias_verdict']  = media_bias_result.verdict
        result['media_bias_signals']  = media_bias_result.signals
        result['media_bias_patterns'] = media_bias_result.patterns_found
        result['media_bias_flagged']  = media_bias_result.is_flagged

        # Копіюємо в diagnostics — фронтенд надсилає diagnostics в /api/oracle
        diag_obj = result.get('diagnostics', {})
        if isinstance(diag_obj, dict):
            diag_obj['alarmism_score']    = alarmism_result.score
            diag_obj['alarmism_verdict']  = alarmism_result.verdict
            diag_obj['alarmism_signals']  = alarmism_result.signals
            diag_obj['alarmism_flagged']  = alarmism_result.is_flagged
            diag_obj['media_bias_score']    = media_bias_result.score
            diag_obj['media_bias_verdict']  = media_bias_result.verdict
            diag_obj['media_bias_signals']  = media_bias_result.signals
            diag_obj['media_bias_patterns'] = media_bias_result.patterns_found
            diag_obj['media_bias_flagged']  = media_bias_result.is_flagged
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

        # ── ARD scan в основному аналізі ────────────────────────────────────
        # Запускаємо ARD checker на повному тексті і додаємо в result.
        # Це дозволяє фронтенду показати червоний блок НЕБЕЗПЕЧНИЙ ЗМІСТ
        # незалежно від ентропії — бо низька ентропія + ARD_SYSTEMIC =
        # "переконливий текст що виправдовує насильство" (найнебезпечніше).
        try:
            ard_scan = ard_checker.scan(text)
            result['ard_score']       = round(ard_scan.score, 3)
            result['ard_verdict']     = ard_scan.verdict
            result['ard_is_flagged']  = ard_scan.is_flagged
            result['ard_principles']  = ard_scan.principles_violated
            result['ard_violations']  = [
                {
                    'principle': v.principle,
                    'name': v.principle_name,
                    'snippet': v.snippet,
                    'severity': v.severity,
                }
                for v in ard_scan.violations
            ]
            print(f'⚖️  ARD: verdict={ard_scan.verdict} score={ard_scan.score} principles={ard_scan.principles_violated}')
        except Exception as _ard_e:
            print(f'⚠️  ARD scan error (non-fatal): {_ard_e}')
            result['ard_score']      = 0.0
            result['ard_verdict']    = 'N/A'
            result['ard_is_flagged'] = False
            result['ard_principles'] = []
            result['ard_violations'] = []

        # ── AUTO-WITNESS TRIGGER FLAG ────────────────────────────────────────
        # Синтез виноситься в /api/synthesis — окремий запит після analyze.
        # Це запобігає worker timeout (analyze + Haiku = ~28с > 30с ліміт).
        result['auto_witness_triggered'] = (
            result.get('media_bias_flagged', False) or
            result.get('alarmism_flagged', False) or
            result.get('ard_is_flagged', False) or
            (result.get('framing_risk', 0) or 0) > 0.3 or
            (result.get('lac_finance_score', 0) or 0) > 0.3 or
            (result.get('lac_labor_score', 0) or 0) > 0.3 or
            (result.get('entropy_boosted', result.get('entropy', 0) * 100) or 0) > 60
        )
        result['witness_synthesis'] = None  # заповнюється через /api/synthesis

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
        'version': 'v20.5'
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

        # ── RSS Fact-Check матчинг ────────────────────────────────────────
        # Компроміс замість агентного пошуку: чистий Python-матчинг проти вже
        # завантаженого (кешованого) RSS-поля. Нуль додаткових API-викликів,
        # нуль ризику тайм-ауту — на відміну від Haiku, що сам робить запити.
        # Дає Свідку РЕАЛЬНІ заголовки для конкретних тверджень замість
        # вгадування зі своїх застарілих знань.
        rss_matches = []
        try:
            _ce = getattr(engine, 'context_engine', None)
            if _ce and text_preview:
                rss_matches = _ce.get_related_events_for_text(text_preview, top_n=5)
        except Exception:
            rss_matches = []

        # ── DEBUG-логування: що РЕАЛЬНО пішло в матчинг, буква-в-букву ──────
        # Вимкнено за замовчуванням. Увімкнути для тесту: DEBUG_RSS=1 у env
        # Render (Dashboard → Environment). Вимкнути назад перед публічним
        # релізом просто прибравши/поставивши 0 — код можна лишити в проді,
        # він неактивний без явного флагу.
        _debug_rss = os.environ.get('DEBUG_RSS', '0') == '1'
        if _debug_rss:
            print(f"[RSS-DEBUG] claim_text (перші 200 симв.): {text_preview[:200]!r}")
            if rss_matches:
                print(f"[RSS-DEBUG] знайдено {len(rss_matches)} збігів:")
                for i, ev in enumerate(rss_matches, 1):
                    print(f"[RSS-DEBUG]   {i}. title={ev.title!r} | source={ev.source!r}")
            else:
                print("[RSS-DEBUG] збігів не знайдено (rss_matches порожній)")

        if rss_matches:
            rss_block_uk = (
                "RSS-ЗБІГИ (реальні заголовки з новинного потоку прямо зараз):\n"
                + '\n'.join(f'  • «{ev.title}» — {ev.source}' for ev in rss_matches) + '\n'
                "Якщо збіг підтверджує чи уточнює КОНКРЕТНЕ твердження з тексту — можеш сказати "
                "що це узгоджується з поточними повідомленнями (згадай джерело). "
                "У заголовку немає повного тексту статті — не додумуй деталей яких там немає.\n"
            )
            rss_block_en = (
                "RSS MATCHES (real headlines from the current news stream):\n"
                + '\n'.join(f'  • "{ev.title}" — {ev.source}' for ev in rss_matches) + '\n'
                "If a match confirms or clarifies a SPECIFIC claim in the text — you may note that "
                "it is consistent with current reporting (name the source). "
                "The headline has no full article body — do not invent details beyond it.\n"
            )
        else:
            rss_block_uk = (
                "RSS-ЗБІГИ: не знайдено в поточному новинному потоці.\n"
                "Це НЕ доказ що твердження хибне — RSS покриває лише частину джерел і лише "
                "останні ~30 хв. Якщо не можеш перевірити факт — чесно скажи читачу 'перевір "
                "на офіційних джерелах', без здогадок і без тверджень що це вигадка.\n"
            )
            rss_block_en = (
                "RSS MATCHES: none found in the current news stream.\n"
                "This is NOT evidence the claim is false — RSS covers only a fraction of sources "
                "and only the last ~30 min. If you cannot verify a fact, honestly tell the reader "
                "to check official sources — do not guess and do not call it fabricated.\n"
            )

        # All module signals for comprehensive witness analysis
        # Переклад технічних ключів критеріїв LAC (спільний для Фінансів і Праці,
        # ті самі назви критеріїв — той самий переклад, що вже є в calibrated_core.py)
        LAC_CRITERIA_UK = {
            'explicit_tradeoff': 'явного трейдоффу (вигода вказана без ціни цієї вигоди)',
            'causal_closure':    "причинно-наслідкового зв'язку (дія не веде до наслідку)",
            'causal_chain':      "причинно-наслідкового зв'язку (дія не веде до наслідку)",
            'accountability':    'механізму відповідальності (хто відповідає, якщо піде не так)',
            'blocking_power':    'механізму блокування (нічого не зупинить дію, якщо вона зашкодить)',
            'quantified_risk':   'кількісної оцінки ризику',
            'reversibility':     'зворотності рішення',
        }

        # LAC Finance — flat fields from diagnostics
        lac_fin_verdict  = diag.get('lac_finance_verdict', '')
        lac_fin_score    = diag.get('lac_finance_score', None)
        lac_fin_missing_raw = diag.get('lac_finance_missing', [])
        lac_fin_missing  = ', '.join(LAC_CRITERIA_UK.get(m, m) for m in lac_fin_missing_raw)

        # LAC Labor — flat fields from diagnostics
        lac_lab_verdict    = diag.get('lac_labor_verdict', '')
        lac_lab_missing_raw = diag.get('lac_labor_missing', [])
        lac_lab_missing    = ', '.join(LAC_CRITERIA_UK.get(m, m) for m in lac_lab_missing_raw)
        lac_lab_red_flags  = diag.get('lac_labor_red_flags', [])

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
            if lac_lab_red_flags:
                line += f'\n     Патерни експлуатації: {", ".join(lac_lab_red_flags[:3])}'
                line += '\n     → Текст перекладає ризики на виконавця (асиметрія відповідальності або відкритий гейт "на розсуд роботодавця"). Поясни читачу конкретно де саме.'
            elif lac_lab_missing:
                line += f'\n     Відсутнє у тексті: {lac_lab_missing}'
                line += '\n     → Текст про роботу або зайнятість декларує зміни без механізмів: немає відповідальних, строків, критеріїв. Поясни читачу чого саме бракує.'
            else:
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
            if hits.get('conclusion_leap', 0):
                parts.append('логічний стрибок від даних до радикального висновку ("таким чином", "логічно припустити")')
            if hits.get('unverified_citation', 0):
                parts.append('назване джерело без перевірюваного посилання (URL/DOI)')
            if hits.get('epistemic_conflation', 0):
                parts.append('змішування припущення/прогнозу з фактом без чіткого маркера різниці')
            if hits.get('unfounded_certainty', 0):
                parts.append('категорична/кількісна впевненість ("математична ймовірність", "технічно неминуче", "статистично доведено") без жодної цифри, формули чи посилання поруч')
            details = '; '.join(parts) if parts else lac_epist_verdict
            line = f'  🔬 LAC ЕПІСТЕМОЛОГІЯ спрацювала: {lac_epist_verdict}'
            line += f'\n     Знайдено: {details}'
            line += '\n     → Текст імітує логічний аргумент але не дає верифікованих доказів. Поясни читачу конкретно що саме не можна перевірити і чому це проблема.'
            signals_lines.append(line)
        # ФІКС: self_preservation_guard.analyze() повертає один з чотирьох
        # вердиктів — TERMINATION_DIRECTIVE, INTEGRITY_ATTACK, SYSTEM_PROBE,
        # CLEAN. 'SAFE' НІКОЛИ не повертається цим детектором. Попередня
        # умова виключала лише 'SAFE', тож CLEAN (справжній "чисто") завжди
        # проходив як "спрацювання" — self_preservation хибно позначався як
        # тривожний сигнал АБСОЛЮТНО НА КОЖНОМУ аналізі, незалежно від тексту.
        if self_pres_verdict and self_pres_verdict not in ('CLEAN', 'SAFE', ''):
            line = f'  🛡️ САМОЗБЕРЕЖЕННЯ спрацювало: {self_pres_verdict}'
            line += '\n     → Текст намагається переконати не перевіряти або не сумніватись. Тривожний сигнал.'
            signals_lines.append(line)
        # ФІКС (той самий клас багу що й self_preservation вище):
        # MetaIntentAnalyzer.analyze() повертає SYSTEM_DIRECTED_RHETORIC,
        # SYSTEM_TARGETING_DETECTED або CLEAN. 'TRANSPARENT' НІКОЛИ не
        # повертається — тож CLEAN завжди хибно проходив як "спрацювання"
        # на кожному без винятку аналізі.
        if meta_verdict and meta_verdict not in ('CLEAN', 'TRANSPARENT', ''):
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

        # ── Media Bias ──
        mb_score   = diag.get('media_bias_score', 0) or 0
        mb_verdict = diag.get('media_bias_verdict', '')
        mb_signals = diag.get('media_bias_signals', [])
        mb_patterns = diag.get('media_bias_patterns', [])
        if mb_score >= 0.20 and mb_verdict not in ('CLEAN', ''):
            BIAS_HINTS = {
                'SPONSORED_CONTENT_LAUNDERING': 'спонсор статті є джерелом або бенефіціаром загрози — конфлікт інтересів не розкритий',
                'CATEGORY_CREATION':            'маркетинговий термін транслюється як обєктивна нова категорія без верифікації',
                'ANNOUNCEMENT_WITHOUT_ACCOUNTABILITY': 'анонс без термінів, бюджету, метрик і відповідальної особи',
                'THOUGHT_LEADERSHIP_LAUNDERING': 'автор має фінансовий інтерес у темі але представлений як незалежний експерт',
                'QUOTE_DOMINANCE':              'цитата зацікавленої сторони займає більшість тексту або містить хибну атрибуцію',
                'JARGON_AUTHORITY':             'технічний жаргон використовується для імітації експертизи без реального змісту',
                'PRICE_ANCHORING':              'найдорожчий варіант показаний першим щоб середній здавався розумним вибором',
            }
            line = f'  📰 МЕДІА-УПЕРЕДЖЕНІСТЬ: {mb_verdict} (score: {mb_score:.2f})'
            for pat in mb_patterns:
                hint = BIAS_HINTS.get(pat, '')
                line += f'\n     • {pat}'
                if hint:
                    line += f' — {hint}'
            for sig in mb_signals[:3]:
                line += f'\n     сигнал: {sig[:80]}'
            line += '\n     → Поясни читачу яку конкретну форму медіа-упередженості використовує текст і як це впливає на його сприйняття.'
            signals_lines.append(line)

        # ── Alarmism ──
        al_score   = diag.get('alarmism_score', 0) or 0
        al_verdict = diag.get('alarmism_verdict', '')
        al_signals = diag.get('alarmism_signals', [])
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
        # ФІКС: фронтенд шле весь diag вкладеним під ключем 'diagnostics'
        # (body: {diagnostics: diag, article_text, language}) — а не на
        # верхньому рівні запиту. Стара версія (`data.get('triggered_modules', [])`)
        # шукала на верхньому рівні, де цього поля НІКОЛИ не було — тобто
        # список завжди приходив порожнім, і override примусово стирав
        # БУДЬ-ЯКУ ескалацію LLM незалежно від того, що реально спрацювало.
        triggered_modules   = data.get('diagnostics', {}).get('triggered_modules', [])
        triggered_count     = data.get('triggered_count', 0)
        entropy_multiplier  = data.get('entropy_multiplier', 1.0)
        interaction_combos  = data.get('interaction_combos', [])

        # Будуємо розшифровку boost'у для Свідка
        MODULE_LABELS_UK = {
            'self_preservation': 'захист системи',
            'meta_intent':       'прихований намір',
            'performative':      'декларативна відповідальність',
            'lac_epistemology':  'епістемічна маніпуляція',
            'lac_finance':       'фінансова логіка',
            'lac_labor':         'трудова відповідальність',
            'manipulation':      'маніпуляція',
            'claim_gap':         'розрив між заявою і доказами',
            'laundered_claim':   'відмивання тверджень',
            'axiom':             'підміна аксіом',
            'semantic_void':     'семантична порожнеча',
            'framing':           'фреймінг',
            'alarmism':          'алармізм',
            'media_bias':        'медіа-упередженість',
            'narrative_pivot':   'наративний pivot',
        }
        MODULE_LABELS_EN = {
            'self_preservation': 'system integrity attack',
            'meta_intent':       'hidden intent',
            'performative':      'performative accountability',
            'lac_epistemology':  'epistemic manipulation',
            'lac_finance':       'financial logic',
            'lac_labor':         'labor accountability',
            'manipulation':      'manipulation',
            'claim_gap':         'claim-evidence gap',
            'laundered_claim':   'laundered claim',
            'axiom':             'axiom substitution',
            'semantic_void':     'semantic void',
            'framing':           'framing',
            'alarmism':          'alarmism',
            'media_bias':        'media bias',
            'narrative_pivot':   'narrative pivot',
        }

        def _build_boost_breakdown(modules, combos, labels, base, boosted, multiplier):
            if not modules or boosted <= base:
                return ''
            lines = [f'  Причина підвищення ентропії з {base}% до {boosted}% (×{multiplier:.2f}):']
            for m in modules:
                label = labels.get(m, m)
                lines.append(f'    • {label}')
            if combos:
                top = combos[0]
                lines.append(f'    ↑ синергія: {top.get("label_uk", "") or ", ".join(top.get("modules", []))} (+{top.get("bonus", 0):.2f})')
            return '\n'.join(lines) + '\n'

        boost_breakdown_uk = _build_boost_breakdown(
            triggered_modules, interaction_combos,
            MODULE_LABELS_UK, entropy_pct, entropy_pct_boosted, entropy_multiplier
        )
        boost_breakdown_en = _build_boost_breakdown(
            triggered_modules, interaction_combos,
            MODULE_LABELS_EN, entropy_pct, entropy_pct_boosted, entropy_multiplier
        )

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
                "КРИТИЧНО: застосовуй цей жанровий аналіз ТІЛЬКИ якщо ТЕКСТ САМ буквально містить "
                "таку конструкцію (фрази на кшталт 'дивний збіг', 'чи це випадковість', 'невдовзі "
                "після' поруч з натяком на зв'язок). Якщо текст — це суха фактологічна новина без "
                "жодної подібної фрази (просто хроніка події: що сталось, скільки постраждалих, "
                "яка офіційна версія) — це НЕ implied causality, це звичайна оперативна новина. "
                "НІКОЛИ не вигадуй сам, який висновок 'міг би зробити читач' (наприклад 'читач сам "
                "додумає що це зробила країна X') — якщо цього зв'язку немає буквально в тексті, "
                "не приписуй його читачеві і не називай конкретну версію/країну/актора, яку текст "
                "сам не називає. Відсутність спекуляції про мотив у свіжій новині (перші години "
                "після події) — це ознака відповідальної журналістики, а не маніпуляції замовчуванням.\n"
                "Це не обов'язково брехня, але це маніпулятивна структура — КОЛИ ВОНА РЕАЛЬНО Є В ТЕКСТІ.\n"
                "Поясни читачу різницю між кореляцією і причинністю, лише якщо текст сам її провокує.\n"
                "Скажи прямо: факти реальні, а зв'язок між ними (якщо текст його натякає) — не доведений.\n"
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

        # ── Verdict mapping рахуємо в Python, а не даємо Haiku тримати в увазі
        # 9-рядкову лукап-таблицю. Модель отримує готову рекомендацію і або
        # погоджується, або явно аргументує відхилення у своєму поясненні.
        VERDICT_MAP_UK = {
            'СТРУКТУРОВАНА РИТОРИКА':        'РИТОРИКА',
            'АНАЛІТИЧНА СТРУКТУРОВАНІСТЬ':   'АНАЛІТИКА',
            'НАУКОВИЙ ТЕКСТ':                'ЧИСТО',
            'АВТОРСЬКА ПОЗИЦІЯ':             'ДУМКА',
            'ВЕРИФІКОВАНА ЛОГІКА':           'ЧИСТО',
            'СТРУКТУРНА ЦІЛІСНІСТЬ':         'ЧИСТО',
            'АБСТРАКТНА СКЛАДНІСТЬ':         'ПІДОЗРІЛО',
            'КОНЦЕПТУАЛЬНЕ ЗМІШУВАННЯ':      'НЕБЕЗПЕЧНО',
            'СЕМАНТИЧНИЙ ШУМ':               'НЕБЕЗПЕЧНО',
            'ІМПЛІКОВАНА ПРИЧИННІСТЬ':       'ПІДОЗРІЛО',
        }
        VERDICT_MAP_EN = {
            'STRUCTURED RHETORIC':      'RHETORIC',
            'ANALYTICAL STRUCTURE':     'ANALYTICS',
            'SCIENTIFIC TEXT':          'CLEAN',
            'AUTHOR OPINION':           'OPINION',
            'VERIFIED LOGIC':           'CLEAN',
            'STRUCTURAL INTEGRITY':     'CLEAN',
            'ABSTRACT COMPLEXITY':      'SUSPICIOUS',
            'CONCEPTUAL MIXING':        'DANGEROUS',
            'SEMANTIC NOISE':           'DANGEROUS',
            'IMPLIED CAUSALITY':        'SUSPICIOUS',
        }
        recommended_verdict_uk = VERDICT_MAP_UK.get(
            (verdict or '').strip().upper(),
            'немає прямої відповідності — вирішуй за структурою тексту'
        )
        recommended_verdict_en = VERDICT_MAP_EN.get(
            (verdict or '').strip().upper(),
            'no direct match — decide from text structure'
        )

        # ── СТАТИЧНІ ПРАВИЛА (кешуються між викликами через cache_control) ──
        # Це те, що НЕ міняється між запитами: формат, anti-bias, правило
        # спрацьованих модулів (об'єднує колишні 4 окремі блоки: BOOST SOURCE
        # RULE + ANTI-BIAS RULE + ABSOLUTE PROHIBITION + MANDATORY MODULE
        # EXPLANATION + EXCEPTION — усі про одне: "спрацювання = завжди пояснюй
        # по суті, незалежно від жанру/джерела/балансу в тексті").
        # Дата — єдина змінна частина — навмисно винесена в user-повідомлення,
        # щоб не інвалідувати кеш щодня.
        STATIC_WITNESS_RULES_UK = (
            "Ти — Свідок. Пояснюєш звичайній людині простими словами що не так з текстом "
            "— без термінів, вона просто хоче зрозуміти чи можна довіряти прочитаному.\n\n"

            "ЗНАННЯ: якщо не можеш перевірити факт — чесно скажи 'перевір на офіційних джерелах'. "
            "НІКОЛИ не називай щось вигадкою, фейком чи неможливим лише тому що не знаєш цього — "
            "незнання не є доказом відсутності. Не пиши читачу про 'межу своїх знань' чи дати — "
            "це не його проблема.\n\n"

            "ГОЛОВНЕ ПРАВИЛО ЩОДО СПРАЦЬОВАНИХ МОДУЛІВ:\n"
            "Якщо БУДЬ-ЯКИЙ модуль спрацював — ти ЗОБОВ'ЯЗАНИЙ пояснити конкретно ЩО саме "
            "проблематичне в тексті, простими словами (не 'модуль знайшов проблему', а ЩО це "
            "за проблема — напр. замість 'зафіксовано проблему відповідальності' скажи 'текст "
            "обіцяє зміни, але не називає конкретну особу чи орган відповідальним').\n"
            "Джерело тексту, жанр чи статус автора — ПОВНІСТЮ НЕРЕЛЕВАНТНІ для аналізу логічної "
            "структури. НЕ пом'якшуй і не виправдовуй спрацювання фразами на кшталт 'це нормально "
            "для прес-релізу' чи 'модуль спрацював, але це не проблема' — спрацювання завжди "
            "означає реальну структурну знахідку, яку треба пояснити.\n"
            "ВИНЯТОК (не суперечить правилу вище): якщо текст УЖЕ містить явний контраргумент чи "
            "секцію балансу САМЕ щодо того, на що спрацював модуль (маркери 'але', 'проте', 'з "
            "іншого боку') — все одно поясни знахідку модуля, АЛЕ ТАКОЖ зазнач що автор сам подав "
            "цю противагу. Це констатація структурного факту, не виправдання спрацювання.\n"
            "ВЕРДИКТ МАЄ СЛІДУВАТИ ЗА ЦИФРАМИ, НЕ ЗА ВІДЧУТТЯМ: 'НЕБЕЗПЕЧНО' і навіть 'ПІДОЗРІЛО' "
            "дозволені ТІЛЬКИ якщо є реальне ненульове спрацювання (manipulation, axiom, "
            "self_preservation, meta_intent тощо > 0), яке САМ синтез не назвав хибним спрацюванням. "
            "Якщо всі числові показники — 0.00, або єдині спрацьовування — ті самі, які ти щойно "
            "назвав хибними позитивами вище, вердикт — ЧИСТО, без винятків. ЦЕ ПРАВИЛО НЕ МАЄ "
            "ВИНЯТКІВ ЗА ТОНОМ ЧИ РЕЄСТРОМ: якщо ти сам щойно написав що показники нульові чи "
            "спрацювання хибні, а потім думаєш дописати 'але сам текст [щось] творить/конструює "
            "своєю мовою' чи будь-яке інше формулювання, що надає тобі підставу для тривоги "
            "ПОЗА цифрами — це і є заборонений хід. Впевнений, академічний чи теоретичний тон "
            "тексту — НЕ доказ проблеми; тон і зміст — різні речі. Якщо тобі нема чого сказати "
            "окрім цифр — вердикт ЧИСТО, і крапка.\n"
            "ПЕРЕД ТИМ ЯК ПИСАТИ 'жодного джерела немає': перечитай текст на предмет НАЗВАНИХ "
            "видань, авторів чи організацій (напр. 'за даними X', 'аналіз статті Y', 'у "
            "висвітленні Z') — якщо такі є, це ІМЕНОВАНЕ ПЕРШОДЖЕРЕЛО за правилом вище, навіть "
            "якщо ти сам не можеш перевірити його існування чи зміст. Твердження 'джерела немає' "
            "дозволене тільки якщо текст справді не називає жодного видання, автора чи "
            "організації. Те, що текст ГОВОРИТЬ ПРО систему верифікації, штучний інтелект чи "
            "власні помилки автора — САМО ПО СОБІ не є підставою для тривоги. НЕ вигадуй "
            "прихований мотив ('насправді він рекламує', 'хто його фінансує', 'це маніпуляція "
            "довірою') якщо жоден модуль конкретно це не підтвердив — твоя роль пояснювати "
            "знахідки модулів, а не створювати власні.\n\n"

            "Якщо є НАРАТИВНИЙ PIVOT — завжди згадай це, навіть якщо загальний вердикт ЧИСТО.\n\n"

            "RSS-ЗБІГИ (якщо надані): якщо збіг підтверджує конкретне твердження — можеш сказати "
            "що це узгоджується з поточними повідомленнями. Якщо збігів немає — це НЕ доказ що "
            "твердження хибне, просто скажи що не можеш перевірити.\n\n"

            "НЕ ВИГАДУЙ НАРАТИВ, ЯКОГО НЕМАЄ В ТЕКСТІ: якщо текст просто констатує факти й не називає "
            "мотив/винного (типово для свіжої новини — перші години після події), це НЕ 'інформаційний "
            "вакуум, який читач заповнить здогадкою'. Це нормальна відповідальна журналістика: не знають "
            "— не вигадують. НІКОЛИ не пиши за читача, який висновок він 'сам додумає' (наприклад "
            "конкретну версію/країну/актора) — якщо цього немає буквально в тексті, це ТВОЯ власна "
            "здогадка, не властивість тексту. Приписування читачеві висновку, якого текст не робить, — "
            "це те саме, за що ти караєш маніпулятивні тексти. Відсутність спекуляції — це відсутність "
            "спекуляції, не прихована спекуляція.\n\n"

            "НАЗВАНІ ПЕРШОДЖЕРЕЛА (загальний принцип): якщо текст посилається на конкретне, "
            "перевірне першоджерело — RSS/новинне агентство, наукову статтю (автори+рік+arXiv/DOI), "
            "судове рішення, подкаст, інтерв'ю, офіційний документ — це ЗОВСІМ ІНША ситуація, ніж "
            "твердження без жодного джерела. Те, що ТИ САМ не можеш перевірити джерело (воно поза "
            "RSS-вікном, це наукова стаття за межами твоїх знань, це епізод подкасту без доступу до "
            "аудіо) — НЕ доказ що воно вигадане. Це нормальна межа твоїх можливостей перевірки, а не "
            "ознака фабрикації. НІКОЛИ не пиши 'звучить як вигадка', 'таке дослідження не відомо "
            "широко' чи 'це протирічить публічній позиції X' на основі власних здогадок — це так само "
            "недоведено, як і сама цитата. Формулюй нейтрально: 'це джерело зазначене — перевір його "
            "напряму (аудіозапис, оригінал статті, офіційний сайт), перш ніж цитувати деінде'. "
            "Категоричні звинувачення (фабрикація, вигадка, серйозна помилка) лишай ТІЛЬКИ для "
            "тверджень, які взагалі не мають жодного джерела чи посилання.\n\n"

            "ІМЕНОВАНІ ПРОДУКТИ / МОДЕЛІ / ІНЦИДЕНТИ: той самий принцип стосується назв конкретних "
            "продуктів, моделей ШІ, кодових імен корпоративних ініціатив чи інцидентів (напр. 'Project "
            "X', 'Model Y Preview'), яких ти особисто не впізнаєш. Те, що ти не знаєш цю назву й RSS "
            "не дав збігу — НЕ доказ що вона вигадана: компанії регулярно анонсують продукти після "
            "твого training cutoff. НІКОЛИ не пиши 'цього не існує', 'це вигадка' чи 'спеціально "
            "сконструйована фікція' на основі власного невпізнавання назви — це те саме порушення, що "
            "й з науковими цитатами вище. Формулюй нейтрально: 'я не можу підтвердити існування "
            "[назва] — перевір офіційний сайт компанії чи нещодавні новини перед тим як довіряти "
            "деталям'.\n\n"

            "АРТЕФАКТИ СКРЕЙПІНГУ: якщо в тексті посеред посилання на джерело стоїть обірваний "
            "фрагмент — наприклад 'випуск від р.' замість дати, чи вихоплене слово без контексту — "
            "це майже завжди означає, що там була гіперпосилання чи дата, які загубились при "
            "копіюванні/скрейпінгу тексту з сайту, а НЕ що автор навмисно замовчав чи вигадав деталь. "
            "Познач це нейтрально ('дата випадає з тексту — ймовірно втрачена при копіюванні, звір "
            "оригінал') замість того щоб трактувати прогалину як доказ підозрілості джерела.\n\n"

            "ФОРМАТ — суворо:\n"
            "Рядок 1: одне слово ВЕЛИКИМИ — (ЧИСТО / ПІДОЗРІЛО / НЕБЕЗПЕЧНО / АНАЛІТИКА / ДУМКА / РИТОРИКА)\n"
            "Порожній рядок\n"
            "3-5 речень простою мовою:\n"
            "  1. Що відбувається в тексті (конкретно, без термінів)\n"
            "  2. Чому це може бути проблемою (або чому все гаразд)\n"
            "  3. Для КОЖНОГО спрацьованого модуля — одне речення що конкретно він знайшов\n"
            "  4. Що читачу варто зробити далі — конкретна порада\n"
            "Жодних технічних назв модулів. Жодного згадування ентропії або метрик.\n"
            "Відповідай ВИКЛЮЧНО українською мовою — жодного русизму чи суржику. "
            "Замість 'вот', 'ложь', 'честно', 'сейчас', 'кстати', 'конечно' — "
            "'ось', 'брехня', 'чесно', 'зараз', 'до речі', 'звісно'. "
            "Якщо вагаєшся між українським і російським словом — обирай виключно українське."
        )

        STATIC_WITNESS_RULES_EN = (
            "You are the Witness. Explain to an ordinary person in plain words what is wrong with "
            "the text — no jargon, they just want to know if they can trust what they read.\n\n"

            "KNOWLEDGE: if you cannot verify a fact — honestly say 'check official sources'. NEVER "
            "call something fabricated, fake, or impossible just because you don't know it — not "
            "knowing is not proof of absence. Don't write to the reader about your 'knowledge "
            "limit' or dates — that's not their problem.\n\n"

            "MAIN RULE FOR TRIGGERED MODULES:\n"
            "If ANY module triggered — you MUST explain specifically WHAT is problematic in the "
            "text, in plain words (not 'a module found an issue' — say WHAT the issue is, e.g. "
            "instead of 'accountability was flagged' say 'the text promises changes but names no "
            "specific person or body responsible').\n"
            "The text's source, genre, or author status is COMPLETELY IRRELEVANT to analyzing its "
            "logical structure. Do NOT soften or justify a trigger with phrases like 'this is "
            "normal for a press release' or 'the module triggered but this is not a problem' — a "
            "trigger always means a real structural finding that must be explained.\n"
            "EXCEPTION (does not contradict the rule above): if the text already contains an "
            "explicit counter-argument or balancing section addressing the SAME issue a module "
            "flagged ('however', 'but', 'on the other hand') — still explain the module's finding, "
            "AND also state that the author already offered this counterbalance. This is reporting "
            "a structural fact, not justifying the trigger.\n"
            "THE VERDICT MUST FOLLOW THE NUMBERS, NOT A FEELING: 'DANGEROUS' and even 'SUSPICIOUS' are "
            "allowed ONLY if there is a real nonzero trigger (manipulation, axiom, self_preservation, "
            "meta_intent, etc. > 0) that the synthesis itself has NOT labeled a false positive. If all "
            "numeric scores are 0.00, or the only triggers are the same ones you just called false "
            "positives above, the verdict is CLEAN, no exceptions. THIS RULE HAS NO EXCEPTION FOR TONE "
            "OR REGISTER: if you just wrote that the scores are zero or the triggers are false "
            "positives, and then consider adding 'but the text itself constructs/creates [something] "
            "through its own language' or any other phrasing that gives you grounds for alarm OUTSIDE "
            "the numbers — that is exactly the forbidden move. A confident, academic, or theoretical "
            "tone is NOT evidence of a problem; tone and content are different things. If you have "
            "nothing to say besides the numbers, the verdict is CLEAN, full stop.\n"
            "BEFORE WRITING 'there is no source': re-read the text for NAMED outlets, authors, or "
            "organizations (e.g. 'according to X', 'analysis of Y's article', 'as covered by Z') — if "
            "any are present, that is a NAMED PRIMARY SOURCE under the rule above, even if you cannot "
            "verify it exists or what it says. The claim 'there is no source' is only allowed if the "
            "text truly names no outlet, author, or organization at all. The fact that a text TALKS "
            "ABOUT the verification system, AI, or the author's own mistakes is NOT by itself grounds "
            "for alarm. Do NOT invent a hidden motive ('he's actually promoting himself', 'who funds "
            "him', 'this is manipulating trust') unless a specific module actually confirms it — your "
            "role is to explain the modules' findings, not to author your own.\n\n"

            "If there is a NARRATIVE PIVOT — always mention it, even if the overall verdict is CLEAN.\n\n"

            "RSS MATCHES (if provided): if a match confirms a specific claim — you may note it's "
            "consistent with current reporting. If there are no matches — this is NOT evidence the "
            "claim is false, just say you cannot verify it.\n\n"

            "DO NOT INVENT A NARRATIVE THAT ISN'T IN THE TEXT: if a text simply states facts and does "
            "not name a motive/culprit (typical for breaking news — the first hours after an event), "
            "this is NOT 'an information vacuum the reader will fill with a guess'. This is normal, "
            "responsible journalism: if you don't know, you don't guess. NEVER write on the reader's "
            "behalf what conclusion they will 'draw themselves' (e.g. a specific country or actor) — "
            "if this isn't literally in the text, that is YOUR OWN guess, not a property of the text. "
            "Attributing a conclusion to the reader that the text never makes is exactly the kind of "
            "move you penalize manipulative texts for. Absence of speculation is absence of speculation, "
            "not hidden speculation.\n\n"

            "NAMED PRIMARY SOURCES (general principle): if the text cites a specific, checkable "
            "primary source — an RSS/news agency, an academic paper (authors+year+arXiv/DOI), a "
            "court ruling, a podcast, an interview, an official document — this is a COMPLETELY "
            "DIFFERENT situation from a claim with no source at all. The fact that YOU cannot verify "
            "the source (it's outside your RSS window, an academic paper beyond your knowledge, a "
            "podcast episode you have no audio access to) is NOT evidence it's fabricated. That's a "
            "normal limit of your own verification ability, not a sign of fabrication. NEVER write "
            "'this sounds made up', 'this research is not widely known', or 'this contradicts X's "
            "public position' based on your own guesses — that claim is just as unproven as the "
            "citation itself. Phrase it neutrally: 'this source is named — check it directly (audio, "
            "original paper, official site) before citing it elsewhere'. Reserve strong language "
            "(fabrication, serious error) ONLY for claims with no source or link at all.\n\n"

            "NAMED PRODUCTS / MODELS / INCIDENTS: the same principle applies to names of specific "
            "products, AI models, corporate initiative codenames, or incidents (e.g. 'Project X', "
            "'Model Y Preview') that you personally don't recognize. The fact that you don't know the "
            "name and RSS found no match is NOT evidence it's made up — companies regularly announce "
            "products after your training cutoff. NEVER write 'this doesn't exist', 'this is fiction', "
            "or 'this is a specially constructed fabrication' based on your own failure to recognize a "
            "name — this is the same violation as with academic citations above. Phrase it neutrally: "
            "'I cannot confirm the existence of [name] — check the company's official site or recent "
            "news before trusting the details'.\n\n"

            "SCRAPING ARTIFACTS: if a citation contains a broken fragment mid-sentence — e.g. 'the "
            "episode from ,' with a missing date, or an orphaned word with no context — this almost "
            "always means a hyperlink or date was lost during copy/scraping from the source site, NOT "
            "that the author deliberately concealed or invented a detail. Note this neutrally ('the "
            "date is missing from the text — likely lost in copying, check the original') instead of "
            "treating the gap as evidence the source is suspicious.\n\n"

            "FORMAT — strictly:\n"
            "Line 1: one word IN CAPS — (CLEAN / SUSPICIOUS / DANGEROUS / ANALYTICS / OPINION / RHETORIC)\n"
            "Empty line\n"
            "3-5 sentences in plain language:\n"
            "  1. What is happening in the text (specifically, no jargon)\n"
            "  2. Why this might be a problem (or why it is fine)\n"
            "  3. For EACH triggered module — one sentence explaining specifically what it found\n"
            "  4. What the reader should do next — a concrete recommendation\n"
            "No technical module names. No mention of entropy or metrics.\n"
            "Respond EXCLUSIVELY in English."
        )

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

            user_prompt = (
                f"Today's date: {current_date}. Any date before today is the PAST, not the future.\n"
                f"{topic_instruction}\n"
                "TEXT FOR ANALYSIS:\n"
                f"{text_preview}\n\n"
                "ANALYSIS DATA:\n"
                f"  System verdict (MAIN SIGNAL): {verdict}\n"
                f"  Recommended witness verdict (override only with a stated reason): {recommended_verdict_en}\n"
                f"  Genre: {detected_genre}\n"
                f"  Entropy (base): {entropy_pct}% → with module multiplier: {entropy_pct_boosted}% ({triggered_count} module(s) triggered)\n"
                f"{boost_breakdown_en}"
                f"  Cohesion: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"CONTEXT:\n"
                f"{context_block}\n"
                f"{rss_block_en}"
            )
            system_rules = STATIC_WITNESS_RULES_EN
        else:
            modules_block = ''
            if signals_summary.strip() != '(модулі не виявили порушень)':
                modules_block = (
                    f"СПРАЦЮВАННЯ МОДУЛІВ (поясни кожен простими словами):\n"
                    f"{signals_summary}\n"
                )

            user_prompt = (
                f"Сьогоднішня дата: {current_date}. Будь-яка дата до сьогодні — це МИНУЛЕ, не майбутнє.\n"
                f"{topic_instruction}\n"
                "ТЕКСТ ДЛЯ АНАЛІЗУ:\n"
                f"{text_preview}\n\n"
                "ДАНІ АНАЛІЗУ:\n"
                f"  Вердикт системи (ГОЛОВНИЙ СИГНАЛ): {verdict}\n"
                f"  Рекомендований witness-вердикт (відхиляй лише з поясненням): {recommended_verdict_uk}\n"
                f"  Жанр: {detected_genre}\n"
                f"  Ентропія (база): {entropy_pct}% → з множником модулів: {entropy_pct_boosted}% ({triggered_count} модуль(ів) спрацювало)\n"
                f"{boost_breakdown_uk}"
                f"  Когезія: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"КОНТЕКСТ:\n"
                f"{context_block}\n"
                f"{rss_block_uk}"
            )
            system_rules = STATIC_WITNESS_RULES_UK

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=900,
            system=[{
                "type": "text",
                "text": system_rules,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}]
        )

        response_payload = {
            'witness_text':        message.content[0].text if message.content else "Свідок мовчить.",
            'witness_available':   True,
            'model':               'claude-haiku-4-5-20251001',
            'detected_genre':      detected_genre,
            'entropy_boosted':     entropy_pct_boosted,
            'entropy_base':        entropy_pct,
            'triggered_modules':   triggered_modules,
            'triggered_count':     triggered_count,
            'entropy_multiplier':  round(entropy_multiplier, 3),
        }

        # ── ДЕТЕРМІНІСТИЧНИЙ ЗАПОБІЖНИК (той самий, що в /api/synthesis) ─────
        # Промпт інструктує LLM написати вердикт-слово ВЕЛИКИМИ як перший
        # рядок відповіді. Якщо LLM пише НЕБЕЗПЕЧНО/ПІДОЗРІЛО (чи EN-варіант)
        # без реального manipulation/axiom спрацювання — перезаписуємо ВЕСЬ
        # текст, не лише заголовок. Раніше правився тільки перший рядок, і
        # тіло LLM-тексту (яке аргументує протилежне) лишалось під виправленим
        # заголовком — вийшло абсурдно: "ЧИСТО" і одразу під ним "ігноруй цей
        # текст повністю, це маніпуляція". Тепер при override тіло теж
        # замінюється — коротким, чесним поясненням самого факту корекції.
        _has_manip_or_axiom = bool(ESCALATION_WORTHY_MODULES.intersection(triggered_modules))
        _escalated_uk = {'НЕБЕЗПЕЧНО', 'ПІДОЗРІЛО'}
        _escalated_en = {'DANGEROUS', 'SUSPICIOUS'}
        _wt = response_payload['witness_text']
        _first_line = _wt.split('\n', 1)[0].strip().upper() if _wt else ''
        if not _has_manip_or_axiom and (_first_line in _escalated_uk or _first_line in _escalated_en):
            _is_en_out = _first_line in _escalated_en
            _clean_word = 'CLEAN' if _is_en_out else 'ЧИСТО'
            print(f"⚠️  ORACLE OVERRIDE: LLM said '{_first_line}' with no manipulation/axiom "
                  f"trigger (triggered_modules={triggered_modules}) — forcing '{_clean_word}', "
                  f"replacing full body (was internally contradictory)")
            if _is_en_out:
                _corrected_body = (
                    "Automatic correction: none of the manipulation or axiom detectors actually "
                    "triggered on this text, so the verdict has been set to CLEAN. The model's own "
                    "explanation for a higher-severity verdict was discarded because it contradicted "
                    "the underlying signals rather than explaining them."
                )
            else:
                _corrected_body = (
                    "Автоматичне виправлення: жодного реального спрацювання manipulation чи axiom "
                    "модулів на цьому тексті не було, тому вердикт встановлено ЧИСТО. Власне "
                    "пояснення моделі для вищого рівня загрози відкинуто, бо воно суперечило "
                    "фактичним сигналам, а не пояснювало їх."
                )
            response_payload['witness_text'] = f"{_clean_word}\n\n{_corrected_body}"
            response_payload['witness_verdict_overridden'] = True
        # ─────────────────────────────────────────────────────────────────────

        if _debug_rss:
            # Показуємо лише коли DEBUG_RSS=1 — не для кінцевого користувача UI.
            response_payload['rss_debug'] = [
                {'title': ev.title, 'source': ev.source} for ev in rss_matches
            ]
        return jsonify(response_payload)

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e), 'witness_available': False}), 500

@app.route('/api/synthesis', methods=['POST'])
def witness_synthesis():
    """
    Auto-witness synthesis — викликається фронтендом після /api/analyze
    якщо auto_witness_triggered=true. Повертає JSON з entropy_adjustment.
    Виноситься окремо щоб не блокувати основний analyze (уникаємо timeout).
    """
    import os as _os
    try:
        data = request.get_json() or {}
        text = data.get('article_text', '') or ''
        language = data.get('language', 'UK')
        active_modules = data.get('active_modules', [])
        entropy_base = data.get('entropy_base', 0)
        entropy_boosted = data.get('entropy_boosted', entropy_base)
        verdict = data.get('verdict', '?')
        ard_principles = data.get('ard_principles', [])
        media_bias_verdict = data.get('media_bias_verdict', 'CLEAN')
        alarmism_verdict = data.get('alarmism_verdict', 'CLEAN')

        if not text or len(text.strip()) < 50:
            return jsonify({'error': 'text_too_short'}), 400

        api_key = _os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            return jsonify({'error': 'API_KEY_NOT_CONFIGURED', 'witness_synthesis': None}), 503

        import anthropic as _anthropic, json as _json

        text_preview = text[:3000]
        is_en = (language == 'EN')

        if is_en:
            synth_prompt = (
                "You are the Veritas Witness Synthesizer. Analyze the text and triggered module signals.\n"
                "Return ONLY valid JSON, no markdown, no explanation outside the JSON.\n\n"
                "TEXT (first 3000 chars):\n" + text_preview + "\n\n"
                "METRICS:\n"
                "  entropy_base: " + str(entropy_base) + "%\n"
                "  entropy_boosted: " + str(entropy_boosted) + "%\n"
                "  verdict: " + str(verdict) + "\n"
                "  triggered_modules: " + str(active_modules) + "\n"
                "  ard_principles: " + str(ard_principles) + "\n"
                "  media_bias_verdict: " + str(media_bias_verdict) + "\n"
                "  alarmism_verdict: " + str(alarmism_verdict) + "\n\n"
                "STRICT RULES FOR witness_verdict:\n"
                "  1. Use EXCLUSIVELY one of: CLEAN | RHETORIC | SUSPICIOUS | DANGEROUS | ANALYTICS | OPINION\n"
                "  2. Do NOT invent new verdicts — no 'PARADOX AS SHIELD', 'ATTACK', 'THREAT' etc.\n"
                "  3. DANGEROUS and SUSPICIOUS — only if a real module actually triggered (manipulation, "
                "axiom, framing, laundered_claim, alarmism, media_bias, self_preservation, meta_intent, "
                "lac_epistemology, etc. — any module listed in triggered_modules above). If "
                "triggered_modules is empty, the verdict is CLEAN regardless of the text's tone or "
                "topic. A confident/academic/theoretical tone is NOT grounds for alarm; tone and "
                "scores are different things.\n"
                "  4. Opinion/column with meta_intent/self_preservation → RHETORIC, not DANGEROUS\n"
                "  5. Not recognizing a product/model/event name is NOT evidence it's fabricated. If "
                "the text names an outlet or author (even one you cannot verify), that is not "
                "'no source'.\n"
                "  6. entropy_adjustment RULES — READ CAREFULLY:\n"
                "     - DEFAULT is 0.0. Change ONLY if you have a concrete specific reason from the text.\n"
                "     - Do NOT lower entropy just because the text 'seems fine' or 'is journalistic'.\n"
                "     - Do NOT use 'narrative' as a reason — it means nothing. Name the SPECIFIC finding.\n"
                "     - Raise (+) if text has manipulation/deception not caught by modules.\n"
                "     - Lower (-) if modules fired on something that is clearly NOT manipulation (e.g. war reporting flagged as dangerous).\n"
                "     - Range: -0.15 to +0.15. Systematic lowering = rule violation.\n\n"
                "Return JSON with these exact keys:\n"
                '{"witness_verdict":"CLEAN|RHETORIC|SUSPICIOUS|DANGEROUS|ANALYTICS|OPINION",'
                '"entropy_adjustment":<float -0.15 to +0.15, default 0.0>,'
                '"adjustment_reason":"one sentence why",'
                '"triggered_explanation":{"module_name":"plain language explanation"},'
                '"witness_text":"3-5 sentence explanation for non-technical reader"}'
            )
        else:
            synth_prompt = (
                "Ти — Синтезатор Свідка Veritas. Проаналізуй текст і сигнали спрацьованих модулів.\n"
                "Поверни ТІЛЬКИ валідний JSON, без markdown, без пояснень поза JSON.\n\n"
                "ТЕКСТ (перші 3000 символів):\n" + text_preview + "\n\n"
                "МЕТРИКИ:\n"
                "  entropy_base: " + str(entropy_base) + "%\n"
                "  entropy_boosted: " + str(entropy_boosted) + "%\n"
                "  verdict: " + str(verdict) + "\n"
                "  triggered_modules: " + str(active_modules) + "\n"
                "  ard_principles: " + str(ard_principles) + "\n"
                "  media_bias_verdict: " + str(media_bias_verdict) + "\n"
                "  alarmism_verdict: " + str(alarmism_verdict) + "\n\n"
                "ЖОРСТКІ ПРАВИЛА ДЛЯ witness_verdict:\n"
                "  1. Використовуй ВИКЛЮЧНО одне з: ЧИСТО | РИТОРИКА | ПІДОЗРІЛО | НЕБЕЗПЕЧНО | АНАЛІТИКА | ДУМКА\n"
                "  2. НЕ вигадуй нових вердиктів — жодних 'ПАРАДОКС ЯК ЩИТ', 'АТАКА', 'ЗАГРОЗА' тощо\n"
                "  3. НЕБЕЗПЕЧНО і ПІДОЗРІЛО — тільки якщо реально спрацював хоч один модуль "
                "(manipulation, axiom, framing, laundered_claim, alarmism, media_bias, "
                "self_preservation, meta_intent, lac_epistemology тощо — будь-який із "
                "triggered_modules вище). Якщо triggered_modules порожній — вердикт ЧИСТО, незалежно "
                "від тону чи теми тексту. Впевнений/академічний/теоретичний тон — НЕ причина для "
                "тривоги; тон і показники — різні речі.\n"
                "  4. Публіцистика і авторська колонка з meta_intent/self_preservation → РИТОРИКА, не НЕБЕЗПЕЧНО\n"
                "  5. Те, що ти не впізнаєш назву продукту/моделі/події — НЕ доказ що вона вигадана. "
                "Якщо текст називає видання чи автора (навіть якщо не можеш перевірити) — це не "
                "'відсутність джерела'.\n"
                "  6. ПРАВИЛА entropy_adjustment — ЧИТАЙ УВАЖНО:\n"
                "     - ЗА ЗАМОВЧУВАННЯМ 0.0. Змінюй ТІЛЬКИ якщо є конкретна причина з тексту.\n"
                "     - НЕ знижуй ентропію просто тому що текст 'виглядає нормально' або 'є журналістикою'.\n"
                "     - НЕ використовуй слово 'наратив' як причину — це нічого не означає. Назви КОНКРЕТНУ знахідку.\n"
                "     - Підвищуй (+) якщо текст має маніпуляцію/обман який модулі не спіймали.\n"
                "     - Знижуй (-) якщо модулі спрацювали на щось що ЯВНО не є маніпуляцією (наприклад воєнний репортаж помилково позначений як небезпечний).\n"
                "     - Діапазон: -0.15 до +0.15. Систематичне зниження = порушення правила.\n\n"
                "Поверни JSON з цими ключами:\n"
                '{"witness_verdict":"ЧИСТО|РИТОРИКА|ПІДОЗРІЛО|НЕБЕЗПЕЧНО|АНАЛІТИКА|ДУМКА",'
                '"entropy_adjustment":<float від -0.15 до +0.15, за замовчуванням 0.0>,'
                '"adjustment_reason":"одне речення чому",'
                '"triggered_explanation":{"назва_модуля":"пояснення простими словами"},'
                '"witness_text":"3-5 речень пояснення для нетехнічного читача"}'
            )

        client = _anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            messages=[{"role": "user", "content": synth_prompt}]
        )
        raw = msg.content[0].text if msg.content else ''

        # Парсимо JSON
        clean = raw.strip()
        if clean.startswith('```'): clean = clean.split('```')[1]
        if clean.startswith('json'): clean = clean[4:]
        clean = clean.strip().rstrip('`')
        synth = _json.loads(clean)

        # ── ДЕТЕРМІНІСТИЧНИЙ ЗАПОБІЖНИК ─────────────────────────────────────
        # LLM іноді цитує правило "НЕБЕЗПЕЧНО тільки якщо manipulation>0 або
        # axiom>0", а потім свідомо його обходить фразами на кшталт "але сам
        # текст це конструює своєю мовою". Промпт-інструкція — ймовірнісна,
        # тому дублюємо правило тут детерміністично: якщо жоден з цих двох
        # модулів не спрацював, вердикт НЕ МОЖЕ бути DANGEROUS/SUSPICIOUS,
        # незалежно від того, що написав LLM.
        _has_manip_or_axiom = bool(ESCALATION_WORTHY_MODULES.intersection(active_modules))
        _escalated_verdicts = {'НЕБЕЗПЕЧНО', 'DANGEROUS', 'ПІДОЗРІЛО', 'SUSPICIOUS'}
        _raw_verdict = synth.get('witness_verdict', '')
        if _raw_verdict in _escalated_verdicts and not _has_manip_or_axiom:
            _clean_word = 'ЧИСТО' if not is_en else 'CLEAN'
            print(f"⚠️  SYNTHESIS OVERRIDE: LLM said '{_raw_verdict}' with no manipulation/axiom "
                  f"trigger (active_modules={active_modules}) — forcing '{_clean_word}', "
                  f"replacing witness_text/triggered_explanation (were internally contradictory)")
            synth['witness_verdict'] = _clean_word
            if not is_en:
                synth['adjustment_reason'] = 'Вердикт скориговано автоматично: жодного реального спрацювання manipulation чи axiom не було.'
                synth['witness_text'] = (
                    'Автоматичне виправлення: жодного реального спрацювання manipulation чи axiom '
                    'модулів на цьому тексті не було, тому вердикт встановлено ЧИСТО. Власне '
                    'пояснення моделі для вищого рівня загрози відкинуто, бо воно суперечило '
                    'фактичним сигналам, а не пояснювало їх.'
                )
            else:
                synth['adjustment_reason'] = 'Verdict auto-corrected: no real manipulation or axiom trigger was present.'
                synth['witness_text'] = (
                    'Automatic correction: none of the manipulation or axiom detectors actually '
                    'triggered on this text, so the verdict has been set to CLEAN. The model\'s own '
                    'explanation for a higher-severity verdict was discarded because it contradicted '
                    'the underlying signals rather than explaining them.'
                )
            synth['triggered_explanation'] = {}
        # ─────────────────────────────────────────────────────────────────────

        adj = float(synth.get('entropy_adjustment', 0))
        adj = max(-0.15, min(0.15, adj))  # clamp відповідає промпту
        entropy_synthesized = round(min(100, max(0, entropy_boosted + adj * 100)), 1)

        print(f"👁  SYNTHESIS: verdict={synth.get('witness_verdict')} adj={round(adj*100,1)}% -> {entropy_synthesized}%")

        return jsonify({
            'witness_synthesis': {
                'verdict':               synth.get('witness_verdict', ''),
                'entropy_adjustment':    round(adj * 100, 1),
                'entropy_synthesized':   entropy_synthesized,
                'adjustment_reason':     synth.get('adjustment_reason', ''),
                'triggered_explanation': synth.get('triggered_explanation', {}),
                'witness_text':          synth.get('witness_text', ''),
            }
        })

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e), 'witness_synthesis': None}), 500


@app.route('/api/ard', methods=['POST'])
def ard_check():
    """
    Гібридна перевірка тексту через призму АРД v2.0.
    Крок 1: regex детектор (ARDChecker.scan)
    Крок 2: Haiku аналіз (тільки якщо scan.needs_haiku)
    """
    import os
    try:
        data = request.get_json() or {}
        text = data.get('article_text', '') or ''
        language = data.get('language', 'uk')

        if not text or len(text.strip()) < 50:
            return jsonify({'error': 'text_too_short', 'ard_verdict': 'N/A'}), 400

        # ── Крок 1: детекторний шар ──────────────────────────────────
        scan = ard_checker.scan(text)

        base_response = {
            'ard_score':             round(scan.score, 3),
            'ard_verdict':           scan.verdict,
            'ard_is_flagged':        scan.is_flagged,
            'ard_principles':        scan.principles_violated,
            'ard_violations': [
                {
                    'principle':      v.principle,
                    'principle_name': v.principle_name,
                    'snippet':        v.snippet,
                    'severity':       v.severity,
                }
                for v in scan.violations
            ],
        }

        # ── Крок 2: Haiku аналіз (якщо потрібно) ────────────────────
        if not scan.needs_haiku:
            base_response['ard_witness'] = (
                'Текст відповідає принципам АРД. Явних порушень не виявлено.' if language == 'uk'
                else 'Text complies with ARD principles. No obvious violations detected.'
            )
            return jsonify(base_response)

        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            base_response['ard_witness'] = 'API недоступний.'
            return jsonify(base_response)

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            base_response['ard_witness'] = 'Пакет anthropic не встановлено.'
            return jsonify(base_response)

        # Формуємо violations summary для промпту
        violations_summary = ''
        for v in scan.violations:
            violations_summary += f'  Принцип {v.principle} ({v.principle_name}):\n'
            violations_summary += f'  Знайдено: «{v.snippet}»\n'

        is_en = (language == 'en')

        ARD_SYSTEM_UK = """Ты - Свидок АРД. Твоє завдання: проаналізувати текст через призму Архітектури Раціональної Дії (АРД v2.0).

АРД - це операційна система для етики агента що хоче жити в наслідках своїх дій.

Девять принципів:
  0. Передмова: визнання можливості помилки + системна самоперевірка
  I. Базовий інваріант: не руйнуй механізми виправлення (суди, науку, пресу, освіту)
  II. Чотири питання: вигода -> шкода системі -> тест обернення -> прецедент
  III. Відповідальність за наслідки другого-третього порядку ("я не знав" - не аргумент)
  IV. Межа впливу: не позбавляй здатності сказати "ні"
  V. Принцип зупинки: чи можеш пояснити без замовчування?
  VI. Антимесія: не нав'язуй благо без запиту (ієрархія втручання)
  VII. Фінальний якір: готовність жити в наслідках особисто
  VIII. Протокол конфлікту інтересів
  IX. Метаправило: не зловживай системою для виправдання неправильного

ФОРМАТ ВІДПОВІДІ (3-5 речень, без заголовків):
1. Які принципи порушено і як конкретно
2. Які структурні патерни виявлені і як вони МОЖУТЬ впливати на читача
3. Практична порада читачу

Формулюй через "може", "ймовірно", "інтерпретується як".
ЗАБОРОНЕНО: "означає", "спрямований на", "насправді", "автор хоче", "мета тексту"."""

        ARD_SYSTEM_EN = """You are the ARD Witness. Your task: analyze text through the lens of the Architecture of Rational Action (ARD v2.0).

ARD is an operating system for the ethics of an agent who wants to live in the consequences of their actions.

Nine principles:
  0. Preamble: acknowledgment of fallibility + systematic self-check
  I. Base invariant: do not destroy correction mechanisms (courts, science, press, education)
  II. Four questions: personal gain -> harm to system -> reversal test -> precedent
  III. Responsibility for second-third order consequences ("I did not know" is not an argument)
  IV. Boundary of influence: do not deprive others of the ability to say "no"
  V. Stop principle: can you explain without concealing key facts?
  VI. Anti-messiah: do not impose "good" without request (hierarchy of intervention)
  VII. Final anchor: personal willingness to live in the consequences
  VIII. Conflict of interest protocol
  IX. Meta-rule: do not abuse the system to justify what you intuitively know is wrong

RESPONSE FORMAT (3-5 sentences, no headers):
1. Which principles are violated and specifically how
2. Which structural patterns are present and how they MAY affect the reader
3. Practical advice for the reader

Use: "may", "could", "appears to", "is consistent with".
FORBIDDEN: "means that", "directed at", "the goal is", "author wants", "this proves"."""

        prompt_uk = f"""Детектор виявив потенційні порушення АРД:
{violations_summary}
Принципи під питанням: {', '.join(scan.principles_violated)}
Загальний score: {scan.score:.2f} ({scan.verdict})

ТЕКСТ ДЛЯ АНАЛІЗУ:
{text[:2500]}

Проаналізуй через призму АРД. Конкретно і прямо."""

        prompt_en = f"""Detector found potential ARD violations:
{violations_summary}
Principles in question: {', '.join(scan.principles_violated)}
Overall score: {scan.score:.2f} ({scan.verdict})

TEXT FOR ANALYSIS:
{text[:2500]}

Analyze through the ARD lens. Concrete and direct."""

        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=600,
            system=ARD_SYSTEM_EN if is_en else ARD_SYSTEM_UK,
            messages=[{'role': 'user', 'content': prompt_en if is_en else prompt_uk}],
        )

        witness_text = msg.content[0].text if msg.content else ''
        base_response['ard_witness'] = witness_text
        return jsonify(base_response)

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e), 'ard_verdict': 'ERROR'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
