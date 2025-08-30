from sympy import mod_inverse, discrete_log

# Parameters
p = 14912432766367177751
g = 2784687438861268863
h = 8201777436716393968
c1 = 12279519522290406516
c2 = 10734305369677133991

# Solve for private key x: g^x ≡ h (mod p)
x = discrete_log(p, h, g)

# Decrypt: m = c2 * (c1^x)^(-1) mod p
m = (c2 * mod_inverse(pow(c1, x, p), p)) % p

# Convert to integer
message_int = m

# Convert to bytes (big endian)
message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, "big")

print("Private key x =", x)
print("Decrypted message (int) =", message_int)
print("Decrypted message (bytes) =", message_bytes)
print("UTF-8:", message_bytes.decode("utf-8", errors="replace"))
