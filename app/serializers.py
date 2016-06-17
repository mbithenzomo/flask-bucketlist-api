from flask_restful import fields

"""
Defining how users, bucketlists, and bucketlist items are represented
"""

item_serializer = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "is_done": fields.Boolean,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
    "created_by": fields.Integer,
    "bucketlist_id": fields.Integer
}

bucketlist_serializer = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "items": fields.Nested(item_serializer),
    "created_by": fields.Integer,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime
}

user_serializer = {
    "id": fields.Integer,
    "username": fields.String
}
