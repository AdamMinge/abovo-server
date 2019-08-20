from flask_restful import fields


class Enum(fields.Raw):
    def format(self, value):
        return str(value.name)
