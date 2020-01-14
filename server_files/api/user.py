"""
User functions
"""

# Library set-up
from urllib.request import urlretrieve
from datetime import datetime
from PIL import Image
from server_files.data import database
from server_files.util import jwt_handler
from server_files.util import validator
from server_files.util import json_time_translator
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, INVALID_USER, INVALID_NAME, INVALID_EMAIL, NOT_UNIQUE_EMAIL,\
    INVALID_HANDLE, NOT_UNIQUE_HANDLE, IMAGE_NOT_JPG, IMAGE_CANT_FETCH,\
    INVALID_COORDINATES, INVALID_CROP

"""
API Functions
"""


def user_profile(token, u_id):
    """For a valid user, returns information about their email, first name,
    last name, and handle"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Check u_id is valid
    if not validator.is_valid_user(u_id):
        raise ValueError(INVALID_USER)

    # Return user profile
    user = database.get_user_by_id(u_id)
    return {
        "email": user["email"],
        "name_first": user["name_first"],
        "name_last": user["name_last"],
        "handle_str": user["handle"],
        "profile_img_url": user["profile_img_url"]
    }


def user_profile_setname(token, name_first, name_last):
    """Update the authorised user's first and last name"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    u_id = jwt_handler.decode_token(token)

    # Check Valid input Name
    if not validator.is_valid_name(name_first) or not validator.is_valid_name(name_last):
        raise ValueError(INVALID_NAME)

    # Update the database with new changes
    database.update_user_by_id(u_id, {
        "name_first": name_first,
        "name_last": name_last
    })

    return {}


def user_profile_setemail(token, email):
    """Update the authorised user's email address"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    u_id = jwt_handler.decode_token(token)

    # Check valid email
    if not validator.is_valid_email(email):
        raise ValueError(INVALID_EMAIL)

    # Check that email is not already in use
    if not validator.is_unique_email(email):
        raise ValueError(NOT_UNIQUE_EMAIL)

    # Update the database with new changes
    database.update_user_by_id(u_id, {
        "email": email
    })

    return {}


def user_profile_sethandle(token, handle_str):
    """Update the authorised user's handle (i.e. display name)"""

    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    u_id = jwt_handler.decode_token(token)

    # Check valid handle
    if not validator.is_valid_handle(handle_str):
        raise ValueError(INVALID_HANDLE)

    # Check if handle is already in use
    if not validator.is_unique_handle(handle_str):
        raise ValueError(NOT_UNIQUE_HANDLE)

    # Update the database with new changes
    database.update_user_by_id(u_id, {
        "handle": handle_str
    })

    return {}


def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """Given a URL of an image on the internet, crops the image within bounds
    (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left."""
    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)


    if img_url[-3:].lower() != "jpg" and img_url[-4:].lower() != "jpeg":
        raise ValueError(IMAGE_NOT_JPG)

    # Save Image
    file_name = json_time_translator.datetime_to_timestamp(datetime.utcnow())
    local_url = f"server_files/static/{file_name}"
    try:
        urlretrieve(img_url, local_url + ".jpg")
    except Exception:
        raise ValueError(IMAGE_CANT_FETCH)

    image_object = Image.open(local_url + ".jpg")

    width, height = image_object.size
    if not 0 <= x_start < width or not 0 < x_end <= width or not \
            0 <= y_start < height or not 0 < y_end <= height:
        raise ValueError(INVALID_COORDINATES)

    if x_end <= x_start or y_end <= y_start:
        raise ValueError(INVALID_CROP)

    cropped = image_object.crop((x_start, y_start, x_end, y_end))
    cropped.save(local_url + "_crop.jpg")

    # Change current user's profile image
    u_id = jwt_handler.decode_token(token)
    database.update_user_by_id(u_id, {
        "profile_img_url": f"http://127.0.0.1:5001/static/{file_name}_crop.jpg"
    })

    return {}
