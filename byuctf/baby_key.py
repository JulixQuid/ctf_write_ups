from Crypto.PublicKey import RSA

public_key_pem = """
-----BEGIN PUBLIC KEY-----
MIIBAjANBgkqhkiG9w0BAQEFAAOB8AAwgewCgeQo+PHTOEh57OGg5PqZD97ln4O8
z1/EHSeDplfjytTxgfChwrf2Hg85G3sRr8UCsHDlVaOcFNmz6ubInjMOD2j7d4kk
OOk+bBzJSGnOgFJbWdCXwMeDFhoUjVNw/UreHmX0kGCni9ci4PpO1iTzdHpNYZAS
L9G3eMpbu9hcoEzuE+GXvlJ11MWBGiot8YbjdK1fixH29QHDLNqmrBFwd5Y5XCqV
e1xzmEAcm5vgbBjduXmBxevx7OdWT0K4RDcFBqC8nfwq5UZJqwXvSDmB59fs1tbb
uqzcToCcxUr6xM4wiUPHxeECAwEAAQ==
-----END PUBLIC KEY-----
""".strip()  # Critical: Remove whitespace

key = RSA.import_key(public_key_pem)
print(f"N = {key.n}\ne = {key.e}")

import math

def integer_sqrt(N):
    return math.isqrt(N)  # Python 3.8+ has integer square root function

# Example usage:
N = key.n  # Replace this with your actual N
sqrt_N_integer = integer_sqrt(N)
e = key.e
print(f"Integer part of sqrt({N}): {sqrt_N_integer}")

import math
from Crypto.Util.number import inverse, long_to_bytes

def decrypt_sqrt_N(N, e):
    # Step 1: Compute integer part of sqrt(N)
    c = math.isqrt(N)  # ciphertext = floor(sqrt(N))
    print(f"[+] Ciphertext (sqrt(N)): {c}")

    # Step 2: Try to factor N (to get p and q)
    def factor(N):
        # Pollard's Rho (works for small N)
        if N % 2 == 0: return 2
        if N % 3 == 0: return 3
        if N % 5 == 0: return 5

        while True:
            a = 2
            b = 2
            while True:
                a = (a * a + 1) % N
                b = (b * b + 1) % N
                b = (b * b + 1) % N
                d = math.gcd(abs(a - b), N)
                if d > 1 and d < N:
                    return d
                if d == N:
                    break

    try:
        p = factor(N)
        q = N // p
        print(f"[+] Factors found: p = {p}, q = {q}")

        # Step 3: Compute phi(N) and d
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        print(f"[+] Private exponent (d): {d}")

        # Step 4: Decrypt c^d mod N
        m = pow(c, d, N)
        print(f"[+] Decrypted message (as number): {m}")

        # Try to convert to bytes (ASCII/UTF-8)
        try:
            msg = long_to_bytes(m).decode()
            print(f"[+] Decrypted message (as text): {msg}")
        except:
            print("[!] Decrypted message is not text (could be raw bytes)")

    except:
        print("[!] Failed to factor N (too large or secure)")


decrypt_sqrt_N(N, e)