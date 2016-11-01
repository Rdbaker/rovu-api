# -*- coding: utf-8 -*-
"""Event schema."""
from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(attribute='eb_name_html')
    start_datetime = fields.DateTime()
    end_datetime = fields.DateTime()
    venue = fields.Raw(attribute='eb_venue')

    class Meta:
        type_ = 'events'
        strict = True


class EventSchemaFull(EventSchema):
    description = fields.Str(attribute='eb_description_html')
    capacity = fields.Integer(attribute='eb_capacity')
    external_url = fields.URL(attribute='eb_url')
