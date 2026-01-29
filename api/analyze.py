"""
Vercel Python Serverless Function
Endpoint: /api/analyze
"""

from http.server import BaseHTTPRequestHandler
import json
import http.server
import os
import sys

# 1. ТИЦЯЄМО НОСОМ У КОРІНЬ (Path Fix)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 2. ІМПОРТ (Синхронізація назв)
try:
    from veritas_calibrated_core import VeritasCalibratedCore
    # Створюємо об'єкт з ПРАВИЛЬНОЮ назвою
    engine = VeritasCalibratedCore()
except Exception as e:
    engine = None
    print(f"Import Error: {e}")

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
        self.wfile.write(json.dumps({"status": "online", "engine_ready": engine is not None}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            text = data.get('text', '')
            
            # ВИПРАВЛЕНО: викликаємо engine (об'єкт), а не Engine (клас)
            if engine:
                result = engine.evaluate_integrity(text)
            else:
                raise Exception("Engine not initialized")
            
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
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
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
            engine = VeritasCalibratedEngine()
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
