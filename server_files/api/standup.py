"""
Standup functions
"""

# Library set-up
from datetime import datetime, timedelta
from threading import Timer
from server_files.data import database
from server_files.blueprints import message as msg
from server_files.util import jwt_handler, json_time_translator, validator
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, INVALID_CHANNEL, INVALID_MESSAGE, CHANNEL_CANT_VIEW_DETAIL, STANDUP_RUNNING,\
    STANDUP_NOT_RUNNING, STANDUP_TIME_INVALID

"""
Checking and collating functions
"""


def is_standup_running(channel_id):
    """Returns true if standup is running in this channel, flase otherwise"""
    time_end = database.get_standup_finish_time(channel_id)
    if time_end is not None and\
            json_time_translator.json_to_datetime(time_end) >= datetime.utcnow():
        return True
    return False


def standup_collect(token, channel_id):
    """Collect and collate standup messages, returns collated message"""
    if not is_standup_running(channel_id):
        u_id = jwt_handler.decode_token(token)
        starter = database.get_user_by_id(u_id)
        standup_info = database.get_standup_channel_info(channel_id)
        output_msg = f"STANDUP SUMMARY. Started By: {starter['handle']}. " +\
                     f"Length: {standup_info['length']}seconds\n\n" +\
                     f"MESSAGES:\n"
        for message in standup_info["messages"]:
            user = database.get_user_by_id(message["u_id"])
            output_msg = output_msg + f"{user['handle']}: "
            output_msg = output_msg + f"{message['message']}\n"
        database.wipe_standup_messages(channel_id)
        return output_msg
    return None


def standup_end_action(token, channel_id):
    """Collates standups and returns the message if standup has ended"""
    if not is_standup_running(channel_id):
        # print the stuff into channel
        message = standup_collect(token, channel_id)

        # This may break if the user signs out
        msg.message_send(token, channel_id, message)


def standup_timer_start(token, channel_id, length):
    """Starts a threaded timer that is scheduled to print the collated standup message"""
    timer = Timer(length + 1, standup_end_action, [token, channel_id])
    timer.daemon = True
    timer.start()


"""
API Functions
"""


def standup_start(token, channel_id, length):
    """Will return standup finish time if user and channel are both valid"""
    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    length = int(length)

    # Check channel existence
    channel = database.get_channel_by_id(channel_id)
    if channel is None:
        raise ValueError(INVALID_CHANNEL)

    # Check user is member of channel
    u_id = jwt_handler.decode_token(token)
    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    # Check the startup is not currently active in this channel
    old_time_end = database.get_standup_finish_time(channel_id)
    if old_time_end is not None and\
            json_time_translator.json_to_datetime(old_time_end) >= datetime.utcnow():
        raise ValueError(STANDUP_RUNNING)

    # Check for non-zero length
    if length <= 0:
        raise ValueError(STANDUP_TIME_INVALID)

    # Set channel standup_end to now+X min and add finish time to database
    time_end_datetime = datetime.utcnow() + timedelta(seconds=length)
    time_end_json = json_time_translator.datetime_to_json(time_end_datetime)

    # Move old standup messages
    database.move_standup_to_unused_by_id(channel_id)

    database.update_standup_by_id(channel_id, {
        "time_finish": time_end_json,
        "length": length
    })

    time_end_timestamp = int(json_time_translator.datetime_to_timestamp(
        time_end_datetime
    ))

    # Start threaded timer
    standup_timer_start(token, channel_id, length)

    return {"time_finish": time_end_timestamp}


def standup_active(token, channel_id):
    """Adds message to standup buffer if standup is currently active"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Check channel existence
    channel = database.get_channel_by_id(channel_id)
    if channel is None:
        raise ValueError(INVALID_CHANNEL)

    is_active = is_standup_running(channel_id)
    time_finish = None
    if is_active:
        time_finish = int(json_time_translator.json_to_timestamp(
            database.get_standup_finish_time(channel_id)
        ))

    return {
        "is_active": is_active,
        "time_finish": time_finish
    }


def standup_send(token, channel_id, message):
    """Adds message to standup buffer if standup is currently active"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Check channel existence
    channel = database.get_channel_by_id(channel_id)
    if channel is None:
        raise ValueError(INVALID_CHANNEL)

    # Check user is member of channel
    u_id = jwt_handler.decode_token(token)
    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    # Check the startup is not currently active in this channel
    old_time_end = database.get_standup_finish_time(channel_id)
    if old_time_end is None or\
            json_time_translator.json_to_datetime(old_time_end) < datetime.utcnow():
        raise ValueError(STANDUP_NOT_RUNNING)

    # Check valid message
    if not validator.is_valid_message(message):
        raise ValueError(INVALID_MESSAGE)

    # Save message
    database.add_standup_message(channel_id, {
        "u_id": u_id,
        "message": message,
        "time_created": json_time_translator.datetime_to_json(datetime.utcnow()),
    })

    return {}
