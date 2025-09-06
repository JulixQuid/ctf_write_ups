# solve_lwe_small_alphabet.py
import ast, random, math
from pathlib import Path

P = 140_797  # prime modulus
E = [97_491, 14_061, 55_776]
D = {(a - b) % P for a in E for b in E}  # {0, 41715, 57367, 83430, 99082}

def inv_mod(a, p=P):
    return pow(a % p, p - 2, p)

def solve_linear_mod(M, y, p=P):
    """
    Gaussian elimination mod p.
    M: list[list[int]] size m x n (m>=n), y: list[int] size m
    Returns x (list[int] size n) or None if singular.
    """
    m, n = len(M), len(M[0])
    # Augment
    A = [row[:] + [yy % p] for row, yy in zip(M, y)]
    r = c = 0
    pivots = [-1]*n
    while r < m and c < n:
        # find pivot
        piv = None
        for i in range(r, m):
            if A[i][c] % p:
                piv = i; break
        if piv is None:
            c += 1
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = inv_mod(A[r][c], p)
        # normalize row
        for j in range(c, n+1):
            A[r][j] = (A[r][j] * inv) % p
        # eliminate others
        for i in range(m):
            if i == r: continue
            f = A[i][c]
            if f % p:
                for j in range(c, n+1):
                    A[i][j] = (A[i][j] - f*A[r][j]) % p
        pivots[c] = r
        r += 1; c += 1
    # check consistency
    for i in range(r, m):
        if all(A[i][j] % p == 0 for j in range(n)) and A[i][n] % p != 0:
            return None
    # read solution (unique if full rank)
    x = [0]*n
    for j in range(n):
        if pivots[j] != -1:
            x[j] = A[pivots[j]][n] % p
        else:
            # underdetermined (shouldn’t happen if we enforce full rank)
            return None
    return x

def parse_out(path="out.txt"):
    s = Path(path).read_text()
    # file is "A_values = [...] ; b_values = [...]"
    # split robustly:
    left, right = s.split(";")
    A = ast.literal_eval(left.split("=",1)[1].strip())
    b = ast.literal_eval(right.split("=",1)[1].strip())
    # reduce mod P
    A = [[a % P for a in row] for row in A]
    b = [bb % P for bb in b]
    return A, b

def dot(a,b,p=P): return sum((x*y) % p for x,y in zip(a,b)) % p

def recover_S(A, b, trials=4000, seed=0xC0FFEE):
    random.seed(seed)
    m = len(A); n = len(A[0])  # 52, 44
    # precompute pairwise differences
    pairs = []
    for i in range(m):
        for j in range(i+1, m):
            Ai = [(A[i][k] - A[j][k]) % P for k in range(n)]
            bi = (b[i] - b[j]) % P
            pairs.append((Ai, bi, i, j))
    best = None
    # RANSAC: sample n pairs, solve, score by |residual in D|
    for _ in range(trials):
        sample = random.sample(pairs, n)
        M = [Ai for (Ai,_,_,_) in sample]
        y = [bi for (_,bi,_,_) in sample]
        x = solve_linear_mod(M, y)
        if x is None: 
            continue
        # score on all pairs
        ok_pairs = 0
        zero_pairs = 0
        for Ai, bi, _, _ in pairs:
            r = (bi - dot(Ai, x)) % P
            if r in D:
                ok_pairs += 1
                if r == 0: zero_pairs += 1
        score = (ok_pairs, zero_pairs)
        if best is None or score > best[0]:
            best = (score, x)
    if best is None:
        raise RuntimeError("No candidate S found — increase trials.")
    S = best[1]
    # Validate per-row residuals fall in E
    row_res = [ (b[i] - dot(A[i], S)) % P for i in range(len(A)) ]
    bad = [i for i,r in enumerate(row_res) if r not in set(E)]
    if bad:
        # quick polish: refit using only rows with residual in E (subtract it)
        good_rows = [i for i in range(len(A)) if row_res[i] in set(E)]
        # choose any E-aligned 44 rows, subtract their residuals, solve exactly
        chosen = random.sample(good_rows, len(A[0]))
        M = [A[i][:] for i in chosen]
        y = [ (b[i] - row_res[i]) % P for i in chosen]
        S2 = solve_linear_mod(M, y)
        if S2 is not None:
            S = S2
    return S

def base_p_digits_to_bytes(S, p=P):
    # S are least-significant-first digits
    N = 0
    powp = 1
    for d in S:
        N = (N + d * powp) % (1<<10_000)  # big int
        powp *= p
    # now build full integer precisely
    N = 0
    for i, d in enumerate(S):
        N += d * (p ** i)
    # convert to bytes
    # long_to_bytes implementation (no Crypto)
    out = []
    while N:
        out.append(N & 0xff)
        N >>= 8
    out = bytes(reversed(out)) or b"\x00"
    return out

def main():
    A, b = parse_out("out.txt")
    S = recover_S(A, b, trials=4000)
    flag_bytes = base_p_digits_to_bytes(S)
    print("Recovered flag:", flag_bytes)
    try:
        print("As UTF-8:", flag_bytes.decode())
    except:
        pass

if __name__ == "__main__":
    main()
