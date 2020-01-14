"""
Error message global variables
"""

'''Validation'''
INVALID_TOKEN = "Invalid user token"

INVALID_USER = "Target user is invalid"
INVALID_EMAIL = "Invalid email"
INVALID_NAME_FIRST = "Invalid first name"
INVALID_NAME_LAST = "Invalid last name"
INVALID_NAME = "Invalid name"
INVALID_HANDLE = "Invalid handle"
INVALID_PASS = "Invalid new password"

INVALID_CHANNEL = "Invalid channel ID"

INVALID_MESSAGE = "Invalid message length"

NOT_UNIQUE_EMAIL = "Email is already in use"
NOT_UNIQUE_HANDLE = "Handle is already in use"

""" API FUNCTIONS """

'''admin'''
INVALID_PERM_ID = "Invalid permission ID"
NO_PERMISSION = "You are not authorised to change these permissions"

'''auth'''
WRONG_PASS = "Incorrect password"
EMAIL_NOT_FOUND = "Email not found"
EMPTY_RESET_CODE = "Empty reset code"
INVALID_RESET_CODE = "Invalid reset code"

'''channel'''
CHANNEL_INV_NO_AUTH = "You are not authorised to add people to this channel"
CHANNEL_ALREADY_JOINED = "User is already in channel"
CHANNEL_CANT_VIEW_DETAIL = "You are not authorised to view this channel"
CHANNEL_CANT_VIEW_MSG = "You are not authorised to view this channel's messages"
CHANNEL_NO_MORE_MSG = "No messages left to return in channel"
CHANNEL_ADD_OWNER_NO_AUTH = "You do not have permissions to add owners"
CHANNEL_ALREADY_OWNER = "User is already owner in this channel"
CHANNEL_DEL_OWNER_NO_AUTH = "You do not have permissions to remove owners"
CHANNEL_NOT_OWNER = "The user you are trying to remove is not an owner"

NOT_IN_CHANNEL = "You are not in this channel"

'''channels'''
CHANNEL_LONG_NAME = "Channel name is too long"

'''message'''
MESSAGE_TIME_INVALID = "Message must be set to after the current time"
MESSAGE_SEND_NO_AUTH = "You are not authorised to send messages this channel"
MESSAGE_REMOVE_NOT_EXIST = "The message you are trying to remove does not exist"
MESSAGE_EDIT_NO_AUTH = "You are not authorised to edit messages in this channel"
MESSAGE_EDIT_NOT_EXIST = "The message you are trying to edit does not exist"
INVALID_REACT = "Invalid reaction"
MESSAGE_ALREADY_REACTED = "You have already reacted to this message"
MESSAGE_NOT_REACTED = "You have not reacted to this message"
MESSAGE_PIN_NOT_EXIST = "The message you are trying to pin does not exist"
MESSAGE_PIN_NO_AUTH = "You do not have permissions to pin messages"
MESSAGE_ALREADY_PINNED = "Message is already pinned"
MESSAGE_UNPIN_NOT_EXIST = "The message you are trying to unpin does not exist"
MESSAGE_UNPIN_NO_AUTH = "You do not have permissions to unpin messages"
MESSAGE_NOT_PINNED = "Message is not pinned"

'''search functions'''
# Nothing here

'''standup functions'''
STANDUP_RUNNING = "Standup is currently running in this channel"
STANDUP_NOT_RUNNING = "Standup is not currently running in this channel"
STANDUP_TIME_INVALID = "Standup time must be greater than 0 seconds"

'''user functions'''
IMAGE_NOT_JPG = "Supplied image is not .jpg or .jpeg"
IMAGE_CANT_FETCH = "Unable to fetch image"
INVALID_COORDINATES = "Coordinates outside image size"
INVALID_CROP = "Crop start cannot be greater than or equal to end"
