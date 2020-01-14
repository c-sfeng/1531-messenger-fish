"""
Module to translate between datetime, json time format, and unix timestamp
With help from
- https://www.tutorialspoint.com/How-to-convert-Python-date-in-JSON-format?
fbclid=IwAR0MwJpbuGXzSFRhg7xA3mEksn2kE8aUr1nLN-kBId2bDT7aYA3SgxIRhR0
- https://stackoverflow.com/questions/10805589/convert-json-date-string-to-
python-datetime?fbclid=IwAR0gZF4CizLB0fjL2Yd_ovbtQ9heaXzdL3hT5x7gb6cdWMpfNF6x90pKohQ
"""
from datetime import datetime, timezone

def json_to_datetime(json_time):
    """Converts json to Python datetime"""
    try:
        if json_time.endswith('Z'):
            return datetime.strptime(json_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return datetime.strptime(json_time, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(json_time, '%Y-%m-%dT%H:%M:%S')

def datetime_to_json(datetime_time):
    """Converts json to Python datetime"""
    # return datetime_time.isoformat()
    return datetime_time.strftime('%Y-%m-%dT%H:%M:%S')

def datetime_to_timestamp(datetime_time):
    """Converts datetime to timestamp"""
    return int(float(datetime_time.replace(tzinfo=timezone.utc).timestamp()))

def timestamp_to_datetime(timestamp_time):
    """Converts timestamp to datetime"""
    try:
        timestamp_time = int(timestamp_time)
    except ValueError:
        timestamp_time = int(float(timestamp_time))

    # If input is measured in milliseconds, divide by 1000
    try:
        ret = datetime.utcfromtimestamp(timestamp_time)
    except ValueError:
        ret = datetime.utcfromtimestamp(timestamp_time / 1000)
    return ret

def json_to_timestamp(json_time):
    """Converts json to timestamp"""
    return int(float(datetime_to_timestamp(json_to_datetime(json_time))))
