"""
Flask error handler
"""

from json import dumps
from werkzeug.exceptions import HTTPException

def default_handler(err):
    """Default error handler"""
    if err is not None and err.get_response() is not None:
        response = err.get_response()
        response.data = dumps({
            "code": err.code,
            "name": "System Error",
            "message": err.description
        })
        response.content_type = 'application/json'
    else:
        response = {
            "data": {
                "code": "Error",
                "name": "System Error",
                "message": "Unspecified Error"
            },
            "content_type": "application/json"
        }
    return response

class ValueError(HTTPException):
    """Raised when ... """
    code = 400

class AccessError(HTTPException):
    """Raised when an action which goes against the
    permission principles is executed """
    code = 401
