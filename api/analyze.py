"""
Vercel Python Serverless Function
Endpoint: /api/analyze
"""

from http.server import BaseHTTPRequestHandler
import json
import http.server
import os
import sys

# 1. Чітко вказуємо шлях до кореня
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 2. Імпортуємо правильну назву класу
try:
    from veritas_calibrated_core import VeritasCalibratedCore
    # Створюємо екземпляр з правильною назвою!
    engine = VeritasCalibratedCore()
except Exception as e:
    print(f"Критична помилка імпорту: {e}")
    engine = None


class handler(BaseHTTPRequestHandler):
    
    def _set_cors_headers(self):
        """Set CORS headers to allow frontend access"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'online',
            'service': 'Veritas Protocol Analysis API',
            'version': '3.0-calibrated',
            'endpoint': '/api/analyze (POST)'
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """Main analysis endpoint"""
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
            
            # Extract text
            text = data.get('text', '').strip()
            source = data.get('source', 'Unknown')
            
            if not text:
                self._send_error(400, 'No text provided')
                return
            
            # Check if engine is available
            if VeritasCalibratedCore is None:
                self._send_error(500, 'Analysis engine not available')
                return
            
            # Initialize engine and analyze
            engine = VeritasCalibratedCore()
            result = engine.analyze(text)
            
            # Add source to result
            result['source'] = source
            
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
