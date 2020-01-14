"""
Search Flask wrapper
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.search import search

# Set up Flask Blueprint
SEARCH_API = Blueprint('search_api', __name__)

"""
Flask Routes
"""
@SEARCH_API.route('', methods=['GET'])
def flask_search():
    """Flask wrapper for search"""
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token, query_str))
