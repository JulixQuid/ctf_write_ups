from Crypto.Util.number import long_to_bytes
import math
import random

def factor_n(n, max_diff=10000):
    """Factorize n given that q = p + k where k is small (up to max_diff)."""
    # Since n = p*q and q = p + k, we can write n = p*(p + k)
    # Which is p^2 + k*p - n = 0. Solve for p.
    for k in range(1, max_diff + 1):
        # Solve quadratic equation: p^2 + k*p - n = 0
        discriminant = k**2 + 4 * n
        sqrt_discriminant = math.isqrt(discriminant)
        if sqrt_discriminant * sqrt_discriminant == discriminant:
            p = (-k + sqrt_discriminant) // 2
            if p > 0 and n % p == 0:
                q = n // p
                return p, q
    return None, None

def lcm(a, b):
    """Compute the least common multiple of a and b."""
    return a * b // math.gcd(a, b)

def L(x, n):
    """Compute the L function: L(x) = (x - 1) / n."""
    return (x - 1) // n

def decrypt(c, n, g):
    """Decrypt ciphertext c using private key derived from n and g."""
    p, q = factor_n(n)
    if p is None or q is None:
        raise ValueError("Failed to factorize n")
    
    lambda_n = lcm(p - 1, q - 1)
    # Compute g^lambda mod n^2
    g_lambda = pow(g, lambda_n, n**2)
    # Compute L(g_lambda)
    L_g_lambda = L(g_lambda, n)
    # Compute mu as the modular inverse of L_g_lambda mod n
    mu = pow(L_g_lambda, -1, n)
    
    # Compute c^lambda mod n^2
    c_lambda = pow(c, lambda_n, n**2)
    # Compute L(c_lambda)
    L_c_lambda = L(c_lambda, n)
    # Recover m
    m = (L_c_lambda * mu) % n
    return m

#Public Key (n, g):
n = 11596790285009779332288660306670955733087055429749842841040722149983792324904218924606607469519900980272903931109062999644114140971700838770753531624961997
g = 11596790285009779332288660306670955733087055429749842841040722149983792324904218924606607469519900980272903931109062999644114140971700838770753531624961998

#Encrypted Flag (c):
c = 124884047360367808788475923986252219794553274578278768678220719369332702794001073543421786779337873835074804079505488400442758793369566475790329733177666782308774320432727171471607300433637805564742274256730965110977012936554641001686435445502856557258429285896098026847859492917232886635193189656262496752584


# Decrypt the flag
m = decrypt(c, n, g)
flag = long_to_bytes(m)
print(flag.decode())