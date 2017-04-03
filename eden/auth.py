import jwt

def get_token(secret, issuer, role):
    claims = {'iss': issuer, 'role': role}
    return jwt.encode(claims, secret, algorithm='HS256').decode("utf-8")
