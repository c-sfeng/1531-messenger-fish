import pytest
from ..blueprints import channels
from ..util import pytest_helper
from ..exceptions.my_exceptions import AccessError, ValueError
from ..data import database


@pytest.fixture
def reset():
    database.reset_database()


"""
Tests for channels_list
"""


def test_channels_list_invalid_token():
    token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        assert channels.channels_list(token)


def test_channels_list_valid_token():
    token = pytest_helper.login_token_owner()
    assert channels.channels_list(token) == {
        "channels": [
            {
                "channel_id": 0,
                "name": "#general"
            },
            {
                "channel_id": 1,
                "name": "#slackr_admins"
            },
            {
                "channel_id": 4,
                "name": "comp3331"
            },
        ]
    }


"""
Tests for channels_listall
"""


def test_channels_listall_invalid_token():
    token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        assert channels.channels_listall(token)


def test_channels_listall_valid_token():
    token = pytest_helper.login_token_owner()
    result = channels.channels_listall(token)
    assert result == {'channels':
                      [
                          {'channel_id': 0, 'name': '#general'},
                          {'channel_id': 1, 'name': '#slackr_admins'},
                          {'channel_id': 2, 'name': '#comp1531'},
                          {'channel_id': 3, 'name': '#comp1531_group'},
                          {'channel_id': 4, 'name': 'comp3331'},
                          {'channel_id': 5, 'name': '#spam'}]}


"""
Tests for channels_create
"""


def test_channels_create_invalid_token():
    token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channels.channels_create(token, "test channel", "true")


def test_channels_create_invalid_channel_name():
    token = pytest_helper.login_token_owner()
    channel_name = "This is a wayyyyyyy too long of a channel name"
    with pytest.raises(ValueError):
        assert channels.channels_create(token, channel_name, "true")


def test_channels_create_ideal():
    token = pytest_helper.login_token_owner()
    assert channels.channels_create(token, "test channel", "true") == {
        "channel_id": 6
    }


def test_clear_tokens():
    database.reset_database()
