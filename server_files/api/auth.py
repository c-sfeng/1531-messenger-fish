"""
Authorisation functions and Flask routes
"""

# Library set-up
from flask_mail import Mail, Message
from flask import current_app
from server_files.data import database
from server_files.util import jwt_handler, validator, code_generator, constants
from server_files.exceptions.my_exceptions import ValueError
from server_files.exceptions.err_msgs import\
    INVALID_EMAIL, WRONG_PASS, EMAIL_NOT_FOUND, INVALID_NAME_FIRST, INVALID_NAME_LAST,\
    NOT_UNIQUE_EMAIL, INVALID_PASS, EMPTY_RESET_CODE, INVALID_RESET_CODE


"""
API Functions
"""


def auth_login(email, password):
    """Given a registered users' email and password and generates a valid token
    for the user to remain authenticated"""
    # Validate data
    if not validator.is_valid_email(email):
        raise ValueError(INVALID_EMAIL)

    # Loop searches within the user database
    users = database.get_all_users()
    for user in users:
        # Checks if email matches an email
        if user["email"] == email:
            # Checks if password matches the email's password
            if user["password"] != password:
                raise ValueError(WRONG_PASS)
            # Creates a new token for the user
            token = jwt_handler.encode_u_id(user["u_id"])
            token_list = user["tokens"]
            token_list.append(token)
            # Updates the json file
            database.update_user_by_id(user["u_id"], {
                "tokens": token_list
            })
            return {
                "u_id": user["u_id"],
                "token": token
            }
    raise ValueError(EMAIL_NOT_FOUND)


def auth_logout(token):
    """Given an active token, invalidates the taken to log the user out. If a
    valid token is given, and the user is successfully logged out, it returns
    true, otherwise false."""
    # Validate data
    if not validator.is_valid_token(token):
        return {"is_success": False}

    # Converts token to u_id
    u_id = jwt_handler.decode_token(token)
    # Searches for the user by u_id
    user = database.get_user_by_id(u_id)

    # Searches for and removes the token from the user's active tokens
    token_list = user["tokens"]
    token_list.remove(token)
    database.update_user_by_id(user["u_id"], {
        "tokens": token_list
    })
    return {"is_success": True}


def auth_register(email, password, name_first, name_last):
    """Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for authentication
    in their session. A handle is generated that is the concatentation of a
    lowercase-only first name and last name. If the concatenation is longer
    than 20 characters, it is cutoff at 20 characters. If the handle is
    already taken, you may modify the handle in any way you see fit to
    make it unique."""
    # Validate data
    if not validator.is_valid_name(name_first):
        raise ValueError(INVALID_NAME_FIRST)
    if not validator.is_valid_name(name_last):
        raise ValueError(INVALID_NAME_LAST)
    if not validator.is_valid_email(email):
        raise ValueError(INVALID_EMAIL)
    if not validator.is_unique_email(email):
        raise ValueError(NOT_UNIQUE_EMAIL)
    if not validator.is_valid_password(password):
        raise ValueError(INVALID_PASS)

    # Set permission to MEMBER
    perm = constants.MEMBER
    # If no members, permission is OWNER
    if len(database.get_all_users()) == 0:
        perm = constants.OWNER

    # user["handle"] handling
    if len(name_first + name_last) > 20:
        handle = []
        temp = (name_first + name_last).lower()

        for x in range(0, 20):
            handle.append(temp[x])
        handle_str = "".join(handle)
    else:
        handle_str = (name_first + name_last).lower()

    users = database.get_all_users()
    index = 0
    for user in users:
        if user["handle"][0: len(handle_str)] == handle_str:
            index += 1

    if index > 0:
        handle_str = handle_str + str(index)

    u_id = database.add_user({
        "tokens": [],
        "name_first": name_first,
        "name_last": name_last,
        "handle": handle_str,
        "email": email,
        "password": password,
        "permission": perm,
        "pw_reset_code": "",
        "profile_img_url": "http://127.0.0.1:5001/static/default.jpg"
    })

    token = jwt_handler.encode_u_id(u_id)
    user = database.get_user_by_id(u_id)
    token_list = user["tokens"]
    token_list.append(token)
    database.update_user_by_id(u_id, {
        "tokens": token_list
    })
    return {
        "token": token
    }


def auth_passwordreset_request(email):
    """Given an email address, if the user is a registered user, send's them a
    an email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email."""
    # Validate data
    users = database.get_all_users()
    if validator.is_unique_email(email):
        raise ValueError(EMAIL_NOT_FOUND)

    for user in users:
        if user["email"] == email:
            # Deletes previous reset code
            if user["pw_reset_code"] != "":
                code_generator.delete_reset_code(user["pw_reset_code"])

            reset_code_str = code_generator.generate_code()
            database.update_user_by_id(user["u_id"], {
                "pw_reset_code": reset_code_str
            })

            # Sends email with reset_code
            mail = Mail(current_app)
            try:
                msg = Message("Password reset from COMP1531",
                              sender="coveremail001@gmail.com",
                              recipients=[email])
                msg.body = reset_code_str
                mail.send(msg)
            except Exception as excp:
                print(str(excp))
    return {}


def auth_passwordreset_reset(reset_code, new_password):
    """Given a reset code for a user, set that user's new password to the
    password provided"""
    # Validate data
    if not validator.is_valid_password(new_password):
        raise ValueError(INVALID_PASS)

    # Ignore reset_code
    if reset_code == "":
        raise ValueError(EMPTY_RESET_CODE)

    users = database.get_all_users()
    reset_code_found = False
    for user in users:
        if user["pw_reset_code"] == reset_code:
            reset_code_found = True
            database.update_user_by_id(user["u_id"], {
                "password": new_password,
                "pw_reset_code": ""
            })
            code_generator.delete_reset_code(reset_code)
    if not reset_code_found:
        raise ValueError(INVALID_RESET_CODE)
    return {}
