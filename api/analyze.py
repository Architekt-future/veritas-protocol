import json
import http.server
import os
import sys
import traceback

# Імпортуємо з поточної директорії (api/)
try:
    from veritas_calibrated_core import VeritasCalibratedCore
    print(f"✅ Module loaded successfully. Available methods: {[m for m in dir(VeritasCalibratedCore) if not m.startswith('_')]}")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in api/: {os.listdir('.')}")
    VeritasCalibratedCore = None

class handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """For debugging"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        debug_info = {
            "status": "API is running",
            "module_loaded": VeritasCalibratedCore is not None,
            "files_in_api": os.listdir('.'),
            "python_version": sys.version
        }
        self.wfile.write(json.dumps(debug_info).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            post_data = self.rfile.read(content_length)
            print(f"📨 Received POST data: {post_data[:500]}...")  # Логуємо перші 500 символів
            
            data = json.loads(post_data)
            text = data.get('text', '')
            print(f"📝 Text to analyze: {text[:100]}...")

            if VeritasCalibratedCore is None:
                raise Exception("VeritasCalibratedCore module not loaded")

            v_core = VeritasCalibratedCore()
            print("✅ Core instance created")
            
            # Динамічно знаходимо метод
            if hasattr(v_core, 'evaluate_integrity'):
                result = v_core.evaluate_integrity(text)
            elif hasattr(v_core, 'evaluate'):
                result = v_core.evaluate(text)
            elif hasattr(v_core, 'analyze'):
                result = v_core.analyze(text)
            else:
                raise AttributeError("No analysis method found")
            
            print(f"✅ Analysis result: {result}")
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print(f"🔍 TRACEBACK: {traceback.format_exc()}")
            
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                "error": f"Analysis failed: {str(e)}",
                "traceback": traceback.format_exc().split('\n')[-10:]  # Останні 10 рядків
            }
            self.wfile.write(json.dumps(error_response).encode())
