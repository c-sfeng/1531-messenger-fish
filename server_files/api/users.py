"""
User functions
"""

# Library set-up
from server_files.data import database
from server_files.util import validator
from server_files.exceptions.my_exceptions import AccessError
from server_files.exceptions.err_msgs import INVALID_TOKEN

"""
API Functions
"""

def users_all(token):
    """Returns a list of all users, each user being a dictionary:
       {u_id, email, name_first, name_last, handle_str, profile_img_url}"""
    # Check valid token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # This works for all users with good tokens. Add lines here to handle different permissions

    # Retreive users and create output list
    user_list = []
    users = database.get_all_users()
    for user in users:
        user_list.append({
            "u_id": user["u_id"],
            "email": user["email"],
            "name_first": user["name_first"],
            "name_last": user["name_last"],
            "handle_str": user["handle"],
            "profile_img_url": user["profile_img_url"]
        })

    return {"users": user_list}
