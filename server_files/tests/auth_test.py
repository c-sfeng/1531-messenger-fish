import pytest
from ..blueprints import auth
from ..util import pytest_helper, code_generator
from ..exceptions.my_exceptions import ValueError
from ..data import database

@pytest.fixture
def reset():
    database.reset_database()

"""
Test for auth_login()
"""
def test_auth_login_ideal(reset):
    member_token = pytest_helper.login_token_member()
    assert member_token is not None
    admin_token = pytest_helper.login_token_admin()
    assert admin_token is not None
    owner_token = pytest_helper.login_token_owner()
    assert owner_token is not None

def test_auth_login_email_nonexistent(reset):
    email = "idontexist@test.com"
    password = "abc123"

    with pytest.raises(ValueError):
        auth.auth_login(email, password)

def test_auth_login_invalid_email_and_password(reset):
    email = "invalid.test.com"
    password = "abc"

    with pytest.raises(ValueError):
        auth.auth_login(email, password)

def test_auth_login_invalid_email_valid_password(reset):
    email = "invalid.test.com"
    password = pytest_helper.USER_MEMBER["password"]

    with pytest.raises(ValueError):
        auth.auth_login(email, password)

def test_auth_login_valid_email_invalid_password(reset):
    email = pytest_helper.USER_MEMBER["email"]
    password = "abc"

    with pytest.raises(ValueError):
        auth.auth_login(email, password)

"""
Test for auth_logout()
"""
def test_auth_logout_ideal(reset):
    token = pytest_helper.login_token_owner()
    assert auth.auth_logout(token) == {"is_success": True}

def test_auth_logout_invalid_token(reset):
    token = pytest_helper.INVALID_TOKEN
    assert auth.auth_logout(token) == {"is_success": False}

"""
Test for auth_register()
"""
def test_auth_register_ideal(reset):
    email = "test@test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsum"

    assert auth.auth_register(email, password, name_first, name_last) is not None

def test_auth_register_no_current_users(reset):
    pytest_helper.remove_all_users()
    email = "test@test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsum"

    assert auth.auth_register(email, password, name_first, name_last) is not None

def test_auth_register_invalid_data(reset):
    email = "invalid.test.com"
    password = "abc"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_valid_email(reset):
    email = "test@test.com"
    password = "abc"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_valid_password(reset):
    email = "invalid.test.com"
    password = "abc123"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_valid_first_name(reset):
    email = "invalid.test.com"
    password = "abc"
    name_first = "Lorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_valid_last_name(reset):
    email = "invalid.test.com"
    password = "abc"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_email_and_password(reset):
    email = "test@test.com"
    password = "abc123"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_email_and_first_name(reset):
    email = "test@test.com"
    password = "abc"
    name_first = "Lorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_email_and_last_name(reset):
    email = "test@test.com"
    password = "abc"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_password_and_first_name(reset):
    email = "invalid.test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_password_and_last_name(reset):
    email = "invalid.test.com"
    password = "abc123"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_valid_names(reset):
    email = "invalid.test.com"
    password = "abc"
    name_first = "Lorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_invalid_last_name(reset):
    email = "test@test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_invalid_first_name(reset):
    email = "test@test.com"
    password = "abc123"
    name_first = "Loremloremloremloremloremloremloremloremloremloremlorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_invalid_email(reset):
    """ Case 15: email invalid """
    email = "invalid.test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_only_invalid_password(reset):
    """ Case 16: password invalid """
    email = "test@test.com"
    password = "abc"
    name_first = "Lorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

def test_auth_register_fullname_longer_than_20(reset):
    """ Case 17: tests handle concatenation """
    email = "test@test.com"
    password = "abc123"
    name_first = "Aaaaabbbbbccccc"
    name_last = "Aaaaabbbbbccccc"

    assert auth.auth_register(email, password, name_first, name_last) is not None

def test_auth_register_duplicate_handles(reset):
    """ Case 18: tests for duplicate handles """
    email = "test@test.com"
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsum"

    assert auth.auth_register(email, password, name_first, name_last) is not None

    email = "test1@test.com"
    password = "def456"
    name_first = "Lorem"
    name_last = "Ipsum"

    assert auth.auth_register(email, password, name_first, name_last) is not None

def test_auth_register_duplicate_email(reset):
    """ Case 19: email duplicated """
    email = pytest_helper.USER_MEMBER["email"]
    password = "abc123"
    name_first = "Lorem"
    name_last = "Ipsum"

    with pytest.raises(ValueError):
        auth.auth_register(email, password, name_first, name_last)

"""
Test for auth_passwordreset_request()
"""
'''
auth_passwordreset_request can't be tested for the ideal case, as it involves
sending a Flask mail; which in turn requires the server to be running
This results in a lessened coverage percentage
def test_auth_passwordreset_request_ideal(reset):
    email = pytest_helper.USER_MEMBER["email"]
    assert auth.auth_passwordreset_request(email) == {}
'''

def test_auth_passwordreset_request_invalid_email(reset):
    email = "invalid.test.com"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_request(email)

def test_auth_passwordreset_request_nonexistent_email(reset):
    email = "nonexistent@test.com"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_request(email)

"""
Test for auth_passwordreset_reset()
"""
'''
auth_passwordreset_request can't be tested for the ideal case, as it involves
sending a Flask mail; which in turn requires the server to be running
def test_auth_passwordreset_reset_ideal(reset):
    reset_code = pytest_helper.USER_MEMBER["pw_reset_code"]
    new_password = "abc123"
    assert auth.auth_passwordreset_reset(reset_code, new_password) == {}
'''
def test_auth_passwordreset_reset_idea(reset):
    reset_code = pytest_helper.USER_MEMBER["pw_reset_code"]
    database.update_user_by_id(pytest_helper.USER_MEMBER["u_id"], {
        "pw_reset_code": reset_code
    })
    codes = code_generator.get_all_reset_codes()
    codes.append(reset_code)
    code_generator.update_reset_codes(codes)
    new_password = "abc123"
    assert auth.auth_passwordreset_reset(reset_code, new_password) == {}

def test_auth_passwordreset_reset_invalid_data(reset):
    reset_code = "invalid"
    new_password = "abc"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_reset(reset_code, new_password)

def test_auth_passwordreset_reset_invalid_password(reset):
    reset_code = pytest_helper.USER_MEMBER["pw_reset_code"]
    new_password = "abc"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_reset(reset_code, new_password)

def test_auth_passwordreset_reset_invalid_reset_code(reset):
    reset_code = "invalid"
    new_password = "abc123"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_reset(reset_code, new_password)

def test_auth_passwordreset_reset_default_code(reset):
    reset_code = ""
    new_password = "abc123"
    with pytest.raises(ValueError):
        auth.auth_passwordreset_reset(reset_code, new_password)

def test_reset_users_database(reset):
    database.wipe_tokens()
