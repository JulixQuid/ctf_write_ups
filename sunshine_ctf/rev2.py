#!/usr/bin/env python3
# decrypt_enc.py
# Reads enc.txt, subtracts 1 from each byte, writes dec.txt

import sys
from pathlib import Path

in_path = Path("enc.txt")
out_path = Path("dec.txt")

if not in_path.exists():
    print(f"Input file {in_path} not found.", file=sys.stderr)
    sys.exit(1)

data = in_path.read_bytes()
# subtract 1 from each byte (mod 256)
dec = bytes((b - 1) & 0xFF for b in data)
out_path.write_bytes(dec)
print(f"Wrote decrypted output to {out_path}")
