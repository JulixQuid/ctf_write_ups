#!/bin/bash

# Server address and port
SERVER=83.136.251.145
PORT=55348
#!/bin/bash

# Connect to the server using netcat with unbuffered I/O
{
    # Disable buffering for stdin, stdout, and stderr
    stdbuf -i0 -o0 -e0 nc "$SERVER" "$PORT" | while IFS= read -r line; do
        echo "$line"  # Print the server's response

        # Check for specific strings in the previous line and send answers immediately
        if [[ "$prev_line" == *"are given the sacred prime:"* ]]; then
            echo "384"  # Answer to question 1
        elif [[ "$prev_line" == *"Enter the full factorization of the order of the multiplicative group"* ]]; then
            echo "2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1"  # Answer to question 2
        elif [[ "$prev_line" == *"For this question, you will have to send 1 if the element is a generator of the finite field F_p, otherwise 0."* ]]; then
            # Check if the current line is a generator question
            if [[ "$line" == *"?"* ]]; then
                # Generate a random 50/50 answer (1 or 0)
                if (( RANDOM % 2 == 0 )); then
                    echo "1"
                else
                    echo "0"
                fi
            fi
        fi

        # Store the current line as the previous line for the next iteration
        prev_line="$line"
    done
}
