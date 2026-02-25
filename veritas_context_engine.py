"""
Veritas Context Engine v1.0
"Периферійний зір Свідка"

Philosophy:
Текст — це не ізольований об'єкт. Це подія в інформаційному полі.
Свідок має бачити не тільки що написано, але і КОЛИ і НА ЯКОМУ ТЛІ.

Architecture:
  RSS/News API → EventExtractor → ContextState → DisplacementDetector

How it works:
1. Тягнемо заголовки з кількох RSS-фідів (без API ключів)
2. Витягуємо "гарячі теми" — кластери пов'язаних заголовків
3. Будуємо ContextState — знімок інформаційного поля прямо зараз
4. При аналізі нового тексту — порівнюємо його з полем
5. Якщо текст сенсаційний але тематично ізольований від поля — підозріло

Displacement hypothesis:
"Якщо в полі активна accountability-криза, а з'являється
несподівана висока-salience тема без причинно-наслідкового зв'язку —
це може бути навмисне відволікання."

Limitations (free tier):
- In-memory cache only (resets on server sleep)
- RSS headlines only, not full articles
- ~30 min cache TTL to avoid hammering sources
"""

import re
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import Counter


# ── RSS FEED LIST ────────────────────────────────────────────────────────────
# No API keys required. Mix of global sources for diverse coverage.
RSS_FEEDS = [
    # Global news
    ('Reuters World',    'https://feeds.reuters.com/reuters/worldNews'),
    ('AP Top News',      'https://feeds.apnews.com/rss/apf-topnews'),
    ('BBC World',        'http://feeds.bbci.co.uk/news/world/rss.xml'),
    ('Guardian World',   'https://www.theguardian.com/world/rss'),
    ('Al Jazeera',       'https://www.aljazeera.com/xml/rss/all.xml'),
    # US/Politics
    ('NPR News',         'https://feeds.npr.org/1001/rss.xml'),
    ('NYT HomePage',     'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'),
    ('CNN Top Stories',  'http://rss.cnn.com/rss/edition.rss'),
    # Tech/Business
    ('Reuters Tech',     'https://feeds.reuters.com/reuters/technologyNews'),
    ('BBC Tech',         'http://feeds.bbci.co.uk/news/technology/rss.xml'),
]

# Cache TTL — 30 minutes
CACHE_TTL_SECONDS = 30 * 60


# ── ACCOUNTABILITY CRISIS KEYWORDS ───────────────────────────────────────────
# Topics that signal an active accountability crisis in the field
# When these are hot, high-salience distractions become more suspicious
ACCOUNTABILITY_CRISIS_KEYWORDS = [
    # Legal/criminal
    r'\b(indictment|indicted|arrested|charges|criminal|prosecution|trial|verdict)\b',
    r'\b(investigation|probe|subpoena|testimony|whistleblower|leak|leaked)\b',
    r'\b(scandal|corruption|misconduct|fraud|cover.?up|concealment)\b',
    # Political accountability
    r'\b(impeachment|resignation|fired|ousted|removed\s+from|stepping\s+down)\b',
    r'\b(hearing|congress|senate|inquiry|committee\s+investigation)\b',
    r'\b(epstein|assange|snowden|panama\s+papers|wikileaks)\b',
    # Corporate accountability
    r'\b(lawsuit|settlement|fine|penalty|regulatory\s+action|sec\s+investigation)\b',
    r'\b(data\s+breach|privacy\s+violation|antitrust|monopoly\s+abuse)\b',
]

# HIGH SALIENCE DISTRACTION TOPICS
# Topics that historically appear as distractions
# Not inherently bad — but suspicious when appearing alongside accountability crises
DISTRACTION_TOPIC_PATTERNS = [
    r'\b(ufo|uap|alien|extraterrestrial|unidentified\s+(aerial|flying))\b',
    r'\b(declassified|secret\s+files|hidden\s+files|government\s+files|released\s+files)\b',
    r'\b(celebrity|kardashian|taylor\s+swift|kanye|beyonc)\b',
    r'\b(sports\s+drama|player\s+transfer|championship\s+controversy)\b',
    r'\b(royal\s+family|meghan|harry|palace\s+drama)\b',
    r'\b(shark\s+attack|missing\s+(person|child)|miracle|rescue)\b',
]

