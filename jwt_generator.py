import secrets
import base64

def generate_jwt_secret(length: int = 32):
    secret = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(secret).decode('utf-8')

if __name__ == "__main__":
    jwt_secret = generate_jwt_secret()
    print(f"Generated JWT Secret: {jwt_secret}")