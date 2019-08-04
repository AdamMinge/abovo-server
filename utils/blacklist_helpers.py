from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token
from exceptions import TokenNotFound
from models import TokenBlacklistModel
from app import db


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklistModel(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    try:
        token = TokenBlacklistModel.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def revoke_token(decoded_token, user):
    jti = decoded_token['jti']
    try:
        token = TokenBlacklistModel.query.filter_by(jti=jti, user_identity=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(jti))


def unrevoke_token(decoded_token, user):
    jti = decoded_token['jti']
    try:
        token = TokenBlacklistModel.query.filter_by(jti=jti, user_identity=user).one()
        token.revoked = False
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(jti))


def prune_database():
    now = datetime.now()
    expired = TokenBlacklistModel.query.filter(TokenBlacklistModel.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()
