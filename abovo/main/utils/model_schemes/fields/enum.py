from marshmallow import fields


class Enum(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value.name)
