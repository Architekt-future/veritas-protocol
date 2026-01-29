import json
import http.server
import os
import sys

# 1. Чітко вказуємо шлях до кореня проекту
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 2. Імпортуємо Core (саме Core, як у тебе в файлі!)
try:
    from veritas_calibrated_core import VeritasCalibratedCore
except ImportError as e:
    print(f"Import Error: {e}")
    VeritasCalibratedCore = None

class handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            text = data.get('text', '')

            # ПЕРЕВІРКА: чи підтягнувся клас
            if VeritasCalibratedCore is None:
                raise Exception("Файл ядра знайдено, але клас VeritasCalibratedCore не завантажився.")

            # 3. ОСЬ ТУТ БУЛА ПОМИЛКА:
            # Створюємо екземпляр КОРУ (не Engine!), як у твоєму файлі
            v_core = VeritasCalibratedCore()
            
            # Викликаємо метод аналізу (теж за назвою з ядра)
            result = v_core.evaluate_integrity(text)
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Analysis failed: {str(e)}"}).encode())
