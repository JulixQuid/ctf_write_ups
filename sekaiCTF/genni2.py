def dream_multiply(x, y):
    x_str, y_str = str(x), str(y)
    if len(x_str) != len(y_str) + 1:
        return float('inf')
    digits = x_str[0]
    for a, b in zip(x_str[1:], y_str):
        digits += str(int(a) * int(b))
    return int(digits)

def evaluate(x, y):
    product = x * y
    dream = dream_multiply(x, y)
    difference = abs(product - dream)
    return difference, product, dream

# Current best
current_x, current_y = 25555764, 9596799
best_diff, best_prod, best_dream = evaluate(current_x, current_y)
print(f"Current best: x={current_x}, y={current_y}")
print(f"Difference: {best_diff}, Product: {best_prod}, Dream: {best_dream}")

# Brute-force search in neighborhood
search_range = 10000  # How many numbers to check around current values
min_diff = best_diff
found_better = False

print("\nSearching for better solutions...")
for dx in range(-search_range, search_range + 1):
    for dy in range(-search_range, search_range + 1):
        x = current_x + dx
        y = current_y + dy
        
        # Ensure valid 8 and 7 digit numbers
        if not (10**7 <= x < 10**8 and 10**6 <= y < 10**7):
            continue
        
        diff, prod, dream = evaluate(x, y)
        
        if diff < min_diff:
            min_diff = diff
            print(f"\nNew best: x={x}, y={y}")
            print(f"Difference: {diff} (improvement of {best_diff - diff})")
            print(f"Product: {prod}")
            print(f"Dream: {dream}")
            found_better = True
            
        if diff == 0:
            print("PERFECT SOLUTION FOUND!")
            exit()

if not found_better:
    print("\nNo better solutions found in the neighborhood.")
else:
    print("\nSearch complete. Better solution(s) found.")