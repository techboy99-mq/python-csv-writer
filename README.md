Start Python HTTP CSV Server: python3 simple_csv_server.py

Write data to the Python HTTP CSV Server with the following:

curl -X POST http://localhost:8080/submit \
  -H "Authorization: Bearer your_secure_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "mq-host-01",
    "mq_install_type": "client",
    "mq_version": "9.3.5",
    "date": "2025-07-04",
    "install_status": "success"
  }'

SystemD File Details:

WorkingDirectory: Set this to the directory you want the server to serve (like /var/www/html or your project folder).
ExecStart: Launches Python’s built-in HTTP server on port 8000.
ExecStop: Sends a SIGTERM to the process to stop it cleanly.
Restart=on-failure: Restarts the server if it crashes (optional).
