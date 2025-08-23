import pickle
import pickletools
from io import BytesIO
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Your original wrapper functions (unchanged)
def py_pickle_wrapper(data: bytes) -> bool:
    class SafePyUnpickler(pickle.Unpickler):
        def find_class(self, module_name: str, global_name: str):
            print("no no no")
            exit(1)
    try:
        SafePyUnpickler(BytesIO(data)).load()
        return True
    except Exception:
        return False

def c_pickle_wrapper(data: bytes) -> bool:
    class SafeCUnpickler(pickle._Unpickler):
        def find_class(self, module_name: str, global_name: str):
            print("no no no")
            exit(1)
    try:
        SafeCUnpickler(BytesIO(data)).load()
        return True
    except Exception:
        return False

def pickletools_wrapper(data: bytes) -> bool:
    try:
        pickletools.dis(data)
        return True
    except Exception:
        return False

# All possible pickle opcodes (as bytes)
OPCODES = [
    b'(', b'.', b'0', b'1', b'2', b'F', b'I', b'J', b'K', b'L', b'M',
    b'N', b'P', b'Q', b'R', b'S', b'T', b'U', b'V', b'X', b'a', b'b',
    b'c', b'd', b'}', b'e', b'g', b'h', b'i', b'j', b'l', b']', b'o',
    b'p', b'q', b'r', b's', b't', b')', b'u', b'G', b'\x80', b'\x81',
    b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88',
    b'\x89', b'\x8a', b'\x8b', b'B', b'C', b'\x8c', b'\x8d', b'\x8e',
    b'\x8f', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95',
    b'\x96', b'\x97', b'\x98'
]

# Thread-safe solution storage
solutions = {}
solution_lock = threading.Lock()
found_event = threading.Event()

def generate_pickles(max_length=5):
    """Generate all possible pickles up to max_length bytes"""
    for length in range(1, max_length + 1):
        for combo in product(OPCODES, repeat=length):
            yield b''.join(combo)

def test_pickle(pickle_data, check_num):
    """Test a single pickle against a specific check condition"""
    if found_event.is_set():
        return None
        
    p = py_pickle_wrapper(pickle_data)
    c = c_pickle_wrapper(pickle_data)
    t = pickletools_wrapper(pickle_data)
    
    conditions = {
        #1: p and c and not t,
        #2: not p and c and t,
        #3: p and not c and t,
        #4: not p and not c and t,
        5: not p and c and not t
    }
    
    if conditions.get(check_num, False):
        with solution_lock:
            if check_num not in solutions:
                solutions[check_num] = pickle_data.hex()
                found_event.set()
                return pickle_data.hex()
    return None

def find_pickle_for_check(check_num, max_workers=8):
    """Threaded search for a pickle that satisfies the check condition"""
    global solutions, found_event
    solutions = {}
    found_event.clear()
    
    print(f"Threaded search for Check {check_num}...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pickle_data in generate_pickles():
            if found_event.is_set():
                break
            futures.append(executor.submit(test_pickle, pickle_data, check_num))
            
        for future in as_completed(futures):
            if found_event.is_set():
                break
            result = future.result()
            if result:
                print(f"Check {check_num} passed with: {result}")
                return result
                
    return None

# Find solutions for all checks
final_solutions = {}
for check_num in range(1, 6):
    solution = find_pickle_for_check(check_num)
    if solution:
        final_solutions[check_num] = solution
    else:
        print(f"Failed to find solution for Check {check_num}")

print("\nFinal Solutions:")
for check, sol in final_solutions.items():
    print(f"Check {check}: {sol}")