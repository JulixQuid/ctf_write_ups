from Registry import Registry
import sys
# Load hive
hive = Registry.Registry("/home/julixquid/Downloads/Users/rumi/NTUSER.DAT")

# List top-level keys
print("Top-level keys:")
for key in hive.root().subkeys():
    print(" -", key.name())

def rec(key, depth=0):
    print( "   " * depth + key.path())

    for subkey in key.subkeys():
        rec(subkey, depth + 1)

rec(hive.root())

try:
    key = hive.open("Software\\TightVNC")
    for value in key.values():
        print("XXX ",value.name(), value.value_type_str(), value.value())
except Exception as e:
    print("TightVNC key not found or empty:", e)

if True:
    key = hive.open("Software\TightVNC\Server")


for value in [v for v in key.values() \
                   if v.value_type() == Registry.RegSZ or \
                      v.value_type() == Registry.RegExpandSZ]:
    print("%s: %s" % (value.name(), value.value()))


from Crypto.Cipher import DES

# Encrypted password from registry
enc = b'~\x9b1\x12H\xb7\xc8\xa8'

# Fixed TightVNC DES key
key = bytes([0x17, 0x52, 0x6a, 0x2e, 0x9c, 0xe2, 0x55, 0x8c])

cipher = DES.new(key, DES.MODE_ECB)
dec = cipher.decrypt(enc)

# Strip null bytes and show different interpretations
print("Decrypted (raw bytes):", dec)
print("Decrypted (hex):", dec.hex())
print("Decrypted (latin-1):", dec.rstrip(b'\x00').decode("latin-1", errors="ignore"))
from Crypto.Cipher import DES

# The 8-byte blob you found
enc = b'~\x9b1\x12H\xb7\xc8\xa8'

# Fixed TightVNC key (hardcoded in the source of old versions)
TIGHTVNC_KEY = bytes([
    23, 82, 107, 6, 35, 78, 88, 7
])

cipher = DES.new(TIGHTVNC_KEY, DES.MODE_ECB)
dec = cipher.decrypt(enc)

# Strip nulls and print result
print("Decrypted:", dec.decode('latin-1').rstrip('\x00'))


from Crypto.Cipher import DES

# Encrypted blob you found
enc = b'~\x9b1\x12H\xb7\xc8\xa8'

# TightVNC’s static obfuscation key
obfKey = bytes([23, 82, 107, 6, 35, 78, 88, 7])

cipher = DES.new(obfKey, DES.MODE_ECB)
dec = cipher.decrypt(enc)

print("PPPassword:", dec.decode('latin-1').rstrip("\x00"))

echo -n 7e9b311248b7c8a8 | xxd -r -p | openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d -provider legacy -provider default | hexdump -Cv