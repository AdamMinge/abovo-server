from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token
from exceptions import TokenNotFound


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    from models import TokenBlacklistModel
    from app import db

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
    from models import TokenBlacklistModel
    jti = decoded_token['jti']
    try:
        token = TokenBlacklistModel.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    from models import TokenBlacklistModel
    return TokenBlacklistModel.query.filter_by(user_identity=user_identity).all()


def revoke_token(token_id, user):
    from models import TokenBlacklistModel
    from app import db

    try:
        token = TokenBlacklistModel.query.filter_by(id=token_id, user_identity=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def unrevoke_token(token_id, user):
    from models import TokenBlacklistModel
    from app import db

    try:
        token = TokenBlacklistModel.query.filter_by(id=token_id, user_identity=user).one()
        token.revoked = False
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def prune_database():
    from models import TokenBlacklistModel
    from app import db

    now = datetime.now()
    expired = TokenBlacklistModel.query.filter(TokenBlacklistModel.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()
