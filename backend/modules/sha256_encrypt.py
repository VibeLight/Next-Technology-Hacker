import hashlib

def sha256_encrypt(text):
    return hashlib.sha256(text.encode()).hexdigest()
