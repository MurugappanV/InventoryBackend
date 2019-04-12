import jwt

def validateUserToken(encoded_jwt):
    return jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])