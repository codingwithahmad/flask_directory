from . import users
from flask import request
from .models import User
from directory import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, jwt_refresh_token_required
from directory.utils.request import json_only

@users.route('/', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'JSON Only!'}, 400

    args = request.get_json()

    new_user = User()
    try:
        new_user.username = args.get('username')
        new_user.password = args.get('password')
        db.session.add(new_user)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {"Error": f'{e}' }, 400
    except IntegrityError as e:
        db.session.rollback()
        return {"Error": "Username is duplicated."}, 400


    return {"message": "Account created successfully."}, 201

@users.route('/auth/', methods=['POST'])
@json_only
def login():

    args = request.get_json()

    username = args.get('username')
    password = args.get('password')

    user = User.query.filter(User.username.ilike(username)).first()
    if not user:
        return {'Error': 'Username/Password dosn\'t match'}, 403

    if not user.check_password(password):
        return {'Error': 'Username/Password dosn\'t match'}, 403

    access_token = create_access_token(identity=user.username, fresh=True)
    refresh_token = create_refresh_token(identity=user.username)

    return {'access': access_token, 'refresh_token': refresh_token}, 200

@users.put('/auth/')
@jwt_refresh_token_required
def get_new_access_token():
    identity = get_jwt_identity()
    return {'access_token': create_access_token(identity=identity)}

@users.route('/', methods=['GET'])
@jwt_required
def get_user():
    identity = get_jwt_identity()
    user = User.query.filter(User.username.ilike(identity)).first()

    return { 'username': user.username }
