"""
Module to generate, get and store reset codes
"""

import random
import string
import json

def generate_code():
    """Generates code for password reset"""
    reset_code = []
    i = 0
    while i < 8:
        alphabet = string.ascii_letters + string.digits
        reset_code.append(alphabet[random.randint(0, len(alphabet) - 1)])
        i += 1
    reset_code_str = "".join(reset_code)

    # checks if code is unique
    if is_unique_code(reset_code_str):
        codes = get_all_reset_codes()
        codes.append(reset_code_str)
        update_reset_codes(codes)
        return reset_code_str
    generate_code()
    return None


def is_unique_code(code):
    """Checks that a code is unique"""
    codes = get_all_reset_codes()
    if code not in codes:
        return True
    return False


def get_all_reset_codes():
    """Returns all reset codes from database"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        return data["reset_codes"]


def update_reset_codes(new):
    """Updates reset codes"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        data["reset_codes"] = new
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )


def delete_reset_code(target):
    """Removes reset code from database"""
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        codes = data["reset_codes"]
        codes.remove(target)
        open("server_files/data/users.json", "w").write(
            json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        )
