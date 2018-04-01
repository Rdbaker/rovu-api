#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lambda ingest script."""
import os

from sqlalchemy import create_engine


DATABASE_URI = os.environ.get('DATABASE_URI', '')
EB_KEYS = os.environ.get('EB_KEYS', '').split(':')
ENGINE = create_engine('postgres://' + DATABASE_URI,
                       connect_args={'sslmode': 'require'})


def lambda_ingest(*args, **kwargs):
    """Ingest events data from eventbrite."""
    from eventbrite import extract_events, execute_reaper
    extract_events(engine=ENGINE, keys=EB_KEYS)
    execute_reaper(engine=ENGINE)
