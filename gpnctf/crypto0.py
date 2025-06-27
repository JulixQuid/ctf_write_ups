import sys
from gmpy2 import mpz, invert, digits, from_binary

# Given data (converted to integers)
n = mpz(0x7249a9f5872abbbae3cec6c685e7e21bc316fcc8926403bec246b19ba70328aefa0894285f7f80b0f71cc053c09e19f4b2b16b738394a94a5d39b5a44950c50c34e147c10a95f845421183f8b1a1d65545cb91f1791e6cbc4d04c6651a1e4ddfbf294835a860143090775191e0fca6b49d990e770f05102d7544e94bd0dcad16e7f12e8b2c5aca7589524d32e115bb701da3343dbd116817405d94c10f12721f963cdfbd1bc3c8a778dfd12c215dcff23149fa62e2682e9003ea741e39361a7d7429cb215e08ed766e546ae8769a6e82e4c054ad9af9bbfdf0c269e5d709d1ec9e957507ca5e789d2e8919c648f8ef698dd7d41b6d20df729da75f9233786a69)
e = mpz(0x10001)
c = mpz(0x4dd8883cc05af5360d351692fb45ff95673a62de60f2d2ad414376eaa289615dc4f909273a077e460cf28aba556b0e71f736a5897b1eef4b5937720315d811bd74043ca929d4899d9d2f5d0239b78e9c1c18bf6b9d688048bca07507249edfb142fd9c1d5ef6f43f64fd00a078c7e9d5873adf3f2b280f6ccaddfef2933f7d9d903f7aada7f29819694ffa15a79eb8808821ba52829376ee62a3d63e58d299646c5d6539706229523b378f54624e1f02bb635beba60369ad78588708bc25b056e22b5240d2ed4711bf60d3f1b9cee73dca9470bfdfc560b808b27424a79dbb7c42ec1ac922de228a5be7067f0d27593790f250164ea139630b22ea1d7c85a3bd)
V = (0, 5, 4, 1, 0, 0, 5, 1, 6, 3, 4, 4, 5, 4, 1, 2, 5, 3, 6, 2, 0, 1, 4, 1, 4, 5, 6, 5, 2, 6, 3, 0, 2, 5, 0, 6, 4, 0, 2, 6, 3, 1, 0, 5, 4, 1, 4, 5, 4, 1, 3, 6, 0, 0, 5, 0, 0, 3, 2, 3, 6, 4, 0, 4, 3, 1, 5, 6, 1, 4, 5, 5, 5, 4, 4, 4, 1, 4, 5, 1, 3, 4, 3, 3, 5, 5, 5, 5, 2, 6, 5, 1, 3, 2, 0, 0, 6, 1, 1, 5, 1, 1, 2, 2, 2, 0, 5, 4, 0, 5, 6, 5, 4, 0, 5, 3, 6, 6, 3, 0, 0, 2, 2, 5, 2, 1, 2, 3, 2, 2, 0, 0, 1, 5, 3, 6, 6, 1, 0, 1, 5, 6, 2, 5, 6, 1, 4, 3, 2, 6, 0, 3, 3, 4, 6, 5, 4, 2, 1, 3, 2, 0, 2, 3, 6, 2, 1, 1, 2, 3, 3, 6, 5, 1, 4, 3, 5, 3, 1, 2, 0, 0, 4, 0, 6, 0, 0, 0, 3, 0, 0, 4, 6, 4, 0, 2, 2, 0, 5, 5, 0, 3, 5, 3, 3, 4, 4, 4, 0, 4, 0, 0, 1, 3, 4, 3, 1, 3, 2, 1, 4, 2, 6, 2, 4, 3, 6, 5, 6, 2, 3, 4, 6, 6, 0, 5, 1, 1, 3, 6, 5, 1, 2, 4, 3, 0, 5, 0, 0, 4, 5, 5, 4, 0, 4, 5, 3, 0, 6, 5, 3, 2, 2, 6, 2, 6, 6, 4, 3, 2, 4, 5, 3, 6, 4, 0, 3, 6, 4, 2, 2, 6, 5, 2, 1, 2, 3, 2, 1, 4, 5, 1, 5, 0, 6, 6, 1, 4, 6, 1, 6, 2, 2, 2, 2, 6, 6, 1, 4, 6, 1, 4, 5, 5, 3, 1, 5, 2, 1, 1, 4, 2, 5, 2, 0, 1, 2, 2, 1, 6, 2, 2, 3, 6, 6, 2, 5, 5, 2, 3, 3, 1, 0, 3, 6, 5, 5, 2, 3, 3, 2, 0, 1, 5, 1, 1, 6, 2, 2, 3, 2, 0, 4, 5, 4, 0, 0)

# Convert n to base 7 digits (little-endian)
def number_to_base(n, b):
    digits = []
    while n > 0:
        digits.append(int(n % b))
        n = n // b
    return digits

n_digits = number_to_base(n, 7)
max_len = len(V)
n_digits += [0] * (max_len - len(n_digits))  # Pad with zeros

# Backtracking to find p and q
def solve_pq():
    p_digits = []
    q_digits = []
    
    # Start from the least significant digit (index 0)
    for i in range(max_len):
        target_sum = V[i]
        found = False
        
        # Try all possible (p_i, q_i) pairs
        for p_i in range(7):
            for q_i in range(7):
                if (p_i + q_i) % 7 == target_sum:
                    # Tentatively add digits
                    p_digits.append(p_i)
                    q_digits.append(q_i)
                    
                    # Reconstruct p and q up to current digit
                    p = sum(p_digits[k] * (7 ** k) for k in range(len(p_digits)))
                    q = sum(q_digits[k] * (7 ** k) for k in range(len(q_digits)))
                    
                    # Check if p * q matches n up to current digit
                    if (p * q) % (7 ** (i + 1)) == n % (7 ** (i + 1)):
                        found = True
                        break
                    else:
                        p_digits.pop()
                        q_digits.pop()
            if found:
                break
        if not found:
            return None, None
    
    p = sum(p_digits[i] * (7 ** i) for i in range(max_len))
    q = sum(q_digits[i] * (7 ** i) for i in range(max_len))
    
    if p * q == n:
        return p, q
    else:
        return None, None

p, q = solve_pq()

if p is not None:
    print(f"Found p = {p}")
    print(f"Found q = {q}")
    
    # Decrypt the flag
    phi = (p - 1) * (q - 1)
    d = invert(e, phi)
    m = pow(c, d, n)
    
    # Convert m to bytes (flag)
    flag = bytes.fromhex(hex(m)[2:])
    print(f"Flag: {flag.decode()}")
else:
    print("Failed to factor n.")