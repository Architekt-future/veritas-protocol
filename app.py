"""
Veritas Protocol - Flask API v16.6
Forces fresh import of Veritas modules on every restart
"""

import sys
import os

# CRITICAL: Clear module cache to force reload
print("🔄 Veritas v16.6 - Clearing module cache...")
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('veritas_')]
for module in modules_to_clear:
    del sys.modules[module]
print(f"✅ Cache cleared. Loading fresh Veritas v16.6 modules...")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__)
CORS(app)

# Initialize Veritas engine
engine = VeritasCalibratedCore()
print("✅ Veritas engine initialized")
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
            'version': 'v16.7',
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
                'version': 'v16.6',
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
                
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; VeritasBot/1.0)'}
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
                for attr in ['class', 'id']:
                    for tag in soup.find_all(True):
                        val = ' '.join(tag.get(attr, []) if isinstance(tag.get(attr), list) else [tag.get(attr, '')])
                        if any(x in val.lower() for x in [
                            'nav', 'menu', 'sidebar', 'ad', 'advertisement',
                            'social', 'share', 'comment', 'related', 'popular',
                            'trending', 'cookie', 'banner', 'promo', 'subscribe',
                            'newsletter', 'paywall', 'modal', 'overlay', 'feedback',
                            'breadcrumb', 'tag', 'label', 'byline', 'timestamp',
                        ]):
                            tag.decompose()
                            break
                
                # Try to find main content area
                main_content = None
                for selector in ['article', 'main', '[role="main"]', '.article-body',
                                  '.story-body', '.content', '.article', '.post-content']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break
                
                # Get text from main content or entire soup
                raw = (main_content or soup).get_text(separator=' ')

                # Clean: collapse whitespace, remove short UI lines (< 4 words)
                lines = [l.strip() for l in raw.splitlines()]
                meaningful = [l for l in lines if len(l.split()) >= 4]
                text = ' '.join(meaningful)

                # Deduplicate: remove lines that appear 3+ times (nav repetition)
                import collections
                word_chunks = text.split('. ')
                counts = collections.Counter(word_chunks)
                text = '. '.join(c for c in word_chunks if counts[c] < 3)

                # Limit to 1500 words
                words = text.split()
                if len(words) > 1500:
                    text = ' '.join(words[:1500])
                
                if not text or len(text) < 100:
                    return jsonify({
                        'error': 'Could not extract enough text from URL',
                        'status': 'error'
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
        
        # Add scraped text preview if URL was provided
        if url:
            # Preview: first 1000 words (not chars!)
            words = text.split()
            preview_words = words[:1000] if len(words) > 1000 else words
            result['scraped_text_preview'] = ' '.join(preview_words)
            result['scraped_word_count'] = len(words)
            result['scraped_url'] = url
        
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
        'version': 'v16.7'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)


@app.route('/api/oracle', methods=['POST'])
def oracle():
    """
    Witness endpoint (v16.7)
    Приймає diagnostics від Свідка, формує промпт, питає Claude.
    Вимагає ANTHROPIC_API_KEY в environment.
    """
    import os

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
        status       = diag.get('status', '—')

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

        text_preview = data.get('text_preview', '')[:300]
        text_topic   = data.get('text_topic')  # e.g. 'SPORT', 'CULTURE', None

        topic_labels_uk = {
            'SPORT':     'спортивний репортаж',
            'CULTURE':   'культурний контент',
            'SCIENCE':   'науковий текст',
            'TECH':      'технологічний текст',
            'LIFESTYLE': 'lifestyle-контент',
        }
        topic_context = ''
        if text_topic and text_topic in topic_labels_uk:
            topic_context = (
                f"\n⚠️ ВАЖЛИВО: Цей текст класифіковано як «{topic_labels_uk[text_topic]}».\n"
                "Аналізуй ЛИШЕ структуру і подачу тексту в рамках його жанру.\n"
                "НЕ згадуй геополітику, кризи, відволікання уваги — це не застосовується.\n"
                "Якщо текст структурно чистий для свого жанру — так і скажи.\n"
            )

        prompt = (
            "Ти — модуль патернового аналізу системи Veritas Protocol.\n"
            "Твоя задача: на основі метрик зробити висновок про ІНФОРМАЦІЙНИЙ ПАТЕРН — "
            "не про конкретних людей, не про політику, а про тип маніпуляції або викривлення.\n"
            f"{topic_context}\n"
            "МЕТРИКИ СВІДКА:\n"
            f"  Ентропія: {entropy_pct}%\n"
            f"  Вердикт: {verdict}\n"
            f"  Displacement: {ctx_verdict}\n"
            f"  Сигнали: {ctx_signals}\n"
            f"  Performative pattern: {perf_verdict} (score: {perf_score})\n"
            f"  Гарячі теми поля: {hot_topics}\n"
            f"  Кризові заголовки: {crisis_count}/{total_events} ({crisis_pct}%)\n\n"
            "На основі цих метрик опиши:\n"
            "1. Який інформаційний патерн зафіксовано (без згадки конкретних осіб)\n"
            "2. Як цей патерн зазвичай розвивається в інформаційному полі\n"
            "3. Що варто перевірити читачу\n\n"
            "ФОРМАТ — суворо:\n"
            "Рядок 1: одне слово-класифікатор патерну ВЕЛИКИМИ ЛІТЕРАМИ\n"
            "Порожній рядок\n"
            "Рядки 3-6: рівно 4 речення про патерн. З великої літери, крапка в кінці.\n"
            "Порожній рядок\n"
            "Останній рядок: практична порада читачу після тире.\n\n"
            "Мова — українська. Всі речення завершені."
        )

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )

        witness_text = message.content[0].text if message.content else "Свідок мовчить."

        return jsonify({
            'witness_text':      witness_text,
            'witness_available': True,
            'model':            'claude-haiku-4-5-20251001',
        })

    except Exception as e:
        import traceback
        print(f"Oracle error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'witness_available': False}), 500
