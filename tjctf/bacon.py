# Reverse Baconian cipher from out.txt

# First, reverse the ASCII shift by adding 13 to each character
with open('out.txt') as f:
    shifted_text = f.read().strip()

# Reverse the ASCII shift
ciphertext = ''.join([chr(ord(i) + 13) for i in shifted_text])

# Baconian dictionary (reversed)
reverse_baconian = {
    '00000': 'a', '00001': 'b',
    '00010': 'c', '00011': 'd',
    '00100': 'e', '00101': 'f',
    '00110': 'g', '00111': 'h',
    '01000': 'i', '01001': 'k',
    '01010': 'l', '01011': 'm',
    '01100': 'n', '01101': 'o',
    '01110': 'p', '01111': 'q',
    '10000': 'r', '10001': 's',
    '10010': 't', '10011': 'u',
    '10100': 'w', '10101': 'x',
    '10110': 'y', '10111': 'z'
}

# Extract Baconian codes from the ciphertext
flag = ''
for i in range(0, len(ciphertext), 5):
    chunk = ciphertext[i:i+5]
    if len(chunk) < 5:
        break  # In case the text isn't a multiple of 5
    
    # Create binary code based on case
    binary_code = ''
    for char in chunk:
        if char.isupper():
            binary_code += '1'
        else:
            binary_code += '0'
    
    # Look up the letter
    flag += reverse_baconian.get(binary_code, '?')

print("Deciphered flag:", flag)