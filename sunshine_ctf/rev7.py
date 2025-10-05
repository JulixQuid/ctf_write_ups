#!/usr/bin/env python3
"""
pluto_decrypt_try_rc4.py
Usage:
    python3 pluto_decrypt_try_rc4.py capture.pcap

Requires: scapy
    pip install scapy

This script:
- finds TCP payloads,
- looks for packets with an 8-byte header: [uVar1 (4 bytes)][len (4 bytes)] followed by payload,
- attempts RC4-like decryption assuming the key is derived from uVar1 in several common encodings.
"""

import sys
from scapy.all import rdpcap, TCP, Raw, IP
from collections import defaultdict

# ---------- RC4 implementation ----------
def rc4_ksa(key: bytes):
    # key: bytes
    S = list(range(256))
    j = 0
    keylen = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) & 0xff
        S[i], S[j] = S[j], S[i]
    # store indices as bytes after S to mimic pvVar2[256], pvVar2[257] if needed
    return S, 0, 0

def rc4_prga(S, i=0, j=0):
    # generator yielding keystream bytes, returns generator object
    while True:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xff]
        yield K

def rc4_decrypt_with_key(key: bytes, data: bytes) -> bytes:
    S, i, j = rc4_ksa(list(key))
    ks = rc4_prga(S, i, j)
    return bytes([b ^ next(ks) for b in data])

# ---------- PCAP stream assembly (simple concatenation per 4-tuple direction) ----------
def key_for_pkt(pkt):
    return (pkt[IP].src, pkt[TCP].sport, pkt[IP].dst, pkt[TCP].dport)

def assemble_streams(packets):
    streams = defaultdict(bytearray)
    for pkt in packets:
        if IP not in pkt or TCP not in pkt:
            continue
        if not pkt.haslayer(Raw):
            continue
        payload = bytes(pkt[Raw].load)
        k = key_for_pkt(pkt)
        streams[k] += payload
    return streams

# ---------- Parse packets with 8-byte header ----------
def find_packets_in_stream(buf: bytes):
    """
    Yield tuples (offset, uVar1 (int), payload_bytes)
    The format we're looking for: [uVar1:4][payload_len:4][payload...]
    We will scan the stream for plausible headers.
    """
    i = 0
    found = []
    while i + 8 <= len(buf):
        # read 4-byte seed and 4-byte len (little endian)
        uVar1_le = int.from_bytes(buf[i:i+4], 'little')
        plen_le = int.from_bytes(buf[i+4:i+8], 'little')
        # quick sanity checks: plen not crazy
        if 0 <= plen_le <= 10000 and i + 8 + plen_le <= len(buf):
            payload = bytes(buf[i+8:i+8+plen_le])
            found.append((i, uVar1_le, plen_le, payload, 'le'))
            i = i + 8 + plen_le
            continue
        # try big endian
        uVar1_be = int.from_bytes(buf[i:i+4], 'big')
        plen_be = int.from_bytes(buf[i+4:i+8], 'big')
        if 0 <= plen_be <= 10000 and i + 8 + plen_be <= len(buf):
            payload = bytes(buf[i+8:i+8+plen_be])
            found.append((i, uVar1_be, plen_be, payload, 'be'))
            i = i + 8 + plen_be
            continue
        # otherwise advance by 1
        i += 1
    return found

# ---------- Try a handful of key encodings derived from uVar1 ----------
def candidate_keys_from_uvar1(uvar1: int):
    b_le = uvar1.to_bytes(4, 'little')
    b_be = uvar1.to_bytes(4, 'big')
    # common expansions: repeat 4 bytes to 16, 32; ascii hex; ascii decimal
    cand = []
    cand.append(b_le)
    cand.append(b_be)
    cand.append(b_le * 4)   # 16 bytes
    cand.append(b_be * 4)
    cand.append(uvar1.to_bytes(4,'little').hex().encode())  # ascii hex as key
    cand.append(str(uvar1).encode())                        # ascii decimal
    # also try zero-padded / truncated to 8
    cand.append((b_le * 2)[:8])
    cand.append((b_be * 2)[:8])
    # unique them
    seen = set()
    out = []
    for k in cand:
        if k in seen: continue
        seen.add(k)
        out.append(k)
    return out

def printable_ratio(b: bytes):
    if not b:
        return 0.0
    cnt = sum(1 for x in b if 32 <= x <= 126 or x in (9,10,13))
    return cnt / len(b)

# ---------- Main ----------
def main(pcap_path):
    pkts = rdpcap(pcap_path)
    streams = assemble_streams(pkts)
    total = 0
    for k, buf in streams.items():
        hits = find_packets_in_stream(buf)
        if not hits:
            continue
        print(f"\n--- Stream {k[0]}:{k[1]} -> {k[2]}:{k[3]} ---")
        for off, uvar1, plen, payload, endian in hits:
            print(f"\nFound candidate at offset {off}: uVar1={uvar1} (endian={endian}), plen={plen}")
            keys = candidate_keys_from_uvar1(uvar1)
            best = []
            for key in keys:
                dec = rc4_decrypt_with_key(key, payload)
                ratio = printable_ratio(dec)
                # store some info
                best.append((ratio, key, dec))
            # sort by printable ratio desc
            best.sort(reverse=True, key=lambda x: x[0])
            # show top 5 attempts
            for idx, (ratio, key, dec) in enumerate(best[:5], start=1):
                key_repr = key if len(key) <= 16 else key[:16] + b'...'
                try:
                    text = dec.decode('utf-8')
                except:
                    text = None
                print(f"Attempt {idx}: printable={ratio:.2f}, key(len={len(key)}): {key_repr!r}")
                if text is not None and len(text) > 0 and ratio > 0.3:
                    # likely human readable
                    print("DECRYPTED (utf-8):")
                    print(text)
                else:
                    # print first 200 bytes repr
                    print("DECRYPTED (hex or partial):", dec[:200].hex())
            total += 1
    if total == 0:
        print("No candidate packets found in streams.")
    else:
        print(f"\nExamined {total} candidate packet(s).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pluto_decrypt_try_rc4.py capture.pcap")
        sys.exit(1)
    main(sys.argv[1])
