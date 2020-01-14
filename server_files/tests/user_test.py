"""
Tests for user.py
"""
import pytest
from ..blueprints import user
from ..exceptions.my_exceptions import AccessError, ValueError
from ..util import pytest_helper
from ..data import database

def reset_data_owner():
    """Resets the data of owner user"""
    database.update_user_by_id(pytest_helper.USER_OWNER["u_id"], {
        "email": "mcalice@mail.com",
        "handle": "Chicken",
        "name_first": "Alison",
        "name_last": "McChicken"
    })

def reset_data_admin():
    """Resets the data of admin user"""
    database.update_user_by_id(pytest_helper.USER_ADMIN["u_id"], {
        "email": "i.am.admin@mail.com",
        "handle": "Adomin",
        "name_first": "Aomine",
        "name_last": "Lee"
    })

def reset_data_member():
    """Resets the data of member user"""
    database.update_user_by_id(pytest_helper.USER_MEMBER["u_id"], {
        "email": "i.am.user@mail.com",
        "handle": "Uoser",
        "name_first": "Charles",
        "name_last": "Dickens"
    })

def reset_data_all():
    reset_data_owner()
    reset_data_admin()
    reset_data_member()

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


# Tests for userprofile(token, u_id)

def test_user_profile_self(one_user):
    usr = one_user["user"]
    assert user.user_profile(one_user["token"], usr["u_id"]) == {"email": usr["email"],
                                                                 "name_first": usr["name_first"],
                                                                 "name_last": usr["name_last"],
                                                                 "handle_str": usr["handle"],
                                                                 "profile_img_url": usr["profile_img_url"]}


def test_user_profile_other(two_user):
    usr1 = two_user["user1"]
    usr2 = two_user["user2"]
    usr1_token = two_user["user1_token"]
    usr2_token = two_user["user2_token"]
    assert user.user_profile(usr1_token, usr2["u_id"]) == {"email": usr2["email"],
                                                           "name_first": usr2["name_first"],
                                                           "name_last": usr2["name_last"],
                                                           "handle_str": usr2["handle"],
                                                           "profile_img_url": usr2["profile_img_url"]}
    assert user.user_profile(usr2_token, usr1["u_id"]) == {"email": usr1["email"],
                                                           "name_first": usr1["name_first"],
                                                           "name_last": usr1["name_last"],
                                                           "handle_str": usr1["handle"],
                                                           "profile_img_url": usr1["profile_img_url"]}


