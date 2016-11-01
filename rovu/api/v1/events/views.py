# -*- coding: utf-8 -*-
"""Event views."""
from datetime import datetime
from dateutil.parser import parse

from flask import Blueprint, request

from rovu.api.v1.events.models import Event
from rovu.api.v1.events.schema import EventSchema

blueprint = Blueprint('event', __name__, url_prefix='/api/v1/events')
EVENT_SCHEMA = EventSchema()


@blueprint.route('/', strict_slashes=False)
def events():
    """List events."""
    period_start = request.args.get('period_start', None)
    period_end = request.args.get('period_end', None)

    if period_start is None:
        query_args = [Event.start_datetime >= datetime.utcnow().isoformat()]
    else:
        query_args = [Event.start_datetime >= parse(period_start)]

    if period_end is not None:
        query_args.append(Event.end_datetime <= period_end)

    return EVENT_SCHEMA.dumps(Event.query.filter(*query_args).all(),
                              many=True)
