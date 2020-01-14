"""
Database interface functions for interacting with database
"""
import json
import os
import glob
import shutil

"""
get_all Functions
"""
def get_all_channels():
    """Returns all channels"""
    with open("server_files/data/channels.json", "r") as data_file:
        data = json.load(data_file)
        return data["channels"]


def get_all_messages():
    """Returns all messages"""
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        return data["messages"]


def get_all_standups():
    """Returns all standup messages"""
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        return data["standups"]


def get_all_reacts(message_id):
    """Returns all reacts for a message"""
    if not isinstance(message_id, int):
        message_id = int(message_id)
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        for msg in data["messages"]:
            if msg["message_id"] == message_id:
                return msg["reacts"]
    return None

def get_all_users():
    """Returns all users"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        return data["users"]


"""
get_by_id Functions
"""
def get_channel_by_id(param_id):
    """Returns channel corresponding to the channel_id"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/channels.json", "r") as data_file:
        data = json.load(data_file)
        channels = data["channels"]
        for chnl in channels:
            if chnl["channel_id"] == param_id:
                print(chnl)
                return chnl
    return None


def get_message_by_id(param_id):
    """Returns message correspondong to message_id"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        messages = data["messages"]
        for msg in messages:
            if msg["message_id"] == param_id:
                return msg
    return None


def get_user_by_id(param_id):
    """Returns user corresponding to u_id"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        users = data["users"]
        for usr in users:
            if usr["u_id"] == param_id:
                return usr
    return None


"""
update_by_id Functions
"""
def update_channel_by_id(param_id, new):
    """Updates channel, corresponding with channel_id, with
    dictionary with updated values"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/channels.json", "r") as data_file:
        data = json.load(data_file)
        channels = data["channels"]
        for chnl in channels:
            if chnl["channel_id"] == param_id:
                chnl.update(new)
                break
        open("server_files/data/channels.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def update_message_by_id(param_id, new):
    """Updates message, corresponding with message_id, with
    dictionary with updated values"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        messages = data["messages"]
        for msg in messages:
            if msg["message_id"] == param_id:
                msg.update(new)
                break
        open("server_files/data/messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def update_standup_by_id(channel_id, new):
    """Updates standup data, corresponding with channel_id, with
    dictionary with updated values"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standup = data["standups"]
        found = False
        for stdp in standup:
            if stdp["channel_id"] == channel_id:
                stdp.update(new)
                found = True
                break

        # If no channel found in standups
        if not found:
            standup.append({
                "channel_id": channel_id,
                "time_finish": None,
                "messages": [],
                "length": None
            })
            standup[len(standup) - 1].update(new)
        open("server_files/data/standup_messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def update_user_by_id(param_id, new):
    """Updates user, corresponding with u_id, with
    dictionary with updated values"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        users = data["users"]
        for usr in users:
            if usr["u_id"] == param_id:
                usr.update(new)
                break
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )

