import re


def validate_username(value):
    if not isinstance(value, str) or len(value) > 50:
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,}$"
    if re.match(pattern, value):
        return True
    return False


def validate_email(value):
    if not isinstance(value, str) or len(value) > 100:
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, value):
        return True
    return False


def validate_password(value):
    if not isinstance(value, str) or len(value) < 6:
        return False
    if len(value) >= 6 & len(value) <= 25:
        return True
    return False


def validate_user_type(value):
    if not isinstance(value, str):
        return False
    valid_types = ['admin', 'normal']
    if value in valid_types:
        return True
    return False


def validate_code(value):
    if not isinstance(value, str) or len(value) != 6:
        return False
    return True
