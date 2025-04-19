from collections import Counter
import struct
from matplotlib import pyplot as plt
import numpy as np

def load_samples(filename):
    with open(filename, 'r') as f:
        return np.array([float(line.strip()) for line in f])

node_samples = load_samples('../innov8/innov8_excav8/node_output.txt')
d8_samples = load_samples('../innov8/innov8_excav8//d8_output.txt')
# --- Step 2: Digit Frequency Analysis ---
def get_digit_counts(samples):
    digits = []
    for num in samples:
        decimal_part = f"{num:.20f}".split(".")[1]  # Extract 20 decimal digits
        digits.extend(list(decimal_part))
    return Counter(digits)

node_counts = get_digit_counts(node_samples)
d8_counts = get_digit_counts(d8_samples)

# --- Step 3: Calculate Proportions ---
def calculate_proportions(counter, total_digits):
    return {digit: counter.get(digit, 0) / total_digits for digit in '0123456789'}

total_digits = len(node_samples) * 20  # 20 digits per number
node_props = calculate_proportions(node_counts, total_digits)
d8_props = calculate_proportions(d8_counts, total_digits)

#print("Node.js digit proportions:", node_props)
#print("d8 digit proportions:", d8_props)

# --- Step 4: Visualize ---
def plot_digit_proportions(props, title):
    digits = sorted(props.keys())
    proportions = [props[d] for d in digits]
    plt.bar(digits, proportions, alpha=0.7)
    plt.axhline(y=0.1, color='red', linestyle='--', label="Ideal (10%)")
    plt.title(title)
    plt.xlabel("Digit")
    plt.ylabel("Proportion")
    plt.legend()
    plt.show()

plot_digit_proportions(node_props, "Node.js Digit Proportions")
plot_digit_proportions(d8_props, "d8 Digit Proportions")
print("node: ", min(node_props.values()),max(node_props.values()), np.std(list(node_props.values())))
print("d8  : ", min(d8_props.values()),max(d8_props.values()), np.std(list(d8_props.values())))

"""
# Example: Reconstruct secret from the original Python script's output
output = [...]  # Replace with the `output` array from the original script
if len(output) > 0:
    secret_bits = ''.join([classify_chunk(output[i:i+24]) for i in range(0, len(output), 24)])
    secret = ''.join(chr(int(secret_bits[i:i+8], 2)) for i in range(0, len(secret_bits), 8))
    print("\nRecovered secret:", secret)
else:
    print("\nNo output data provided. Replace `output` with the original script's array.")"
"""