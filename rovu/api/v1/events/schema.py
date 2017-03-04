# -*- coding: utf-8 -*-
"""Event schema."""
from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(attribute='eb_name_html')
    # it's stored as a string internally, but let's convert it to an int
    category_id = fields.Integer(attribute='eb_category_id')
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


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    # it's stored as a string internally, but let's convert it to an int
    external_id = fields.Integer(attribute='eb_id')
    parent_id = fields.String(attribute='eb_parent_id')
    name = fields.Str(attribute='eb_name')
    name_short = fields.Str(attribute='eb_name_short')

    class Meta:
        type_ = 'categories'
        strict = True


class CategoryFacetSchema(Schema):
    # it's stored as a string internally, but let's convert it to an int
    category_id = fields.Integer(attribute='eb_id')
    event_count = fields.Integer()
    name = fields.Str(attribute='eb_name')
