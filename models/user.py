from app import db
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    permissions = db.relationship("PermissionModel")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return "<User(id='{}', username='{}', password={}, email={})>" \
            .format(self.id, self.username, self.password, self.email)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
