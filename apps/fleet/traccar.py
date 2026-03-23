"""
Traccar GPS API service layer.

Talks to a Traccar server via its REST API using HTTP Basic Auth.
All functions return empty/safe defaults if the server is unreachable.
"""
import urllib.request
import urllib.error
import json
import base64
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def _get_headers():
    credentials = f"{settings.TRACCAR_USER}:{settings.TRACCAR_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Accept': 'application/json',
    }


def _fetch(endpoint):
    """Make a GET request to the Traccar API. Returns parsed JSON or None on failure."""
    cache_key = f"traccar_api_{endpoint}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    url = f"{settings.TRACCAR_URL.rstrip('/')}/api/{endpoint}"
    req = urllib.request.Request(url, headers=_get_headers())
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            cache.set(cache_key, data, timeout=10)  # Cache for 10 seconds
            return data
    except Exception as e:
        logger.warning(f"Traccar API error on {endpoint}: {e}")
        return None


def get_all_positions():
    """
    Fetch current GPS positions for all devices.
    Returns a dict keyed by device ID (as string): {lat, lng, speed, course, fixTime}
    """
    data = _fetch('positions')
    if not data:
        return {}

    result = {}
    for pos in data:
        device_id = str(pos.get('deviceId', ''))
        if device_id:
            result[device_id] = {
                'lat': pos.get('latitude', 0),
                'lng': pos.get('longitude', 0),
                'speed': round(pos.get('speed', 0) * 1.852, 1),  # knots -> km/h
                'course': pos.get('course', 0),
                'fix_time': pos.get('fixTime', ''),
                'valid': pos.get('valid', False),
            }
    return result


def get_devices_map():
    """
    Fetch all registered devices from Traccar.
    Returns a dict: {device_id_str: device_name}
    """
    data = _fetch('devices')
    if not data:
        return {}
    return {str(d['id']): d.get('name', str(d['id'])) for d in data}


def is_connected():
    """Quick health check — returns True if Traccar is reachable."""
    result = _fetch('server')
    return result is not None
