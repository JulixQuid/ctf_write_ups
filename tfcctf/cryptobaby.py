#!/usr/bin/env python3
"""
process_dump.py <dump-file> [--prefix PREFIX]

Parses the dump from the challenge (output of your interactive script),
attempts to reconstruct MT19937 internal state from either:
 - muava bytes (8-bit outputs from omlets), or
 - guava samples (26-bit outputs),
optionally boosted by known-key bytes derived from a provided prefix.

If state is recovered, it will predict key bytes and decrypt the
last omlet found in the file, printing the recovered flag.
"""

import re, sys, argparse
from random import Random

# -------------------------
# MT19937 untemper helpers
# -------------------------
def _unright(y, shift):
    res = 0
    for i in range(0, 32, shift):
        part = y ^ (res >> shift)
        res |= (part & ((1 << shift) - 1)) << i
    return res & 0xFFFFFFFF

def _unleft(y, shift, mask):
    res = 0
    for i in range(0, 32, shift):
        part = y ^ ((res << shift) & mask)
        res |= (part & ((1 << shift) - 1)) << i
    return res & 0xFFFFFFFF

def untemper(y: int) -> int:
    # inverse of the standard MT19937 tempering
    y = _unright(y, 18)
    y = _unleft(y, 15, 0xEFC60000)
    y = _unleft(y, 7,  0x9D2C5680)
    y = _unright(y, 11)
    return y & 0xFFFFFFFF