# ── TOPIC CLASSIFIER ─────────────────────────────────────────────────────────
# If text clearly belongs to one of these domains — context displacement
# analysis is not meaningful. Sport is sport. Recipe is recipe.

NON_NEWS_TOPIC_PATTERNS = {
    'SPORT': [
        r'\b(футбол|баскетбол|волейбол|теніс|хокей|бокс|змагання|турнір|чемпіонат)\b',
        r'\b(football|basketball|volleyball|tennis|hockey|boxing|championship|tournament)\b',
        r'\b(гол|м\'яч|матч|рахунок|тайм|пенальті|офсайд|суддя|арбітр)\b',
        r'\b(goal|match|score|halftime|penalty|offside|referee|stadium)\b',
        r'\b(гравець|тренер|команда|клуб|ліга|збірна|стадіон)\b',
        r'\b(player|coach|team|club|league|squad|stadium)\b',
    ],
    'CULTURE': [
        r'\b(фільм|кіно|серіал|театр|виставка|концерт|альбом|пісня)\b',
        r'\b(film|movie|series|theatre|exhibition|concert|album|song)\b',
        r'\b(режисер|актор|художник|письменник|музикант|співак)\b',
        r'\b(director|actor|artist|writer|musician|singer)\b',
    ],
    'SCIENCE': [
        r'\b(дослідження|експеримент|відкриття|наука|лабораторія|вчені)\b',
        r'\b(research|experiment|discovery|science|laboratory|scientists)\b',
        r'\b(молекула|ДНК|геном|квант|нейрон|рецептор|фотон)\b',
        r'\b(molecule|DNA|genome|quantum|neuron|receptor|photon)\b',
    ],
    'TECH': [
        r'\b(програмування|розробка|код|алгоритм|додаток|сервіс)\b',
        r'\b(programming|development|code|algorithm|application|software)\b',
        r'\b(смартфон|процесор|чіп|оновлення|версія|реліз)\b',
        r'\b(smartphone|processor|chip|update|version|release)\b',
    ],
    'LIFESTYLE': [
        r'\b(рецепт|страва|кухня|інгредієнт|приготування)\b',
        r'\b(десерт|борщ|суп|салат|випічка|соус|маринад)\b',
        r'\b(recipe|dish|cuisine|ingredient|cooking|dessert)\b',
        r'\b(здоров\'я|дієта|вправа|фітнес|медитація|йога)\b',
        r'\b(health|diet|exercise|fitness|meditation|yoga)\b',
        r'\b(подорож|туризм|готель|курорт|відпустка|маршрут)\b',
        r'\b(travel|tourism|hotel|resort|vacation|route)\b',
    ],
}


def detect_text_topic(text: str) -> Optional[str]:
    """
    Detect if the text clearly belongs to a non-political domain.
    Returns topic name (e.g. 'SPORT') or None if it looks like news/politics.
    Requires at least 2 pattern matches for confident classification.
    """
    text_lower = text.lower()
    scores = {}
    for topic, patterns in NON_NEWS_TOPIC_PATTERNS.items():
        hits = sum(
            1 for p in patterns
            if re.search(p, text_lower, re.IGNORECASE)
        )
        if hits >= 2:
            scores[topic] = hits
    if scores:
        return max(scores, key=scores.get)
    return None


# ── EVENT ────────────────────────────────────────────────────────────────────

