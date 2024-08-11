from datetime import datetime
import re
from database import get_db_connection


def validate_name(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
    if re.match(pattern, value):
        return True
    return False


def validate_opt_name(value):
    if isinstance(value, type(None)):
        return True
    if not (isinstance(value, str)):
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{0,300}$"
    if re.match(pattern, value):
        return True
    return False


def validate_birthday(value):
    if not isinstance(value, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, value):
        return False
    birthday = datetime.strptime(value, "%Y-%m-%d")
    today = datetime.today()
    if birthday > today:
        return False
    return True


def validate_phone(value):
    if not isinstance(value, str):
        return False
    if len(value) == 10:
        return True
    return False


def validate_email(value):
    if not isinstance(value, str):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, value):
        return True
    return False


def validate_nickname(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,30}$"
    if re.match(pattern, value):
        return True
    return False

def validate_password(value):
    if not isinstance(value, str):
        return False
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?:{}|<>]).{6,}$'
    if re.match(pattern, value):
        return True
    return False


def validate_user_type(value):
    if not isinstance(value, str):
        return False
    allowed_types = ['admin', 'normal']
    if value not in allowed_types:
        return False
    return True


def validate_description(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,}$"
    if re.match(pattern, value):
        return True
    return False


def validate_start_date(value):
    if not isinstance(value, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    if not re.match(pattern, value):
        return False
    event_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    today = datetime.today()
    if event_date < today:
        return False
    return True


def validate_end_date(start_date, end_date):
    if not isinstance(end_date, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    if not re.match(pattern, end_date):
        return False
    event_end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    event_start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
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
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
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
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,255}$"
    if re.match(pattern, value):
        return True
    return False


def validate_notes_meeting(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )(?!.*['\";\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]]).{3,}$"
    if re.match(pattern, value):
        return True
    return False


def validate_id(value):
    if isinstance(value, str):
        if not value.isdigit():
            return False
        value = int(value)
    if isinstance(value, int) and (value < 1 or value > 999999999):
        return False
    return True


def exists_by_id(value):
    if value is None:
        return False
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM events WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()


def exists_event(value):
    if value is None:
        return False
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM events WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()

def exists_user(value):
    if value is None:
        return False
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM people WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()

def exists_user_phone(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM people WHERE phone = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()

def exists_user_nick(value):
    if value is None:
        return False
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM people WHERE nickname = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()

def exists_group(value):
    if value is None:
        return False
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT id FROM group_members WHERE id = %s"""
            cursor.execute(query, value)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()