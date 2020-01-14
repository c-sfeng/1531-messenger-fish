"""
Admin functions
"""

# Library set-up
from server_files.data import database
from server_files.util import jwt_handler, validator
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, INVALID_USER, INVALID_PERM_ID, NO_PERMISSION
from server_files.util.constants import OWNER, ADMIN, MEMBER

"""
API Functions
"""


def admin_userpermission_change(token, u_id, permission_id):
    """Given a User by their user ID, set their permissions to new permissions
    described by permission_id"""
    permission_id = int(permission_id)
    # Check validity
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_user(u_id):
        raise ValueError(INVALID_USER)
    if permission_id not in [OWNER, ADMIN, MEMBER]:
        raise ValueError(INVALID_PERM_ID)

    # Get users
    user_acting = database.get_user_by_id(jwt_handler.decode_token(token))
    user_target = database.get_user_by_id(u_id)

    # Check that token has valid permissions for this permission id, then make
    # the change
    if user_acting["permission"] == OWNER:
        # Owners can do anything
        database.update_user_by_id(u_id, {
            "permission": permission_id
        })
    elif user_acting["permission"] == ADMIN and\
            user_target["permission"] != OWNER and\
            permission_id != OWNER:
        database.update_user_by_id(u_id, {
            "permission": permission_id
        })
    else:
        raise AccessError(NO_PERMISSION)

    return {}