class NewsEvent:
    """A single news event extracted from a headline."""

    def __init__(self, title: str, source: str, pub_date: Optional[str] = None):
        self.title = title
        self.title_lower = title.lower()
        self.source = source
        self.pub_date = pub_date

        # Derived fields
        self.is_accountability = self._check_accountability()
        self.is_distraction_topic = self._check_distraction()
        self.keywords = self._extract_keywords()

    def _check_accountability(self) -> bool:
        return any(
            re.search(p, self.title_lower, re.IGNORECASE)
            for p in ACCOUNTABILITY_CRISIS_KEYWORDS
        )

    def _check_distraction(self) -> bool:
        return any(
            re.search(p, self.title_lower, re.IGNORECASE)
            for p in DISTRACTION_TOPIC_PATTERNS
        )

    def _extract_keywords(self) -> List[str]:
        """Extract meaningful keywords (no stopwords, 4+ chars)."""
        stopwords = {
            'that', 'this', 'with', 'from', 'have', 'will', 'been', 'were',
            'they', 'their', 'what', 'about', 'after', 'before', 'would',
            'could', 'should', 'says', 'said', 'says', 'more', 'also',
            'than', 'then', 'when', 'where', 'there', 'here', 'into',
            'over', 'under', 'some', 'many', 'much', 'very', 'just',
        }
        words = re.findall(r'\b[a-zA-Z]{4,}\b', self.title_lower)
        return [w for w in words if w not in stopwords]


# ── CONTEXT STATE ─────────────────────────────────────────────────────────────

class ContextState:
    """
    Snapshot of the current information field.
    Built from N recent news headlines across multiple sources.
    """

    def __init__(self, events: List[NewsEvent], built_at: float):
        self.events = events
        self.built_at = built_at
        self.total_events = len(events)

        # Aggregate signals
        self.accountability_events = [e for e in events if e.is_accountability]
        self.distraction_events = [e for e in events if e.is_distraction_topic]

        # Hot topics — keywords appearing in 2+ headlines
        # Exclude generic words that appear in many unrelated contexts
        GENERIC_WORDS = {
            'files', 'report', 'says', 'said', 'news', 'new', 'year',
            'time', 'home', 'make', 'take', 'know', 'come', 'look',
            'case', 'deal', 'plan', 'move', 'week', 'days', 'week',
            'president', 'government', 'official', 'officials', 'country',
            'state', 'court', 'people', 'world', 'after', 'over',
            'first', 'last', 'back', 'more', 'says', 'next', 'show',
        }
        all_keywords = []
        for e in events:
            all_keywords.extend(e.keywords)
        keyword_counts = Counter(all_keywords)
        self.hot_topics = {
            word: count
            for word, count in keyword_counts.items()
            if count >= 2 and word not in GENERIC_WORDS
        }

        # Crisis level: what fraction of headlines are accountability-related
        self.crisis_ratio = (
            len(self.accountability_events) / max(1, self.total_events)
        )

    def has_active_accountability_crisis(self, threshold: float = 0.10) -> bool:
        """True if 10%+ of current headlines are accountability-related."""
        return self.crisis_ratio >= threshold

    def is_topic_in_field(self, text: str) -> Tuple[bool, float]:
        """
        Check if text's topics overlap with current hot topics.
        Returns (is_present, overlap_score 0-1)
        """
        text_lower = text.lower()
        text_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', text_lower))

        if not self.hot_topics:
            return False, 0.0

        overlap = sum(
            1 for word in text_words
            if word in self.hot_topics
        )
        score = min(1.0, overlap / max(1, len(self.hot_topics) * 0.3))
        return overlap > 0, round(score, 3)

    def age_minutes(self) -> float:
        return (time.time() - self.built_at) / 60

    def summary(self) -> Dict:
        return {
            'total_events':        self.total_events,
            'accountability_count': len(self.accountability_events),
            'distraction_count':   len(self.distraction_events),
            'crisis_ratio':        round(self.crisis_ratio, 3),
            'hot_topics_count':    len(self.hot_topics),
            'top_topics':          sorted(
                self.hot_topics.items(), key=lambda x: -x[1]
            )[:10],
            'age_minutes':         round(self.age_minutes(), 1),
        }


# ── CONTEXT ENGINE ────────────────────────────────────────────────────────────

