"""
End-to-End Backend Functional Test
----------------------------------
✅ Generates a valid token
✅ Calls / (root) to confirm backend is live
✅ Uploads a sample ZIP to /bulk_evaluate
✅ Prints result summary
"""

import requests
import time
import json

# === CONFIG ===
BASE_URL = "http://127.0.0.1:8000"
ZIP_PATH = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\backend\sample_data\salary_slip_samples.zip"

# === Step 1: Generate valid token ===
token = f"SuperSecureToken123:{time.time()}"
signature = "bWFzdGVyLXNpZ25hdHVyZQ=="

print("🟢 Generated access token:", token)

# === Step 2: Check root endpoint ===
try:
    root_resp = requests.get(f"{BASE_URL}/")
    print("🌐 Root response:", root_resp.status_code, root_resp.json())
except Exception as e:
    print("❌ Could not reach backend:", e)
    exit(1)

# === Step 3: Upload ZIP to /bulk_evaluate ===
try:
    with open(ZIP_PATH, "rb") as f:
        files = {"file": (ZIP_PATH.split("\\")[-1], f, "application/zip")}
        data = {"token": token, "signature": signature}
        print("📤 Uploading ZIP for evaluation...")
        resp = requests.post(f"{BASE_URL}/bulk_evaluate", data=data, files=files)
except Exception as e:
    print("❌ Upload failed:", e)
    exit(1)

# === Step 4: Print formatted result ===
print("\n--- Server Response ---")
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print("Raw:", resp.text)

print("\n✅ End-to-End test completed.")
