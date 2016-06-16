from flask_restful import fields

"""
Defining how users, bucketlists, and bucketlist items are represented
"""

item_serializer = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "is_done": fields.Boolean,
    "date_added": fields.DateTime,
    "date_edited": fields.DateTime
}

bucketlist_serializer = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "items": fields.Nested(item_serializer),
    "user_id": fields.Integer,
    "date_added": fields.DateTime,
    "date_edited": fields.DateTime
}

user_serializer = {
    "id": fields.Integer,
    "username": fields.String
}
