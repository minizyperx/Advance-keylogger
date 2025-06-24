from http.server import HTTPServer, BaseHTTPRequestHandler
import os

UPLOAD_DIR = "received_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SimpleUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        filename = self.headers.get('X-Filename', 'unknown_file')
        file_data = self.rfile.read(content_length)

        # Ensure secure path
        safe_filename = os.path.basename(filename)
        save_path = os.path.join(os.getcwd(), UPLOAD_DIR, safe_filename)

        try:
            with open(save_path, 'wb') as f:
                f.write(file_data)
            print(f"[+] Received and saved: {save_path}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Upload successful.")
        except Exception as e:
            print(f"[!] Error saving file: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Upload failed.")

def run(server_class=HTTPServer, handler_class=SimpleUploadHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Server running. Listening on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
