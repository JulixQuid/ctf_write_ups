def check(input_string):
    key = [
        29, 231, 186, 121, 34, 225, 137, 22, 224, 209,
        63, 142, 249, 193, 157, 144, 124, 72, 5, 96,
        157, 221, 103, 68, 40, 45, 109, 136, 123, 173,
        37
    ]
    
    expected = [
        110, 150, 207, 72, 80, 147, 236, 122, 155, 186,
        15, 250, 149, 240, 243, 207, 21, 59, 90, 3,
        173, 237, 86, 27, 70, 28, 30, 188, 23, 153,
        88
    ]
    
    if len(input_string) != len(expected):
        return False
    
    result = []
    for i in range(len(input_string)):
        xor_result = ord(input_string[i]) ^ key[i]
        result.append(xor_result)
    
    print("Computed:", result)
    print("Expected:", expected)
    
    return result == expected


# Helper function to find the correct input string
def find_correct_input():
    key = [
        29, 231, 186, 121, 34, 225, 137, 22, 224, 209,
        63, 142, 249, 193, 157, 144, 124, 72, 5, 96,
        157, 221, 103, 68, 40, 45, 109, 136, 123, 173,
        37
    ]
    
    expected = [
        110, 150, 207, 72, 80, 147, 236, 122, 155, 186,
        15, 250, 149, 240, 243, 207, 21, 59, 90, 3,
        173, 237, 86, 27, 70, 28, 30, 188, 23, 153,
        88
    ]
    
    correct_chars = []
    for i in range(len(key)):
        correct_char = chr(expected[i] ^ key[i])
        correct_chars.append(correct_char)
    
    return ''.join(correct_chars)


# Example usage
if __name__ == "__main__":
    # Find the correct input that would make check() return True
    solution = find_correct_input()
    print(f"The correct input is: {solution}")
    
    # Test the check function
    print("Check result:", check(solution))  # Should print True