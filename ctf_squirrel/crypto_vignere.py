import socket
import time

def get_encrypted_flag():
    host = "20.84.72.194"
    port = 5007
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = s.recv(1024).decode().strip()
        
        # Extract the flag (assuming format is consistent)
        flag_line = [line for line in data.split('\n') if line.startswith('Flag:')]
        if flag_line:
            return flag_line[0].split(': ')[1]
        return None

def main():
    flags = []
    max_attempts = 1000
    
    for i in range(max_attempts):
        try:
            flag = get_encrypted_flag()
            if flag:
                flags.append(flag)
                print(f"Attempt {i+1}/{max_attempts}: Collected flag {flag}")
            else:
                print(f"Attempt {i+1}/{max_attempts}: No flag found")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Attempt {i+1}/{max_attempts}: Error - {str(e)}")
            time.sleep(1)  # Longer delay if error occurs
    
    # Save to file
    with open('collected_flags.txt', 'w') as f:
        for flag in flags:
            f.write(f"{flag}\n")
    
    print(f"\nCompleted! Collected {len(flags)} flags. Saved to collected_flags.txt")

if __name__ == "__main__":
    main()