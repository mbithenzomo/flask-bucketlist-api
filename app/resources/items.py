from flask import g
from flask.ext.restful import Resource, marshal
from flask_restful import reqparse
from .. serializers.serializers import item_serializer
from .. models import Bucketlist, Item
from base import unauthorized, add_item, delete_item, edit_item


class ItemsAPI(Resource):
    """
    URL: /api/v1/bucketlists/<id>/items/
    Request methods: GET, POST
    """
    def get(self, id):
        """ Get all items in a bucket list """
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                items = Item.query.filter_by(bucketlist_id=id).all()
                if items:
                    return marshal(items, item_serializer)
                return {"message": "The bucket list sepcified has no items. "
                        "Add one and try again!"}
            else:
                return unauthorized()
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")

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
    def get(self, id, item_id):
        """ Get a bucket list item """
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            item = Item.query.filter_by(bucketlist_id=id,
                                        id=item_id).first()
            if item:
                if item.created_by == g.user.id:
                    return marshal(item, item_serializer)
                else:
                    return unauthorized()
            else:
                return unauthorized("Error: The bucket list item specified "
                                    "does not exist. Please try again!")
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")

    def put(self, id, item_id):
        """ Edit a bucket list item """
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            item = Item.query.filter_by(bucketlist_id=id,
                                        id=item_id).first()
            if item:
                if item.created_by == g.user.id:
                    parser = reqparse.RequestParser()
                    parser.add_argument("title",
                                        required=True,
                                        help="No title provided.")
                    parser.add_argument("description", type=str, default="")
                    args = parser.parse_args()
                    title, description = args["title"], args["description"]
                    item.title = title
                    item.description = description
                    item.bucketlist_id = id
                    return edit_item(name="title",
                                     item=item,
                                     serializer=item_serializer,
                                     is_user=False,
                                     is_bucketlist=False,
                                     is_item=True)
                else:
                    return unauthorized()
            else:
                return {"message": "The bucket list item you are trying to "
                        "edit does not exist. Please try again!"}
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")

    def delete(self, id, item_id):
        """ Delete a bucket list item """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            item = Item.query.filter_by(bucketlist_id=id,
                                        id=item_id).first()
            if item:
                if item.created_by == g.user.id:
                    return delete_item(item,
                                       item.title,
                                       is_user=False,
                                       is_bucketlist=False,
                                       is_item=True)
                else:
                    return unauthorized()
            else:
                return {"message": "The bucket list item you are trying to "
                        "delete does not exist. Please try again!"}
        else:
            return unauthorized("Error: The bucket list specified does not "
                                "exist. Please try again!")
