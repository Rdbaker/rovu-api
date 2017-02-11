#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lambda ingest script."""
import os

from sqlalchemy import create_engine


DATABASE_URI = os.environ.get('DATABASE_URI', '')
EB_KEYS = os.environ.get('EB_KEYS', '').split(',')
ENGINE = create_engine('postgresql://' + DATABASE_URI)


def lambda_ingest():
    """Ingest events data from eventbrite."""
    from rovu.ingest.eventbrite import extract_events
    extract_events(engine=ENGINE, keys=EB_KEYS)
