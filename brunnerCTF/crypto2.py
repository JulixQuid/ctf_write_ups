import itertools

class SDES:
    def __init__(self, key):
        if len(key) != 10 or not all(bit in '01' for bit in key):
            raise ValueError("Key must be a 10-bit binary string")
        self.key = key
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
        self.S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

    def permute(self, bits, permutation):
        return ''.join(bits[i-1] for i in permutation)

    def left_shift(self, bits, n):
        return bits[n:] + bits[:n]

    def generate_keys(self):
        p10_key = self.permute(self.key, self.P10)
        left = self.left_shift(p10_key[:5], 1)
        right = self.left_shift(p10_key[5:], 1)
        k1 = self.permute(left + right, self.P8)
        left = self.left_shift(left, 2)
        right = self.left_shift(right, 2)
        k2 = self.permute(left + right, self.P8)
        return k1, k2

    def xor(self, a, b):
        return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

    def s_box_substitution(self, bits, s_box):
        row = int(bits[0] + bits[3], 2)
        col = int(bits[1] + bits[2], 2)
        return format(s_box[row][col], '02b')

    def f_function(self, right, key):
        expanded = self.permute(right, self.EP)
        xor_result = self.xor(expanded, key)
        left_half = xor_result[:4]
        right_half = xor_result[4:]
        s0_out = self.s_box_substitution(left_half, self.S0)
        s1_out = self.s_box_substitution(right_half, self.S1)
        return self.permute(s0_out + s1_out, self.P4)

    def decrypt_block(self, ciphertext):
        if len(ciphertext) != 8 or not all(bit in '01' for bit in ciphertext):
            raise ValueError("Ciphertext must be an 8-bit binary string")
        k1, k2 = self.generate_keys()
        ip_result = self.permute(ciphertext, self.IP)
        left = ip_result[:4]
        right = ip_result[4:]
        f_result = self.f_function(right, k2)
        new_right = self.xor(left, f_result)
        f_result = self.f_function(new_right, k1)
        new_left = self.xor(right, f_result)
        combined = new_left + new_right
        plaintext = self.permute(combined, self.IP_inv)
        return plaintext

    def decrypt(self, ciphertext):
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext length must be a multiple of 8")
        plaintext_blocks = []
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            decrypted_block = self.decrypt_block(block)
            plaintext_blocks.append(decrypted_block)
        return ''.join(plaintext_blocks)

def hex_to_binary(hex_string):
    binary_string = ""
    for hex_char in hex_string:
        byte = format(int(hex_char, 16), '04b')
        binary_string += byte
    return binary_string

def binary_to_text(binary_string):
    text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            char_code = int(byte, 2)
            if 32 <= char_code <= 126:
                text += chr(char_code)
            else:
                text += '?'
    return text

def brute_force_sdes(hex_ciphertext, target_word="brunner"):
    ciphertext_binary = hex_to_binary(hex_ciphertext)
    possible_keys = []
    total_keys = 2**10
    
    print(f"Brute forcing {total_keys} possible keys...")
    print(f"Ciphertext (hex): {hex_ciphertext}")
    print(f"Ciphertext (binary): {ciphertext_binary}")
    
    for key_int in range(total_keys):
        key_bin = format(key_int, '010b')
        try:
            sdes = SDES(key_bin)
            decrypted_binary = sdes.decrypt(ciphertext_binary)
            decrypted_text = binary_to_text(decrypted_binary)
            
            if target_word.lower() in decrypted_text.lower():
                possible_keys.append((key_bin, decrypted_text))
                print(f"Found potential key: {key_bin} -> '{decrypted_text}'")
                
        except:
            continue
    
    return possible_keys

if __name__ == "__main__":
    hex_ciphertext = input("Enter ciphertext (hex): ").strip()
    possible_solutions = brute_force_sdes(hex_ciphertext)
    
    print(f"\nFound {len(possible_solutions)} possible solutions:")
    for key, text in possible_solutions:
        print(f"Key: {key} -> Text: '{text}'")