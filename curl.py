import sys
import json
import urllib.request

# --- Check Args ---
if len(sys.argv) != 8:
    print("Usage: python curl.py <hostname> <mq_install_type> <mq_version> <date> <time> <install_status> <install_result>")
    sys.exit(1)

# --- Get Values from CLI ---
hostname = sys.argv[1]
mq_install_type = sys.argv[2]
mq_version = sys.argv[3]
date = sys.argv[4]
time = sys.argv[5]
install_status = sys.argv[6]
install_result = sys.argv[7]

# --- JSON Payload ---
data = {
    "hostname": hostname,
    "mq_install_type": mq_install_type,
    "mq_version": mq_version,
    "date": date,
    "time": time,
    "install_status": install_status,
    "install_result": install_result
}

# --- URL and Headers ---
url = "http://localhost:8080/submit"  # Change this if needed
token = "your_secure_token_here"      # Replace with actual bearer token

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# --- Encode and Send ---
json_data = json.dumps(data).encode("utf-8")
req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        print("Response:", response_body)
except urllib.error.HTTPError as e:
    print("HTTP error:", e.code, e.reason)
    print(e.read().decode())
except urllib.error.URLError as e:
    print("Connection error:", e.reason)
