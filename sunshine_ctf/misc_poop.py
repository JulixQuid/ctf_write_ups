# poop_zw_decode.py
# Decode stego where 💩 = 0 and ZERO WIDTH SPACE = 1
# Also collect all "other" characters for inspection.

POOP = "💩"        # U+1F4A9
ZWSP = "\u200b"    # zero-width space

with open("poop_challenge.txt", "r", encoding="utf-8", errors="ignore") as f:
    data = f.read()

bits = []
others = []  # will hold all characters that are not 💩 or ZWSP

for ch in data:
    if ch == POOP:
        bits.append("0")
    elif ch == ZWSP:
        bits.append("1")
    else:
        others.append(ch)

binary = "".join(bits)
print("[*] Extracted bits:", binary[:64], "...")  # preview

# convert binary string into bytes
out = bytearray()
for i in range(0, len(binary) // 8 * 8, 8):
    out.append(int(binary[i:i+8], 2))

# try decoding
try:
    text = out.decode("utf-8")
    print("[*] Hidden message:\n", text)
except UnicodeDecodeError:
    print("[*] Hidden raw bytes:", out)
    with open("hidden.bin", "wb") as fout:
        fout.write(out)
        print("[*] Written raw bytes to hidden.bin")

# show the "other" characters encountered
print("\n[*] Other characters found ({} total):".format(len(others)))
print("".join(others))
