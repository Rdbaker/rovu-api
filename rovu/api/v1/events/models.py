# -*- coding: utf-8 -*-
"""Event models."""
import datetime

from sqlalchemy.dialects.postgresql import JSONB

from rovu.database import Column, Model, SurrogatePK, db


class Event(SurrogatePK, Model):
    """An event that takes place."""

    __tablename__ = 'events'
    eb_name_html = Column(db.String(255), nullable=False)
    eb_description_html = Column(db.Text())
    eb_id = Column(db.String(90), nullable=False)
    eb_url = Column(db.String(255), nullable=False)
    eb_start_utc = Column(db.String(90))
    eb_end_utc = Column(db.String(90))
    eb_capacity = Column(db.Integer())
    eb_venue = Column(JSONB())
    start_datetime = Column(db.DateTime(), default=datetime.datetime.utcnow)
    end_datetime = Column(db.DateTime(), default=datetime.datetime.utcnow)
