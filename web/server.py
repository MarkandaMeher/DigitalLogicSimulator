# =============================================================
# server.py — Local HTTP & C++ Simulator Bridge Server
# =============================================================
# Serves the web-based Digital Logic Circuit Simulator interface
# and synchronizes circuit simulations with simulator.exe.
#
# Usage:
#   cd c:\Projects\DigitalLogicSimulator\web
#   python server.py
#
# Then open http://localhost:8000 in your browser!
# =============================================================

import os
import sys
import json
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
SIMULATOR_EXE = os.path.join(os.path.dirname(WEB_DIR), "simulator.exe")

class CircuitSimulatorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_POST(self):
        # API: Synchronize with C++ Simulator
        if self.path == "/api/run-cpp-demo":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            req = json.loads(post_data) if post_data else {}

            demo_choice = str(req.get('demo', '11')) # 11=Half Adder, 14=ISCAS c17

            # Execute simulator.exe via stdin
            try:
                process_input = f"{demo_choice}\n0\n"
                result = subprocess.run(
                    [SIMULATOR_EXE],
                    input=process_input,
                    text=True,
                    capture_output=True,
                    timeout=5
                )

                response = {
                    "success": True,
                    "stdout": result.stdout,
                    "returncode": result.returncode
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": str(e)
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

def run():
    print("=" * 65)
    print("  DIGITAL LOGIC CIRCUIT SIMULATOR — WEB MODULE")
    print("=" * 65)
    print(f"  • Serving Web GUI from: {WEB_DIR}")
    print(f"  • Linked C++ Engine:     {SIMULATOR_EXE}")
    print(f"  • URL:                   http://localhost:{PORT}")
    print("=" * 65)
    print("  Opening web browser automatically...")
    
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, CircuitSimulatorHandler)
    
    try:
        # Launch browser
        import webbrowser
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped by user. Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    run()
