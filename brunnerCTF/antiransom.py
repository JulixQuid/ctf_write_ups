from pathlib import Path
from itertools import cycle

def recover_key(encrypted_file: Path, known_plaintext: bytes, offset: int = 0) -> bytes:
    """
    Recover the encryption key using known plaintext
    encrypted_file: Path to the .enc file
    known_plaintext: Bytes you know should be in the original file
    offset: Position where the known plaintext starts (default: 0)
    """
    with open(encrypted_file, "rb") as f:
        ciphertext = f.read()
    
    # Extract the ciphertext segment corresponding to known plaintext
    ciphertext_segment = ciphertext[offset:offset + len(known_plaintext)]
    
    # XOR ciphertext with known plaintext to get key bytes
    key_bytes = bytes(c ^ p for c, p in zip(ciphertext_segment, known_plaintext))
    
    return key_bytes

def decrypt_with_partial_key(file: Path, partial_key: bytes, key_length: int = 16) -> None:
    """
    Try to decrypt using a partially recovered key
    """
    with open(file, "rb") as f:
        ciphertext = f.read()
    
    # Create full key by repeating partial key
    full_key = (partial_key * (len(ciphertext) // len(partial_key) + 1))[:len(ciphertext)]
    
    plaintext = bytes(a ^ b for a, b in zip(ciphertext, full_key))
    
    original_filename = file.with_suffix('')
    with open(original_filename, "wb") as f:
        f.write(plaintext)
    
    print(f"Attempted decryption of {file.name}")

# Example usage
if __name__ == "__main__":
    encrypted_file = Path("/home/julixquid/Downloads/crypto_encrypted-and-desperate (2)/recipes/1f.png.enc")
    
    # Common file headers (try these first!)
    common_headers = {
        "PDF": b"%PDF-",
        "ZIP": b"PK\x03\x04",  # ZIP file header
        "PNG": b"\x89PNG\r\n\x1a\n",
        "JPEG": b"\xff\xd8\xff",
        "GIF": b"GIF89a",
        "Windows Executable": b"MZ",
        "UTF-8 BOM": b"\xef\xbb\xbf",
        "UTF-16 BOM": b"\xff\xfe",
        "Text file": b"# " or b"// " or b"<?xml" or b"<!DOCTYPE"
    }
    
    for file_type, header in common_headers.items():
        try:
            recovered_key = recover_key(encrypted_file, header)
            print(f"Possible {file_type} key: {recovered_key.hex()}")
            
            # Try decrypting with this key
            decrypt_with_partial_key(encrypted_file, recovered_key)
            print(f"Check if {encrypted_file.with_suffix('')} looks correct!")
            break
            
        except Exception as e:
            print(e)
            continue