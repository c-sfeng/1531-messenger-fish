"""
Tests for users.py
"""
import json
import pytest
from ..blueprints import users
from ..exceptions.my_exceptions import AccessError
from ..util import pytest_helper
from ..data import database

def wipe_users():
    """Wipes tokens from users, run every time server starts up"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        data["users"] = []
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )

def reset():
    database.reset_database()

@pytest.fixture
def owner():
    """Fixture to login one user"""
    token = pytest_helper.login_token_owner()
    return {
        "token": token,
        "user": pytest_helper.USER_OWNER
    }

@pytest.fixture
def admin():
    """Fixture to login two users"""
    token = pytest_helper.login_token_admin()
    return {
        "token": token,
        "user": pytest_helper.USER_ADMIN
    }

@pytest.fixture
def member():
    """Fixture to login two users"""
    token = pytest_helper.login_token_member()
    return {
        "token": token,
        "user": pytest_helper.USER_MEMBER
    }

ALL_USERS = [
    {'u_id': 0,
     'email': 'mcalice@mail.com',
     'name_first': 'Alison',
     'name_last': 'McChicken',
     'handle_str': 'Chicken',
     'profile_img_url': 'http://127.0.0.1:5001/static/chicken.jpg'},
    {'u_id': 1,
     'email': 'i.am.admin@mail.com',
     'name_first': 'Aomine',
     'name_last': 'Lee',
     'handle_str': 'Adomin',
     'profile_img_url': 'http://127.0.0.1:5001/static/default.jpg'},
    {'u_id': 2,
     'email': 'i.am.user@mail.com',
     'name_first': 'Charles',
     'name_last': 'Dickens',
     'handle_str': 'Uoser',
     'profile_img_url': 'http://127.0.0.1:5001/static/default.jpg'},
    {'u_id': 3,
     'email': 'channel.lover@mail.com',
     'name_first': 'David',
     'name_last': 'Jones',
     'handle_str': "I'm lovin' it",
     'profile_img_url': 'http://127.0.0.1:5001/static/default.jpg'},
    {'u_id': 4,
     'email': 'master.of.channels@mail.com',
     'name_first': 'Evan',
     'name_last': 'EvanLast',
     'handle_str': 'EvanHandle',
     'profile_img_url': 'http://127.0.0.1:5001/static/default.jpg'},
    {'u_id': 5,
     'email': 'registered.user@mail.com',
     'name_first': 'Jackson',
     'name_last': 'James',
     'handle_str': 'The Doctor',
     'profile_img_url': 'http://127.0.0.1:5001/static/default.jpg'}
]

# Tests for users_all(token)
def test_users_all_bad_token(owner):
    token = owner["token"] + "abc123"
    with pytest.raises(AccessError):
        users.users_all(token)

def test_users_all_owner(owner):
    token = owner["token"]
    assert users.users_all(token) == {"users": ALL_USERS}

def test_users_all_admin(admin):
    token = admin["token"]
    assert users.users_all(token) == {"users": ALL_USERS}

def test_users_all_member(member):
    token = member["token"]
    assert users.users_all(token) == {"users": ALL_USERS}

def test_wipe():
    database.reset_database()
