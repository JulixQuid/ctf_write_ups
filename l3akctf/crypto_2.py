from math import gcd
from Crypto.Util.number import bytes_to_long

# Given points
x1 = 103905521866731574234430443362297034336
y1 = 116589269353056499566212456950780999584
x2 = 171660318017081135625337806416866746485
y2 = 122407097490400018041253306369079974706
x3 = 161940138185633513360673631821653803879
y3 = 167867902631659599239485617419980253311
x4 = 95406403280474692216804281695624776780
y4 = 109560844064302254814641159241201048462

# Compute k_i = y_i^2 - x_i^3
k1 = y1**2 - x1**3
k2 = y2**2 - x2**3
k3 = y3**2 - x3**3
k4 = y4**2 - x4**3

# Compute differences for pairwise equations
d12 = k1 - k2
d13 = k1 - k3
d14 = k1 - k4
d23 = k2 - k3
d24 = k2 - k4
d34 = k3 - k4

# Compute T values from different point combinations
T1 = d12 * (x1 - x3) - d13 * (x1 - x2)
T2 = d12 * (x1 - x4) - d14 * (x1 - x2)
T3 = d13 * (x1 - x4) - d14 * (x1 - x3)
T4 = d23 * (x2 - x4) - d24 * (x2 - x3)
T5 = d13 * (x2 - x4) - d14 * (x2 - x3)
T6 = d23 * (x1 - x4) - d24 * (x1 - x3)

# Compute GCD of all T values
total_gcd = gcd(gcd(gcd(T1, T2), gcd(T3, T4)), gcd(T5, T6))

# Factor out small prime factors
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
p_value = abs(total_gcd)
for f in small_primes:
    while p_value % f == 0:
        p_value //= f

# Set modulus p
p = p_value

# Function to compute modular inverse
def mod_inverse(a, modulus):
    t0, t1 = 0, 1
    r0, r1 = modulus, a
    while r1 != 0:
        quotient = r0 // r1
        t0, t1 = t1, t0 - quotient * t1
        r0, r1 = r1, r0 - quotient * r1
    if r0 != 1:
        return None
    return t0 % modulus

# Compute curve parameters a and b using first two points
inv_denom = mod_inverse(x1 - x2, p)
if inv_denom is None:
    raise ValueError("Cannot compute modular inverse for a")

a = (d12 * inv_denom) % p
b = (k1 - a * x1) % p

# Verify all points lie on the curve
def is_on_curve(x, y, a, b, p):
    lhs = pow(y, 2, p)
    rhs = (pow(x, 3, p) + a * x + b) % p
    return lhs == rhs

assert is_on_curve(x1, y1, a, b, p)
assert is_on_curve(x2, y2, a, b, p)
assert is_on_curve(x3, y3, a, b, p)
assert is_on_curve(x4, y4, a, b, p)

# Known plaintexts
pt1 = "L3AK{test_"
pt2 = "flag}"
flag = pt1 + pt2
print(flag)