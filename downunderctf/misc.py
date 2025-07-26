import binascii

# All the hex-encoded ciphertexts from the output
ciphertexts = [
    "f3c9202e92ad822d2370f86fe79b4ad0ec27d69ddeb95fc77e6ba7dfa987054137632111ba2901747b831b118444286d280ab8ad2cc701d3a40706f6da7e079b4c53931f3949fdaec7c0a18d318704fd51610080ec553d57f21ae8506584efe46e8a16078b4f71f3d41eac2076bd4d8dd32d7ad93d682c6152b885a5db05061a17f0884a2ef037e09cdae260f5ca51e12b7e91f9a0134351e31ab7270f8a8b4f18986d93d277691905f84149c8f72eeb4c9fbab4281721a8dba241e8e99b5f3aef8a1fe5777bf03416e4c1b78cecfea79d76df95768110e556b4f1a9f8570aa48d2d6173110a4212114cdd1522483c0ee9b84696a796766feb29875899488533e2b5763287364709f279e41b7f32f408093cdf0abcf3344f96d35401215d32736beb5b4a2943c4ebe60e43dce10aafd5a3f61202bc10c4fb930a5dedc8e447280483d20e1c85db4469a6c69200613641a1c8794b6ef8d227cdfb009f68d37e7519c6e08dab661368b36d5acfb22c9b942b05703544ef8ba21651c2855592d62646ca1253fdcaaf0fa18c001e74934fc78dceefdc95987835cf2188eddac55c6856bba83fd2a0f75076584fa599abd737b71c041cd94eb6f481e08cec201d6764e49ae8f68a2b53dee888bdcaf25b6d149c6ac71c3fbeeba30ce06489adcf532abba9bd023cf8bed44c6d4a972fa9033d86",
    "f3df250eb1be98371946e47ff98f57ddec2ada99c6b465f7515ab5dea19a2e463769256ff5037d27d725c2d4a70daa249ef247b8a7346f04238a246817e649546c5b8e1f05cc153cafde3745fa154634d5abaa67bbfff0e191c6349917007866071e22809a719e8f72e9656fe2198605b3af66938553829b0065f1691d2565fdb789761f85b878158fc538d813cc3e4f3e90ec97a5bb93301918a556d0c45d00e9bd91285e660ea7087d6d38f229e31d4d9709d25a2a4d9a8565ae37c9b4881e75658ed1f00b71852219ddf3cdd4f10445dbd9cb9aa0daf1a3910820e727c0f4ff9f68c927ffc23f1b4d376f5825ff72e515314b83fee3a88f",
    "f3c81725baaf9f293642e479ec9559deec14d386f5a753e5244eee5e7ed74f7881250a52dd1293f4853fc70caf6cbf33353464c435e54b732cb0fd27672ebdb293755843f938371b7b5d3827c335ecca5162d6c28a4a9c6551a97ceeaa8cfe9ed07bbe6e78fe0f81994732b9ae2d2b3ad1c2318c294f6be1509a7f6cc052cfa47209929e79e196b42187b5d3d176572a0a949b3a65ec93c2ec7bba304f0f189a905679963b7a",
    "f3da06148ba2862a194afc45d69d5ff6ec2e95e56a6d4675e7a53eb026b8e308177419879d95b665538f9519c4d1d8b3f7c6565701fdfbcf43969cc645928f37cca525501616f353baa33295000799e224572600b6d3ca2c907546f549ef58b19d8fa501ae6ddf80aaef89a517e099cfc1a650138fb9f8580c12d5fc79",
    "f3e70b03a08982312a58fe7fd69032d37396818d3be288839c37b0ed2484c3072cc5370a3d979757977fbab0a2e316cdb718f530d70ec7ccc776f65ae7cf3787a6002eba077a6ecb7dcdf2a30c5440fc258662c192dd4deee868b48f59ec7c824b6794ea",
    "f3e80d13a4a293241943cf73a3c680975a01bd0b38684e604c86ac94296193fce8a2e5a5499a8fcfd7f3a47504996535205ab4c6eaaab76221c1302f151c529d0941d9beb89b313a8ed4f295f51806a75dbf43",
    "f3f41116bba29724215d9a8231dba19e53dc02eb488a30d7e15b3ae96ba7b1bbe82a2d1601d63b8413174b56c35d2df7959d4fe5cf5e19fde97b7f7c43f1df75e1c7fd1ff2b5ec"
]

# Convert all to bytes
ciphers = [binascii.unhexlify(ct) for ct in ciphertexts]

# We know flag[1] == 'U', so we can find keystream[1]
# From first cipher (stride 1), cipher[1] = flag[1] ^ keystream[1]
keystream_byte_1 = ciphers[0][1] ^ ord('U')

# Now we can find all keystream bytes at positions 1 + 7k since these appear in the last cipher (stride 7)
# Then use these to find more flag bytes from other ciphers, and so on

# Initialize flag with known length (at least as long as the first cipher)
flag_len = len(ciphers[0])
flag = bytearray(flag_len)

# We'll collect known keystream bytes
keystream = bytearray(flag_len)

# First set the known keystream byte
keystream[1] = keystream_byte_1

# Now we can recover flag bytes from the other ciphers where we know keystream bytes
# This is an iterative process where each new known flag byte helps us discover more keystream bytes

# For each stride (1 through 7)
for stride in range(1, 8):
    cipher = ciphers[stride-1]  # 0-based index
    for i in range(0, len(cipher)):
        pos = i * stride  # Position in original flag
        if pos >= flag_len:
            continue
        
        # If we know the keystream at this position, we can get the flag byte
        if keystream[pos] != 0:
            flag[pos] = cipher[i] ^ keystream[pos]
        # If we know the flag byte, we can get the keystream
        elif flag[pos] != 0:
            keystream[pos] = cipher[i] ^ flag[pos]

# The flag is likely the part before the random padding
# From the assert, we know the flag starts with ?U (second char is U)
# Let's look for the end of meaningful text
for i in range(flag_len):
    if flag[i] == 0:
        # Try to find where the flag ends (before padding)
        possible_flag = flag[:i]
        if all(32 <= b <= 126 or b == 10 or b == 13 for b in possible_flag):
            print("Possible flag:", possible_flag.decode('latin-1'))
            break

# Alternative approach: since we know the flag format is likely CTF{...}, we can look for that
# Let's assume the first few characters are CTF{ and use that to get more keystream bytes
known_prefix = b"DUCTF{"
for i in range(min(len(known_prefix), len(ciphers[0]))):
    keystream[i] = ciphers[0][i] ^ known_prefix[i]

# Now re-run the reconstruction with this additional knowledge
for stride in range(1, 8):
    cipher = ciphers[stride-1]
    for i in range(0, len(cipher)):
        pos = i * stride
        if pos >= flag_len:
            continue
        
        if keystream[pos] != 0:
            flag[pos] = cipher[i] ^ keystream[pos]
        elif flag[pos] != 0:
            keystream[pos] = cipher[i] ^ flag[pos]

# Print the flag up to the first null byte
try:
    null_pos = flag.index(0)
    final_flag = flag[:null_pos]
except ValueError:
    final_flag = flag

print("Final flag:", final_flag.decode('latin-1'))