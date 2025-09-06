import numpy as np
import itertools

def rotate_left(data):
    upper = data << 1
    lower = np.roll(data, -1) >> 7
    return (upper | lower) & 0xFF

def rotate_right(data):
    lower = data >> 1
    upper = (np.roll(data, 1) << 7) & 0xFF
    return (upper | lower) & 0xFF

def rule(data):
    left = rotate_left(data)
    right = rotate_right(data)
    res = ~((left & right & data) |
            (~left & ~right & ~data) |
            (~left & right & ~data))
    return res & 0xFF

def expand_seed(seed, length=1200):
    """Repeat the short seed to fill the array"""
    return np.array((seed * (length // len(seed) + 1))[:length], dtype=np.uint8)

def evolve(seed, rounds):
    data = expand_seed(seed)
    for _ in range(rounds):
        data = rule(data)
        if not np.any(data):
            return None  # all zeros
    return tuple(data)

def brute_force(max_val=4, seed_len=4, test_rounds=(100, 200, 300)):
    """Try all seeds and check if they stabilize to same result across test_rounds"""
    good_seeds = []
    for seed in itertools.product(range(max_val), repeat=seed_len):
        results = []
        for r in test_rounds:
            state = evolve(seed, r)
            if state is None:
                break
            results.append(state)
        if len(results) == len(test_rounds) and all(s == results[0] for s in results):
            print(f"[+] Stable seed found: {seed}")
            good_seeds.append(seed)
    return good_seeds


if __name__ == "__main__":
    seeds = brute_force(max_val=8, seed_len=4, test_rounds=(200, 500, 1000))
    print("\nStable seeds:", seeds)
