"""
Module for encoding and decoding jwt
"""

from datetime import datetime
import jwt
from server_files.util import json_time_translator

def encode_u_id(u_id):
    """Returns endoded u_id and current time with jwt"""
    return jwt.encode({
        "u_id": u_id,
        "datetime": json_time_translator.datetime_to_json(datetime.utcnow())
    }, '1$Arh"1bWa/7+OS', algorithm='HS256').decode('utf-8')

def decode_token(token):
    """Decodes jwt token and returns u_id"""
    payload = None
    try:
        payload = jwt.decode(token.encode('utf-8'), '1$Arh"1bWa/7+OS', algorithm='HS256')['u_id']
    except jwt.InvalidTokenError:
        pass
    return payload
