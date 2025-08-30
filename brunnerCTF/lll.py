# requirements: argon2-cffi, cryptography
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_key(password: str, hash_salt_hex: str, key_salt_hex: str) -> bytes:
    argon2_hash = hash_secret_raw(
        secret=password.encode(),
        salt=bytes.fromhex(hash_salt_hex),
        time_cost=5,
        memory_cost=262144,   # matches their code
        parallelism=4,
        hash_len=64,
        type=Type.ID
    )
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=bytes.fromhex(key_salt_hex), info=b'user-data-encryption')
    return hkdf.derive(argon2_hash)

def decrypt_aesgcm(nonce_hex: str, ciphertext_hex: str, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(bytes.fromhex(nonce_hex), bytes.fromhex(ciphertext_hex), None)

# Example: Dud entry (from CSV)
nonce = "bd1251d5608613fc58dd0706"
hash_salt = "a1df29bca0ae24fe6d656e1f55506ffd"
key_salt  = "3f559ae3727f4205d0d85736a9c4f08e"
enc_hex   = "d2687c3ddc27a27c36ab700f59cd39d96796e4"

# discovered pepper: "e9d8"  (used only for password hashing storage, not for encryption)
password = "dud"  # cracked for Dud/Emul
key = derive_key(password, hash_salt, key_salt)
plaintext = decrypt_aesgcm(nonce, enc_hex, key)
print(plaintext)   # b'Dud'
