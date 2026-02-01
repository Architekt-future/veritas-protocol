"""
Veritas Protocol - Flask Backend for Render
Main application file — v2.0 (fixed structure + debug logging)
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_architecture import VeritasArchitecture

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine
engine = VeritasArchitecture()


# ============================================================
# DEBUG MIDDLEWARE — logs every incoming request
# ============================================================
@app.before_request
def log_request_info():
    app.logger.info('--- INCOMING REQUEST ---')
    app.logger.info('Method: %s | Path: %s', request.method, request.path)
    app.logger.info('Content-Type: %s', request.content_type)
    app.logger.info('Content-Length: %s', request.content_length)
    app.logger.info('Body (raw): %s', request.get_data(as_text=True)[:500])


# ============================================================
# SIMPLE HTML EXTRACTOR
# ============================================================
class SimpleExtractor:
    """Simplified scraper without external dependencies"""

    def extract_from_url(self, url: str, html: str) -> dict:
        try:
            cleaned = self._clean_html(html)
            title  = self._extract_title(html)
            text   = self._extract_paragraphs(cleaned)
            source = self._extract_domain(url)
            return {'success': True, 'title': title, 'text': text, 'source': source, 'url': url}
        except Exception as e:
            return {'success': False, 'error': str(e), 'url': url}

    def _clean_html(self, html):
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>',  '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<nav[^>]*>.*?</nav>',      '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<header[^>]*>.*?</header>','', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<footer[^>]*>.*?</footer>','', html, flags=re.DOTALL | re.IGNORECASE)
        return html

    def _extract_title(self, html):
        m = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html, re.IGNORECASE)
        if m: return m.group(1)
        m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if m: return m.group(1).strip()
        return "Unknown Title"

    def _extract_paragraphs(self, html):
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        if not paragraphs:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
                return self._clean_text(text)
        text = re.sub(r'<[^>]+>', ' ', ' '.join(paragraphs))
        return self._clean_text(text)

    def _clean_text(self, text):
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;',      ' ', text)
        text = re.sub(r'\s+',         ' ', text)
        return text.strip()

    def _extract_domain(self, url):
        m = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return m.group(1) if m else "unknown"


extractor = SimpleExtractor()


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    # --- OPTIONS (CORS preflight) ---
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # --- GET (health-check) ---
    if request.method == 'GET':
        return jsonify({
            'status': 'online',
            'version': '2.0-architectural',
            'engine': 'VeritasArchitecture'
        }), 200

    # --- POST (main analysis) ---
    try:
        # 1. Parse JSON body
        if not request.content_type or 'application/json' not in request.content_type:
            app.logger.warning('Bad Content-Type: %s', request.content_type)
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json(silent=True)
        app.logger.info('Parsed JSON: %s', data)

        if not data:
            app.logger.error('No JSON data received (empty body or parse failure)')
            return jsonify({'error': 'No data received'}), 400

        url  = data.get('url',  '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Manual Input')
        title  = ''

        app.logger.info('url=%s | text_len=%d', url, len(text))

        # 2. Fetch text from URL if provided
        if url:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                extraction = extractor.extract_from_url(url, html)
                if not extraction['success']:
                    raise Exception(extraction.get('error', 'Extraction failed'))
                text   = extraction['text']
                title  = extraction['title']
                source = extraction['source']
                app.logger.info('Extracted %d chars from %s', len(text), url)
            except Exception as e:
                app.logger.error('Scraping error: %s', str(e))
                return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

        # 3. Validate we have text
        if not text or len(text) < 10:
            app.logger.error('Text too short: %d chars', len(text))
            return jsonify({'error': 'Text too short (min 10 characters)'}), 400

        # 4. Run engine
        result = engine.analyze(text)
        app.logger.info('Engine result status: %s | entropy: %s', result.get('status'), result.get('entropy'))

        # 5. Attach meta
        result['source']         = source
        result['title']          = title or 'Manual Input'
        result['url']            = url
        result['mode']           = 'url_scraping' if url else 'manual_input'
        result['extracted_text'] = text[:1500] + ('...' if len(text) > 1500 else '')

        return jsonify(result), 200

    except Exception as e:
        app.logger.error('Unhandled exception in /api/analyze: %s', str(e), exc_info=True)
        return jsonify({'error': str(e)}), 500


# ============================================================
# TEST ENDPOINT — для отладки POST
# ============================================================
@app.route('/api/test', methods=['POST'])
def test_endpoint():
    try:
        data = request.get_json(silent=True)
        app.logger.info('Test endpoint received: %s', data)
        return jsonify({
            'success': True,
            'received_data': data,
            'message': 'POST working correctly'
        }), 200
    except Exception as e:
        app.logger.error('Test endpoint error: %s', str(e))
        return jsonify({'error': str(e)}), 400


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
