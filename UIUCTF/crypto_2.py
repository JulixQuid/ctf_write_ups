from sympy import nextprime, randprime, prevprime
import math
import gmpy2
from Crypto.Util.number import long_to_bytes

N =  34546497157207880069779144631831207265231460152307441189118439470134817451040294541962595051467936974790601780839436065863454184794926578999811185968827621504669046850175311261350438632559611677118618395111752688984295293397503841637367784035822653287838715174342087466343269494566788538464938933299114092019991832564114273938460700654437085781899023664719672163757553413657400329448277666114244272477880443449956274432819386599220473627937756892769036756739782458027074917177880632030971535617166334834428052274726261358463237730801653954955468059535321422372540832976374412080012294606011959366354423175476529937084540290714443009720519542526593306377
ct =  32130352215164271133656346574994403191937804418876038099987899285740425918388836116548661879290345302496993945260385667068119439335225069147290926613613587179935141225832632053477195949276266017803704033127818390923119631817988517430076207710598936487746774260037498876812355794218544860496013734298330171440331211616461602762715807324092281416443801588831683678783343566735253424635251726943301306358608040892601269751843002396424155187122218294625157913902839943220894690617817051114073999655942113004066418001260441287880247349603218620539692362737971711719433735307458772641705989685797383263412327068222383880346012169152962953918108171850055943194
e = 65537
p_inf = nextprime(2**127) 
p_sup = prevprime(2**128)
N = 1
p = p_inf
i = 0
while N < 2**2048:
	N *= p
	p = nextprime(p)
	i+=1
print(f"[+] inf {i}")

p = p_sup


i = 0
N = 1
while N < 2**2048:
	N *= p
	p = nextprime(p)
	i+=1
print(f"[+] sup {i}")



N_mpz = gmpy2.mpz(N)
root_16 = gmpy2.iroot(N_mpz, 16)
root = int(root_16[0])
primes = []
p = int(root) - 1
for i in range(30):
	p = nextprime(p)

	primes.append(p)
	
divs = [elem for elem in primes if N%elem==0]
p = int(root) - 1
primes = []

for i in range(10):
	p = prevprime(p)

	divs = [p] + divs
print(len(divs))
divs = [prime for prime in divs if N%prime==0]
assert N == math.prod(divs)

factors = sorted(divs) # Replace p1, p2, ..., p16 with actual primes

# Step 1: Compute phi(from Crypto.Util.number import long_to_bytes

#phi_N = math.prod([p - 1 for p in factors])
phi_N = 1
for p in factors:
    phi_N *= (p - 1)

print(f"phi(N) = {phi_N}")
# Step 2: Compute private exponent d
d = pow(e, -1, phi_N)
assert math.gcd(phi_N, 65537) == 1
# Step 3: Decrypt ciphertext
pt = pow(ct, d, N)

d = pow(e, -1, phi_N)

# Decrypt ciphertext
pt = pow(ct, d, N)
# Try different ways to decode the plaintext
d = pow(e, -1, phi_N)
assert (e * d) % phi_N == 1  # Must hold true
assert math.prod(factors) == N
assert math.prod(factors) == N, "Factorization failed!"
pt_decrypted = pow(ct, d, N)
ct_reconstructed = pow(pt_decrypted, e, N)

pt = pow(ct, d, N)
ct_reconstructed = pow(pt, e, N)
e = 65537
d = pow(e, -1, phi_N)


print(f"Found {len(factors)} factors.")
assert math.prod(factors) == N, "Factorization failed!"

# Compute phi(N)
phi_N = 1
for p in factors:
    phi_N *= (p - 1)

print(f"phi(N) = {phi_N}")

# Compute d
d = pow(e, -1, phi_N)
assert (e * d) % phi_N == 1, "Incorrect d!"

# Decrypt
pt = pow(ct, d, N)
print(f"Decrypted pt: {pt}")

# Verify round-trip
ct_reconstructed = pow(pt, e, N)
print(f"Original ct: {ct}")
print(f"Reconstructed ct: {ct_reconstructed}")
#assert ct == ct_reconstructed, "Decryption failed!"

# Try decoding
flag = long_to_bytes(pt)
print(f"Flag (raw): {flag}")

# Trim null bytes
flag_trimmed = flag.strip(b'\x00')
print(f"Flag (trimmed): {flag_trimmed}")

# Hex decode fallback
try:
    hex_str = hex(pt)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    flag_hex = bytes.fromhex(hex_str)
    print(f"Flag (hex): {flag_hex}")
except:
    pass
assert (e * d) % phi_N == 1, "Incorrect d!"
print(f"d = {d}")
print(f"Original ct: {ct}")
print(f"Reconstructed ct: {ct_reconstructed}")
#assert ct == ct_reconstructed, "Decryption failed!"
#assert ct_reconstructed == ct  # Must match original ciphertext
#print(long_to_bytes(pt).decode('utf-8', errors='ignore'))
#flag = long_to_bytes(pt).strip(b'\x00')
print(bytes.fromhex(hex(pt)[2:]))



c = ct
n=N
# primes are factored from n
primes = factors
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

ts = []
xs = []
ds = []

for i in range(len(primes)):
	ds.append(modinv(e, primes[i]-1))

m = primes[0]

for i in range(1, len(primes)):
	ts.append(modinv(m, primes[i]))
	m = m * primes[i]

for i in range(len(primes)):
	xs.append(pow((c%primes[i]), ds[i], primes[i]))

x = xs[0]
m = primes[0]

for i in range(1, len(primes)):
	x = x + m * ((xs[i] - x % primes[i]) * (ts[i-1] % primes[i]))
	m = m * primes[i]


print(hex(x%n))

pt = 0x8a9da5abeb897fdac3970a01ce1132ef6d551f0221f47ea02518109934f7c2411db5fc84c8907a4c91cf3aa6e29c07b2b7d0017beb07ab46ada7c675db2e0c167aae94d23020f13a834b498b92ce17228d5fb79af3ebe0d4c93837f055dbbddb5ce2260f4722ef4ebe336fdef11f962d3a254189f50d2b3a37386b83561b465ae571666e92746180921d91f3d187351a8ace39419e8326264afca36f35d3211f77dd4e9db6988b74e2b386eda6ee2d90b67b9f2df6e41478f40ff55654a3456e5a2c80af5fd83d7198534c3c161c9d1509664a366c5ecded14d75cd701ba49a1403c81b7d5572bb462277cb2ec167d6602ddbf2a7341deedb35df582705c2558
hex_str = hex(pt)[2:]  # Remove '0x' prefix
print("Hex representation:", hex_str)
from binascii import unhexlify

try:
    flag_bytes = unhexlify(hex_str)
    print("Flag (hex decoded):", flag_bytes)
except:
    print("Not valid hex!")
import base64

try:
    # First, convert pt to raw bytes
    pt_bytes = long_to_bytes(pt)
    # Try base64 decoding
    flag = base64.b64decode(pt_bytes).decode('utf-8')
    print("Flag (base64 decoded):", flag)
except:
    print("Not base64!")