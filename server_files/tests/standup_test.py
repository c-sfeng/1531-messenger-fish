"""
Test for standup.py
"""

from datetime import datetime, timedelta
from time import sleep
import pytest
from ..api import standup
from ..data import database
from ..exceptions.my_exceptions import AccessError, ValueError
from ..util import pytest_helper, json_time_translator

CHANNEL_NOT_AUTH_USER2 = 1

def reset():
    database.reset_database()

@pytest.fixture
def one_user():
    """Fixture to login one user"""
    reset()
    token = pytest_helper.login_token_owner()
    return {
        "token": token,
        "user": pytest_helper.USER_OWNER
    }

@pytest.fixture
def two_user():
    """Fixture to login three users"""
    reset()
    token1 = pytest_helper.login_token_owner()
    token2 = pytest_helper.login_token_member()
    return {
        "user1": pytest_helper.USER_OWNER,
        "user1_token": token1,
        "user2": pytest_helper.USER_MEMBER,
        "user2_token": token2
    }


# standup_start(token, channel_id)

def test_standup_start_invalidToken(one_user):
    user_token = one_user["token"]
    with pytest.raises(AccessError):
        standup.standup_start(user_token + "yeet", pytest_helper.OWNER_CHANNEL_ID, 3)


def test_standup_start_invalidChannelId(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID + 100000, 3)


def test_standup_start_invalidChannelAccess(two_user):
    user2_token = two_user["user2_token"]
    with pytest.raises(AccessError):
        standup.standup_start(user2_token, CHANNEL_NOT_AUTH_USER2, 3)

def test_standup_start_invalidTime_zero(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 0)

def test_standup_start_invalidTime_negative(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, -1)

def test_standup_start_valid(one_user):
    user_token = one_user["token"]
    length = 3
    # The time returned is within 1 second of 15 minutes from when the function was called
    assert abs(json_time_translator.timestamp_to_datetime(standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, length)["time_finish"]) - datetime.utcnow() - timedelta(seconds=length)) < timedelta(seconds=1)
    sleep(5)  # to purge old timer daemons

def test_standup_start_running(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 5)
    with pytest.raises(ValueError):
        standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 5)
    sleep(5)


# standup_send(token, channel_id, message)

def test_standup_send_invalidToken(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)

    with pytest.raises(AccessError):
        standup.standup_send(user_token + "yeete", pytest_helper.OWNER_CHANNEL_ID, "I did literally no work in the last three days.")
    sleep(3)

def test_standup_send_invalidChannelId(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)

    with pytest.raises(ValueError):
        standup.standup_send(user_token, pytest_helper.OWNER_CHANNEL_ID + 1000000,
                             "I did literally no work in the last three days.")
    sleep(3)

def test_standup_send_invalidChannelAccess(two_user):
    user1_token = two_user["user1_token"]
    user2_token = two_user["user2_token"]
    standup.standup_start(user1_token, CHANNEL_NOT_AUTH_USER2, 3)

    with pytest.raises(AccessError):
        standup.standup_send(user2_token, CHANNEL_NOT_AUTH_USER2,
                             "I did literally no work in the last three days.")
    sleep(3)

def test_standup_send_LongMessage(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)

    with pytest.raises(ValueError):
        standup.standup_send(user_token, pytest_helper.OWNER_CHANNEL_ID,
                             "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. " +
                             "Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque " +
                             "penatibus et magnis dis parturient montes, nascetur ridiculus mus. " +
                             "Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. " +
                             "Nulla consequat massa quis enim. Donec pede justo, fringilla vel, " +
                             "aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet " +
                             "a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. " +
                             "Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean " +
                             "vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, " +
                             "eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, " +
                             "tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. " +
                             "Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper " +
                             "ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget " +
                             "condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque " +
                             "sed ipsumm...")
    sleep(3)

def test_standup_send_emptyMessage(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)

    with pytest.raises(ValueError):
        standup.standup_send(user_token, pytest_helper.OWNER_CHANNEL_ID, "")
    sleep(5)  # purge old timer daemons


def test_standup_send_validMessage(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)
    standup_message = "Today, I wrote some test cases for the new function we are expecting to " +\
                      "implement later this month. I have also finished checking tests I was " +\
                      "assigned to validate."
    assert standup.standup_send(user_token, pytest_helper.OWNER_CHANNEL_ID, standup_message) == {}
    sleep(5)  # Wait for standup to finish
    messages = database.get_all_messages()
    message = messages[-1]
    assert message["message"] == f"STANDUP SUMMARY. Started By: Chicken. Length: 3seconds\n\nMESSAGES:\nChicken: {standup_message}\n"

def test_standup_send_standupNotActive(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        standup.standup_send(user_token, pytest_helper.OWNER_CHANNEL_ID, "I did literally no work in the last three days.")



# Test standup_active(token, channel_id)

def test_standup_active_invalidToken(one_user):
    user_token = one_user["token"]
    with pytest.raises(AccessError):
        standup.standup_active(user_token + "yeet", pytest_helper.OWNER_CHANNEL_ID)

def test_standup_active_invalidChannel(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        standup.standup_active(user_token, pytest_helper.OWNER_CHANNEL_ID + 9999999)


def test_standup_running(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)
    with pytest.raises(ValueError):
        standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)
    sleep(3)

def test_standup_active_notActive(one_user):
    user_token = one_user["token"]
    assert standup.standup_active(user_token, pytest_helper.OWNER_CHANNEL_ID) == {
        "is_active": False,
        "time_finish": None
    }

def test_standup_active_active(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)
    ret = standup.standup_active(user_token, pytest_helper.OWNER_CHANNEL_ID)

    assert ret["is_active"] is True
    assert ret["time_finish"] is not None
    assert json_time_translator.timestamp_to_datetime(ret["time_finish"]) >= datetime.utcnow()
    sleep(3)
    assert json_time_translator.timestamp_to_datetime(ret["time_finish"]) < datetime.utcnow()

def test_standup_collect(one_user):
    user_token = one_user["token"]
    standup.standup_start(user_token, pytest_helper.OWNER_CHANNEL_ID, 3)
    assert standup.standup_collect(user_token, pytest_helper.OWNER_CHANNEL_ID) is None
    sleep(3)

def test_clear():
    database.reset_database()
