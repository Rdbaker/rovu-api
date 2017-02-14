#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data ingestion for Eventbrite events."""
from dateutil import parser
import logging
import os

import requests

from rovu.api.v1.events.models import Event

logging.getLogger().setLevel(logging.INFO)

eb_key = os.environ.get('EVENTBRITE_KEY')

EB_HOST = 'https://www.eventbriteapi.com/v3'
EB_EVENT_URL = '{}/events/search'.format(EB_HOST)
EB_VENUE_URL = '{}/venues'.format(EB_HOST)
RADIUS = '5mi'
COORDS = {
    'cambridge': {
        'latitude': '42.360967',
        'longitude': '-71.082025'
    },
    'birmingham': {
        'latitude': '52.477564',
        'longitude': '-2.0037141'
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


def get_auth_header():
    """Return the authorization headers for the eventbrite request."""
    return {'Authorization': 'Bearer {}'.format(eb_key)}


def get_cambridge_events(page=1):
    """Get the initial events in the cambridge area."""
    return requests.get(
        EB_EVENT_URL,
        params={'location.within': RADIUS,
                'location.latitude': COORDS['birmingham']['latitude'],
                'location.longitude': COORDS['birmingham']['longitude'],
                'page': page,
                'sort_by': '-date'},
        headers=get_auth_header())


def extract_events():
    """Get the Eventbrite events within RADIUS of LAT:LON."""
    response = get_cambridge_events()
    logging.info('processing page 1')
    extract_page_events(response.json()['events'])
    for page in range(response.json()['pagination']['page_number']+1,
                      response.json()['pagination']['page_count']+1):
        logging.info('processing page {}'.format(page))
        json_response = get_cambridge_events(page).json()
        json_events = json_response['events']
        extract_page_events(json_events)


def extract_page_events(page):
    """Pull the events out of the Eventbrite page."""
    for event in page:
        extract_event(event)


def extract_event(event):
    """Get the event data and turn it into a model we're storing."""
    if event_does_not_exist(event):
        event['location'] = extract_venue(event['venue_id'])
        event_model = create_event(event)
        event_model.save()


def event_does_not_exist(event):
    """Return True if the event does not exist."""
    return Event.query.filter(Event.eb_id == event.get('id'))\
        .first() is None


def create_event(event_dict):
    """Initialize an event model."""
    event = Event.query.filter(Event.eb_id == event_dict.get('id')).first()
    # make sure we're not storing a duplicate
    if event is not None:
        return event
    event = Event(
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
    return event


def extract_venue(id):
    """Pull the venue out of the event."""
    response = requests.get(EB_VENUE_URL + '/{}'.format(id),
                            headers=get_auth_header())
    return response.json()
