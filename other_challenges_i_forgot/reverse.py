def decrypt_message(input_str):
    # Encrypted message (hardcoded in the C code)
    encrypted_message = "IUC|t2nqm4`gm5h`5s2uin4u2d~"
    
    # Decrypt the message by shifting each character by -1
    decrypted_message = ''.join(chr(ord(char) - 1) for char in encrypted_message)
    
    # Compare the decrypted message with the input string
    if input_str == decrypted_message:
        print("The Dragon's Heart is hidden beneath the Eternal Flame in Eldoria.")
    else:
        print(decrypted_message)

# Example usage
input_str = "HTB{s1lpl3_3ncrypt10n_1s_fun}"  # Replace with the actual input
decrypt_message(input_str)


 #83.136.248.90:48232/index.php
 {window.location.hostname}@${window.location.port}\\3fe1690d955e8fd2a0b282501570e1f4\\resumes\\
83.136.248.90@48232/3fe1690d955e8fd2a0b282501570e1f4/resumes/