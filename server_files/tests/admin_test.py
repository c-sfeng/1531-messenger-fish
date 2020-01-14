"""
Tests for admin.py
"""

import pytest
from ..blueprints import admin
from ..exceptions.my_exceptions import AccessError, ValueError
from ..util.constants import OWNER, ADMIN, MEMBER
from ..util import pytest_helper
from ..data import database

@pytest.fixture
def reset():
    """Resets database"""
    database.reset_database()

def reset_data_owner():
    """Resets the data of owner user"""
    database.update_user_by_id(pytest_helper.USER_OWNER["u_id"], {
        "email": "mcalice@mail.com",
        "handle": "Chicken",
        "name_first": "Alison",
        "name_last": "McChicken",
        "permission": 1
    })

def reset_data_admin():
    """Resets the data of admin user"""
    database.update_user_by_id(pytest_helper.USER_ADMIN["u_id"], {
        "email": "i.am.admin@mail.com",
        "handle": "Adomin",
        "name_first": "Aomine",
        "name_last": "Lee",
        "permission": 2
    })

def reset_data_member():
    """Resets the data of member user"""
    database.update_user_by_id(pytest_helper.USER_MEMBER["u_id"], {
        "email": "i.am.user@mail.com",
        "handle": "Uoser",
        "name_first": "Charles",
        "name_last": "Dickens",
        "permission": 3
    })

def reset_data_all():
    # Resets all data
    reset_data_owner()
    reset_data_admin()
    reset_data_member()

def check_permission_id(u_id, perm_id):
    # Checks permission of user with u_id
    user = database.get_user_by_id(u_id)
    return user["permission"] == perm_id

@pytest.fixture
def one_user():
    reset_data_all()
    """Fixture to login one user"""
    token = pytest_helper.login_token_owner()
    return {
        "token": token,
        "user": pytest_helper.USER_OWNER
    }

@pytest.fixture
def two_user():
    reset_data_all()
    """Fixture to login two users"""
    token1 = pytest_helper.login_token_owner()
    token2 = pytest_helper.login_token_admin()
    return {
        "user1": pytest_helper.USER_OWNER,
        "user1_token": token1,
        "user2": pytest_helper.USER_ADMIN,
        "user2_token": token2
    }

@pytest.fixture
def three_user():
    reset_data_all()
    """Fixture to login three users"""
    token1 = pytest_helper.login_token_owner()
    token2 = pytest_helper.login_token_admin()
    token3 = pytest_helper.login_token_member()
    return {
        "user1": pytest_helper.USER_OWNER,
        "user1_token": token1,
        "user2": pytest_helper.USER_ADMIN,
        "user2_token": token2,
        "user3": pytest_helper.USER_MEMBER,
        "user3_token": token3
    }


# Tests for admin_userpermission_change(token, u_id, permission_id):


