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
        """
        Get all bucket lists belonging to the current user.
        Implements search and pagination.
        """

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        search = args.get("q")

        if search:
            search_result = Bucketlist.query.filter_by(
                                title=search, created_by=g.user.id).paginate(
                                page, limit, False).items
            if search_result:
                return marshal(search_result, bucketlist_serializer)
            else:
                return {"Message": "The bucketlist '" + search + "' does "
                        "not exist."}

        bucketlists = Bucketlist.query.filter_by(
                            created_by=g.user.id).paginate(
                            page=page, per_page=limit, error_out=False)
        error_message = {"Message": "You have no bucket lists. Add a "
                         "new one and try again!"}
        page_count = bucketlists.pages
        has_next = bucketlists.has_next
        has_previous = bucketlists.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/bucketlists?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/bucketlists?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        bucketlists = bucketlists.items

        output = {"bucketlists": marshal(bucketlists, bucketlist_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if bucketlists:
            return output
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
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                return marshal(bucketlist, bucketlist_serializer)
            else:
                return unauthorized()
        else:
            return unauthorized("Error: The bucket list specified doesn't "
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
                                "edit doesn't exist. Please try again!")

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
                                "delete doesn't exist. Please try again!")
