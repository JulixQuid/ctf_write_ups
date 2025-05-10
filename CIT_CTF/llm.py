import socket
import time
from openai import OpenAI

# ===== CONFIGURATION =====
MODEL = "gpt-3.5-turbo"
SERVER_HOST = "23.179.17.40"
SERVER_PORT = 5393
# =========================

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

def solve_puzzle():
    buffer = ""

    # Connect to the challenge server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.settimeout(5)  # Set timeout

        while True:
            try:
                data = s.recv(4096).decode('utf-8')
                if not data:
                    print("Server closed connection.")
                    break
                time.sleep(2)
                buffer += data

                # Keep checking if we see '>'
                while True:#'>' in buffer:
                    # Split at the FIRST '>'
                    question_part, buffer = buffer.split('>', 1)
                    question = question_part.strip().replace("how much do you know about mongolia?","")

                    if question:
                        print(f"\n[QUESTION]: {question}")

                        # Send to OpenAI
                        answer = get_openai_answer(question)
                        print(f"[ANSWER]: {answer}")
                        time.sleep(2)
                        # Send back to server
                        s.sendall((answer + "\n").encode('utf-8'))
                        time.sleep(3)  # slight delay to avoid flooding

            except socket.timeout:
                print("Timeout, waiting for data...")
                continue
            except Exception as e:
                print(f"Error: {e}")
                break

def get_openai_answer(question):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Answer concisely and accurately, and short do not extend or repeat the question averaga 3 words."},
                {"role": "user", "content": question}
            ],
            max_tokens=200,
            temperature=0.2  # deterministic
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "ERROR"

if __name__ == "__main__":
    print("Starting puzzle solver...")
    solve_puzzle()
