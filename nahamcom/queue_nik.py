import jwt
JWT_SECRET = "4A4Dmv4ciR477HsGXI19GgmYHp2so637XhMC"
algorithm = "hs256"
payload = {
  "user_id": "nico15935746@gmail.com",
  "queue_time": 1.1,
  "exp": 5348065581
}
new_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
print(new_token)