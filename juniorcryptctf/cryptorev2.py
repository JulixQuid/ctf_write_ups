def reverse_puzzle(s: str, step: int) -> str:
    for _ in range(step):
        n = len(s)
        half = (n + 1) // 2
        first_half = s[:half]
        second_half = s[half:]
        s = ''.join([first_half[i] + second_half[i] for i in range(len(second_half))])
        if len(first_half) > len(second_half):
            s += first_half[-1]
    return s

def find_flag():
    target = '789603251257384214725442633'
    middle = reverse_puzzle(target, 5)
    flag = f"grodno{{{middle}}}"
    return flag

flag = find_flag()
print(flag)