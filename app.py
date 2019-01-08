from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

##config for logout
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access', 'refresh']
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)
# jwt = JWT(app, authenticate, identity)  # /auth

@jwt.user_claims_loader
#whenewer we create jw we will add extra data
def add_claims_to_jwt(identity):
    if identity==1:
        return {'is_admin':True}
    return {'is_admin':False}

@jwt.token_in_blacklist_loader
def check_token_if_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:id>')
api.add_resource(UserLogin,'/user/login')
api.add_resource(UserLogout,'/user/logout')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
