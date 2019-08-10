from flask_restful import fields
from flask import request, url_for
from urllib.parse import urlparse, urlunparse


class Url(fields.Raw):
    def __init__(self, endpoint=None, key=None,
                 absolute=False, scheme=None):
        fields.Raw.__init__(self)
        self.key = key
        self.endpoint = endpoint
        self.absolute = absolute
        self.scheme = scheme

    def output(self, key, obj):
        try:
            data = fields.to_marshallable_type(obj)
            endpoint = self.endpoint if self.endpoint is not None else request.endpoint
            if self.key is not None and self.key in data:
                val = data[self.key]
                o = urlparse(url_for(endpoint, _external=self.absolute, id=val))
            else:
                o = urlparse(url_for(endpoint, _external=self.absolute, **data))
            if self.absolute:
                scheme = self.scheme if self.scheme is not None else o.scheme
                return urlunparse((scheme, o.netloc, o.path, "", "", ""))
            return urlunparse(("", "", o.path, "", "", ""))
        except TypeError as te:
            raise fields.MarshallingException(te)