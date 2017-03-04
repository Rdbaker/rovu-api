# -*- coding: utf-8 -*-
"""Event models."""
import datetime

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import Table, Column, String, MetaData, Text, DateTime, Integer


metadata = MetaData()


event = Table(
    'events',
    metadata,
    Column('eb_name_html', String(255)),
    Column('eb_description_html', Text()),
    Column('eb_id', String(90)),
    Column('eb_url', String(255)),
    Column('eb_start_utc', String(90)),
    Column('eb_end_utc', String(90)),
    Column('eb_capacity', Integer()),
    Column('eb_venue', JSONB()),
    Column('eb_category_id', String(90)),
    Column('eb_subcategory_id', String(90)),
    Column('start_datetime', DateTime(), default=datetime.datetime.utcnow),
    Column('end_datetime', DateTime(), default=datetime.datetime.utcnow)
)
