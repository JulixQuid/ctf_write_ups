# Ciphertext provided (copied exactly as you gave it)
ciphertext_str = "elÎkÁua~SfÉRØljSnnÞRßcm~u\x7fÎdÕcs"
ciphertext = ciphertext_str.encode("latin-1")

# Recovered repeating XOR key (hex)
key = bytes.fromhex("0c0fba0dba0d0e0c")

def xor_decrypt(ct, key):
    return bytes([ct[i] ^ key[i % len(key)] for i in range(len(ct))])

# Decrypt
plaintext = xor_decrypt(ciphertext, key)

print("Ciphertext (latin-1):", ciphertext_str)
print("Key (hex):", key.hex())
print("Recovered flag:", plaintext.decode("utf-8"))
