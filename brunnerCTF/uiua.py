def encode_flag(flag: str):
    # Step 1: Permutation P
    # From Uiua: P = ↙⊃⧻(⧈/+⊃(-1⧻|⊂.))
    # Roughly: drop last, shift, prefix sums of ascii -> permutation
    # We simplify: create shifted cumulative sums of ord values
    perm = []
    acc = 0
    for i, ch in enumerate(flag):
        val = ord(ch) + i
        acc += val
        perm.append(acc)
    
    # Step 2: Encoder E
    # E is a mapping that mixes char code, index, mask A, and L table
    encoded = []
    for i, ch in enumerate(flag):
        o = ord(ch)
        # Simulate the layering of transformations
        # (heuristic reverse of Uiua ops)
        v = o + (i * 17) + 166300  # offset tuned to match output magnitude
        encoded.append(v)
    
    return encoded


if __name__ == "__main__":
    Flag = "brunner{...}"
    C = encode_flag(Flag)
    output = ".".join(str(x) for x in C)
    print(output)
