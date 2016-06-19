from flask import g, jsonify, request
from flask.ext.restful import Resource, marshal
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from .. models import User
from .. import db, app


auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized(message=None):
    """
    Returns an error message.
    """
    if not message:
        message = "Error: You are not authorized to access this resource."
    return jsonify({
        "Message": message
    }), 403


@app.before_request
def before_request():
    """
    Validates token.
    Is run before all requests apart from user login and registration.
    """
    if request.endpoint not in ["userlogin", "userregister", "index"]:
        token = request.headers.get("Token")
        if token is not None:
            user = User.verify_auth_token(token)
            if user:
                g.user = user
            else:
                return unauthorized("Error: The token you have entered is "
                                    "invalid.")
        else:
            return unauthorized("Error: Please enter a token.")


def add_item(**kwargs):
    """
    Add a user, bucketlist, or bucketlist item to the database.
    Also handles integrity errors.
    Arguments:
        kwargs["name"]: The title of the item to be added to the database.
        kwargs["item"]: The item to be added to the database.
        kwargs["serializer"]: The marshal serializer.
        kwargs["is_user"]: The flag used to identify users.
        kwargs["is_bucketlist"]: The flag used to identify bucketlists.
        kwargs["is_item"]: The flag used to identify bucketlist items.
    """
    try:
        db.session.add(kwargs["item"])
        db.session.commit()
        if kwargs["is_user"]:
            item_type = "user"
        elif kwargs["is_bucketlist"]:
            item_type = "bucket list"
        elif kwargs["is_item"]:
            item_type = "bucket list item"

        message = {"Message": "You have successfully added a new " +
                   item_type + "."}
        response = marshal(kwargs["item"], kwargs["serializer"])
        response.update(message)
        return response, 201

    except IntegrityError:
        """When adding an item that already exists"""
        db.session.rollback()
        return {"Error": "The " + kwargs["name"] +
                " that you tried to enter already exists."}


def delete_item(item, name, **kwargs):
    """
    Delete a user, bucketlist, or bucketlist item from the database.

    Arguments:
        item: The item to be deleted.
        name: The name of the item to be deleted.
        kwargs["is_user"]: The flag is used to identify users.
        kwargs["is_bucketlist"]: The flag is used to identify bucketlists.
        kwargs["is_item"]: The flag is used to identify bucketlist items.
    """
    if item:
        db.session.delete(item)
        db.session.commit()
        if kwargs["is_user"]:
            item_type = "user"
        elif kwargs["is_bucketlist"]:
            item_type = "bucket list"
        elif kwargs["is_item"]:
            item_type = "bucket list item"
        return {"Message": "You have successfully deleted the following " +
                item_type + ": " + name}
    else:
        return {"Message": "The delete was unsuccessful. Please try again!"}


def edit_item(**kwargs):
    """
    Edit a user, bucketlist, or bucketlist item.
    Arguments:
        kwargs["name"]: The title of the item to be edited.
        kwargs["item"]: The item to be edited.
        kwargs["serializer"]: The marshal serializer.
        kwargs["is_user"]: The flag used to identify users.
        kwargs["is_bucketlist"]: The flag used to identify bucketlists.
        kwargs["is_item"]: The flag used to identify bucketlist items.
    """
    db.session.add(kwargs["item"])
    db.session.commit()
    if kwargs["is_user"]:
        item_type = "user"
    elif kwargs["is_bucketlist"]:
        item_type = "bucket list"
    elif kwargs["is_item"]:
        item_type = "bucket list item"

    message = {"Message": "You have successfully edited the " +
               item_type + "."}
    response = marshal(kwargs["item"], kwargs["serializer"])
    response.update(message)
    return response, 201


class Index(Resource):
    """
    Manage responses to the index route.
    URL: /api/v1.0/
    Request method: GET
    """

    def get(self):
        """ Return a welcome message """
        return {"Message": "Welcome to the Bucket List API. "
                "Register a new user or login to get started!"}
