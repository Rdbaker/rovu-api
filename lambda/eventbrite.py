#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data ingestion for Eventbrite events."""
from dateutil import parser
import logging

import requests

from models import event as Event

logging.getLogger().setLevel(logging.INFO)

EB_HOST = 'https://www.eventbriteapi.com/v3'
EB_EVENT_URL = '{}/events/search'.format(EB_HOST)
EB_VENUE_URL = '{}/venues'.format(EB_HOST)
RADIUS = '5mi'
COORDS = {
    'cambridge': {
        'latitude': '42.360967',
        'longitude': '-71.082025'
    },
    'london': {
        'latitude': '51.507427',
        'longitude': '-0.1353227'
    },
    'worcester': {
        'latitude': '42.277613952716145',
        'longitude': '-71.80649595832824'
    },
    'huntington_beach': {
        'latitude': '33.692000',
        'longitude': '-117.929021'
    },
    'long_beach': {
        'latitude': '33.786281',
        'longitide': '-118.308075'
    },
    'south_la': {
        'latitude': '33.988475',
        'longitude': '-118.300416'
    },
    'west_carson': {
        'latitude': '33.809516',
        'longitude': '-118.291573'
    },
    'west_la': {
        'latitude': '34.044186',
        'longitude': '-118.429549'
    },
    'la': {
        'latitude': '34.032708',
        'longitude': '-118.257540'
    },
    'westmont': {
        'latitude': '33.940710',
        'longitude': '-118.308527'
    },
    'beverly_hills': {
        'latitude': '34.066656',
        'longitude': '-118.428505'
    },
    'sf': {
        'latitude': '37.784024',
        'longitude': '-122.388253'
    }
}


def get_auth_header(key):
    """Return the authorization headers for the eventbrite request."""
    return {'Authorization': 'Bearer {}'.format(key)}


def get_cambridge_events(page=1, keys=None):
    """Get the initial events in the cambridge area."""
    res = requests.get(
        EB_EVENT_URL,
        params={'location.within': RADIUS,
                'location.latitude': COORDS['london']['latitude'],
                'location.longitude': COORDS['london']['longitude'],
                'page': page,
                'sort_by': '-date'},
        headers=get_auth_header(keys[-1]))
    if res.status_code >= 400:
        if len(keys) == 0:
            # hard fail if we ran out of keys
            return False
        keys.pop()
        return get_cambridge_events(page, keys)
    else:
        return res, keys


def extract_events(engine, keys):
    """Get the Eventbrite events within RADIUS of LAT:LON."""
    conn = engine.connect()
    response, keys = get_cambridge_events(keys=keys)
    logging.info('processing page 1')
    extract_page_events(response.json()['events'], conn, keys[-1])
    for page in range(response.json()['pagination']['page_number']+1,
                      response.json()['pagination']['page_count']+1):
        logging.info('processing page {}'.format(page))
        json_response, keys = get_cambridge_events(page, keys=keys)
        json_events = json_response.json()['events']
        extract_page_events(json_events, conn, keys[-1])


def extract_page_events(page, conn, key):
    """Pull the events out of the Eventbrite page."""
    for event in page:
        extract_event(event, conn, key)


def extract_event(event, conn, key):
    """Get the event data and turn it into a model we're storing."""
    if event_does_not_exist(event, conn):
        event['location'] = extract_venue(event['venue_id'], key)
        insert_stmt = create_event(event)
        if insert_stmt is not None:
            conn.execute(insert_stmt)


def event_does_not_exist(event, conn):
    """Return True if the event does not exist."""
    return conn.execute(Event.select().where(Event.c.eb_id == event.get('id')))\
        .first() is None


def create_event(event_dict):
    """Initialize an event model."""
    return Event.insert().values(
        eb_name_html=event_dict.get('name', {}).get('html', ''),
        eb_description_html=event_dict.get('description', {}).get('html', ''),
        eb_id=event_dict.get('id', ''),
        eb_url=event_dict.get('url', ''),
        eb_start_utc=event_dict.get('start', {}).get('utc', ''),
        eb_end_utc=event_dict.get('end', {}).get('utc', ''),
        eb_capacity=event_dict.get('capacity', {}),
        eb_venue=event_dict.get('location', {}),
        start_datetime=parser.parse(event_dict.get('start', {}).get('utc', '')),
        end_datetime=parser.parse(event_dict.get('end', {}).get('utc', ''))
    )


def extract_venue(id, key):
    """Pull the venue out of the event."""
    response = requests.get(EB_VENUE_URL + '/{}'.format(id),
                            headers=get_auth_header(key))
    return response.json()
