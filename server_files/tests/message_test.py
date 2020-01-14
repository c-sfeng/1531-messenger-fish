from datetime import datetime, timedelta
import pytest
from ..blueprints import message
from ..util import pytest_helper, json_time_translator
from ..exceptions.my_exceptions import AccessError, ValueError
from ..data import database


@pytest.fixture
def reset():
    database.reset_database()


"""
Tests for message_sendlater()
"""


def test_message_sendlater_long_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = pytest_helper.MESSAGE_1001
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    with pytest.raises(ValueError):
        assert message.message_sendlater(token, chan, msg, future)


def test_message_sendlater_nearly_long_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = pytest_helper.MESSAGE_1000
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    msg_id = message.message_sendlater(token, chan, msg, future)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}


def test_message_sendlater_past_timestamp(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2018-10-27T05:00:58.524353")
    with pytest.raises(ValueError):
        assert message.message_sendlater(token, chan, msg, future)


def test_message_sendlater_no_previous_messages(reset):
    token = pytest_helper.login_token_admin()
    chan = pytest_helper.PRIVATE_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    msg_id = message.message_sendlater(token, chan, msg, future)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}


def test_message_sendlater_invalid_channel(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.INVALID_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    with pytest.raises(ValueError):
        assert message.message_sendlater(token, chan, msg, future)


def test_message_sendlater_invalid_token(reset):
    token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    with pytest.raises(AccessError):
        assert message.message_sendlater(token, chan, msg, future)


def test_message_sendlater_unauthorised(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    with pytest.raises(AccessError):
        assert message.message_sendlater(token, chan, msg, future)


def test_message_sendlater_before_sendlater(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    future_far = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    future_near = json_time_translator.json_to_timestamp(
        "2020-10-27T05:00:58.524353")
    msg_id1 = message.message_sendlater(token, chan, msg, future_far)["message_id"]
    msg_id2 = message.message_sendlater(token, chan, msg, future_near)["message_id"]
    assert isinstance(msg_id1, int)
    assert isinstance(msg_id2, int)

    chan_messages = database.get_channel_by_id(chan)["messages"]
    assert chan_messages[-1] == msg_id1
    assert chan_messages[-2] == msg_id2

    assert message.message_remove(token, msg_id1) == {}
    assert message.message_remove(token, msg_id2) == {}


def test_message_sendlater_beforeall(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    # Remove all messages
    database.update_channel_by_id(chan, {
        "messages": []
    })
    msg = "This is a short message"
    future_near = json_time_translator.json_to_timestamp(
        "2020-10-27T05:00:58.524353")
    future_far = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    future_world_end = json_time_translator.json_to_timestamp(
        "2222-10-27T05:00:58.524353")
    msg_id1 = message.message_sendlater(token, chan, msg, future_world_end)["message_id"]
    msg_id2 = message.message_sendlater(token, chan, msg, future_far)["message_id"]
    msg_id3 = message.message_sendlater(token, chan, msg, future_near)["message_id"]
    assert isinstance(msg_id1, int)
    assert isinstance(msg_id2, int)
    assert isinstance(msg_id3, int)

    chan_messages = database.get_channel_by_id(chan)["messages"]
    assert chan_messages[-1] == msg_id1
    assert chan_messages[-2] == msg_id2
    assert chan_messages[-3] == msg_id3

    assert message.message_remove(token, msg_id1) == {}
    assert message.message_remove(token, msg_id2) == {}
    assert message.message_remove(token, msg_id3) == {}


def test_message_sendlater_ideal_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    future = json_time_translator.json_to_timestamp(
        "2021-10-27T05:00:58.524353")
    msg_id = message.message_sendlater(token, chan, msg, future)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}


"""
Tests for message_send()
"""


def test_message_send_long_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = pytest_helper.MESSAGE_1001
    with pytest.raises(ValueError):
        assert message.message_send(token, chan, msg)


def test_message_send_nearly_long_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = pytest_helper.MESSAGE_1000
    msg_id = message.message_send(token, chan, msg)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}


def test_message_send_invalid_channel(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.INVALID_CHANNEL_ID
    msg = "This is a short message"
    with pytest.raises(ValueError):
        assert message.message_send(token, chan, msg)


def test_message_send_invalid_token(reset):
    token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    with pytest.raises(AccessError):
        assert message.message_send(token, chan, msg)


def test_message_send_unauthorised(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is a short message"
    with pytest.raises(AccessError):
        assert message.message_send(token, chan, msg)


def test_message_send_no_previous_messages(reset):
    token = pytest_helper.login_token_admin()
    chan = pytest_helper.PRIVATE_CHANNEL_ID
    msg = "This is a short message"
    msg_id = message.message_send(token, chan, msg)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}


def test_message_send_ideal_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a short message"
    msg_id = message.message_send(token, chan, msg)["message_id"]
    assert isinstance(msg_id, int)
    assert message.message_remove(token, msg_id) == {}

def test_message_send_before_futuremsg(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    future = json_time_translator.datetime_to_timestamp(datetime.utcnow() + timedelta(seconds=2))
    msg_id1 = message.message_sendlater(token, chan, "uwu", future)["message_id"]
    msg = "This is a short message"
    msg_id2 = message.message_send(token, chan, msg)["message_id"]
    assert isinstance(msg_id2, int)
    chan_messages = database.get_channel_by_id(chan)["messages"]
    assert chan_messages[-1] == msg_id1
    assert chan_messages[-2] == msg_id2

    assert message.message_remove(token, msg_id1) == {}
    assert message.message_remove(token, msg_id2) == {}

"""
Tests for message_remove
"""


def test_message_remove_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.OWNER_CHANNEL_ID
    msg = "This is a short message"
    msg_id = message.message_send(valid_token, chan, msg)["message_id"]
    with pytest.raises(AccessError):
        assert message.message_remove(invalid_token, msg_id)
    message.message_remove(valid_token, msg_id)


def test_message_remove_invalid_message_1(reset):
    token = pytest_helper.login_token_owner()
    msg_id = pytest_helper.INVALID_MESSAGE_ID
    with pytest.raises(ValueError):
        assert message.message_remove(token, msg_id)


def test_message_remove_invalid_message_2(reset):
    token = pytest_helper.login_token_owner()
    msg_id = "-1"
    with pytest.raises(ValueError):
        assert message.message_remove(token, msg_id)


def test_message_remove_unauthorised(reset):
    authorised_token = pytest_helper.login_token_owner()
    unauthorised_token = pytest_helper.login_token_member()
    # The below msg_id is authorised for login_token_owner, but for no other
    # member-level user
    chan = pytest_helper.OWNER_CHANNEL_ID
    msg = "This is a short message"
    msg_id = message.message_send(authorised_token, chan, msg)["message_id"]
    with pytest.raises(AccessError):
        assert message.message_remove(unauthorised_token, msg_id)
    message.message_remove(authorised_token, msg_id)


def test_message_remove_ideal(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.OWNER_CHANNEL_ID
    msg = "This is a short message"
    msg_id = message.message_send(token, chan, msg)["message_id"]
    assert message.message_remove(token, msg_id) == {}


"""
Tests for message_edit()
"""


def test_message_edit_long_message(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    original_msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, original_msg)["message_id"]
    # Edit the message
    edited_msg = pytest_helper.MESSAGE_1001
    with pytest.raises(ValueError):
        assert message.message_edit(token, msg_id, edited_msg)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_edit_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    original_msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(
        valid_token, chan, original_msg)["message_id"]
    # Edit the message
    edited_msg = "This is an edited message"
    with pytest.raises(AccessError):
        assert message.message_edit(invalid_token, msg_id, edited_msg)
    # Clean up
    message.message_remove(valid_token, msg_id)


def test_message_edit_invalid_message_id(reset):
    token = pytest_helper.login_token_owner()
    msg_id = pytest_helper.INVALID_MESSAGE_ID
    edited_msg = "This is an edited message"
    with pytest.raises(ValueError):
        assert message.message_edit(token, msg_id, edited_msg)


def test_message_edit_unauthorised(reset):
    authorised_token = pytest_helper.login_token_owner()
    unauthorised_token = pytest_helper.login_token_member()
    chan = pytest_helper.OWNER_CHANNEL_ID
    original_msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(
        authorised_token, chan, original_msg)["message_id"]
    # Edit the message
    edited_msg = "This is an edited message"
    with pytest.raises(AccessError):
        assert message.message_edit(unauthorised_token, msg_id, edited_msg)
    # Clean up
    message.message_remove(authorised_token, msg_id)


def test_message_edit_ideal(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    original_msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, original_msg)["message_id"]
    # Edit the message
    edited_msg = "This is an edited message"
    assert message.message_edit(token, msg_id, edited_msg) == {}
    # Clean up
    message.message_remove(token, msg_id)


def test_message_empty(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    original_msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, original_msg)["message_id"]
    # Edit the message with an empty string
    empty_message = ""
    assert message.message_edit(token, msg_id, empty_message) == {}
    # When this message is attempted to be deleted again, error should be
    # returned
    with pytest.raises(ValueError):
        assert message.message_remove(token, msg_id)


"""
Tests for message_react()
"""


def test_message_react_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(valid_token, chan, msg)["message_id"]
    # React to message
    with pytest.raises(AccessError):
        assert message.message_react(
            invalid_token, msg_id, pytest_helper.VALID_REACT_ID)
    # Clean up
    message.message_remove(valid_token, msg_id)


def test_message_react_invalid_target_message_1(reset):
    target_token = pytest_helper.login_token_owner()
    other_token = pytest_helper.login_token_member()
    # other_token is present in chan, but not target_chan
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    react_id = pytest_helper.VALID_REACT_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(other_token, chan, msg)["message_id"]
    # React to message
    with pytest.raises(AccessError):
        assert message.message_react(target_token, msg_id, react_id)
    # Clean up
    message.message_remove(other_token, msg_id)


def test_message_react_invalid_target_message_2(reset):
    target_token = pytest_helper.login_token_owner()
    other_token = pytest_helper.login_token_member()
    # other_token is present in chan, but not target_chan
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    react_id = pytest_helper.VALID_REACT_ID
    msg = "This is the original message"
    # Send the message, however as a string
    msg_id = message.message_send(other_token, chan, msg)["message_id"]
    msg_id = str(msg_id)
    # React to message
    with pytest.raises(AccessError):
        assert message.message_react(target_token, msg_id, react_id)
    # Clean up
    message.message_remove(other_token, msg_id)


def test_message_react_invalid_react_1(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    with pytest.raises(ValueError):
        assert message.message_react(
            token, msg_id, pytest_helper.INVALID_REACT_ID)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_react_invalid_react_2(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message with the react id as a string
    with pytest.raises(ValueError):
        assert message.message_react(
            token, msg_id, str(pytest_helper.INVALID_REACT_ID))
    # Clean up
    message.message_remove(token, msg_id)


def test_message_react_existing_react(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    message.message_react(token, msg_id, pytest_helper.VALID_REACT_ID)
    # Try to react again
    with pytest.raises(ValueError):
        assert message.message_react(
            token, msg_id, pytest_helper.VALID_REACT_ID)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_react_first_react(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    react_id = pytest_helper.VALID_REACT_ID
    assert message.message_react(token, msg_id, react_id) == {}
    # Clean up
    message.message_remove(token, msg_id)


def test_message_react_additional_react(reset):
    token_1 = pytest_helper.login_token_owner()
    token_2 = pytest_helper.login_token_member()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token_1, chan, msg)["message_id"]
    # React to message using two different tokens
    react_id = pytest_helper.VALID_REACT_ID
    assert message.message_react(token_1, msg_id, react_id) == {}
    assert message.message_react(token_2, msg_id, react_id) == {}
    # Clean up
    message.message_remove(token_1, msg_id)


"""
Tests for message_unreact()
"""


def test_message_unreact_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(valid_token, chan, msg)["message_id"]
    # React to message
    react_id = pytest_helper.VALID_REACT_ID
    message.message_react(valid_token, msg_id, react_id)
    # Unreact to message
    with pytest.raises(AccessError):
        assert message.message_unreact(invalid_token, msg_id, react_id)
    # Clean up
    message.message_remove(valid_token, msg_id)


def test_message_unreact_invalid_target_message_1(reset):
    target_token = pytest_helper.login_token_owner()
    other_token = pytest_helper.login_token_member()
    # other_token is present in chan, but not target_chan
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(other_token, chan, msg)["message_id"]
    # React to message
    react_id = pytest_helper.VALID_REACT_ID
    message.message_react(other_token, msg_id, react_id)
    # Unreact to message
    with pytest.raises(AccessError):
        assert message.message_unreact(target_token, msg_id, react_id)
    # Clean up
    message.message_remove(other_token, msg_id)


def test_message_unreact_invalid_target_message_2(reset):
    target_token = pytest_helper.login_token_owner()
    other_token = pytest_helper.login_token_member()
    # other_token is present in chan, but not target_chan
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message, however with the id as a string
    msg_id = message.message_send(other_token, chan, msg)["message_id"]
    msg_id = str(msg_id)
    # React to message
    react_id = pytest_helper.VALID_REACT_ID
    message.message_react(other_token, msg_id, react_id)
    # Unreact to message
    with pytest.raises(AccessError):
        assert message.message_unreact(target_token, msg_id, react_id)
    # Clean up
    message.message_remove(other_token, msg_id)


def test_message_unreact_invalid_react_1(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    valid_react_id = pytest_helper.VALID_REACT_ID
    invalid_react_id = pytest_helper.INVALID_REACT_ID
    message.message_react(token, msg_id, valid_react_id)
    # Unreact to message
    with pytest.raises(ValueError):
        assert message.message_unreact(token, msg_id, invalid_react_id)
    # Clean up
    message.message_remove(token, msg_id)

def test_message_unreact_invalid_react_2(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    valid_react_id = pytest_helper.VALID_REACT_ID
    invalid_react_id = pytest_helper.INVALID_REACT_ID
    message.message_react(token, msg_id, valid_react_id)
    # Unreact to message, however with the id as a string
    with pytest.raises(ValueError):
        assert message.message_unreact(token, msg_id, str(invalid_react_id))
    # Clean up
    message.message_remove(token, msg_id)


def test_message_unreact_no_react(reset):
    token = pytest_helper.login_token_owner()
    another_token = pytest_helper.login_token_member()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message using someone else's token
    react_id = pytest_helper.VALID_REACT_ID
    message.message_react(another_token, msg_id, react_id)
    # Unreact to message
    with pytest.raises(ValueError):
        assert message.message_unreact(token, msg_id, react_id)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_unreact_non_existing_react(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Unreact to message
    react_id = pytest_helper.VALID_REACT_ID
    with pytest.raises(ValueError):
        assert message.message_unreact(token, msg_id, react_id)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_unreact_ideal(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is the original message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # React to message
    react_id = pytest_helper.VALID_REACT_ID
    message.message_react(token, msg_id, react_id)
    # Unreact to message
    assert message.message_unreact(token, msg_id, react_id) == {}
    # Clean up
    message.message_remove(token, msg_id)


"""
Tests for message_pin()
"""


def test_message_pin_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(valid_token, chan, msg)["message_id"]
    # Pin the message
    with pytest.raises(AccessError):
        assert message.message_pin(invalid_token, msg_id)
    # Clean up
    message.message_remove(valid_token, msg_id)


def test_message_pin_invalid_message(reset):
    target_token = pytest_helper.login_token_owner()
    msg_id = pytest_helper.INVALID_MESSAGE_ID
    with pytest.raises(ValueError):
        assert message.message_pin(target_token, msg_id)


def test_message_pin_insufficient_permissions(reset):
    token = pytest_helper.login_token_member()
    # Note: login_token_member is a member of UNAUTH_CHANNEL_ID
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Pin the message
    with pytest.raises(ValueError):
        assert message.message_pin(token, msg_id)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_pin_unauthorised(reset):
    unauthorised_token = pytest_helper.login_token_owner()
    authorised_token = pytest_helper.login_token_admin()
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(authorised_token, chan, msg)["message_id"]
    # Pin the message
    with pytest.raises(AccessError):
        assert message.message_pin(unauthorised_token, msg_id)
    # Clean up
    message.message_remove(authorised_token, msg_id)


def test_message_pin_already_pinned(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Pin the message, then try pinning again
    message.message_pin(token, msg_id)
    with pytest.raises(ValueError):
        assert message.message_pin(token, msg_id)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_pin_ideal(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Pin the message
    assert message.message_pin(token, msg_id) == {}
    # Clean up
    message.message_remove(token, msg_id)


"""
Tests for message_unpin()
"""


def test_message_unpin_invalid_token(reset):
    valid_token = pytest_helper.login_token_owner()
    invalid_token = pytest_helper.INVALID_TOKEN
    chan = pytest_helper.OWNER_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(valid_token, chan, msg)["message_id"]
    # Pin the message
    message.message_pin(valid_token, msg_id)
    # Unpin the message
    with pytest.raises(ValueError):
        assert message.message_unpin(invalid_token, msg_id)
    # Clean up
    message.message_remove(valid_token, msg_id)


def test_message_unpin_invalid_message(reset):
    target_token = pytest_helper.login_token_owner()
    msg_id = pytest_helper.INVALID_MESSAGE_ID
    with pytest.raises(ValueError):
        assert message.message_unpin(target_token, msg_id)


def test_message_unpin_insufficient_permissions(reset):
    owner_token = pytest_helper.login_token_owner()
    member_token = pytest_helper.login_token_member()
    chan = pytest_helper.OWNER_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(owner_token, chan, msg)["message_id"]
    # Pin the message
    message.message_pin(owner_token, msg_id)
    # Unpin the message
    with pytest.raises(AccessError):
        assert message.message_unpin(member_token, msg_id)
    # Clean up
    message.message_remove(owner_token, msg_id)


def test_message_unpin_unauthorised(reset):
    unauthorised_token = pytest_helper.login_token_owner()
    authorised_token = pytest_helper.login_token_admin()
    chan = pytest_helper.UNAUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(authorised_token, chan, msg)["message_id"]
    # Unpin the message
    with pytest.raises(AccessError):
        assert message.message_unpin(unauthorised_token, msg_id)
    # Clean up
    message.message_remove(authorised_token, msg_id)


def test_message_unpin_already_pinned(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Pin the message
    message.message_pin(token, msg_id)
    # Unpin the message, then try unpinning again
    message.message_unpin(token, msg_id)
    with pytest.raises(ValueError):
        assert message.message_unpin(token, msg_id)
    # Clean up
    message.message_remove(token, msg_id)


def test_message_unpin_ideal(reset):
    token = pytest_helper.login_token_owner()
    chan = pytest_helper.AUTH_CHANNEL_ID
    msg = "This is a message"
    # Send the message
    msg_id = message.message_send(token, chan, msg)["message_id"]
    # Pin the message
    message.message_pin(token, msg_id)
    # Unin the message
    assert message.message_unpin(token, msg_id) == {}
    # Clean up
    message.message_remove(token, msg_id)


def test_clear_tokens():
    database.reset_database()
