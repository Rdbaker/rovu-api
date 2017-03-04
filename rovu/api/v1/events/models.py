# -*- coding: utf-8 -*-
"""Event models."""
import datetime

from sqlalchemy.dialects.postgresql import JSONB

from rovu.database import Column, Model, SurrogatePK, db


class Category(SurrogatePK, Model):
    __tablename__ = 'categories'
    eb_id = Column(db.String(90), index=True)
    eb_parent_id = Column(db.String(90))
    eb_name = Column(db.String(255))
    eb_name_short = Column(db.String(90))


class Event(SurrogatePK, Model):
    """An event that takes place."""

    __tablename__ = 'events'
    eb_name_html = Column(db.String(255))
    eb_description_html = Column(db.Text())
    eb_id = Column(db.String(90))
    eb_url = Column(db.String(255))
    eb_start_utc = Column(db.String(90))
    eb_end_utc = Column(db.String(90))
    eb_capacity = Column(db.Integer())
    eb_venue = Column(JSONB())
    eb_category_id = Column(db.String())
    eb_subcategory_id = Column(db.String())
    start_datetime = Column(db.DateTime(), default=datetime.datetime.utcnow)
    end_datetime = Column(db.DateTime(), default=datetime.datetime.utcnow)
