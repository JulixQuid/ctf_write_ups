from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# Hardcoded ciphertext (hex)
ciphertext_hex = "713d7f2c0f502f485a8af0c284bd3f1e7b03d27204a616a8340beaae23f130edf65401c1f99fe99f63486a385ccea217"
ciphertext = bytes.fromhex(ciphertext_hex)

# Try all possible ASCII characters (0-255)
for c in range(256):
    char = bytes([c])
    # Compute BLAKE2b hash (64 bytes)
    h = hashlib.blake2b(char, digest_size=64)
    hash_bytes = h.digest()  # 64-byte hash

    # First 32 bytes = AES key, next 16 = IV
    key = hash_bytes[:32]
    iv = hash_bytes[32:48]

    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = cipher.decrypt(ciphertext)
        # Remove PKCS#7 padding (if any)
        decrypted_unpadded = unpad(decrypted, AES.block_size)
        # Check if the result is printable and looks like a flag
        if decrypted_unpadded.startswith(b"scriptCTF{"):
            print(f"Found valid char: {chr(c)} (ASCII {c})")
            print(f"Decrypted flag: {decrypted_unpadded.decode()}")
            break
    except (ValueError, UnicodeDecodeError):
        # Padding error or non-printable, ignore
        pass



