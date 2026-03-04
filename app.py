"""
Veritas Protocol - Flask API v16.9
Forces fresh import of Veritas modules on every restart
SCRAPER: Daily Mail selectors + <p> fallback (2026-02-26)
GENRE: GenreDetector v2.0 — CONSPIRACY_NEWS + fixed SPORT/CULTURE false positives
"""

import sys
import os

# CRITICAL: Clear module cache to force reload
print("🔄 Veritas v16.9 - Clearing module cache...")
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('veritas_')]
for module in modules_to_clear:
    del sys.modules[module]
print(f"✅ Cache cleared. Loading fresh Veritas v16.9 modules...")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__)
CORS(app)

# Initialize Veritas engine
engine = VeritasCalibratedCore()
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
print(f"   Self-preservation:     {getattr(engine, 'self_preservation_guard', None) is not None}")
print(f"   Meta-intent:           {getattr(engine, 'meta_intent_analyzer', None) is not None}")
print(f"   Certainty factor:      {getattr(engine, 'certainty_factor', None) is not None}")
print(f"   Performative detector: {getattr(engine, 'performative_detector', None) is not None}")

@app.route('/')
def home():
    """Serve the HTML interface"""
    try:
        return send_file('index.html')
    except:
        return jsonify({
            'status': 'online',
            'version': 'v16.9',
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
                'version': 'v16.9',
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
                    'newsletter', 'paywall', 'modal', 'overlay', 'breadcrumb']
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

                # ── Jina fallback if scrape returned too little ──────────
                word_count_check = len(text.split())
                if word_count_check < 80:
                    import os as _os
                    jina_key = _os.environ.get('JINA_API_KEY', '')
                    if jina_key:
                        try:
                            print(f'🔄 Jina fallback: only {word_count_check} words from direct scrape')
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
        
        # Analyze text
        result = engine.analyze(text)
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

        return jsonify(result)
    
    except Exception as e:
        import traceback
        print(f"❌ Error in analyze: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': 'v16.9'
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
        lac_finance      = diag.get('lac_finance', {})
        lac_fin_verdict  = lac_finance.get('verdict', '') if isinstance(lac_finance, dict) else ''
        lac_fin_score    = lac_finance.get('score', None) if isinstance(lac_finance, dict) else None
        lac_fin_missing  = ', '.join(lac_finance.get('missing', [])) if isinstance(lac_finance, dict) else ''

        lac_labor        = diag.get('lac_labor', {})
        lac_lab_verdict  = lac_labor.get('verdict', '') if isinstance(lac_labor, dict) else ''

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
        signals_summary = '\n'.join(signals_lines) if signals_lines else '  (модулі не виявили порушень)'

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
                "Your knowledge ends in early 2025. The current date is 2026.\n"
                "Anything could have happened since: new leaders, new popes, new presidents, new discoveries.\n"
                "FORBIDDEN: writing 'this pope does not exist', 'this person does not exist', 'this is impossible', 'this is fiction' — "
                "if you simply do not know this fact. Not knowing is NOT proof of absence.\n"
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
                f"  Entropy: {entropy_pct}%\n"
                f"  Cohesion: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"CONTEXT:\n"
                f"{context_block}\n"
                "IMPORTANT: System verdict is your primary guide. Entropy is secondary.\n"
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
                "If modules triggered — explain each one in plain language.\n"
                "FORMAT — strictly:\n"
                "Line 1: one word IN CAPS — (CLEAN / SUSPICIOUS / DANGEROUS / ANALYTICS / OPINION / RHETORIC)\n"
                "Empty line\n"
                "3-5 sentences in plain language:\n"
                "  1. What is happening in the text (specifically, no jargon)\n"
                "  2. Why this might be a problem (or why it is fine)\n"
                "  3. If a module triggered — explain what it found (no module names)\n"
                "  4. What the reader should do next — a concrete recommendation\n"
                "No technical module names. No mention of entropy or metrics.\n"
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
                "Твої знання закінчуються на початку 2025 року. Поточна дата — 2026 рік.\n"
                "За цей час могло статись ЩО ЗАВГОДНО: нові лідери, нові папи, нові президенти, нові відкриття.\n"
                "ЗАБОРОНЕНО писати: 'такого папи не існує', 'такої людини немає', 'це неможливо', 'це вигадка' — "
                "якщо ти просто не знаєш цього факту. Незнання — НЕ доказ відсутності.\n"
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
                f"  Ентропія: {entropy_pct}%\n"
                f"  Когезія: {cohesion}\n"
                f"{modules_block}"
                f"{pivot_line}"
                f"КОНТЕКСТ:\n"
                f"{context_block}\n"
                "ВАЖЛИВО: Вердикт системи — твій головний орієнтир. Ентропія — допоміжна цифра.\n"
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
                "Якщо спрацювали модулі — обов'язково поясни кожен простими словами в тексті відповіді.\n"
                "ФОРМАТ — суворо:\n"
                "Рядок 1: одне слово ВЕЛИКИМИ — (ЧИСТО / ПІДОЗРІЛО / НЕБЕЗПЕЧНО / АНАЛІТИКА / ДУМКА / РИТОРИКА)\n"
                "Порожній рядок\n"
                "3-5 речень простою мовою:\n"
                "  1. Що відбувається в тексті (конкретно, без термінів)\n"
                "  2. Чому це може бути проблемою (або чому все гаразд)\n"
                "  3. Якщо спрацював модуль — поясни що він знайшов (без назви модуля)\n"
                "  4. Що читачу варто зробити далі — конкретна порада\n"
                "Жодних технічних назв модулів. Жодного згадування ентропії або метрик.\n"
                "Відповідай ВИКЛЮЧНО українською мовою."
            )

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=900,
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            'witness_text':      message.content[0].text if message.content else "Свідок мовчить.",
            'witness_available': True,
            'model':             'claude-haiku-4-5-20251001',
            'detected_genre':    detected_genre,
        })

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e), 'witness_available': False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
