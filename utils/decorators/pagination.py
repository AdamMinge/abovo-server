import functools
import flask
import flask_restful.fields


link_fields = {
    'prev': flask_restful.fields.String,
    'next': flask_restful.fields.String,
    'first': flask_restful.fields.String,
    'last': flask_restful.fields.String,
}


meta_fields = {
    'page': flask_restful.fields.Integer,
    'per_page': flask_restful.fields.Integer,
    'total': flask_restful.fields.Integer,
    'pages': flask_restful.fields.Integer,
    'links': flask_restful.fields.Nested(link_fields)
}


def marshal_with(item_field):
    def decorator(func):

        paginate_filed = {
            "items": flask_restful.fields.List(flask_restful.fields.Nested(item_field)),
            'meta': flask_restful.fields.Nested(meta_fields),
        }

        @functools.wraps(func)
        @flask_restful.marshal_with(paginate_filed)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def paginate(max_per_page=100):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            page = flask.request.args.get('page', 1, type=int)
            per_page = min(flask.request.args.get('per_page', max_per_page, type=int), max_per_page)

            query = func(*args, **kwargs)
            p = query.paginate(page, per_page)

            meta = {
                'page': page,
                'per_page': per_page,
                'total': p.total,
                'pages': p.pages,
            }

            links = {}
            if p.has_next:
                links['next'] = flask.url_for(flask.request.endpoint, page=p.next_num,
                                              per_page=per_page, **kwargs)
            if p.has_prev:
                links['prev'] = flask.url_for(flask.request.endpoint, page=p.prev_num,
                                              per_page=per_page, **kwargs)

            links['first'] = flask.url_for(flask.request.endpoint, page=1,
                                           per_page=per_page, **kwargs)
            links['last'] = flask.url_for(flask.request.endpoint, page=p.pages,
                                          per_page=per_page, **kwargs)

            meta['links'] = links
            result = {
                'items': p.items,
                'meta': meta
            }

            return result
        return wrapper
    return decorator
