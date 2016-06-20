from flask import g, request
from flask.ext.restful import Resource, marshal
from flask_restful import reqparse
from .. serializers.serializers import bucketlist_serializer
from base import unauthorized, add_item, delete_item, edit_item
from .. models import Bucketlist


class BucketListsAPI(Resource):
    """
    URL: /api/v1.0/bucketlists/
    Request methods: GET, POST
    """
    def get(self):
        """ Get all bucket lists belonging to the current user """

        search = request.args.get("q")
        if search:
            bucketlists = Bucketlist.query.filter_by(
                                title=search, created_by=g.user.id).all()
            error_message = {"Message": "There are no results for the search "
                             "term specified."}
        else:
            bucketlists = Bucketlist.query.filter_by(
                                created_by=g.user.id).all()
            error_message = {"Message": "You have no bucket lists. Add a "
                             "new one and try again!"}
        if bucketlists:
            return marshal(bucketlists, bucketlist_serializer), 201
        else:
            return error_message

    def post(self):
        """ Add a bucket list """
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True, help="No title provided.")
        parser.add_argument("description", type=str, default="")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        bucketlist = Bucketlist(title=title,
                                description=description,
                                created_by=g.user.id)
        return add_item(name="title",
                        item=bucketlist,
                        serializer=bucketlist_serializer,
                        is_user=False,
                        is_bucketlist=True,
                        is_item=False)


class BucketListAPI(Resource):
    """
    URL: /api/v1.0/bucketlists/<id>
    Request methods: GET, PUT, DELETE
    """
    def get(self, id):
        """ Get a bucket list """
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                created_by=g.user.id).first()
        if bucketlist:
            return marshal(bucketlist, bucketlist_serializer), 201
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")

    def put(self, id):
        """ Edit a bucket list """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                parser = reqparse.RequestParser()
                parser.add_argument("title",
                                    required=True,
                                    help="No title provided.")
                parser.add_argument("description", type=str, default="")
                args = parser.parse_args()
                title, description = args["title"], args["description"]
                bucketlist.title = title
                bucketlist.description = description
                return edit_item(name="title",
                                 item=bucketlist,
                                 serializer=bucketlist_serializer,
                                 is_user=False,
                                 is_bucketlist=True,
                                 is_item=False)
            else:
                return unauthorized()
        else:
            return unauthorized("Error: The bucket list you are trying to "
                                "edit does not exist. Please try again!")

    def delete(self, id):
        """ Delete a bucket list """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                return delete_item(bucketlist,
                                   bucketlist.title,
                                   is_user=False,
                                   is_bucketlist=True,
                                   is_item=False)
            else:
                return unauthorized()
        else:
            return unauthorized("Error: The bucket list you are trying to "
                                "delete does not exist. Please try again!")
