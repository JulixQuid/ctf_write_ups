# solver.py
from random import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, ARC4
from gostcrypto import gostcipher

# ---------- Utilities copied/adapted from the challenge ----------

def ranDOCm_doc(doc: str) -> int:
    docstring_int = int.from_bytes(''.join(doc.split()).encode(), 'big')
    return docstring_int % 11

def SPECIAL_technique(bytes_data: bytes, c: int, d: int) -> bytes:
    xor_bytes = bytearray()
    for i in range(0, len(bytes_data)//32):
        block = bytes_data[i*32:(i+1)*32]
        xor_bytes.extend(x ^ y for x, y in zip(block, (c - (-1)**i * d).to_bytes(32, 'big')))
    return bytes(xor_bytes)

# docstrings (exactly as in the challenge)
DOCS = {
"graham_crackeRSA": "Crush the graham crackers. (For making the crust.)",
"ADDed_SOLUTION_giving_bREADMETEXTure": """Splits a 128 byte ciphertext into two blocks and xors them with values, which besides serving as 
    further encryption intermediately also turns the first block into bytes that if decoded contains 
    plaintext describing in full detail how to get the flag in this challenge.""",
"melted_BITter": "Melt the butter, and mix it with the graham cracker crumbs.",
"ground_CAESARdamom": """Ground cardamom lends a warm, citrus-floral spice (for an intriguingly aromatic depth, 
    reminiscent of e.g. Scandinavian and Middle_Eastern desserts).""",
"an_egGOST": "An egg is needed to help in binding the ingredients together.",
"sour_STREAM": "Sour cream is commonly a central ingredient in a lot of cheesecake recipes.",
"vanilla_eXORtract": "Vanilla extract is often used: For enhancing the flavor of the cheesecake.",
"cAESugar": "Cane sugar is often used in cheesecake recipes (to add sweetness to it).",
"beat_INTEGERgredients": "After adding several different things it's a good time to beat the ingredients together."
}

SEED = {name: ranDOCm_doc(DOCS[name]) for name in DOCS}

# string and i-value used inside beat_INTEGERgredients
S_STR = """,&6y5jz*r~6BR `|FQ39*So7w`,&oC*1^PZhCKp}UT. C^tgoVBRb$z`*Zpa)XB>|b^%MO~6~IR_whvM!}|mA |@jj090!*gP;?Qf*Cj0$"{@5&[HjpVTnig|>?]Q$CT4}{S3i8iC[kUq2GfW3\\>iu:O30qp"""
def s2i(s: str) -> int:
    d = [chr(i) for i in range(32,127)]
    base = len(d)
    total = 0
    for idx, ch in enumerate(s[::-1]):
        total += d.index(ch) * (base ** idx)
    return total

# ---------- Inverses of each step (working backwards) ----------

def inv_beat_INTEGERgredients(final_bytes: bytes) -> bytes:
    # In forward: n = int.from_bytes(x,'big'); out = (n - i) -> bytes (minimal)
    # We need x s.t. (n - i) == 0 => n == i. But x is the 128-byte AES output.
    # So we return the 128-byte big-endian representation of i.
    i_key = SEED["beat_INTEGERgredients"]
    i_val = s2i(S_STR) // i_key
    return i_val.to_bytes(128, 'big')

def inv_cAESugar(target_bytes: bytes) -> bytes:
    # Forward: AES-ECB encrypt with key [key_byte]*16
    key_byte = SEED["cAESugar"]
    key = bytes([key_byte] * 16)
    cipher = AES.new(key, AES.MODE_ECB)
    # inverse = decrypt
    return cipher.decrypt(target_bytes)

def inv_vanilla_eXORtract(target_bytes: bytes) -> bytes:
    # Forward XOR with PRNG bytes where seed used is (seed+1)
    seed = SEED["vanilla_eXORtract"]
    r = Random(seed + 1)
    keystream = bytes(r.getrandbits(8) for _ in range(len(target_bytes)))
    return bytes(b ^ k for b, k in zip(target_bytes, keystream))

def inv_sour_STREAM(target_bytes: bytes) -> bytes:
    # RC4 is symmetric; decrypt == encrypt with same key
    key_byte = SEED["sour_STREAM"]
    cipher = ARC4.new(bytes([key_byte]))
    return cipher.encrypt(target_bytes)

def inv_an_egGOST(target_bytes: bytes) -> bytes:
    # Kuznechik in CTR is symmetric; decrypt == encrypt with same params
    int_key = SEED["an_egGOST"]
    key = int_key.to_bytes(32, 'big')
    cipher = gostcipher.new("kuznechik", key, gostcipher.MODE_CTR, init_vect=b"\0"*8)
    return cipher.encrypt(target_bytes)

def inv_ground_CAESARdamom(target_bytes: bytes) -> bytes:
    # Forward: (b + key) % 256  => inverse: (b - key) % 256
    key = SEED["ground_CAESARdamom"]
    return bytes((b - key) % 256 for b in target_bytes)

def inv_melted_BITter(target_bytes: bytes) -> bytes:
    # Forward: rotate-left by (shift % 8)
    # Inverse: rotate-right by (shift % 8)
    shift = SEED["melted_BITter"] % 8
    if shift == 0:
        return target_bytes
    return bytes(((b >> shift) | ((b << (8 - shift)) & 0xFF)) & 0xFF for b in target_bytes)

def inv_ADDed_SOLUTION_giving_bREADMETEXTure(target_bytes: bytes) -> bytes:
    # Forward: 
    #   SOLUTION_READMETEXT = SPECIAL_technique(ct[:64], c, d)
    #   residual = SPECIAL_technique(ct[64:], c, d)
    #   out = (SOLUTION_READMETEXT + residual) XOR e
    # Inverse:
    #   tmp = out XOR e
    #   Re-apply SPECIAL_technique to each half (since it's XOR with a known stream)
    e = SEED["ADDed_SOLUTION_giving_bREADMETEXTure"]
    c = 46412520328440256871399753615737168429362885041489783567894921161800073479497
    d = 30147310566698376871947829873776459834598978229983782629303180618977163687145
    # XOR with 'e' byte-wise across the whole 128 bytes
    tmp = bytes(b ^ e for b in target_bytes)
    left, right = tmp[:64], tmp[64:]
    # SPECIAL_technique is its own inverse (XOR with the same 32-byte mask per block)
    inv_left  = SPECIAL_technique(left,  c, d)
    inv_right = SPECIAL_technique(right, c, d)
    return inv_left + inv_right

def inv_graham_crackeRSA(target_bytes: bytes) -> str:
    # Forward builds RSA key from PRNG seeded by ranDOCm(doc)
    seed = SEED["graham_crackeRSA"]
    prng = Random(seed)
    def randfunc(n): 
        return prng.getrandbits(n * 8).to_bytes(n, 'big')
    key = RSA.generate(1024, randfunc=randfunc)
    # We need to *decrypt* the raw RSA (no padding). That's modular exponent with d.
    c_int = int.from_bytes(target_bytes, 'big')
    m_int = pow(c_int, key.d, key.n)
    # Convert back to a string (the challenge fed a 128-char string to RSA)
    m_bytes = m_int.to_bytes((m_int.bit_length() + 7)//8, 'big')
    try:
        return m_bytes.decode()
    except UnicodeDecodeError:
        # Leading zeros may be missing; RSA "plaintext" is a big integer.
        # We know the original was exactly 128 chars, so pad if needed:
        # But since it's text, try latin-1 as a fallback to see content.
        return m_bytes.decode('latin-1')

# ---------- Drive the full inverse pipeline ----------

def solve():
    # Start from the fact that the final MD2 input must be empty:
    final = b""  

    # Invert last -> first
    after_AES_out128      = inv_beat_INTEGERgredients(final)
    before_AES            = inv_cAESugar(after_AES_out128)
    before_vanilla        = inv_vanilla_eXORtract(before_AES)
    before_rc4            = inv_sour_STREAM(before_vanilla)
    before_kuznechik      = inv_an_egGOST(before_rc4)
    before_caesar         = inv_ground_CAESARdamom(before_kuznechik)
    before_rotate         = inv_melted_BITter(before_caesar)
    before_readmetext_xor = inv_ADDed_SOLUTION_giving_bREADMETEXTure(before_rotate)
    original_128_str      = inv_graham_crackeRSA(before_readmetext_xor)

    # At this point, original_128_str is the *custom padded* string the recipe built
    # from the true flag text (which itself is plain, e.g., brunner{...}).
    # The padding scheme is a weird cyclic windowing that *preserves* the original
    # text at the start. So just read off the flag as the substring starting with 'brunner{' up to '}'.
    import re
    m = re.search(r'brunner\{[^}]*\}', original_128_str)
    if not m:
        # If not present directly, also check in the first 64 bytes that the challenge
        # says should contain a “README” in plain text after deobfuscation:
        readme = SPECIAL_technique(before_rotate[:64], 
                                   46412520328440256871399753615737168429362885041489783567894921161800073479497,
                                   30147310566698376871947829873776459834598978229983782629303180618977163687145)
        try:
            readme_text = readme.decode(errors='ignore')
        except:
            readme_text = ""
        m = re.search(r'brunner\{[^}]*\}', readme_text)
        if m:
            return m.group(0), original_128_str, readme_text
        else:
            # If still not found, just return the whole recovered string for inspection.
            return None, original_128_str, readme_text

    return m.group(0), original_128_str, ""

if __name__ == "__main__":
    flag, recovered128, readme = solve()
    if flag:
        print("[FLAG]", flag)
    else:
        print("[!] Flag pattern not found automatically.")
        print("Recovered string:", recovered128)
        if readme:
            print("README block:", readme)
