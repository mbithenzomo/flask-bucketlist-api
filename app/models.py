from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from . import db, app


class User(db.Model):
    """ Creates user """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        """
        Prevents access to password property
        """
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """
        Sets password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Checks if password matches
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=20000):
        """
        Generating an authentication token that expires in 20 minutes
        """
        serializer = Serializer(
            app.config["SECRET_KEY"],
            expires_in=expiration)
        return serializer.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            """When token is valid but expired """
            return None
        except BadSignature:
            """When token is invalid """
            return None
        user = User.query.get(data["id"])
        return user

    def __repr__(self):
        return "<User: %r>" % self.username


class Bucketlist(db.Model):
    """ Creates bucketlist  """

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.now)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User",
                           backref=db.backref("users", lazy="dynamic"))

    items = db.relationship("Item",
                            backref=db.backref("bucketlist"))

    def __repr__(self):
        return "<Bucketlist: %r>" % self.title


class Item(db.Model):
    """ Creates items item """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.now)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User",
                           backref=db.backref("items", lazy="dynamic"))

    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlists.id"))

    def __repr__(self):
        return "<Bucketlist Item: %r>" % self.title
