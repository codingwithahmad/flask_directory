from . import users
from flask import request
from .models import User

@users.route('/', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'JSON Only!'}, 400

    args = request.get_json()

    new_user = User()

    new_user.username = args.get('username')
    new_user.password = args.get('password')


    return {}
