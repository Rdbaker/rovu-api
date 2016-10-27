# -*- coding: utf-8 -*-
"""User schema."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    belonging_roles = fields.Nested('RoleSchema')

    class Meta:
        type_ = 'users'
        strict = True


class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()

    class Meta:
        type_ = 'roles'
        strict = True
