# backend/tests/test_api_integration.py
import os
from fastapi.testclient import TestClient
from agents.security_layer1 import generate_key, KEY_PATH
from pathlib import Path

# Import the FastAPI app from main.py (assumes tests are run from backend/)
from main import app

client = TestClient(app)

def test_ocr_encrypt_and_decrypt_flow(tmp_path):
    # Ensure key exists for the demo app (KEY_PATH points to backend/bank_secret.key)
    # generate_key will create the key at KEY_PATH if missing
    generate_key(path=KEY_PATH)

    # Upload a small file via the /ocr endpoint
    files = {"file": ("test.txt", b"dummy content")}
    r = client.post("/ocr", files=files, data={"user": "Officer_01"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert "encrypted_path" in body
    enc_path = body["encrypted_path"]
    assert Path(enc_path).exists()

    # Officer should be forbidden to decrypt
    r_off = client.post("/decrypt_ocr", data={"encrypted_path": enc_path, "role": "Officer"})
    assert r_off.status_code == 403

    # Admin can decrypt
    r_admin = client.post("/decrypt_ocr", data={"encrypted_path": enc_path, "role": "Admin"})
    assert r_admin.status_code == 200
    assert "plaintext" in r_admin.json()

    # Verify logs endpoint
    r_verify = client.get("/verify_logs")
    assert r_verify.status_code == 200
    j = r_verify.json()
    assert isinstance(j.get("ok"), bool)
