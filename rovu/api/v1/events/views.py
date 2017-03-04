# -*- coding: utf-8 -*-
"""Event views."""
from datetime import datetime
from dateutil.parser import parse

from flask import Blueprint, request, jsonify
from sqlalchemy import func, desc

from rovu.api.v1.events.models import Event, Category
from rovu.api.v1.events.schema import (EventSchema, CategorySchema,
                                       CategoryFacetSchema)

blueprint = Blueprint('events', __name__, url_prefix='/api/v1/events')
EVENT_SCHEMA = EventSchema()
CAT_SCHEMA = CategorySchema()
CF_SCHEMA = CategoryFacetSchema()


@blueprint.route('/', strict_slashes=False)
def events():
    """List events."""
    event_start_after = request.args.get('event_start_after')
    event_end_before = request.args.get('event_end_before')
    category_id = request.args.get('category_id')

    if event_start_after is None:
        query_args = [Event.start_datetime >= datetime.utcnow().isoformat()]
    else:
        query_args = [Event.start_datetime >= parse(event_start_after)]

    if event_end_before is not None:
        query_args.append(Event.end_datetime <= event_end_before)

    if category_id is not None:
        query_args.append(Event.eb_category_id == category_id)

    return jsonify(EVENT_SCHEMA.dump(Event.query.filter(*query_args).all(),
                                     many=True).data)


@blueprint.route('/categories/all', strict_slashes=False)
def categories():
    """List all categories."""
    return jsonify(CAT_SCHEMA.dump(Category.query.all(), many=True).data)


@blueprint.route('/categories/facets', strict_slashes=False)
def categories_facets():
    """List facets of categories."""
    query = Category.query.session.query(Category.eb_name,
                                         Category.eb_id,
                                         func.count('*').label('event_count'))\
        .join(Event,
              Category.eb_id == Event.eb_category_id)\
        .group_by(Category.eb_name, Category.eb_id)\
        .order_by(desc('event_count'))
    return jsonify(CF_SCHEMA.dump(query.all(), many=True).data)
