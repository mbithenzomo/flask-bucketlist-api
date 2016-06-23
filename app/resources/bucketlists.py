from flask import g, request
from flask.ext.restful import Resource, marshal
from flask_restful import reqparse
from .. serializers.serializers import bucketlist_serializer
from base import authorized_user_bucketlist, add_item, delete_item, edit_item
from .. models import Bucketlist


class BucketListsAPI(Resource):
    """
    URL: /api/v1/bucketlists/
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
        kwargs = {"created_by": g.user.id}

        if search:
            kwargs.update({"title": search})
            error_message = {"message": "The bucketlist '" + search + "' does "
                                        "not exist."}
        else:
            error_message = {"message": "You have no bucket lists. Add a "
                             "new one and try again!"}
        bucketlists = Bucketlist.query.filter_by(**kwargs).paginate(
                             page=page, per_page=limit, error_out=False)
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
    URL: /api/v1/bucketlists/<id>
    Request methods: GET, PUT, DELETE
    """
    @authorized_user_bucketlist
    def get(self, id):
        """ Get a bucket list """
        return marshal(g.bucketlist, bucketlist_serializer)

    @authorized_user_bucketlist
    def put(self, id):
        """ Edit a bucket list """
        parser = reqparse.RequestParser()
        parser.add_argument("title",
                            required=True,
                            help="No title provided.")
        parser.add_argument("description", type=str, default="")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        g.bucketlist.title = title
        g.bucketlist.description = description
        return edit_item(name="title",
                         item=g.bucketlist,
                         serializer=bucketlist_serializer,
                         is_user=False,
                         is_bucketlist=True,
                         is_item=False)

    @authorized_user_bucketlist
    def delete(self, id):
        """ Delete a bucket list """
        return delete_item(g.bucketlist,
                           g.bucketlist.title,
                           is_user=False,
                           is_bucketlist=True,
                           is_item=False)
