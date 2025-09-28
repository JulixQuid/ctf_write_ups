#!/usr/bin/env python3
"""
recover_flag.py

Brute-force the timestamp-derived key used by the encryption pipeline.

Usage examples:
  # try timestamps in a small range (faster)
  python recover_flag.py --start 1694500000 --end 1694600000

  # try a range expressed as epoch seconds, or use defaults (last 30 days)
  python recover_flag.py --days 30

  # narrow search by known pattern (regex)
  python recover_flag.py --days 7 --pattern "^[a-z0-9_{}]{10,100}$"

Notes:
- The original encryption used key = str(int(os.path.getmtime("flag.txt"))).encode()
  so we brute-force candidate integer seconds and try to decrypt.
- Default filtering looks for printable results that contain '{' and '}'.
"""

import argparse
import os
import sys
import time
import re
from multiprocessing import Pool, cpu_count
from typing import Optional, Tuple, List

# --- encryption parameters (must match the encryptor) ---
RSA_A = 7
RSA_B = 13
B91_ALPHABET = [chr(i) for i in range(33, 124)]
B91_LEN = len(B91_ALPHABET)


# ----------------- reverse pipeline helpers -----------------
def modinv(a: int, m: int = 256) -> int:
    """Return multiplicative inverse of a modulo m (Extended Euclid)."""
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        raise ValueError("no inverse for a modulo m")
    if t < 0:
        t += m
    return t


A_INV = modinv(RSA_A, 256)


def base91_decode(encoded: str) -> bytes:
    """Decode the custom 'base91-like' encoding back to bytes."""
    if len(encoded) % 2 != 0:
        raise ValueError("encoded length must be even")
    out = []
    for i in range(0, len(encoded), 2):
        hi = B91_ALPHABET.index(encoded[i])
        lo = B91_ALPHABET.index(encoded[i + 1])
        out.append(hi * B91_LEN + lo)
    return bytes(out)


def affine_decrypt(data: bytes, a_inv: int = A_INV, b: int = RSA_B) -> bytes:
    """Affine decryption: a_inv * (x - b) mod 256"""
    return bytes([(a_inv * (c - b)) % 256 for c in data])


def xor_layer(data: bytes, key: bytes) -> bytes:
    """Repeating XOR decryption (symmetric)."""
    if len(key) == 0:
        return data
    return bytes([c ^ key[i % len(key)] for i, c in enumerate(data)])


def decrypt_with_timestamp(encoded_cipher: str, ts: int) -> bytes:
    """
    Try decrypting using timestamp ts as key: key = str(ts).encode()
    Returns decrypted bytes.
    """
    try:
        aff = base91_decode(encoded_cipher)
    except Exception:
        # malformed encoded data (shouldn't happen for valid cipher.txt)
        return b""
    dec_aff = affine_decrypt(aff)
    key = str(ts).encode()
    plain = xor_layer(dec_aff, key)
    return plain


# ----------------- heuristics / filtering -----------------
def is_likely_plaintext(pt: bytes, pattern: Optional[re.Pattern] = None) -> bool:
    """
    Heuristic to test whether plaintext looks like a flag:
      - majority printable ASCII
      - contains '{' and '}'
      - matches optional regex pattern (if provided)
    """
    if not pt:
        return False
    try:
        s = pt.decode('utf-8', errors='ignore')
    except Exception:
        return False

    # printable ratio
    printable_chars = sum(1 for ch in s if 32 <= ord(ch) <= 126)
    printable_ratio = printable_chars / max(1, len(s))

    if printable_ratio < 0.85:
        return False

    # must contain braces (common for CTF flags)
    if '{' not in s or '}' not in s:
        # still accept some candidates if pattern provided
        if not pattern:
            return False

    if pattern and not pattern.search(s):
        return False

    # length sanity check
    if len(s) < 4 or len(s) > 500:
        return False

    return True


# ----------------- worker for multiprocessing -----------------
def worker_task(args: Tuple[int, str, Optional[re.Pattern]]) -> Optional[Tuple[int, str]]:
    ts, encoded, pattern = args
    plain = decrypt_with_timestamp(encoded, ts)
    if is_likely_plaintext(plain, pattern):
        try:
            s = plain.decode('utf-8', errors='replace')
        except Exception:
            s = repr(plain)
        return ts, s
    return None


# ----------------- CLI / main logic -----------------
def parse_args():
    p = argparse.ArgumentParser(description="Brute-force timestamp-derived key to recover flag.")
    p.add_argument('--cipher', '-c', default='cipher.txt', help='file containing ciphertext (default cipher.txt)')
    p.add_argument('--start', type=int, help='start epoch second (inclusive)')
    p.add_argument('--end', type=int, help='end epoch second (inclusive)')
    p.add_argument('--days', type=int, default=None,
                   help='if provided, search last N days (overrides start/end defaults)')
    p.add_argument('--pattern', type=str,
                   help='optional regex (python) the plaintext should match; e.g. "ictf\\{[a-z0-9_]+\\}"')
    p.add_argument('--processes', '-p', type=int, default=max(1, cpu_count()-1),
                   help='number of parallel processes to use (default = cpu_count-1)')
    p.add_argument('--step', type=int, default=1, help='step between timestamps (seconds). Set >1 to speed up coarse search.')
    return p.parse_args()


def load_cipher(path: str) -> str:
    if not os.path.exists(path):
        print(f"cipher file {path} missing", file=sys.stderr)
        sys.exit(1)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().strip()


def main():
    args = parse_args()
    cipher_text = load_cipher(args.cipher)

    # compile pattern if provided
    pattern = re.compile(args.pattern) if args.pattern else None

    # choose timestamp range
    now = int(time.time())
    if args.days is not None:
        end_ts = now
        start_ts = max(0, now - args.days * 86400)
    else:
        start_ts = args.start if args.start is not None else max(0, now - 30 * 86400)  # default last 30 days
        end_ts = args.end if args.end is not None else now

    if start_ts > end_ts:
        start_ts, end_ts = end_ts, start_ts

    print(f"[+] searching timestamps from {start_ts} to {end_ts} (step={args.step}) using {args.processes} processes")
    total = (end_ts - start_ts) // args.step + 1
    print(f"[+] {total} candidates to try (approx)")

    # prepare args for workers
    timestamps = range(start_ts, end_ts + 1, args.step)
    worker_args = ((ts, cipher_text, pattern) for ts in timestamps)

    found: List[Tuple[int, str]] = []
    with Pool(processes=args.processes) as pool:
        for res in pool.imap_unordered(worker_task, worker_args, chunksize=256):
            if res:
                ts, plaintext = res
                print(f"\n[FOUND] ts={ts} -> {plaintext}\n")
                found.append((ts, plaintext))

    if not found:
        print("[!] No likely candidates found. Try expanding the range, lowering step, or providing a pattern.")
    else:
        print(f"[+] {len(found)} candidate(s) found. Review the outputs above.")


if __name__ == '__main__':
    main()