# Valid everything
def test_admin_userpermission_change_valid(three_user):
    user1_token = three_user["user1_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user3_id, ADMIN) == {}
    assert check_permission_id(user3_id, ADMIN) is True


# Invalid Token
def test_admin_userpermission_change_invalidToken_validUserPerm(one_user):
    invalid_token = one_user["token"] + "apple"
    user_id = one_user["user"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(invalid_token, user_id, MEMBER)


def test_admin_userpermission_change_invalidTokenPerm_validUser(one_user):
    invalid_token = one_user["token"] + "apple"
    user_id = one_user["user"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(invalid_token, user_id, 10)


def test_admin_userpermission_change_invalidTokenUser_validPerm(one_user):
    invalid_token = one_user["token"] + "apple"
    user_id = one_user["user"]["u_id"] + 1000000
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(invalid_token, user_id, MEMBER)


def test_admin_userpermission_change_invalidTokenUserPerm(one_user):
    invalid_token = one_user["token"] + "apple"
    user_id = one_user["user"]["u_id"] + 1000000
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(invalid_token, user_id, 10)

# Not authorised
def test_admin_userpermission_change_memberAccess_MemberToOwner(three_user):
    user3_token = three_user["user3_token"]
    user3_id = three_user["user3"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user3_id, OWNER)


def test_admin_userpermission_change_memberAccess_MemberToAdmin(three_user):
    user3_token = three_user["user3_token"]
    user3_id = three_user["user3"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user3_id, ADMIN)


def test_admin_userpermission_change_memberAccess_MemberToMember(three_user):
    user3_token = three_user["user3_token"]
    user3_id = three_user["user3"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user3_id, MEMBER)


def test_admin_userpermission_change_memberAccess_adminToOwner(three_user):
    user2_id = three_user["user2"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user2_id, OWNER)


def test_admin_userpermission_change_memberAccess_adminToAdmin(three_user):
    user2_id = three_user["user2"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user2_id, ADMIN)


def test_admin_userpermission_change_memberAccess_adminToMember(three_user):
    user2_id = three_user["user2"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user2_id, MEMBER)


def test_admin_userpermission_change_memberAccess_ownerToOwner(three_user):
    user1_id = three_user["user1"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user1_id, OWNER)


def test_admin_userpermission_change_memberAccess_ownerToAdmin(three_user):
    user1_id = three_user["user1"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user1_id, ADMIN)


def test_admin_userpermission_change_memberAccess_ownerToMember(three_user):
    user1_id = three_user["user1"]["u_id"]
    user3_token = three_user["user3_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user3_token, user1_id, MEMBER)


def test_admin_userpermission_change_adminAccess_memberToOwner(three_user):
    user2_token = three_user["user2_token"]
    user3_id = three_user["user3"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user2_token, user3_id, OWNER)


def test_admin_userpermission_change_adminAccess_memberToAdmin(three_user):
    user2_token = three_user["user2_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user2_token, user3_id, ADMIN) == {}
    assert check_permission_id(user3_id, ADMIN)


def test_admin_userpermission_change_adminAccess_memberToMember(three_user):
    user2_token = three_user["user2_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user2_token, user3_id, MEMBER) == {}
    assert check_permission_id(user3_id, MEMBER)


def test_admin_userpermission_change_adminAccess_adminToOwner(three_user):
    user2_token = three_user["user2_token"]
    user2_id = three_user["user2"]["u_id"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user2_token, user2_id, OWNER)


def test_admin_userpermission_change_adminAccess_adminToAdmin(three_user):
    user2_token = three_user["user2_token"]
    user2_id = three_user["user2"]["u_id"]

    assert admin.admin_userpermission_change(user2_token, user2_id, ADMIN) == {}
    assert check_permission_id(user2_id, ADMIN)


def test_admin_userpermission_change_adminAccess_adminToMember(three_user):
    user2_token = three_user["user2_token"]
    user2_id = three_user["user2"]["u_id"]

    assert admin.admin_userpermission_change(user2_token, user2_id, MEMBER) == {}
    assert check_permission_id(user2_id, MEMBER)


def test_admin_userpermission_change_adminAccess_ownerToOwner(two_user):
    user1_id = two_user["user1"]["u_id"]
    user2_token = two_user["user2_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user2_token, user1_id, OWNER)


def test_admin_userpermission_change_adminAccess_ownerToAdmin(two_user):
    user1_id = two_user["user1"]["u_id"]
    user2_token = two_user["user2_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user2_token, user1_id, ADMIN)


def test_admin_userpermission_change_adminAccess_ownerToMember(two_user):
    user1_id = two_user["user1"]["u_id"]
    user2_token = two_user["user2_token"]
    with pytest.raises(AccessError):
        admin.admin_userpermission_change(user2_token, user1_id, MEMBER)



def test_admin_userpermission_change_OwnerAccess_memberToOwner(three_user):
    user1_token = three_user["user1_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user3_id, OWNER) == {}
    assert check_permission_id(user3_id, OWNER)


def test_admin_userpermission_change_OwnerAccess_memberToAdmin(three_user):
    user1_token = three_user["user1_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user3_id, ADMIN) == {}
    assert check_permission_id(user3_id, ADMIN)


def test_admin_userpermission_change_OwnerAccess_memberToMember(three_user):
    user1_token = three_user["user1_token"]
    user3_id = three_user["user3"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user3_id, MEMBER) == {}
    assert check_permission_id(user3_id, MEMBER)


def test_admin_userpermission_change_OwnerAccess_adminToOwner(two_user):
    user1_token = two_user["user1_token"]
    user2_id = two_user["user2"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user2_id, OWNER) == {}
    assert check_permission_id(user2_id, OWNER)


def test_admin_userpermission_change_OwnerAccess_adminToAdmin(two_user):
    user1_token = two_user["user1_token"]
    user2_id = two_user["user2"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user2_id, ADMIN) == {}
    assert check_permission_id(user2_id, ADMIN)

def test_admin_userpermission_change_OwnerAccess_adminToMember(two_user):
    user1_token = two_user["user1_token"]
    user2_id = two_user["user2"]["u_id"]

    assert admin.admin_userpermission_change(user1_token, user2_id, MEMBER) == {}
    assert check_permission_id(user2_id, MEMBER)


def test_admin_userpermission_change_OwnerAccess_ownerToOwner(one_user):
    user_token = one_user["token"]
    user_id = one_user["user"]["u_id"]
    assert admin.admin_userpermission_change(user_token, user_id, OWNER) == {}
    assert check_permission_id(user_id, OWNER)


def test_admin_userpermission_change_OwnerAccess_ownerToAdmin(one_user):
    user_token = one_user["token"]
    user_id = one_user["user"]["u_id"]
    assert admin.admin_userpermission_change(user_token, user_id, ADMIN) == {}
    assert check_permission_id(user_id, ADMIN)

def test_admin_userpermission_change_OwnerAccess_ownerToMember(one_user):
    user_token = one_user["token"]
    user_id = one_user["user"]["u_id"]
    assert admin.admin_userpermission_change(user_token, user_id, MEMBER) == {}
    assert check_permission_id(user_id, MEMBER)

# Invalid User id
def test_admin_userpermission_change_invalidUserId(one_user):
    user_token = one_user["token"]
    user_id = one_user["user"]["u_id"] + 10000
    with pytest.raises(ValueError):
        admin.admin_userpermission_change(user_token, user_id, MEMBER)

# Invalid Permission
def test_admin_userpermission_change_invalidPermId(one_user):
    user_token = one_user["token"]
    user_id = one_user["user"]["u_id"]
    with pytest.raises(ValueError):
        admin.admin_userpermission_change(user_token, user_id, 1232)

def test_wipe():
    database.wipe_tokens()
