# agents/security_layer2.py
import base64

def verify_signature(signature: str) -> bool:
    """
    Basic placeholder verification for a digital signature.
    In real use, verify against stored public key.
    """
    try:
        decoded = base64.b64decode(signature).decode()
        return decoded == "master-signature"
    except Exception:
        return False
