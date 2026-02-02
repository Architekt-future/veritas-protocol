"""
Veritas Protocol - Flask Backend v2.2
Fixed: scraping, structure, imports, multilingual support
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine
engine = VeritasCalibratedCore()


# ============================================================
# DEBUG MIDDLEWARE
# ============================================================
@app.before_request
def log_request_info():
    app.logger.info('=== REQUEST ===')
    app.logger.info('Method: %s | Path: %s', request.method, request.path)
    app.logger.info('Content-Type: %s', request.content_type)
    app.logger.info('Body: %s', request.get_data(as_text=True)[:500])


# ============================================================
# SIMPLE HTML EXTRACTOR
# ============================================================
class SimpleExtractor:
    """Simplified scraper without external dependencies"""

    def extract_from_url(self, url: str, html: str) -> dict:
        try:
            cleaned = self._clean_html(html)
            title   = self._extract_title(html)
            text    = self._extract_paragraphs(cleaned)
            source  = self._extract_domain(url)
            return {
                'success': True,
                'title': title,
                'text': text,
                'source': source,
                'url': url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }

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
            # fallback: extract body
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
                return self._clean_text(text)
            # ultimate fallback: strip all tags
            return self._clean_text(re.sub(r'<[^>]+>', ' ', html))
        
        text = re.sub(r'<[^>]+>', ' ', ' '.join(paragraphs))
        return self._clean_text(text)

    def _clean_text(self, text):
        # HTML entities
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;',      ' ', text)
        # Whitespace
        text = re.sub(r'\s+', ' ', text)
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
    # --- CORS preflight ---
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # --- Health check ---
    if request.method == 'GET':
        return jsonify({
            'status': 'online',
            'version': '2.2-fixed',
            'engine': 'VeritasCalibratedCore'
        }), 200

    # --- POST analysis ---
    try:
        # 1. Parse JSON
        if not request.content_type or 'application/json' not in request.content_type:
            app.logger.warning('Bad Content-Type: %s', request.content_type)
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json(silent=True)
        app.logger.info('Parsed JSON: %s', data)

        if not data:
            app.logger.error('No JSON data')
            return jsonify({'error': 'No data received'}), 400

        url    = data.get('url',  '').strip()
        text   = data.get('text', '').strip()
        source = 'Manual Input'
        title  = 'Manual Input'

        app.logger.info('url=%s | text_len=%d', url, len(text))

        # 2. Fetch from URL if provided
        if url:
            try:
                # URL encode non-ASCII characters (Ukrainian, etc.)
                from urllib.parse import urlparse, quote, urlunparse
                parsed = urlparse(url)
                # Encode path component only (preserves domain)
                encoded_path = quote(parsed.path.encode('utf-8'), safe='/:')
                safe_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    encoded_path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                ))
                
                # Enhanced headers для bypass anti-scraping
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                req = urllib.request.Request(safe_url, headers=headers)
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    # Handle encoding properly для multilingual
                    content_type = response.headers.get('Content-Type', '')
                    charset = 'utf-8'
                    
                    # Extract charset from Content-Type
                    if 'charset=' in content_type:
                        charset = content_type.split('charset=')[-1].split(';')[0].strip()
                    
                    html = response.read().decode(charset, errors='ignore')
                    app.logger.info('Fetched %d bytes, charset=%s', len(html), charset)
                
                extraction = extractor.extract_from_url(url, html)
                
                if not extraction['success']:
                    raise Exception(extraction.get('error', 'Extraction failed'))
                
                text   = extraction['text']
                title  = extraction['title']
                source = extraction['source']
                
                app.logger.info('Extracted %d chars from %s', len(text), url)
                
            except urllib.error.HTTPError as e:
                app.logger.error('HTTP Error %d: %s', e.code, e.reason)
                return jsonify({'error': f'HTTP {e.code}: {e.reason}'}), 500
                
            except urllib.error.URLError as e:
                app.logger.error('URL Error: %s', str(e.reason))
                return jsonify({'error': f'Connection failed: {str(e.reason)}'}), 500
                
            except Exception as e:
                app.logger.error('Scraping error: %s', str(e))
                return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

        # 3. Validate text
        if not text or len(text) < 20:
            app.logger.error('Text too short: %d chars', len(text))
            return jsonify({'error': 'Text too short (minimum 20 characters)'}), 400

        # 4. Run engine
        result = engine.analyze(text)
        app.logger.info('Engine: status=%s entropy=%s', result.get('status'), result.get('entropy'))

        # 5. Attach metadata
        result['source']         = source
        result['title']          = title
        result['url']            = url
        result['mode']           = 'url_scraping' if url else 'manual_input'
        result['extracted_text'] = text[:1500] + ('...' if len(text) > 1500 else '')

        return jsonify(result), 200

    except Exception as e:
        app.logger.error('Unhandled exception: %s', str(e), exc_info=True)
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


# ============================================================
# TEST ENDPOINT
# ============================================================
@app.route('/api/test', methods=['POST'])
def test_endpoint():
    try:
        data = request.get_json(silent=True)
        app.logger.info('Test endpoint: %s', data)
        return jsonify({
            'success': True,
            'received': data,
            'message': 'POST working'
        }), 200
    except Exception as e:
        app.logger.error('Test error: %s', str(e))
        return jsonify({'error': str(e)}), 400


# ============================================================
# ENTRY
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
