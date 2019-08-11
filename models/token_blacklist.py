from app import db


class TokenBlacklistModel(db.Model):
    __tablename__ = 'TokenBlacklist'

    token_id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String, db.ForeignKey("Users.username"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, token_type, username, expires, revoked):
        self.jti = jti
        self.token_type = token_type
        self.username = username
        self.expires = expires
        self.revoked = revoked

    def __repr__(self):
        return "<TokenBlacklistModel(token_id='{}', jti='{}', token_type='{}', " \
               "username='{}', expires='{}', revoked='{}')>" \
            .format(self.token_id, self.jti, self.token_type, self.username, self.expires, self.revoked)
