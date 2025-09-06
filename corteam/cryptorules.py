import socket
import json
import subprocess
import numpy as np

HOST = "ctfi.ng"
PORT = 31126

def rotate_left(data):
    upper = data << 1
    lower = np.roll(data, -1) >> 7
    return upper | lower

def rotate_right(data):
    lower = data >> 1
    upper = np.roll(data, 1) << 7
    return upper | lower

def rule(data):
    left = rotate_left(data)
    right = rotate_right(data)
    return ~((left & right & data) | (~left & ~right & ~data) | (~left & right & ~data))

def recvuntil(s, marker):
    buf = b""
    while not buf.endswith(marker):
        buf += s.recv(1)
    return buf

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    # Step 1: Get POW challenge
    banner = s.recv(4096).decode()
    print("[*] Banner:")
    print(banner)

    if "proof of work" in banner:
        challenge = banner.split("\n")[-2].strip()
        print("[*] POW challenge:", challenge)

        # Run the solver locally
        cmd = f"challenge"
        print("[*] Running POW solver...")
        sol = subprocess.check_output(challenge, shell=True).decode().strip()
        print("[*] POW solution:", sol)
        s.send((sol + "\n").encode())

    # Step 2: Prepare pattern (candidate fixed point)
    pattern = [85, 170] * 600   # length 1200 >= 1024
    arr_str = json.dumps(pattern)

    print("[*] Sending initial array (first 32 bytes):", pattern[:32])
    s.send((arr_str + "\n").encode())

    # Step 3: Guess = same pattern
    print("[*] Sending guess array...")
    s.send((arr_str + "\n").encode())

    # Step 4: Read response
    resp = s.recv(8192).decode()
    print("[*] Response:")
    print(resp)

    # Debug: simulate locally a few steps
    data = np.array(pattern, dtype=np.uint8)
    for i in range(3):  # show 3 rounds locally
        data = rule(data)
        print(f"[*] After round {i+1}, first 32 bytes:", data[:32])

if __name__ == "__main__":
    main()
