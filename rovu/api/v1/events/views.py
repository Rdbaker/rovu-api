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
    event_start_after = request.args.get('event_start_after', None)
    event_end_before = request.args.get('event_end_before', None)

    if event_start_after is None:
        query_args = [Event.start_datetime >= datetime.utcnow().isoformat()]
    else:
        query_args = [Event.start_datetime >= parse(event_start_after)]

    if event_end_before is not None:
        query_args.append(Event.end_datetime <= event_end_before)

    return EVENT_SCHEMA.dumps(Event.query.filter(*query_args).all(),
                              many=True)
