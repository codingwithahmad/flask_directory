from . import users
from flask import request
from .models import User
from directory import db
from sqlalchemy.exc import IntegrityError

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
        return {"Error": "Username is duplicated."}


    return {"message": "Account created successfully."}, 201
