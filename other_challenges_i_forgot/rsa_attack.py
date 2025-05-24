from pwn import *
import re
from Crypto.Util.number import inverse, GCD
from math import gcd

DEATH_CAUSES = [
    'a fever', 'dysentery', 'measles', 'cholera', 'typhoid',
    'exhaustion', 'a snakebite', 'a broken leg', 'a broken arm', 'drowning'
]

def extract_page(msg):
    match = re.search(r'turn to page (\d+)', msg)
    return int(match.group(1)) if match else None

def is_live(msg):
    return "you continue walking" in msg

def is_die(msg):
    return any(cause in msg for cause in DEATH_CAUSES)

def recover_m12(xn,e,n,cm):
    inv_xn_e = inverse(pow(xn,e,n),n)
    msg = ((cm * pow(xn,e,n)-1)* inv_xn_e)%n
    return msg
    #msg = (cm*pow(xn,e,n) - 1) * inv_xn_e

def recover_m1(x0, x1, e, n, c1):


    delta = (x0 - x1) % n                    # delta = (x0 - x1) mod n
    delta_e = pow(delta, e, n)               # delta^e mod n
    numerator = (c1 * delta_e - delta) % n   # c1 * delta^e - delta mod n
    inv_delta_e = inverse(delta_e, n)        # (delta^e)^{-1} mod n
    msg1 = (numerator * inv_delta_e) % n     # msg1 = numerator / delta^e
    return msg1
    
def solve_round(conn, round_num):
    print(f"\n=== Round {round_num} ===")
    
    # Receive n, e, x0, x1
    conn.recvuntil(b'n: ')
    n = int(conn.recvline().strip())
    print(f"[+] n = {n}")
    
    conn.recvuntil(b'e: ')
    e = int(conn.recvline().strip())
    print(f"[+] e = {e}")
    
    conn.recvuntil(b'x0: ')
    x0 = int(conn.recvline().strip())
    print(f"[+] x0 = {x0}")
    
    conn.recvuntil(b'x1: ')
    x1 = int(conn.recvline().strip())
    print(f"[+] x1 = {x1}")

    # Set v = max(x0, x1)
    v = (x0+x1)%n 
    print(f"[+] v = {v}")
    conn.sendlineafter(b'v: ', str(v).encode())
    
    # Get c0, c1
    conn.recvuntil(b'c0: ')
    c0 = int(conn.recvline().strip())
    print(f"[+] c0 = {c0}")
    
    conn.recvuntil(b'c1: ')
    c1 = int(conn.recvline().strip())
    print(f"[+] c1 = {c1}")
    
    m0 = recover_m12(x1, e, n, c0)
    m1 = recover_m12(x0, e, n, c1)
    m0 = m0.to_bytes(max((m0.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
    m1 = m1.to_bytes(max((m1.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
    print(f"[+] m0 = {m0}")
    print(f"[+] m1 = {m1}")
    if is_live(m1):
        page = extract_page(m1)
    else:
        page = extract_page(m0)
    """
    # Decode m0 or m1
    if v == x0:
        m0 = c0.to_bytes(max((c0.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
        print(f"[+] m0 = {m0}")
        if is_live(m0):
            page = extract_page(m0)
        elif is_die(m0):
            m1 = recover_m1(x0, x1, e, n, c1)
            if m1 is None:
                exit()
            m1 = m1.to_bytes(max((m1.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
            print(f"[+] m1 = {m1}")
            page = extract_page(m1)
    else:
        m1 = c1.to_bytes(max((c1.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
        print(f"[+] m1 = {m1}")
        if is_live(m1):
            page = extract_page(m1)
        elif is_die(m1):
            m0 = recover_m1(x1, x0, e, n, c0)
            if m0 is None:
                exit()
            m0 = m0.to_bytes(max((m0.bit_length() + 7) // 8, 1), 'big').decode(errors='replace')
            print(f"[+] m0 = {m0}")
            page = extract_page(m0)
    """
    if page is None:
        print("[!] Failed to extract page")
        exit()
    
    print(f"[+] Page = {page}")
    conn.sendlineafter(b'turn to page: ', str(page).encode())

def main():
    conn = remote('dicec.tf', 31001)  # Change to actual target
    print(conn.recvuntil(b'=== CHOOSE YOUR OWN ADVENTURE: Vorpal Sword Edition ===\n').decode())
    print(conn.recvuntil(b'you enter a cave.\n').decode())

    for i in range(64):
        solve_round(conn, i+1)

    print(conn.recvuntil(b'you find a chest containing ').decode())
    flag = conn.recvline().strip().decode()
    print(f"\n[+] FLAG: {flag}")
    conn.close()

if __name__ == '__main__':
    main()