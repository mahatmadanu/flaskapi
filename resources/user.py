from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_raw_jwt
from blacklist import BLACKLIST


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    def get(self,id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message":"User not found"}
        
        return user.json()
    
    def delete(self,id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "User not found"}
        
        user.delete_from_db()
        return {"message":"User deleted"}

class UserLogin(Resource):

    def post(cls):
        #get data from parser
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="cannot be blank")
        parser.add_argument("password", type=str, help="cannot be blank")

        data = parser.parse_args()
        #find user in database
        user = UserModel.find_by_username(data['username'])
        #check password
        if user and user.password == data['password']:
        #create access token
            access_token = create_access_token(identity=user.id, fresh=True)
        #create refresh token
            refresh_token = create_refresh_token(user.id)
        #return json
            return {
                'access_token':access_token,
                'refresh_token': refresh_token
            }
        return {"message":"invalid credentials"}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        #unique identifier for jwt
        jti = get_raw_jwt()['jti'] 
        BLACKLIST.add(jti)
        print(jti)
        return{"message":"Successfully log out"}
