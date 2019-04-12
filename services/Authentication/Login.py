from models.base import db
from models.User import User
import jwt

def login(name, password):
    try:
        user = User.query.filter_by(name=name, is_deleted=False).first()
        if user is None:
            return {
                "data": None,
                "message": "Username does not exist",
                "status": 0
            }
        if user.password != password:
            return {
                "data": None,
                "message": "Username and password does not match",
                "status": 0
            }
        user_type = user.user_type
        userData = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_no": user.phone_no,
            "user_type_id": user_type.id,
            "user_type": user_type.name,
        }
        encoded_jwt = jwt.encode(userData, 'secret', algorithm='HS256')
        return {
            "data": {
                "user_id": user.id,
                "jwt_token": encoded_jwt,
            },
            "message": "Login successfull",
            "status": 1
        }
    except Exception as e:
        return {
            "data": None,
            "message": str(e),
            "status": 0
        }