from pwn import *
import os
from collections import deque

limit = 0xe5db6a6d765b1ba6e727aa7a87a792c49bb9ddeb2bad999f5ea04f047255d5a72e193a7d58aa8ef619b0262de6d25651085842fd9c385fa4f1032c305f44b8a4f92b16c8115d0595cebfccc1c655ca20db597ff1f01e0db70b9073fbaa1ae5e489484c7a45c215ea02db3c77f1865e1e8597cb0b0af3241cd8214bd5b5c1491f

def walking(x, y, part):
    epart = [int.from_bytes(part[i:i+2], "big") for i in range(0, len(part), 2)]
    xx = epart[0] * x + epart[1] * y
    yy = epart[2] * x + epart[3] * y
    return xx % limit, yy % limit

def solve_round(initial_pos, final_pos, mind):
    fragments = []
    for i in range(0, len(mind), 8):
        part = mind[i:i+8]
        fragments.append(part)
    
    # BFS setup
    queue = deque()
    queue.append((initial_pos[0], initial_pos[1], []))  # (x, y, path_indices)
    visited = set()
    visited.add((initial_pos[0] % limit, initial_pos[1] % limit))
    
    while queue:
        x, y, path_indices = queue.popleft()
        
        if (x % limit, y % limit) == (final_pos[0] % limit, final_pos[1] % limit):
            # Reconstruct the path
            path = b''.join([fragments[i] for i in path_indices])
            return path.hex()
        
        for i in range(len(fragments)):
            if i in path_indices:
                continue  # Cat doesn't reuse fragments
            part = fragments[i]
            xx, yy = walking(x, y, part)
            new_state = (xx % limit, yy % limit)
            if new_state not in visited:
                visited.add(new_state)
                new_path = path_indices + [i]
                queue.append((xx, yy, new_path))
    
    return None  # No path found

def main():
    # Connect to the server (assuming remote connection)
    # For local testing, you can replace with process('./challenge.py')
    r = remote('catch.chal.idek.team', 1337)
    
    for round_num in range(20):
        print(f"Round {round_num + 1}/20")
        
        # Receive initial position
        r.recvuntil("🐱✨ Co-location: ")
        initial_pos = eval(r.recvline().decode().strip())
        
        # Receive mind
        r.recvuntil("🔮 Cat's hidden mind: ")
        mind_hex = r.recvline().decode().strip()
        mind = bytes.fromhex(mind_hex)
        print(f"[+] mind: {mind})
        # Receive final position (after "😸 The chase is on!")
        r.recvuntil("🗺️ Cat now at: ")
        final_pos = eval(r.recvline().decode().strip())
        
        # Solve the round
        solution = solve_round(initial_pos, final_pos, mind)
        if solution is None:
            print("Failed to find a path")
            exit()
        
        # Send the solution
        r.sendlineafter("🤔 Path to recall (hex): ", solution)
        
        # Check if we passed the round
        response = r.recvline()
        if b"Reunion!" not in response:
            print("Failed this round")
            exit()
    
    # Get the flag
    r.recvuntil("🏆 Victory! The treasure lies within: ")
    flag = r.recvline().decode().strip()
    print(f"Flag: {flag}")
    r.close()

if __name__ == "__main__":
    main()