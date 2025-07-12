import base64

def decrypt():
    encrypted = "np2Z3p2c3s6YmZ3ezs2ZmM/Tnc7NmJmdz5yYm96cz8+Ym53Z3w=="
    decoded = base64.b64decode(encrypted)
    flag_part = bytes([c ^ 0xAA for c in decoded]).decode()
    return f"grodno{{{flag_part}}}"

print(decrypt())