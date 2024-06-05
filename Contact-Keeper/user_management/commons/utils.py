from datetime import datetime
import re
from user_management.commons import get_db_connection


def validate_id(value):
    if not isinstance(value, int):
        return False
    if value < 1 or value > 999999999:
        return False
    return True


def validate_name(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]{3,70}$"
    if re.match(pattern, value):
        return True
    return False


def validate_surname(value):
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]{3,70}$"
    if re.match(pattern, value):
        return True
    return False


def validate_lastname(value):
    if value is None or value == '':
        return True
    if not isinstance(value, str):
        return False
    pattern = r"^(?!.*  )[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]{3,70}$"
    if re.match(pattern, value):
        return True
    return False


def validate_birthdate(value):
    if not isinstance(value, str):
        return False
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, value):
        return False
    birthdate = datetime.strptime(value, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 15:
        return False
    return True


def validate_email(email):
    if not isinstance(email, str):
        return False
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def validate_password(value):
    if not isinstance(value, str):
        return False
    if len(value) < 3 or len(value) > 150:
        return False
    sql_injection_pattern = r"(.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]].*)"
    if re.match(sql_injection_pattern, value):
        return False
    return True


def validate_phone(value):
    if not isinstance(value, str):
        return False
    pattern = r"^\d{10}$"
    if re.match(pattern, value):
        return True
    return False


def validate_nickname(value):
    if not isinstance(value, str):
        return False
    if len(value) < 3 or len(value) > 150:
        return False
    sql_injection_pattern = r"(.*['\";--\/\*\@\@\(\)=<>\!\+\-\*\/%\^\&\|\~\{\}\[\]].*)"
    if re.match(sql_injection_pattern, value):
        return False
    return True


def exists_by_nickname(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT nickname FROM users WHERE nickname = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()


def exists_by_id(value):
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


def exists_by_email(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT email FROM users WHERE email = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()


def exists_by_phone(value):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT phone FROM users WHERE phone = %s"""
            cursor.execute(query, value)
            rows = cursor.rownumber()
            if rows > 0:
                return True
            else:
                return False
    finally:
        if connection is not None:
            connection.close()