# -------------------------
# Parsers
# -------------------------
def parse_dump(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        s = f.read()

    # guava numeric samples (26-bit)
    guava = [int(x) for x in re.findall(r"uhhh.*?:\s*([0-9]+)", s)]

    # all bracketed arrays (omlets). We'll treat any bracketed list of ints as an omlet candidate.
    arrs = re.findall(r"\[([0-9,\s]+)\]", s, flags=re.S)
    omlets = []
    for a in arrs:
        nums = re.findall(r"\d+", a)
        if nums:
            omlets.append([int(x) for x in nums])

    return guava, omlets

# -------------------------
# Build 32-bit tempered words from streams of k-bit outputs
# -------------------------
def words_from_bit_chunks(chunks, kbits, need_words=624, msb_first=True):
    """
    chunks: iterable of integer values (each of kbits length).
    kbits: number of bits per chunk (8 for bytes, 26 for guava samples).
    Returns list of reconstructed 32-bit tempered words from the concatenated stream.
    Assumes each chunk corresponds to the next kbits taken from the top of the MT bitstream.
    """
    bitbuf = 0
    bitlen = 0
    words = []
    mask = (1 << kbits) - 1
    for val in chunks:
        val &= mask
        # append bits to the right (we treat the earliest bits as most significant)
        bitbuf = (bitbuf << kbits) | val
        bitlen += kbits
        while bitlen >= 32 and len(words) < need_words:
            shift = bitlen - 32
            w = (bitbuf >> shift) & 0xFFFFFFFF
            words.append(w)
            bitlen -= 32
            if shift > 0:
                bitbuf &= (1 << shift) - 1
            else:
                bitbuf = 0
            if len(words) >= need_words:
                break
    return words

# -------------------------
# Try to recover using different data sources
# -------------------------
def try_recover_from_bytes(byte_stream, need_words=624):
    # bytes are 8-bit chunks
    words = words_from_bit_chunks(byte_stream, 8, need_words=need_words)
    return words

def try_recover_from_guava(guava_samples, need_words=624):
    # guava samples: 26-bit chunks
    words = words_from_bit_chunks(guava_samples, 26, need_words=need_words)
    return words

# -------------------------
# Build RNG & decrypt
# -------------------------
def build_rng_from_untempered(untempered_words):
    if len(untempered_words) < 624:
        raise ValueError("need 624 untempered words")
    st = (3, tuple(untempered_words[:624] + [624]), None)
    r = Random()
    r.setstate(st)
    return r

def decrypt_with_rng(rng, omlet):
    key = [rng.randrange(256) for _ in range(len(omlet))]
    flag = "".join(chr(o ^ k) for o, k in zip(omlet, key))
    return flag

# -------------------------
# Utilities & main
# -------------------------
def bits_collected_from(guava_count, omlet_bytes_count):
    return guava_count * 26 + omlet_bytes_count * 8

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dumpfile", help="file containing the saved interaction dump")
    parser.add_argument("--prefix", help="known flag prefix (e.g. TFCCTF{) to produce known key bytes", default=None)
    args = parser.parse_args()

    guava, omlets = parse_dump(args.dumpfile)
    print(f"[+] Parsed dump: {len(guava)} guava samples, {len(omlets)} omlet blocks")

    # Build a byte stream from all omlets (flattened)
    all_bytes = []
    for block in omlets:
        all_bytes.extend(block)

    if args.prefix:
        # derive known key bytes from prefix for the first N blocks where applicable
        pref = args.prefix
        pbytes = [ord(c) for c in pref]
        known_keys = []
        used_blocks = 0
        for block in omlets:
            if len(block) < len(pbytes):
                continue
            for i, pb in enumerate(pbytes):
                known_keys.append(block[i] ^ pb)Load into Ghidra: For a sustained, in-depth analysis. Use the decompiler to understand the logic quickly. The symbol table from step 2 will make the Ghidra analysis much more meaningful from the start.
            used_blocks += 1
        if known_keys:
            print(f"[+] Derived {len(known_keys)} known key bytes from prefix across {used_blocks} omlet blocks")
            # Prepend these known key bytes to the byte stream so they help reconstruction
            # (they are real PRNG outputs, unlike omlet bytes which are FLAG^key)
            # Important: these are the actual key bytes, so we treat them as bytes from PRNG directly.
            all_bytes = known_keys + all_bytes
        else:
            print("[!] Could not derive any known key bytes from the prefix (no omlet with enough length)")

    # First try using byte stream (muava) since it's the cleanest
    print(f"[+] Total bytes available (omlet bytes + known keys if any): {len(all_bytes)}")
    words_from_bytes = try_recover_from_bytes(all_bytes, need_words=624)
    print(f"[+] Reconstructed {len(words_from_bytes)} 32-bit words from byte stream")

    if len(words_from_bytes) >= 624:
        print("[+] EnoughLoad into Ghidra: For a sustained, in-depth analysis. Use the decompiler to understand the logic quickly. The symbol table from step 2 will make the Ghidra analysis much more meaningful from the start. words from byte stream -> untempering and building RNG")
        untempered = [untemper(w) for w in words_from_bytes[:624]]
        rng = build_rng_from_untempered(untempered)
        if not omlets:
            print("[!] No omlet found to decrypt. RNG built - you can predict future keys.")
            return
        # Use the last omlet in file to decrypt
        last_omlet = omlets[-1]
        flag = decrypt_with_rng(rng, last_omlet)
        print("[+] FLAG (using last omlet):", flag)
        return

    # If bytes insufficient, try using guava samples
    words_from_guava = try_recover_from_guava(guava, need_words=624)
    print(f"[+] Reconstructed {len(words_from_guava)} 32-bit words from guava samples")

    if len(words_from_guava) >= 624:
        print("[+] Enough words from guava -> untempering and building RNG")
        untempered = [untemper(w) for w in words_from_guava[:624]]
        rng = build_rng_from_untempered(untempered)
        if not omlets:
            print("[!] No omlet found to decrypt. RNG built - you can predict future keys.")
            return
        last_omlet = omlets[-1]
        flag = decrypt_with_rng(rng, last_omlet)
        print("[+] FLAG (using last omlet):", flag)
        return

    # If neither worked, give guidance and diagnostics
    bits_have = bits_collected_from(len(guava), len(all_bytes))
    print("[-] Insufficient data to reconstruct full MT state yet.")
    print(f"    Bits collected (guava*26 + bytes*8) = {bits_have} bits (need ~19968)")
    if len(all_bytes) > 0:
        print(f"    Byte stream length: {len(all_bytes)} bytes -> ~{len(all_bytes)*8} bits")
    if len(guava) > 0:
        print(f"    Guava samples: {len(guava)} -> ~{len(guava)*26} bits")
    print("Suggestions:")
    print(" - If you have many muava outputs (omlet bytes), collect ~2500 bytes total and retry.")
    print(" - If you only used guava, guava is lossy (6 bits lost per draw). Use muava instead.")
    print(" - If you have a known prefix, include it with --prefix to help bootstrap (script will use prefix across omlets).")
    print(" - If you'd like, paste a small excerpt of your dump here and I can run the script logic on it and try to recover.")

if __name__ == "__main__":
    main()
