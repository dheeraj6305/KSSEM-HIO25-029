# agents/security_layer1.py
from cryptography.fernet import Fernet
import os, time

# Generate or load a persistent key (only once for your app)
KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "bank_secret.key")
if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as f:
    SECRET_KEY = f.read()

fernet = Fernet(SECRET_KEY)

# === Simple token check ===
def verify_access_token(token: str) -> bool:
    """
    Very lightweight demo authentication.
    Expects format:  SuperSecureToken123:<timestamp>
    """
    try:
        parts = token.split(":")
        if len(parts) != 2:
            return False
        secret, ts = parts
        if secret != "SuperSecureToken123":
            return False
        # optional expiry: 10 min
        if abs(time.time() - float(ts)) > 600:
            return False
        return True
    except Exception:
        return False
