def lfsr(state, mask):
    bit = state & 1
    state = state >> 1
    if bit:
        state ^= mask
    return state, bit

def generate_key(initial_state, mask, num_bits):
    state = initial_state
    key = []
    for _ in range(num_bits):
        state, bit = lfsr(state, mask)
        key.append(str(bit))
    return ''.join(key)

# Given parameters
initial_state = 0b1100101011110001
mask = 0b1011010000000001

# Generate 32 bits of the key
key = generate_key(initial_state, mask, 32)
print("Generated Key (32 bits):", key)