from Crypto.Util.number import bytes_to_long, long_to_bytes
import hashlib

def encrypt(m, n, r=1):
    n2 = n * n
    g = n + 1
    c = pow(g, m, n2) * pow(r, n, n2) % n2
    return c

def main():
    n = int(input("Enter n: "))
    username = input("Enter non-admin username: ").strip()
    token_hex = input("Enter token for non-admin user: ").strip()
    
    token = bytes.fromhex(token_hex)
    msg_part, _, mac_part = token.partition(b'|')
    user_start = msg_part.find(b'user=') + 5
    non_admin_msg = msg_part
    non_admin_username = msg_part[user_start:]
    
    if non_admin_username == b'admin':
        print("Cannot use admin user")
        return

    admin_msg = b'user=admin'
    print(f"Non-admin message: {non_admin_msg}")
    print(f"Admin message: {admin_msg}")
    
    non_admin_mac = bytes_to_long(mac_part)
    
    non_admin_hash = hashlib.sha256(non_admin_msg).digest()
    admin_hash = hashlib.sha256(admin_msg).digest()
    
    delta = (bytes_to_long(admin_hash) - bytes_to_long(non_admin_hash)) % (2**256)
    
    adjustment = encrypt(delta, n)
    new_mac = (non_admin_mac * adjustment) % (n * n)
    
    new_token = admin_msg + b'|' + long_to_bytes(new_mac)
    print("Forged token:", new_token.hex())

if __name__ == "__main__":
    main()