import json
import http.server
import urllib.parse
import sys
import os

# Додаємо шлях до кореня, щоб знайти файл ядра
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Імпортуємо правильну назву класу з ядра
try:
    from veritas_calibrated_core import VeritasCalibratedCore
except ImportError:
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
        
        response = {
            "status": "online",
            "engine_ready": VeritasCalibratedCore is not None
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            text = data.get('text', '')
            source = data.get('source', 'direct_input')

            # ПЕРЕВІРКА: Використовуємо правильну назву класу
            if VeritasCalibratedCore is None:
                self._send_error(500, 'Analysis engine not available (Import failed)')
                return
            
            # Створюємо екземпляр ПРАВИЛЬНОГО класу
            engine = VeritasCalibratedCore()
            
            # ВИКЛИКАЄМО ПРАВИЛЬНИЙ МЕТОД (evaluate_integrity замість analyze)
            result = engine.evaluate_integrity(text)
            
            result['source'] = source

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self._send_error(500, f"Analysis failed: {str(e)}")

    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode())
