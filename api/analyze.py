import json
import http.server
import os
import sys

# Налаштовуємо шлях до ядра
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from veritas_calibrated_core import VeritasCalibratedCore
    # Створюємо глобальний об'єкт відразу при запуску
    V_ENGINE = VeritasCalibratedCore()
except Exception as e:
    V_ENGINE = None
    print(f"Init error: {e}")

class handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            if V_ENGINE is None:
                raise Exception("Veritas Core not loaded. Check file paths.")

            data = json.loads(post_data)
            text = data.get('text', '')
            
            # Викликаємо метод аналізу
            result = V_ENGINE.evaluate_integrity(text)
            
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
