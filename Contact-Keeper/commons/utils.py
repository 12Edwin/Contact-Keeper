import re


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def encrypt_string(hash_string):
    import hashlib
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
