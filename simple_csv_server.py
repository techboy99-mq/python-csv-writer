import http.server
import json
import csv
import re
from urllib.parse import urlparse
from datetime import datetime

AUTH_TOKEN = "your_secure_token_here"
CSV_FILE_PATH = "mq_install_logs.csv"

class CSVRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        # Simple route check
        if self.path != "/submit":
            self.send_error(404, "Not Found")
            return

        # Auth check
        auth = self.headers.get("Authorization")
        if not auth or auth != f"Bearer {AUTH_TOKEN}":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        # Read and parse JSON body
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        # Extract and validate fields
        hostname = data.get("hostname", "").strip()
        mq_install_type = data.get("mq_install_type", "").strip().lower()
        mq_version = data.get("mq_version", "").strip()
        date_str = data.get("date", "").strip()
        install_status = data.get("install_status", "").strip().lower()
        conn_test_status = data.get("conn_test_status", "").strip().lower()

        if not re.match(r"^[a-zA-Z0-9._-]{1,253}$", hostname):
            return self.send_json_error("Invalid hostname")
        if mq_install_type not in {"client", "server"}:
            return self.send_json_error("Invalid install type")
        if not re.match(r"^\d+\.\d+\.\d+(?:\.\d+)?$", mq_version):
            return self.send_json_error("Invalid MQ version format")
        try:
            datetime.strptime(date_str, "%Y-%m-%d-%H:%M")
        except ValueError:
            return self.send_json_error("Invalid date format. Expected YYYY-MM-DD-HH:MM")
        if install_status not in {"success", "failed"}:
            return self.send_json_error("Invalid install status")
        if conn_test_status not in {"success", "failed"}:
            return self.send_json_error("Invalid connection test status")

        # Write to CSV
        try:
            with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    hostname,
                    mq_install_type,
                    mq_version,
                    date_str,
                    install_status,
                    conn_test_status
                ])
        except Exception as e:
            return self.send_json_error(f"Failed to write to CSV: {str(e)}", status=500)

        # Success response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())

    def send_json_error(self, message, status=400):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

if __name__ == "__main__":
    PORT = 8080
    IP = 0.0.0.0
    server = http.server.HTTPServer((IP, PORT), CSVRequestHandler)
    print(f"Server running on http://{IP}:{PORT}")
    server.serve_forever()