import pytest
from ..blueprints import search, message
from ..util import pytest_helper
from ..exceptions.my_exceptions import AccessError
from ..data import database

@pytest.fixture
def reset():
    database.reset_database()

'''
    Tests for search
    Given a <query_str> and <token> returns a collection of <messages>
'''

def test_search_short_query():
    """ Case 1: Short query """
    token_owner = pytest_helper.login_token_owner()
    token_member = pytest_helper.login_token_member()
    message.message_react(token_member, 0, 1)
    query_str = "H"
    assert search.search(token_owner, query_str) is not None

def test_search_long_query():
    """ Case 2: Long query """
    token_owner = pytest_helper.login_token_owner()
    message.message_react(token_owner, 0, 1)
    query_str = "Hello everyone! This is a pinned message"
    assert search.search(token_owner, query_str) is not None

def test_search_no_results():
    """ Case 3: No results """
    token = pytest_helper.login_token_owner()
    query_str = "no results will return"
    assert search.search(token, query_str) == {"messages": []}

def test_search_empty_query():
    """ Case 4: Empty query """
    token = pytest_helper.login_token_owner()
    query_str = ""
    assert search.search(token, query_str) == {"messages": []}

def test_search_space():
    """ Case 5: Just a space """
    token = pytest_helper.login_token_owner()
    query_str = " "
    assert search.search(token, query_str) == {"messages": []}

def test_search_multiple_spaces():
    """ Case 6: Multiple spaces """
    token = pytest_helper.login_token_owner()
    query_str = "   "
    assert search.search(token, query_str) == {"messages": []}

def test_search_invalid_token():
    """ Case 7: Invalid token """
    token = pytest_helper.INVALID_TOKEN
    query_str = "est"
    with pytest.raises(AccessError):
        search.search(token, query_str)

def test_wipe():
    database.reset_database()
