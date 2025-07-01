def rot47(s):
    return ''.join(
        chr(33 + ((ord(c) - 33 + 47) % 94)) 
        if '!' <= c <= '~' else c 
        for c in s
    )

def solve_password():
    # Decode the ROT47-encoded pool
    encoded_pool = "?o>`Wn0o0U0N?05o0ps}q0|mt`ne`us&400_pn0ss_mph_0`5"
    pool = list(rot47(encoded_pool))
    print(f"Decoded pool: {''.join(pool)}")

    # Initialize variables as in the JavaScript code
    i = 1337
    step = 1
    password = []

    # Simulate the password-checking logic
    while pool:
        # Compute j and the index in the pool
        j = ((i or 1) * 16807 + (step - 1)) % 2147483647
        idx = j % len(pool)
        
        # Append the character to the password and remove it from the pool
        password.append(pool[idx])
        pool.pop(idx)
        
        # Update i and step for the next iteration
        i = j
        step *= 2

    # The password is the sequence of characters extracted from the pool
    return ''.join(password)

if __name__ == "__main__":
    password = solve_password()
    print(f"Password: {password}")