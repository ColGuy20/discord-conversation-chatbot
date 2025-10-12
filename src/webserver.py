import os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

#--Web Server--

class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"HEALTHY"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

    # Silence Request Logging
    def log_message(self, format, *args):
        return

def start_web_server():
    server = HTTPServer(("0.0.0.0", 8080), _HealthHandler)
    thread = threading.Thread(target=server.serve_forever, name="health-server", daemon=True)
    thread.start()
    return server, thread

def stop_web_server(server: HTTPServer):
    server.shutdown()
    server.server_close()