def test_user_profile_invaidToken_validUser(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "yeet123"
    user_id = usr["u_id"]
    with pytest.raises(AccessError):
        user.user_profile(invalid_token, user_id)


def test_user_profile_invaidToken_invalidUser(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "yeet123"
    invalid_id = usr["u_id"] + 1000
    with pytest.raises(AccessError):
        user.user_profile(invalid_token, invalid_id)


def test_user_profile_invaidUser(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    invalid_id = usr["u_id"] + 1000
    with pytest.raises(ValueError):
        user.user_profile(user_token, invalid_id + 1)


# Tests for user_profile_setname(token, name_first, name_last)

def test_user_profile_setname_validToken_validName(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    assert user.user_profile(user_token, usr["u_id"]) == {"email": usr["email"],
                                                          "name_first": usr["name_first"],
                                                          "name_last": usr["name_last"],
                                                          "handle_str": usr["handle"],
                                                          "profile_img_url": usr["profile_img_url"]}
    assert user.user_profile_setname(user_token, "Asta", "Tanomich") == {}
    assert user.user_profile(user_token, usr["u_id"]) == {"email": usr["email"],
                                                          "name_first": "Asta",
                                                          "name_last": "Tanomich",
                                                          "handle_str": usr["handle"],
                                                          "profile_img_url": usr["profile_img_url"]}
    reset_data_all()


def test_user_profile_setname_invalidToken_validName(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token, "First", "Last")


def test_user_profile_setname_invalidToken_longFirst(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt",
                                  "Last")


def test_user_profile_setname_invalidToken_longLast(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token,
                                  "First",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_invalidToken_longFirstLast(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_invalidToken_emptyFirst(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token, "", "Last")


def test_user_profile_setname_invalidToken_emptyLast(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token, "First", "")


def test_user_profile_setname_invalidToken_emptyFirstLast(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token, "", "")


def test_user_profile_setname_invalidToken_emptyFirst_longLast(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token, "",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_invalidToken_emptyLast_longFirst(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hahaha"
    with pytest.raises(AccessError):
        user.user_profile_setname(invalid_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt", "")


def test_user_profile_setname_validToken_longFirst(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt",
                                  "Last")


def test_user_profile_setname_validToken_longLast(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token,
                                  "First",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_validToken_longFirstLast(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_validToken_emptyFirst(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token, "", "Last")


def test_user_profile_setname_validToken_emptyLast(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token, "First", "")


def test_user_profile_setname_validToken_emptyFirstLast(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token, "", "")


def test_user_profile_setname_validToken_emptyFirst_longLast(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token, "",
                                  "LastLastLastLastLastLastLastLastLastLastLastLastLast")


def test_user_profile_setname_validToken_emptyLast_longFirst(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setname(user_token,
                                  "FirstFirstFirstFirstFirstFirstFirstFirstFirstFirstt", "")


# Tests for user_profile_setemail(token, email)

def test_user_profile_setemail_validToken_validEmail(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    user_id = usr["u_id"]
    user_email = usr["email"]
    new_email = "newemail." + user_email
    assert user.user_profile(user_token, user_id) == {"email": usr["email"],
                                                      "name_first": usr["name_first"],
                                                      "name_last": usr["name_last"],
                                                      "handle_str": usr["handle"],
                                                      "profile_img_url": usr["profile_img_url"]}
    assert user.user_profile_setemail(user_token, new_email) == {}
    assert user.user_profile(user_token, user_id) == {"email": new_email,
                                                      "name_first": usr["name_first"],
                                                      "name_last": usr["name_last"],
                                                      "handle_str": usr["handle"],
                                                      "profile_img_url": usr["profile_img_url"]}
    reset_data_all()


def test_user_profile_setemail_validToken_sameEmail(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    user_email = usr["email"]
    with pytest.raises(ValueError):
        user.user_profile_setemail(user_token, user_email)


def test_user_profile_setemail_invalidToken_validEmail(one_user):
    invalid_token = one_user["token"] + "hello"
    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, "newemail@email.com")


def test_user_profile_setemail_invalidToken_usedEmail(one_user):
    invalid_token = one_user["token"] + "words"
    user2_email = pytest_helper.USER_ADMIN["email"]
    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, user2_email)


def test_user_profile_setemail_invalidToken_sameEmail(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "hello"
    user1_email = usr["email"]
    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, user1_email)


def test_user_profile_setemail_invalidToken_invalidEmail(one_user):
    invalid_token = one_user["token"] + "hello"
    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, "happy brithday")


def test_user_profile_setemail_invalidToken_emptyEmail(one_user):
    invalid_token = one_user["token"] + "hello"
    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, "")


def test_user_profile_setemail_validToken_usedEmail(one_user):
    user1_token = one_user["token"]
    user2_email = pytest_helper.USER_ADMIN["email"]
    with pytest.raises(ValueError):
        user.user_profile_setemail(user1_token, user2_email)


def test_user_profile_setemail_validToken_emptyEmail(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setemail(user_token, "")


def test_user_profile_setemail_validToken_invalidEmail_text(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_setemail(user_token, "happy brithday george")



# Tests for user_profile_sethandle(token, handle_str)

def test_user_profile_sethandle_validToken_validHandle(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    user_id = usr["u_id"]
    user_handle = usr["handle"]
    new_handle = user_handle[::-1]
    assert user.user_profile(user_token, user_id) == {"email": usr["email"],
                                                      "name_first": usr["name_first"],
                                                      "name_last": usr["name_last"],
                                                      "handle_str": usr["handle"],
                                                      "profile_img_url": usr["profile_img_url"]}
    assert user.user_profile_sethandle(user_token, new_handle) == {}
    assert user.user_profile(user_token, user_id) == {"email": usr["email"],
                                                      "name_first": usr["name_first"],
                                                      "name_last": usr["name_last"],
                                                      "handle_str": new_handle,
                                                      "profile_img_url": usr["profile_img_url"]}
    reset_data_all()


def test_user_profile_sethandle_validToken_sameHandle(one_user):
    usr = one_user["user"]
    user_token = one_user["token"]
    user_handle = usr["handle"]
    with pytest.raises(ValueError):
        user.user_profile_sethandle(user_token, user_handle)


def test_user_profile_sethandle_validToken_usedHandle(one_user):
    usr = one_user["user"]
    user1_token = one_user["token"]
    user2_handle = pytest_helper.USER_ADMIN["handle"]
    with pytest.raises(ValueError):
        user.user_profile_sethandle(user1_token, user2_handle)


def test_user_profile_sethandle_invalidToken_validHandle(one_user):
    invalid_token = one_user["token"] + "potat"
    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, "bicycle_handle")


def test_user_profile_sethandle_invalidToken_sameHandle(one_user):
    usr = one_user["user"]
    invalid_token = one_user["token"] + "potat"
    user_handle = usr["handle"]
    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, user_handle)


def test_user_profile_sethandle_invalidToken_usedHandle(one_user):
    invalid_token = one_user["token"] + "words"
    user2_handle = pytest_helper.USER_ADMIN["handle"]
    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, user2_handle)


def test_user_profile_sethandle_invalidToken_longHandle(one_user):
    invalid_token = one_user["token"] + "potat"
    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, "NickNickNickNickNickk")


def test_user_profile_sethandle_invalidToken_emptyHandle(one_user):
    invalid_token = one_user["token"] + "potat"
    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, "")


def test_user_profile_sethandle_validToken_longHandle(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_sethandle(user_token, "NickNickNickNickNickk")


def test_user_profile_sethandle_validToken_emptyHandle(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profile_sethandle(user_token, "")



# Tests for user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
# Other http codes cant be tested (cant currently find url with other codes)

URL = "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg"
PNG_URL = "http://pluspng.com/img-png/flower-png-dahlia-flower-png-transparent-image-1644.png"
INVALID_URL = "http://www.asdf.asdf/imageaaaaaaa.jpg"
# x: 500, y: 477

def test_user_profiles_uploadphoto(one_user):
    user_token = one_user["token"]
    assert user.user_profiles_uploadphoto(user_token, URL, 10, 10, 200, 400) == {}

def test_user_profiles_uploadphoto_png(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, PNG_URL, 10, 10, 200, 400)

def test_user_profiles_uploadphoto_invalidURL(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, INVALID_URL, 10, 10, 200, 400)

def test_user_profiles_uploadphoto_invalidToken(one_user):
    invalid_token = one_user["token"] + "eh_token"
    with pytest.raises(AccessError):
        user.user_profiles_uploadphoto(invalid_token, URL, 10, 10, 200, 400)


def test_user_profiles_uploadphoto_outsideBounds_xStart(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 505, 10, 550, 400)


def test_user_profiles_uploadphoto_outsideBounds_xEnd(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 400, 10, 550, 400)


def test_user_profiles_uploadphoto_xStart_edgeLeft(one_user):
    user_token = one_user["token"]
    assert user.user_profiles_uploadphoto(user_token, URL, 10, 10, 200, 400) == {}


def test_user_profiles_uploadphoto_xStart_edgeRight(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 500, 10, 550, 400)


def test_user_profiles_uploadphoto_xEnd_edgeLeft(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, -10, 10, 0, 400)


def test_user_profiles_uploadphoto_xEnd_edgeRight(one_user):
    user_token = one_user["token"]
    assert user.user_profiles_uploadphoto(user_token, URL, 400, 10, 500, 400) == {}


def test_user_profiles_uploadphoto_outsideBounds_yStart(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 500, 200, 550)


def test_user_profiles_uploadphoto_outsideBounds_yEnd(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 400, 200, 500)


def test_user_profiles_uploadphoto_yStart_edgeTop(one_user):
    user_token = one_user["token"]
    assert user.user_profiles_uploadphoto(user_token, URL, 10, 0, 200, 400) == {}


def test_user_profiles_uploadphoto_yStart_edgeBottom(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 477, 200, 500)


def test_user_profiles_uploadphoto_yEnd_edgeTop(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, -10, 200, 0)


def test_user_profiles_uploadphoto_yEnd_edgeBottom(one_user):
    user_token = one_user["token"]
    assert user.user_profiles_uploadphoto(user_token, URL, 10, 10, 200, 477) == {}


def test_user_profiles_uploadphoto_invalidXStartEndDifferent(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 200, 10, 10, 400)


def test_user_profiles_uploadphoto_invalidYStartEndDifferent(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 400, 200, 10)


def test_user_profiles_uploadphoto_XStartEndEqual(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 10, 10, 100)


def test_user_profiles_uploadphoto_YStartEndEqual(one_user):
    user_token = one_user["token"]
    with pytest.raises(ValueError):
        user.user_profiles_uploadphoto(user_token, URL, 10, 10, 100, 10)

def test_wipe():
    database.reset_database()