"""
add Functions
"""
def add_channel(new):
    """Appends a new channel to database"""
    with open("server_files/data/channels.json", "r") as data_file:
        data = json.load(data_file)
        channels = data["channels"]

        new["channel_id"] = data["index"]
        channels.append(new)
        data["index"] += 1

        open("server_files/data/channels.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )
        return new["channel_id"]


def add_message(new):
    """Appends a new message to database"""
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        messages = data["messages"]

        new["message_id"] = data["index"]
        messages.append(new)
        data["index"] += 1

        open("server_files/data/messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )
        return new["message_id"]

def add_standup_message(channel_id, new):
    """Appends a new standup message to database"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standup = data["standups"]

        for stdp in standup:
            if stdp["channel_id"] == channel_id:
                stdp["messages"].append(new)
                break

        open("server_files/data/standup_messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def add_user(new):
    """Appends a new user to database"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        users = data["users"]

        new["u_id"] = data["index"]
        users.append(new)
        data["index"] += 1

        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )
        return new["u_id"]

"""
delete_by_id Functions
"""
def delete_channel_by_id(param_id):
    """Deletes channel, corresponding to channel_id, from database"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/channels.json", "r") as data_file:
        data = json.load(data_file)
        channels = data["channels"]
        index = 0
        for chnl in channels:
            if chnl["channel_id"] == param_id:
                channels.pop(index)
                break
            index += 1
        open("server_files/data/channels.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def delete_message_by_id(param_id):
    """Deletes message, corresponding to message_id, from database"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/messages.json", "r") as data_file:
        data = json.load(data_file)
        messages = data["messages"]
        index = 0
        for msg in messages:
            if msg["message_id"] == param_id:
                messages.pop(index)
                break
            index += 1
        open("server_files/data/messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def delete_user_by_id(param_id):
    """Deletes user, corresponding to u_id, from database"""
    if not isinstance(param_id, int):
        param_id = int(param_id)
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        users = data["users"]
        index = 0
        for usr in users:
            if usr["u_id"] == param_id:
                users.pop(index)
                break
            index += 1
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


"""
Other Interface Functions
"""
def wipe_tokens():
    """Wipes tokens from users, run every time server starts up"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        for user in data["users"]:
            user["tokens"] = []
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def wipe_standup_messages(channel_id):
    """Wipes standup messages, run after collating messages"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standup = data["standups"]
        for stdp in standup:
            if stdp["channel_id"] == channel_id:
                data["standups"].remove(stdp)

        open("server_files/data/standup_messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )

def get_standup_channel_info(channel_id):
    """Gets standup information for given channel with corresponding
    channel_id"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standup = data["standups"]
        for stdp in standup:
            if stdp["channel_id"] == channel_id:
                return stdp
    return None

def get_standup_messages(channel_id):
    """Returns all standup messages given channel_id"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standup = data["standups"]
        for stdp in standup:
            if stdp["channel_id"] == channel_id:
                return stdp["messages"]
    return None


def get_standup_finish_time(channel_id):
    """Returns standup finish time given channel_id"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standups = data["standups"]
        for stdp in standups:
            if stdp["channel_id"] == channel_id:
                return stdp["time_finish"]
    return None


def get_standup_length(channel_id):
    """Returns standup length given channel_id, in seconds"""
    if not isinstance(channel_id, int):
        channel_id = int(channel_id)
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standups = data["standups"]
        for stdp in standups:
            if stdp["channel_id"] == channel_id:
                return int(stdp["length"])
    return None

def move_standup_to_unused_by_id(channel_id):
    '''Moves all unused standups into unused_msg'''
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        standups = data["standups"]
        if "unused_msg" not in data.keys():
            data["unused_msg"] = []
        # Find channel
        for standup in standups:
            if standup["channel_id"] == channel_id:
                data["unused_msg"].append(standup)
                data["standups"].remove(standup)
        # Update database
        open("server_files/data/standup_messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )

def move_all_standup_to_unused():
    '''Moves all unused standups into unused_msg'''
    with open("server_files/data/standup_messages.json", "r") as data_file:
        data = json.load(data_file)
        # Move all unsent standups to `unused_msg`
        standups = data["standups"]
        if "unused_msg" not in data.keys():
            data["unused_msg"] = []
        data["unused_msg"].extend(standups)
        data["standups"] = []
        # Update database
        open("server_files/data/standup_messages.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )

"""
Database reset functions
"""
def reset_database():
    '''Resets database to backup database'''
    backup_channels = "server_files/data/backup/channels.json"
    backup_messages = "server_files/data/backup/messages.json"
    backup_standup_messages = "server_files/data/backup/standup_messages.json"
    backup_users = "server_files/data/backup/users.json"
    actual_channels = "server_files/data/channels.json"
    actual_messages = "server_files/data/messages.json"
    actual_standup_messages = "server_files/data/standup_messages.json"
    actual_users = "server_files/data/users.json"

    channels_data = json.load(open(backup_channels, "r"))
    messages_data = json.load(open(backup_messages, "r"))
    standup_messages_data = json.load(open(backup_standup_messages, "r"))
    users_data = json.load(open(backup_users, "r"))

    open(actual_channels, "w").write(
        json.dumps(channels_data, sort_keys=True, indent=4, separators=(',', ': '))
    )
    open(actual_messages, "w").write(
        json.dumps(messages_data, sort_keys=True, indent=4, separators=(',', ': '))
    )
    open(actual_standup_messages, "w").write(
        json.dumps(standup_messages_data, sort_keys=True, indent=4, separators=(',', ': '))
    )
    open(actual_users, "w").write(
        json.dumps(users_data, sort_keys=True, indent=4, separators=(',', ': '))
    )

    # Only works from source directory
    # Remove new images
    for file in glob.glob("server_files/static/*.jpg"):
        os.remove(file)
    for file in glob.glob("server_files/static/*.jpeg"):
        os.remove(file)

    # Replace with backup images
    src = "server_files/data/backup/static"
    dest = "server_files/static/"
    src_files = os.listdir(src)
    for file_name in src_files:
        file_path = os.path.join(src, file_name)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)
