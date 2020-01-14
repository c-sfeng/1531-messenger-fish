import pytest
from ..blueprints import echo
from ..data import database

@pytest.fixture
def reset():
    database.reset_database()

"""
Tests for echo_get()
"""
def test_echo_get_string():
    assert echo.echo_get("hello") == {"echo": "hello"}

def test_echo_get_number():
    assert echo.echo_get(48) == {"echo": 48}

def test_echo_get_empty():
    assert echo.echo_post("") == {"echo": ""}


"""
Test for echo_post()
"""
def test_echo_post_string():
    assert echo.echo_post("hello") == {"echo": "hello"}

def test_echo_post_number():
    assert echo.echo_post(48) == {"echo": 48}

def test_echo_post_empty():
    assert echo.echo_post("") == {"echo": ""}
