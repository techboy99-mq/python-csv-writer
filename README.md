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
