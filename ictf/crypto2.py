#!/usr/bin/env python3
"""
recover_from_file.py

Usage:
    python3 recover_from_file.py data.txt

This script attempts to:
 - parse m (or N?), ct, and nums from a text file (supports several common print formats),
 - run pairwise gcd(nums[i] - nums[j], m) and gcd(nums[i], m) to find factors,
 - attempt to fully factor m, compute d and decrypt ct.

Requires: pycryptodome (for long_to_bytes and inverse). Install with:
    pip install pycryptodome
"""
import sys
import re
from math import gcd
from Crypto.Util.number import long_to_bytes, inverse

def parse_file(path):
    txt = open(path, 'r', encoding='utf-8', errors='ignore').read()

    # Try JSON-ish block: look for ct = <int> or "ct": <int>
    def find_int(key):
        # patterns like ct=123... or "ct": 123... or 'ct': 123...
        patterns = [
            rf'{key}\s*=\s*([0-9]+)',
            rf'["\']{key}["\']\s*:\s*([0-9]+)'
        ]
        for p in patterns:
            m = re.search(p, txt)
            if m:
                return int(m.group(1))
        return None

    ct = find_int('ct') or find_int('CT') or find_int('ciphertext')
    m = find_int('m') or find_int('M') or find_int('modulus') or find_int('N')

    # Try to find a Python-style list for nums: nums = [123, 456, ...]
    nums = None
    mlist = re.search(r'nums\s*=\s*\[([0-9,\s]+)\]', txt)
    if mlist:
        items = [s.strip() for s in mlist.group(1).split(',') if s.strip()]
        nums = [int(x) for x in items]
    else:
        # maybe printed as "nums=[...]" without spaces or as multiple lines
        mlist = re.search(r'nums\s*=\s*\[([^\]]+)\]', txt, re.S)
        if mlist:
            items = re.split(r',\s*', mlist.group(1).strip())
            try:
                nums = [int(x.strip()) for x in items if x.strip()]
            except:
                nums = None

    # fallback: maybe the file contains many big integers; try to extract big ints and heuristically assign
    if (ct is None or m is None or nums is None):
        bigints = [int(x) for x in re.findall(r'([0-9]{50,})', txt)]
        # heuristics:
        # - expect m to be very large (product of many 512-bit primes) -> length ~ 15000 bits ~ ~4500 decimal digits,
        #   but exact lengths depend. We'll pick the largest for m, the next for ct, and remaining possibly nums.
        if bigints:
            bigints_sorted = sorted(bigints, key=lambda x: len(str(x)), reverse=True)
            if m is None:
                m = bigints_sorted[0]
            if ct is None and len(bigints_sorted) > 1:
                ct = bigints_sorted[1]
            if nums is None and len(bigints_sorted) > 2:
                # treat the rest as potential nums (not very reliable)
                nums = bigints_sorted[2:]

    # final sanity checks
    if ct is None or m is None or nums is None:
        print("Failed to parse all values automatically. Parsed so far:")
        print("  ct:", "FOUND" if ct else None)
        print("  m: ", "FOUND" if m else None)
        print("  nums:", f"{len(nums)} items" if nums else None)
        print("\nPlease ensure the file contains explicit 'ct', 'm' (or 'N'), and 'nums = [...]'.")
        sys.exit(1)

    print(f"Parsed ct (bits) = {ct.bit_length()} bits")
    print(f"Parsed m  (bits) = {m.bit_length()} bits")
    print(f"Parsed nums count = {len(nums)}")
    return ct, m, nums

def try_find_factors(m, nums):
    print("Starting gcd pairwise search...")
    found = set()
    L = len(nums)
    for i in range(L):
        a = nums[i]
        # gcd with m
        g = gcd(a, m)
        if 1 < g < m:
            found.add(g)
        for j in range(i+1, L):
            b = nums[j]
            g = gcd(abs(a - b), m)
            if 1 < g < m:
                found.add(g)
        # small progress print
        if i % 16 == 0 and i > 0:
            print(f"  checked pairs for first {i} nums (found factors so far: {len(found)})")
    print(f"Pairwise search complete. Unique gcd-factors found: {len(found)}")
    return sorted(found)

def extract_full_factors(m, seeds):
    M = m
    factors = []
    # Reduce by seeds
    for s in seeds:
        if M % s == 0:
            while M % s == 0:
                factors.append(s)
                M //= s
    return factors, M

def finalize_and_decrypt(m, ct, factors):
    prod = 1
    for f in factors:
        prod *= f
    print(f"Collected {len(factors)} factors. Product bit-length = {prod.bit_length()}. m bit-length = {m.bit_length()}")

    if prod != m:
        print("WARNING: Partial factorization only. Cannot compute full private key yet.")
        return False

    print("Full factorization present. Computing phi and d...")
    phi = 1
    for p in factors:
        phi *= (p - 1)
    e = 0x10001
    try:
        d = pow(e, -1, phi)
    except TypeError:
        d = inverse(e, phi)
    pt = pow(ct, d, m)
    try:
        flag = long_to_bytes(pt)
        print("\nRecovered plaintext (raw bytes):")
        print(flag)
        try:
            print("\nDecoded (utf-8):")
            print(flag.decode())
        except Exception:
            pass
    except Exception as ex:
        print("Decryption produced an integer. Integer value:")
        print(pt)
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 recover_from_file.py data.txt")
        sys.exit(1)
    path = sys.argv[1]
    ct, m, nums = parse_file(path)

    seeds = try_find_factors(m, nums)
    if not seeds:
        print("No seed gcd factors found. Consider increasing nums or using ECM/Pollard's Rho on m.")
        sys.exit(1)

    # Extract repeated factors (divide them out)
    factors, remaining = extract_full_factors(m, seeds)
    if factors:
        print(f"Extracted {len(factors)} factors from gcd seeds. Remaining cofactor bit-length: {remaining.bit_length()}")
    else:
        print("Couldn't extract direct multiplicity from found seeds.")

    # If remaining != 1 try to find additional gcds against remaining
    if remaining != 1:
        extras = set()
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                g = gcd(abs(nums[i]-nums[j]), remaining)
                if 1 < g < remaining:
                    extras.add(g)
        if extras:
            print(f"Found {len(extras)} extra factors for remaining part.")
            for e in extras:
                while remaining % e == 0:
                    factors.append(e)
                    remaining //= e
            print(f"After extras, remaining bit-length: {remaining.bit_length()}")

    # Final attempt to decrypt if we have full factorization
    ok = finalize_and_decrypt(m, ct, factors)
    if not ok:
        print("\nPartial factors found (first 10):", factors[:10])
        print("Next steps:")
        print(" - Run ECM (e.g. msieve/ecm) on the remaining cofactor(s).")
        print(" - Try Pollard-rho on remaining pieces.")
        print(" - If you can produce more nums from the target, that increases chances of gcd collisions.")
    else:
        print("Done.")

if __name__ == '__main__':
    main()
