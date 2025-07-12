from ecdsa import SECP256k1
#from mySecret import d  # For verification only (not needed for attack)

# Given data
r = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
r1 = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
s1 = 0xdf88df0b8b3cc27eedddc4f3a1ecfb55e63c94739e003c1a56397ba261ba381d
h1 = 0x315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3

r2 = 0xe37ce11f44951a60da61977e3aadb42c5705d31363d42b5988a8b0141cb2f50d
s2 = 0x2291d4ab9e8b0c412d74fb4918f57580b5165f8732fd278e65c802ff8be86f61
h2 = 0xa6ab91893bbd50903679eb6f0d5364dba7ec12cd3ccc6b06dfb04c044e43d300
n = SECP256k1.order

# Step 1: Compute Δh and Δs
delta_h = (h1 - h2) % n
delta_s = (s1 - s2) % n

# Step 2: Compute the private key d
d_recovered = ( (s2 * h1 - s1 * h2) * pow(r * delta_s, -1, n) ) % n

print(f"[Recovered Private Key]\nd = {hex(d_recovered)}")
s1==(pow(k, -1, n) * (h1 + r * d)) % n

# Signature for m2
s2 == (pow(k, -1, n) * (h2 + r * d)) % n  