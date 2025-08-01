import math
from decimal import Decimal, getcontext
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
leak = 0.4336282047950153046404  # Your known decimal part
eps = 1e-10  # Tolerance for floating-point precision

candidates = []

# Bounds for n = int(sqrt(r))
low_n = int(math.sqrt(10**10))  # sqrt(10^10) = 10^5
high_n = int(math.sqrt(10**11))  # sqrt(10^11) ≈ 316227.766

for n in range(low_n, high_n + 1):
    # Compute expected r
    expected_r = (n + leak) ** 2
    r_candidate = round(expected_r)
    
    # Check if r_candidate is in [10^10, 10^11)
    if 10**10 <= r_candidate < 10**11:
        # Verify sqrt(r_candidate) has the correct decimal part
        sqrt_r = math.sqrt(r_candidate)
        decimal_part = sqrt_r - int(sqrt_r)
        
        if abs(decimal_part - leak) < eps:
            candidates.append(r_candidate)

# If you want to verify the candidates by reconstructing them from n and leak
ks = [(int(math.sqrt(cand)) + leak)**2 for cand in candidates]

for k in ks:
    leak = int( str( Decimal(k).sqrt() ).split('.')[-1] )
    print(k, leak) # 41642293072.0 4336282047950153046404


from decimal import Decimal, getcontext
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Given values
K = 41642293072
ct_hex = "7863c63a4bb2c782eb67f32928a1deceaee0259d096b192976615fba644558b2ef62e48740f7f28da587846a81697745"
ct = bytes.fromhex(ct_hex)

# Step 1: Compute MD5 hash of K (as string) to get AES key
key = md5(f"{K}".encode()).digest()

# Step 2: Decrypt the ciphertext
cipher = AES.new(key, AES.MODE_ECB)
pt_padded = cipher.decrypt(ct)

# Step 3: Unpad the plaintext to get the flag
flag = unpad(pt_padded, 16).decode()

print("Flag:", flag)