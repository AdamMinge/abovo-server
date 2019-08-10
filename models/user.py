from app import db
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model, UserMixin):
    __tablename__ = 'Users'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    permissions = db.relationship("ProjectPermissionModel")
    tokens = db.relationship("TokenBlacklistModel")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return "<User(username='{}', password='{}', email='{}')>" \
            .format(self.username, self.password, self.email)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
