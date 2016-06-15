from flask_restful import fields

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
    "created_by": fields.Integer,
    "date_added": fields.DateTime,
    "date_edited": fields.DateTime
}

user_serializer = {
    "id": fields.Integer,
    "username": fields.String
}
