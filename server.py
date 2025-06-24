from http.server import HTTPServer, BaseHTTPRequestHandler
import os

UPLOAD_DIR = "received_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SimpleUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        filename = self.headers.get('X-Filename', 'unknown_file')
        file_data = self.rfile.read(content_length)

        save_path = os.path.join(UPLOAD_DIR, filename)
        with open(save_path, 'wb') as f:
            f.write(file_data)
        
        print(f"[+] Received and saved: {save_path}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Upload successful.")

def run(server_class=HTTPServer, handler_class=SimpleUploadHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Listening on port {port} for uploads...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
