#!/usr/bin/env python3
"""
exploit_sunshine_wide_fixed.py

Improved version of the wide-window exploit. Fixes false positives and reads the full
server response before deciding success/failure.

Usage:
  python3 exploit_sunshine_wide_fixed.py [host] [port] [start_ts] [end_ts] [delay]

Defaults:
  host: chal.sunshinectf.games
  port: 25101
  start_ts: now - 172800   (48 hours ago)
  end_ts:   now + 300      (five minutes from now)
  delay:    0.05           (seconds between attempts)
"""

import os, sys, time, subprocess, socket

HOST_DEFAULT = "chal.sunshinectf.games"
PORT_DEFAULT = 25101
HELPER_C = "compute_target.c"
HELPER_BIN = "./compute_target"
PROGRESS_EVERY = 10  # print full preview every N seeds

C_SOURCE = r'''
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s <seed>\n", argv[0]);
        return 1;
    }
    unsigned int seed = (unsigned int)strtoul(argv[1], NULL, 10);
    srand(seed);
    unsigned long r1 = (unsigned long)rand();
    unsigned long r2 = (unsigned long)rand();
    unsigned long r3 = (unsigned long)rand();
    unsigned long long target = ((unsigned long long)r3 << 62) | ((unsigned long long)r2 << 31) | (unsigned long long)r1;
    printf("%llu\n", (unsigned long long) target);
    return 0;
}
'''

def write_and_compile():
    if os.path.exists(HELPER_BIN):
        return True
    with open(HELPER_C, "w") as f:
        f.write(C_SOURCE)
    print("[*] Compiling helper C program...")
    p = subprocess.run(["gcc", "-O2", HELPER_C, "-o", HELPER_BIN], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print("[!] gcc failed:")
        print(p.stderr.decode(errors='ignore'))
        return False
    try:
        os.unlink(HELPER_C)
    except Exception:
        pass
    print("[*] Compiled helper:", HELPER_BIN)
    return True

def compute_candidate(seed):
    try:
        out = subprocess.check_output([HELPER_BIN, str(seed)], timeout=1)
        return out.decode().strip()
    except Exception:
        return None

def recv_all(sock, timeout=2.0, bufsize=4096):
    sock.settimeout(0.5)
    data = b""
    tstart = time.time()
    while True:
        try:
            part = sock.recv(bufsize)
            if not part:
                break
            data += part
            # reset timer whenever we get data
            tstart = time.time()
        except socket.timeout:
            # stop if we've waited long enough since last data
            if time.time() - tstart > timeout:
                break
            else:
                continue
        except Exception:
            break
    return data

def try_candidate(host, port, candidate, connect_timeout=3.0, final_recv_timeout=2.0):
    try:
        s = socket.create_connection((host, port), timeout=connect_timeout)
    except Exception as e:
        return None, f"connect_err: {e}"
    # read banner (but don't decide based on it)
    banner = recv_all(s, timeout=0.001)
    # send candidate
    try:
        s.sendall((str(candidate) + "\n").encode())
    except Exception as e:
        s.close()
        return None, f"send_err: {e}"
    # now read full response until server closes or until final_recv_timeout of inactivity
    resp = recv_all(s, timeout=final_recv_timeout)
    s.close()
    return banner + resp, None

def looks_like_flag(resp_text):
    low = resp_text.lower()
    if "flag" in low or "ctf" in low or "congrat" in low or "you win" in low:
        return True
    if "{" in resp_text and "}" in resp_text:  # typical flag form
        return True
    return False

def main():
    args = sys.argv[1:]
    host = HOST_DEFAULT
    port = PORT_DEFAULT
    delay = 0.05

    if len(args) >= 1:
        host = args[0]
    if len(args) >= 2:
        port = int(args[1])

    now = int(time.time())
    default_start = now - 172800
    default_end   = now + 300

    if len(args) >= 4:
        start_ts = int(args[2])
        end_ts = int(args[3])
    else:
        start_ts = default_start
        end_ts = default_end

    if len(args) >= 5:
        try:
            delay = float(args[4])
        except:
            pass

    if not write_and_compile():
        print("[!] Failed to compile helper. Install gcc and try again.")
        sys.exit(1)

    total = end_ts - start_ts + 1
    print(f"[*] Target: {host}:{port}")
    print(f"[*] Trying seeds from {start_ts} to {end_ts} (newest->oldest). delay={delay}s")
    print(f"[*] Total seeds to try: {total} (this may take a while)")

    tried = 0
    for offset, seed in enumerate(range(end_ts, start_ts - 1, -1)):
        tried += 1
        candidate = compute_candidate(seed)
        if candidate is None:
            if tried % PROGRESS_EVERY == 0:
                print(f"[{tried}/{total}] seed {seed}: failed to compute candidate")
            continue

        banner_and_resp, err = try_candidate(host, port, candidate)
        if err:
            if tried % PROGRESS_EVERY == 0:
                print(f"[{tried}/{total}] seed {seed}: {err}")
        else:
            text = (banner_and_resp or b"").decode(errors='ignore')
            # show short progress every PROGRESS_EVERY attempts; otherwise silent except on potential hit
            if tried % PROGRESS_EVERY == 0:
                print(f"[{tried}/{total}] seed {seed} -> tried {candidate} ; preview: {repr(text)}")
            # now decide success/failure carefully
            lower = text.lower()
            # If it explicitly contains the WRONG string after our input, it's a definite fail
            if "wrong" in lower or "maybe next time" in lower:
                # definite wrong - continue
                pass
            else:
                # If response contains flag-like tokens, consider success
                if looks_like_flag(text):
                    print("[+] Success! seed", seed)
                    print(text)
                    return
                # If server didn't explicitly say WRONG and returned something else, print it (possible odd success)
                # But to avoid false positives we'll still show and ask user to inspect
                print("[!] Non-standard response for seed", seed)
                print(text)
                return

        time.sleep(delay)

    print("[!] Finished: no candidate in given range succeeded.")

if __name__ == "__main__":
    main()
