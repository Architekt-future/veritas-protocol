"""
Vercel Python Serverless Function
Endpoint: /api/analyze
Integrated: NewsExtractor scraper + VeritasCalibratedCore analysis
"""

from http.server import BaseHTTPRequestHandler
import json
import http.server
import os
import sys

# 1. Залізобетонний імпорт ядра
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from veritas_calibrated_core import VeritasCalibratedCore
except Exception as e:
    print(f"Import error: {e}")
    VeritasCalibratedCore = None

class handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "online",
            "info": "Veritas API is ready"
        }).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            text = data.get('text', '')

            if not text:
                raise Exception("No text provided for analysis")

            # Перевірка наявності ядра
            if VeritasCalibratedCore is None:
                raise Exception("Analysis Core (veritas_calibrated_core.py) not found or failed to load")

            # 2. Ініціалізація та виклик
            engine = VeritasCalibratedCore()
            result = engine.evaluate_integrity(text)

            # 3. Відповідь
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e), "status": "error"}).encode())
    
# Inline NewsExtractor (no external deps on Vercel)
class SimpleExtractor:
    """
    Simplified scraper without BeautifulSoup dependency
    Uses regex for content extraction
    """
    
    def extract_from_url(self, url: str, html: str) -> dict:
        """Extract text from HTML"""
        try:
            # Remove unwanted elements
            cleaned = self._clean_html(html)
            
            # Extract title
            title = self._extract_title(html)
            
            # Extract main text
            text = self._extract_paragraphs(cleaned)
            
            # Get source domain
            source = self._extract_domain(url)
            
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
    
    def _clean_html(self, html: str) -> str:
        """Remove scripts, styles, nav, etc."""
        # Remove scripts
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove styles
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove nav
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove header
        html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove footer
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove ads
        html = re.sub(r'<div[^>]*class="[^"]*ad[^"]*"[^>]*>.*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        return html
    
    def _extract_title(self, html: str) -> str:
        """Extract page title"""
        # Try og:title
        match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Try <title>
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try h1
        match = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return "Unknown Title"
    
    def _extract_paragraphs(self, html: str) -> str:
        """Extract text from <p> tags"""
        # Find all <p> tags
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        
        if not paragraphs:
            # Fallback: extract from article/main
            article_match = re.search(r'<article[^>]*>(.*?)</article>', html, flags=re.DOTALL | re.IGNORECASE)
            if article_match:
                article_html = article_match.group(1)
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', article_html, flags=re.DOTALL | re.IGNORECASE)
        
        if not paragraphs:
            # Last resort: get body text
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                body_text = body_match.group(1)
                # Remove all tags
                body_text = re.sub(r'<[^>]+>', ' ', body_text)
                return self._clean_text(body_text)
        
        # Combine paragraphs
        text = ' '.join(paragraphs)
        
        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Clean up
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove HTML entities
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if match:
            return match.group(1)
        return "unknown"


class handler(BaseHTTPRequestHandler):
    
    def _set_cors_headers(self):
        """Set CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Health check"""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'online',
            'service': 'Veritas Protocol Analysis API',
            'version': '3.0-calibrated-scraper',
            'endpoints': {
                'POST /api/analyze': 'Analyze URL or text'
            }
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """Main analysis endpoint with URL scraping support"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._send_error(400, 'Invalid JSON')
                return
            
            # Check if engine is available
            if VeritasCalibratedCore is None:
                self._send_error(500, 'Analysis engine not available')
                return
            
            # Initialize engine
            engine = VeritasCalibratedCore()

            result = engine.evaluate_integrity(text)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
            # Check if URL or text provided
            url = data.get('url', '').strip()
            text = data.get('text', '').strip()
            source = data.get('source', 'Unknown')
            
            if url:
                # URL MODE: Scrape then analyze
                try:
                    # Fetch URL
                    import urllib.request
                    req = urllib.request.Request(
                        url,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                    )
                    
                    with urllib.request.urlopen(req, timeout=10) as response:
                        html = response.read().decode('utf-8', errors='ignore')
                    
                    # Extract content
                    extractor = SimpleExtractor()
                    extraction = extractor.extract_from_url(url, html)
                    
                    if not extraction['success']:
                        raise Exception(extraction.get('error', 'Extraction failed'))
                    
                    # Analyze extracted text
                    text = extraction['text']
                    source = extraction['source']
                    title = extraction['title']
                    
                    if not text or len(text) < 50:
                        raise Exception('Extracted text too short')
                    
                    result = engine.analyze(text)
                    
                    # Add extraction info
                    result['source'] = source
                    result['title'] = title
                    result['url'] = url
                    result['mode'] = 'url_scraping'
                    
                except Exception as e:
                    self._send_error(500, f'Scraping failed: {str(e)}')
                    return
                    
            elif text:
                # TEXT MODE: Direct analysis
                if len(text) < 10:
                    self._send_error(400, 'Text too short')
                    return
                
                result = engine.analyze(text)
                result['source'] = source
                result['mode'] = 'text_input'
                
            else:
                self._send_error(400, 'No URL or text provided')
                return
            
            # Send successful response
            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self._send_error(500, f'Analysis failed: {str(e)}')
    
    def _send_error(self, code: int, message: str):
        """Send error response"""
        self.send_response(code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'error': message,
            'status': 'error'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
