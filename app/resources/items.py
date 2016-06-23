from flask import g
from flask.ext.restful import Resource, marshal
from flask_restful import reqparse
from .. serializers.serializers import item_serializer
from .. models import Bucketlist, Item
from base import unauthorized, add_item, delete_item, edit_item, authorized_user_bucketlist, authorized_user_item


class ItemsAPI(Resource):
    """
    URL: /api/v1/bucketlists/<id>/items/
    Request methods: GET, POST
    """

    def post(self, id):
        """ Add a new item to a bucket list """
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                parser = reqparse.RequestParser()
                parser.add_argument("title",
                                    required=True,
                                    help="No title provided.")
                parser.add_argument("description", type=str, default="")
                args = parser.parse_args()
                title, description = args["title"], args["description"]
                item = Item(title=title,
                            description=description,
                            bucketlist_id=id,
                            created_by=g.user.id)
                return add_item(name="title",
                                item=item,
                                serializer=item_serializer,
                                is_user=False,
                                is_bucketlist=False,
                                is_item=True)
            else:
                return unauthorized()
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")


class ItemAPI(Resource):
    """
    URL: /api/v1/bucketlists/<id>/items/<item_id>
    Request methods: GET, PUT, DELETE
    """
    @authorized_user_item
    @authorized_user_bucketlist
    def get(self, id, item_id):
        """ Get a bucket list item """
        return marshal(g.item, item_serializer)

    @authorized_user_item
    @authorized_user_bucketlist
    def put(self, id, item_id):
        """ Edit a bucket list item """
        parser = reqparse.RequestParser()
        parser.add_argument("title",
                            required=True,
                            help="No title provided.")
        parser.add_argument("description", type=str, default="")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        g.item.title = title
        g.item.description = description
        g.item.bucketlist_id = id
        return edit_item(name="title",
                         item=g.item,
                         serializer=item_serializer,
                         is_user=False,
                         is_bucketlist=False,
                         is_item=True)

    @authorized_user_item
    @authorized_user_bucketlist
    def delete(self, id, item_id):
        """ Delete a bucket list item """
        return delete_item(g.item,
                           g.item.title,
                           is_user=False,
                           is_bucketlist=False,
                           is_item=True)
