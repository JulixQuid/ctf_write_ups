#!/usr/bin/env python3
# inverse_flag.py
# Usage: python3 inverse_flag.py flag.txt

from pathlib import Path

def invert_expand(data: bytes) -> bytes:
    """Inverse of expand(). data length must be even."""
    n = len(data) // 2
    out = bytearray(n)
    bVar1 = False
    local_1d = 0x69
    for i in range(n):
        a = data[2*i]
        b = data[2*i+1]
        if not bVar1:
            # forward: out0=(low(x))|(local_1d<<4), out1=(high(x))|(local_1d>>4)
            low = a & 0x0F
            high = b & 0xF0
            x = low | high
        else:
            # forward: out0=(high(x))|(local_1d>>4), out1=(low(x))|(local_1d<<4)
            high = a & 0xF0
            low = b & 0x0F
            x = low | high
        out[i] = x
        local_1d = (local_1d * 0x0B) & 0xFF
        bVar1 = not bVar1
    return bytes(out)

def invert_flipBits(data: bytes) -> bytes:
    """Inverse of flipBits()."""
    out = bytearray(len(data))
    bVar1 = False
    local_11 = 0x69
    for i, val in enumerate(data):
        if not bVar1:
            out[i] = (~val) & 0xFF
        else:
            out[i] = val ^ local_11
            local_11 = (local_11 + 0x20) & 0xFF
        bVar1 = not bVar1
    return bytes(out)

def main(path):
    data = Path(path).read_bytes()
    # invert expand three times
    d1 = invert_expand(data)
    d2 = invert_expand(d1)
    d3 = invert_expand(d2)
    # invert flipBits
    original = invert_flipBits(d3)
    Path("palatinepackflag_recovered.txt").write_bytes(original)
    print("Recovered file written to palatinepackflag_recovered.txt")
    try:
        print("Preview:", original.decode(errors="replace"))
    except:
        pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 inverse_flag.py flag.txt")
    else:
        main(sys.argv[1])
