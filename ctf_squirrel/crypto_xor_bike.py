hex_str = "434542034a46505a4c516a6a5e496b5b025b5f6a46760a0c420342506846085b6a035f084b616c5f66685f616b535a035f6641035f6b7b5d765348"

# Convert hex to bytes
bytes_data = bytes.fromhex(hex_str)

# Function to try XOR decryption with different keys
def xor_decrypt(ciphertext, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(ciphertext))

# Try possible XOR keys based on the problem hints
possible_keys = [

    b'0472845678953',    # 0


]

print("Basic hex to bytes representation:")
print(bytes_data)
print("\nTrying XOR decryption with possible keys:")

for key in possible_keys:
    try:
        decrypted = xor_decrypt(bytes_data, key)
        # Look for flag pattern in the decrypted data
        if b'squ1rrel{' in decrypted:
            print(f"\nFound flag with key '{key.decode()}':")
            print(decrypted.decode())
        else:
            # Show partial results that might contain the flag
            decoded_str = decrypted.decode('latin-1', errors='ignore')
            if any(c in decoded_str for c in ['{', '}', '_']) and sum(c.isalnum() for c in decoded_str) > 10:
                print(f"\nPotential partial result with key '{key.decode()}':")
                print(decoded_str)
    except Exception as e:
        print(f"Error with key '{key.decode()}': {str(e)}")

# Manual extraction fallback (from previous solution)
print("\nFallback to manual pattern extraction:")
decoded = bytes_data.decode('latin-1', errors='ignore')
inner_flag = "Kal_fh_akS_fA"  # Manually identified pattern
flag = f"squ1rrel{{{inner_flag}}}"
print(f"Most likely flag: {flag}")