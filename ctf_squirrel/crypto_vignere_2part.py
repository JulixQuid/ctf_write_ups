from collections import defaultdict

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenère cipher using provided key"""
    decrypted = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            shift = ord(key[i % key_len].lower()) - ord('a')
            decrypted_char = chr(((ord(c.lower()) - ord('a') - shift) % 26 + ord('a')))
            decrypted.append(decrypted_char)
        else:
            decrypted.append(c)
    return ''.join(decrypted)

def analyze_and_decrypt(filename):
    with open(filename, 'r') as f:
        flags = [line.strip() for line in f.readlines() if line.strip()]
    
    if not flags:
        print("No flags found in the file!")
        return
    
    max_length = max(len(flag) for flag in flags)
    position_counts = [defaultdict(int) for _ in range(max_length)]
    
    # Count letter frequencies at each position
    for flag in flags:
        for i, char in enumerate(flag):
            position_counts[i][char] += 1
    
    # Get most frequent letter at each position
    most_frequent = []
    for i in range(max_length):
        if position_counts[i]:
            most_frequent_char = max(position_counts[i].items(), key=lambda x: x[1])[0]
            most_frequent.append(most_frequent_char)
    
    encrypted_pattern = ''.join(most_frequent)
    print(f"Most frequent encrypted pattern: {encrypted_pattern}")
    
    # Attempt decryption using 'r' as reference
    decrypted_key = []
    for c in encrypted_pattern:
        if c.isalpha():
            # Calculate key character that would map 'r' to this ciphertext character
            key_char = chr((ord(c.lower()) - ord('r')) % 26 + ord('a'))
            decrypted_key.append(key_char)
        else:
            decrypted_key.append('?')
    
    potential_key = ''.join(decrypted_key)
    print(f"\nPotential Vigenère key: {potential_key}")
    
    # Try decrypting the pattern with this key
    decrypted = vigenere_decrypt(encrypted_pattern, potential_key)
    print(f"\nDecrypted pattern: {decrypted}")
    
    # Try decrypting all flags with this key
    print("\nSample decrypted flags:")
    for flag in flags[:5]:  # Show first 5 as example
        print(f"{flag} -> {vigenere_decrypt(flag, potential_key)}")

if __name__ == "__main__":
    analyze_and_decrypt('collected_flags.txt')