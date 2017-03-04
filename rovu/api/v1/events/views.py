# -*- coding: utf-8 -*-
"""Event views."""
from datetime import datetime
from dateutil.parser import parse

from flask import Blueprint, request, jsonify
from sqlalchemy import func

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
    event_start_after = request.args.get('event_start_after', None)
    event_end_before = request.args.get('event_end_before', None)
    category_id = request.args.get('category_id', None)

    if not bool(event_start_after):
        query_args = [Event.start_datetime >= datetime.utcnow().isoformat()]
    else:
        query_args = [Event.start_datetime >= parse(event_start_after)]

    if bool(event_end_before):
        query_args.append(Event.end_datetime <= event_end_before)

    if bool(category_id):
        query_args.append(Event.eb_category_id == category_id)

    ev_query = Event.query.filter(*query_args)
    subquery = ev_query.subquery()
    facet_query = Category.query.session.query(Category.eb_name,
                                               Category.eb_id,
                                               func.count('*').label('event_count'))\
        .join(subquery, Category.eb_id == subquery.c.eb_category_id)\
        .group_by(Category.eb_name, Category.eb_id)\
        .order_by(Category.eb_name)

    return jsonify(events=EVENT_SCHEMA.dump(Event.query.filter(*query_args).all(),
                                            many=True).data,
                   facets=CF_SCHEMA.dump(facet_query.all(), many=True).data)


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
        .order_by(Category.eb_name)
    return jsonify(CF_SCHEMA.dump(query.all(), many=True).data)
