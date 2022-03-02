from . import users


@users.route('/')
def index():
    return {"message": "Hello from users"}
