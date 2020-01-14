"""
Admin Flask route
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.admin import admin_userpermission_change

# Set up Flask Blueprint
ADMIN_API = Blueprint('admin_api', __name__)

"""
Flask Routes
"""
@ADMIN_API.route('/userpermission/change', methods=['POST'])
def flask_admin_userpermission_change():
    """Flask wrapper for admin_userpermission_change"""
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')
    return dumps(admin_userpermission_change(token, u_id, permission_id))
