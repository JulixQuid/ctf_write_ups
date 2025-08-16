# flag was manually Bruteforced
encoded = "7032652791156917671465166913651218232017181420241721222618141725201868182311"
n = 38
first_char = chr(70 + 32)  # 'f'
remaining = [int(encoded[i:i+2]) for i in range(2, len(encoded), 2)]  # Split into pairs
print(len(remaining),'XXXXXXXXXXXXX')
flag0 = [first_char]
print("flag{"+"0"*32+"}")

echo flag\{00000000000000000000000000000000\} | perl -ple '$n=()=/./g;$_=~s/./$|--?ord($&)%$n:ord($&)-$^F**5/eg'
f l a g {                                                                 }
f l a g { 5 e 7 c 4 a 6 e 3 a 2 2 c 4 7 2 4 4 d 1 a 6 f 2 4 1 e 4 8 d 8 7 }
7032652791156917671465166913651218232017181420241721222618141725201868182311
7032652791267026702670267026702670267026702670267026702670267026702670267011 f
7032652791256925692569256925692569256925692569256925692569256925692569256911 e
7032652791246824682468246824682468246824682468246824682468246824682468246811 d
7032652791236723672367236723672367236723672367236723672367236723672367236711 c
7032652791226622662266226622662266226622662266226622662266226622662266226611 b
7032652791216521652165216521652165216521652165216521652165216521652165216511 a
7032652791192519251925192519251925192519251925192519251925192519251925192511 9
7032652791182418241824182418241824182418241824182418241824182418241824182411 8
7032652791172317231723172317231723172317231723172317231723172317231723172311 7
7032652791162216221622162216221622162216221622162216221622162216221622162211 6
7032652791152115211521152115211521152115211521152115211521152115211521152111 5
7032652791142014201420142014201420142014201420142014201420142014201420142011 4
7032652791131913191319131913191319131913191319131913191319131913191319131911 3
7032652791121812181218121812181218121812181218121812181218121812181218121811 2
7032652791111711171117111711171117111711171117111711171117111711171117111711 1
7032652791101610161016101610161016101610161016101610161016101610161016101611 0

import subprocess

def generate_flag(char):
    # Generate a flag like flag{cccccccccccccccccccccccccccccccccc} where c is the test char
    return f"flag{{{char * 36}}}"

def run_perl(flag):
    # Run the Perl command and capture output
    cmd = f"echo {flag} | perl -ple '$n=()=/./g;$_=~s/./$|--?ord($&)%$n:ord($&)-$^F**5/eg'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def compare_pairs(target, test_output):
    # Split both into pairs and compare
    target_pairs = [target[i:i+2] for i in range(0, len(target), 2)]
    test_pairs = [test_output[i:i+2] for i in range(0, len(test_output), 2)]
    
    # The first pair is always '70' (from 'f'), so skip it
    matching_positions = []
    for i in range(1, min(len(target_pairs), len(test_pairs))):
        if target_pairs[i] == test_pairs[i]:
            matching_positions.append(i)
    return matching_positions

def brute_force_flag():
    target = "7032652791156917671465166913651218232017181420241721222618141725201868182311"
    charset = "0123456789ABCDEF"  # Adjust as needed
    
    # Initialize flag with 'flag{' + 36 unknowns + '}'
    flag = list("flag\{" + "?" * 32 + "\}")
    
    for char in charset:
        test_flag = generate_flag(char)
        test_output = run_perl(test_flag)
        print(test_output)
        print(target)
        matches = compare_pairs(target, test_output)
        
        if matches:
            print(f"Character '{char}' matches at positions: {matches}")
            for pos in matches:
                # Adjust for 'flag{' prefix (positions start after '70')
                flag_pos = pos + 4  # Because 'flag{' is 5 chars, and '70' is first pair
                if flag_pos < len(flag):
                    flag[flag_pos] = char
    
    print("Recovered flag:", ''.join(flag))

if __name__ == "__main__":
    brute_force_flag()