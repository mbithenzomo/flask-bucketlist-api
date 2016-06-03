from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db
from datetime import datetime


class User(UserMixin, db.Model):
    ''' Creates user '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        '''prevents access to password
        property
        '''
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        '''Sets password to a hashed password
        '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''Checks if password matches
        '''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: %r>' % self.fullname


class Bucketlist(db.Model):
    ''' Creates bucketlist '''

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    ref = id + title
    description = db.Column(db.Text)
    priority = db.Column(db.String(10))
    was_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<Bucketlist: %r>' % self.ref


class Item(db.Model):
    ''' Creates bucketlist item '''

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    ref = id + title
    description = db.Column(db.Text)
    priority = db.Column(db.String(10))
    was_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('items', lazy='dynamic'))

    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    bucketlist = db.relationship('Bucketlist',
                                 backref=db.backref('bucketlists',
                                                    lazy='dynamic'))

    def __repr__(self):
        return '<Bucketlist: %r>' % self.ref
