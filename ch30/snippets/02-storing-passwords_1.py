import hashlib, hmac, secrets

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"

def verify_password(password: str, stored: str) -> bool:
    _, salt_hex, digest_hex = stored.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)    # constant-time comparison

stored = hash_password("correct horse battery staple")
print(verify_password("correct horse battery staple", stored))   # True
print(verify_password("Correct horse battery staple", stored))   # False
print(hash_password("same") != hash_password("same"))            # True: a new salt each time
