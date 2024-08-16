import json
import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_group, validate_name, exists_user, validate_opt_name


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        body = json.loads(event['body'])
        data = create_group(body)
        result = create_meet_member(body, data['id'])
        return response_200(result)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def create_group(group):
    name = group.get('name')
    description = group.get('description')
    title = group.get('title')
    notes = group.get('notes')
    reminder = group.get('reminder')
    moderator = group.get('moderator')

    # Validate the attributes
    if not validate_name(name):
        raise ValueError(ErrorType.INVALID_NAME)
    if not validate_name(title):
        raise ValueError(ErrorType.INVALID_TITLE)
    if not validate_opt_name(description):
        raise ValueError(ErrorType.INVALID_DESCRIPTION)
    if not validate_opt_name(notes):
        raise ValueError(ErrorType.INVALID_NOTES)
    if not validate_opt_name(reminder):
        raise ValueError(ErrorType.INVALID_REMINDER)
    if not exists_user(moderator):
        raise ValueError(ErrorType.USER_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO `group_members` (`name`, `description`) VALUES (%s, %s)
            """
            cursor.execute(query, (name, description))
            connection.commit()
            return {'id': cursor.lastrowid, 'name': name, 'description': description}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection:
            connection.close()


def create_meet_member(data, group_id):
    title = data.get('title')
    notes = data.get('notes')
    moderator = data.get('moderator')

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO meets (person_id, group_id, status, role, title, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (moderator, group_id, 'pending', 'moderator', title, notes))
            connection.commit()
            return {"message": "group created successfully", "id": cursor.lastrowid}
    except pymysql.OperationalError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()