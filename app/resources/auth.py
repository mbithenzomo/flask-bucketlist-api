from flask.ext.restful import Resource
from flask_restful import reqparse
from .. serializers.serializers import user_serializer
from .. models import User
from base import unauthorized, add_item


class UserRegister(Resource):
    """
    Register a new user.
    URL: /api/v1.0/auth/register/
    Request method: POST
    """

    def post(self):
        """ Add a user """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a username.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]
        user = User(username=username,
                    password=password)
        return add_item(name="username",
                        item=user,
                        serializer=user_serializer,
                        is_user=True,
                        is_bucketlist=False,
                        is_item=False)


class UserLogin(Resource):
    """
    Log a user in.
    URL: /api/v1.0/auth/login/
    Request method: POST
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a username.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]

        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return {"message": "Error: Please enter a username and password."}
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {"message": "You have successfully logged in. Use the "
                    "token below to make requests.",
                    "token": token.decode("ascii")}
        else:
            return unauthorized("Error: Incorrect username and/or password. "
                                "Please try again!")
