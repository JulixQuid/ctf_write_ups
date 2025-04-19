import hashlib
from datetime import datetime, timedelta
import pytz
from tqdm import tqdm

def is_valid_flag(s, forbidden_chars):
    """Check if all characters are printable ASCII (32-126) and not in forbidden list"""
    return all(32 <= ord(c) <= 126 and c not in forbidden_chars for c in s)

def decode_flag():
    flags_ = []
    flag = [0x45, 0x00, 0x50, 0x39, 0x08, 0x6f, 0x4d, 0x5b, 0x58, 0x06, 0x66, 0x40,
            0x58, 0x4c, 0x6d, 0x5d, 0x16, 0x6e, 0x4f, 0x00, 0x43, 0x6b, 0x47, 0x0a,
            0x44, 0x5a, 0x5b, 0x5f, 0x51, 0x66, 0x50, 0x57]
    
    # Define forbidden characters (adjust as needed)
    forbidden_chars = {}
    
    # Start from April 11, 2025 17:00 UTC
    current_time = datetime(2025, 4, 11, 17, 0, tzinfo=pytz.UTC)
    end_time = current_time - timedelta(hours=24)  # Go back 24 hours
    
    # Get all time zones
    all_timezones = pytz.all_timezones
    
    print(f"Brute forcing from {current_time} to {end_time}")
    print(f"Checking {len(all_timezones)} time zones")
    print(f"Excluding characters: {''.join(sorted(forbidden_chars))}")
    print("Looking for flags with all valid printable ASCII characters...")
    
    while current_time >= end_time:
        for tz_name in tqdm(all_timezones, desc=f"Checking {current_time}"):
            try:
                # Convert to target timezone
                tz = pytz.timezone(tz_name)
                localized_time = current_time.astimezone(tz)
                
                # Format the base string
                date_str = localized_time.strftime("%m/%d/%Y")
                time_str = localized_time.strftime("%H:%M")
                base = f"{tz_name}-{date_str}-{time_str}"
                
                # Generate MD5 hash
                hash_md5 = hashlib.md5(base.encode()).hexdigest()
                
                # XOR with flag
                result = []
                for i in range(len(flag)):
                    if i < len(hash_md5):
                        result.append(chr(flag[i] ^ ord(hash_md5[i])))
                    else:
                        result.append(chr(flag[i]))
                decoded = ''.join(result)
                
                # Check if all characters are valid
                if is_valid_flag(decoded, forbidden_chars):
                    print(f"\nFound valid flag at {localized_time} in timezone {tz_name}")
                    print(f"Base string: {base}")
                    print(f"MD5 hash: {hash_md5}")
                    print(f"Decoded flag: {decoded}")
                    flags_.append(decoded)
                    print("-" * 50)
                
            except Exception as e:
                # Skip invalid time zones or conversion errors
                continue
        
        # Move back in time
        current_time -= timedelta(minutes=1)
    
    print("Brute force completed")
    print(flags_)
    return None

if __name__ == "__main__":
    decode_flag()