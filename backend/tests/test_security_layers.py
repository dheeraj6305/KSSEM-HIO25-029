# backend/tests/test_security_layers.py
import os
from pathlib import Path
from agents.security_layer1 import generate_key, SecurityLayer1, KEY_PATH
from agents.security_layer2 import write_log, verify_logs

def test_generate_and_use_key(tmp_path):
    # generate a temporary key and use SecurityLayer1 with it
    kpath = tmp_path / "bank_secret.key"
    generate_key(path=str(kpath))
    sec = SecurityLayer1(key_path=str(kpath))
    assert hasattr(sec, "fernet") and sec.fernet is not None
    data = b"unit-test"
    token = sec.encrypt_bytes(data)
    assert token != data
    assert sec.decrypt_bytes(token, role="Admin") == data

def test_audit_log_write_and_verify(tmp_path, monkeypatch):
    # Write a couple of audit entries then verify logs
    # Note: this will use the project's audit_log.txt path; ensure not running in prod
    write_log("UNIT_TEST_ACTION1", "pytest")
    write_log("UNIT_TEST_ACTION2", "pytest")
    ok, msg = verify_logs()
    assert ok is True
