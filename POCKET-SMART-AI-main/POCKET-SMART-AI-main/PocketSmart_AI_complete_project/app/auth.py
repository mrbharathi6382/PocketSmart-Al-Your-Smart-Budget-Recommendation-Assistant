from datetime import datetime, timedelta, timezone
import base64, hashlib, hmac, os
import jwt
from .config import get_settings

settings = get_settings()

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return "scrypt$" + base64.urlsafe_b64encode(salt).decode() + "$" + base64.urlsafe_b64encode(digest).decode()

def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, salt_b64, digest_b64 = encoded.split("$", 2)
        if scheme != "scrypt": return False
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(digest_b64.encode())
        actual = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False

def create_access_token(subject: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": exp}, settings.secret_key, algorithm="HS256")

def decode_access_token(token: str):
    try: return str(jwt.decode(token, settings.secret_key, algorithms=["HS256"])["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError): return None
