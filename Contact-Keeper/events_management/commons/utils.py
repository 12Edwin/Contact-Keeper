from datetime import datetime
import re
from user_management.commons import get_db_connection


def validate_name(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
    if re.match(pattern, value):
        return True
    return False


def validate_description(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,}$"
    if re.match(pattern, value):
        return True
    return False


def validate_start_date(value):
    if not isinstance(value, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, value):
        return False
    event_date = datetime.strptime(value, "%Y-%m-%d")
    today = datetime.today()
    if event_date < today:
        return False
    return True


def validate_end_date(start_date, end_date):
    if not isinstance(end_date, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, end_date):
        return False
    event_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    event_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if event_end_date < event_start_date:
        return False
    if (event_end_date - event_start_date).days > 1:
        return False
    return True


def validate_event_type(value):
    if not isinstance(value, str):
        return False
    allowed_types = ['meeting', 'session', 'birthday', 'other']
    if value not in allowed_types:
        return False
    return True


def validate_location(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
    if re.match(pattern, value):
        return True
    return False


def validate_status_meeting(value):
    if not isinstance(value, str):
        return False
    allowed_status = ['pending', 'rejected', 'accepted']
    if value not in allowed_status:
        return False
    return True


def validate_role_meeting(value):
    if not isinstance(value, str):
        return False
    allowed_roles = ['moderator', 'member']
    if value not in allowed_roles:
        return False
    return True


def validate_title_meeting(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
    if re.match(pattern, value):
        return True
    return False


def validate_notes_meeting(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,}$"
    if re.match(pattern, value):
        return True
    return False


def validate_id(value):
    if not isinstance(value, int):
        return False
    if value < 1 or value > 999999999:
        return False
    return True


def validate_group_id(value):
    if not isinstance(value, int):
        return False
    if value < 1 or value > 999999999:
        return False
    return True


def validate_user_id(value):
    if not isinstance(value, int):
        return False
    if value < 1 or value > 999999999:
        return False
    return True


def exists_by_id(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM events WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()


def exists_user(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM users WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()


def exists_group(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM group_members WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()