class ContextEngine:
    """
    Fetches RSS feeds, builds ContextState, detects displacement.
    Thread-safe with in-memory cache.
    """

    def __init__(self, cache_ttl: int = CACHE_TTL_SECONDS):
        self.cache_ttl = cache_ttl
        self._context_state: Optional[ContextState] = None
        self._lock = threading.Lock()
        self._last_build_attempt: float = 0
        self._build_errors: List[str] = []

    # ── RSS FETCHING ─────────────────────────────────────────────────────────

    def _fetch_feed(self, name: str, url: str) -> List[NewsEvent]:
        """Fetch and parse a single RSS feed. Returns [] on failure."""
        try:
            import urllib.request
            import xml.etree.ElementTree as ET

            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; VeritasContextBot/1.0)',
                'Accept': 'application/rss+xml, application/xml, text/xml',
            })
            with urllib.request.urlopen(req, timeout=4) as r:
                content = r.read()

            root = ET.fromstring(content)
            events = []

            for item in root.findall('.//item'):
                title_el = item.find('title')
                date_el  = item.find('pubDate')
                if title_el is not None and title_el.text:
                    events.append(NewsEvent(
                        title    = title_el.text.strip(),
                        source   = name,
                        pub_date = date_el.text if date_el is not None else None,
                    ))

            return events[:30]  # max 30 per feed

        except Exception as e:
            self._build_errors.append(f'{name}: {str(e)[:60]}')
            return []

    def _build_context(self) -> ContextState:
        """Fetch all feeds in parallel and build a fresh ContextState."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        self._build_errors = []
        all_events = []

        # Паралельно — всі фіди одночасно, загальний timeout 8 сек
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self._fetch_feed, name, url): name
                for name, url in RSS_FEEDS
            }
            for future in as_completed(futures, timeout=8):
                try:
                    events = future.result()
                    all_events.extend(events)
                except Exception as e:
                    self._build_errors.append(f'future: {str(e)[:60]}')

        return ContextState(events=all_events, built_at=time.time())

    # ── CACHE MANAGEMENT ─────────────────────────────────────────────────────

    def get_context(self, force_refresh: bool = False) -> Optional[ContextState]:
        """
        Returns current ContextState, refreshing if stale.
        Thread-safe. Returns None if all feeds failed.
        """
        with self._lock:
            now = time.time()

            # Avoid hammering feeds — don't retry more than once per minute
            if (now - self._last_build_attempt) < 60 and self._context_state is None:
                return None

            needs_refresh = (
                force_refresh
                or self._context_state is None
                or (now - self._context_state.built_at) > self.cache_ttl
            )

            if needs_refresh:
                self._last_build_attempt = now
                fresh = self._build_context()
                if fresh.total_events > 0:
                    self._context_state = fresh

            return self._context_state

    def inject_mock_context(self, events: List[NewsEvent]):
        """For testing: inject mock events as ContextState."""
        with self._lock:
            self._context_state = ContextState(
                events=events,
                built_at=time.time()
            )

    # ── DISPLACEMENT DETECTION ───────────────────────────────────────────────

    def analyze_displacement(self, text: str) -> Dict:
        """
        Core method: given a text, check if it looks like a displacement
        relative to the current information field.

        Returns displacement score 0.0-1.0 and explanation.
        """
        ctx = self.get_context()

        if ctx is None or ctx.total_events == 0:
            return {
                'displacement_score':   0.0,
                'displacement_verdict': 'NO_CONTEXT',
                'displacement_signals': [],
                'context_available':    False,
                'context_summary':      None,
                'explanation_uk':       'Контекстне поле недоступне. Аналіз без контексту.',
                'explanation_en':       'Context field unavailable. Analysis without context.',
            }

        # ── Topic Guard: якщо текст явно про спорт/культуру/науку —
        # контекстний displacement-аналіз не має сенсу.
        # Повертаємо нейтральний вердикт з поясненням теми.
        detected_topic = detect_text_topic(text)
        if detected_topic:
            topic_labels_uk = {
                'SPORT':     'спортивний',
                'CULTURE':   'культурний',
                'SCIENCE':   'науковий',
                'TECH':      'технологічний',
                'LIFESTYLE': 'lifestyle',
            }
            topic_label = topic_labels_uk.get(detected_topic, detected_topic)
            return {
                'displacement_score':   0.0,
                'displacement_verdict': 'CONTEXTUALLY_NEUTRAL',
                'displacement_signals': [f'TOPIC_{detected_topic}'],
                'context_available':    True,
                'context_summary':      ctx.summary(),
                'text_topic':           detected_topic,
                'explanation_uk':       (
                    f'Текст класифіковано як {topic_label} контент. '
                    f'Аналіз відволікання уваги не застосовується — '
                    f'це не новинний/політичний матеріал.'
                ),
                'explanation_en':       (
                    f'Text classified as {detected_topic.lower()} content. '
                    f'Displacement analysis not applicable — '
                    f'this is not news/political material.'
                ),
            }

        text_lower = text.lower()
        signals = []
        score = 0.0

        # ── Signal 1: Is text a distraction topic? ───────────────────────
        is_distraction_topic = any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in DISTRACTION_TOPIC_PATTERNS
        )

        # ── Signal 2: Is accountability crisis active in the field? ──────
        has_crisis = ctx.has_active_accountability_crisis()

        # ── Signal 3: Does the text overlap with hot field topics? ────────
        # For long texts use only first 150 words — long articles always
        # contain common words that overlap with RSS field, masking displacement
        text_for_field = ' '.join(text.split()[:150])
        in_field, overlap_score = ctx.is_topic_in_field(text_for_field)

        # ── Signal 4: Official/breaking claim ────────────────────────────
        official_claim = bool(re.search(
            r'\b(official|declassified|confirmed|revealed|released|breaking)\b',
            text_lower, re.IGNORECASE
        ))

        # ── Scoring: displacement requires COMBINATION of signals ─────────
        # A crisis alone does NOT penalize unrelated legitimate texts.
        # Displacement = distraction topic + off-field + crisis context.

        if is_distraction_topic:
            signals.append('DISTRACTION_TOPIC')
            score += 0.20

            if has_crisis:
                signals.append('ACTIVE_ACCOUNTABILITY_CRISIS')
                score += 0.25

                if not in_field:
                    signals.append('TOPIC_ISOLATED_FROM_FIELD')
                    score += 0.30

                    if official_claim:
                        signals.append('OFFICIAL_CLAIM_OFF_TOPIC')
                        score += 0.15

        # ── Verdict ──────────────────────────────────────────────────────
        score = round(min(1.0, score), 3)

        if score >= 0.70:
            verdict = 'LIKELY_DISPLACEMENT'
            explanation_uk = (
                'Висока ймовірність навмисного відволікання уваги. '
                'Текст підіймає сенсаційну тему на фоні активної кризи відповідальності, '
                'і його тематика ізольована від поточного інформаційного поля.'
            )
            explanation_en = (
                'High probability of deliberate attention displacement. '
                'Text raises a sensational topic against an active accountability crisis '
                'and its subject is isolated from the current information field.'
            )
        elif score >= 0.45:
            verdict = 'SUSPICIOUS_TIMING'
            explanation_uk = (
                'Підозрілий тайминг публікації. '
                'Тема може бути використана як відволікання, '
                'але недостатньо сигналів для впевненого висновку.'
            )
            explanation_en = (
                'Suspicious publication timing. '
                'Topic may be used as distraction, '
                'but insufficient signals for confident conclusion.'
            )
        elif score >= 0.20:
            verdict = 'MONITOR'
            explanation_uk = 'Слабкі сигнали відволікання. Варто відстежити контекст.'
            explanation_en = 'Weak displacement signals. Worth monitoring context.'
        else:
            verdict = 'CONTEXTUALLY_NEUTRAL'
            explanation_uk = 'Текст органічно вписується в поточне інформаційне поле.'
            explanation_en = 'Text fits organically into the current information field.'

        return {
            'displacement_score':   score,
            'displacement_verdict': verdict,
            'displacement_signals': signals,
            'context_available':    True,
            'topic_in_field':       in_field,
            'field_overlap_score':  overlap_score,
            'context_summary':      ctx.summary(),
            'explanation_uk':       explanation_uk,
            'explanation_en':       explanation_en,
        }
