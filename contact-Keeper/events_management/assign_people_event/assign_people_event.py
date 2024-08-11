import json
import os
import sys
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, validate_id, exists_by_id, get_cognito_ids, exists_group, validate_name, validate_start_date, validate_end_date, validate_event_type, exists_user, validate_opt_name, exists_event


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        body = json.loads(event['body'])
        data = assign_people_event(body)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def assign_people_event(event):
    title = event.get('title')
    notes = event.get('notes')
    reminder = event.get('reminder')
    member = event.get('member')
    event_id = event.get('event_id')

    # Validate the attributes
    if not exists_user(member):
        raise ValueError(ErrorType.USER_NOT_FOUND)
    if not validate_name(title):
        raise ValueError(ErrorType.INVALID_TITLE)
    if not validate_opt_name(notes):
        raise ValueError(ErrorType.INVALID_NOTES)
    if not validate_opt_name(reminder):
        raise ValueError(ErrorType.INVALID_REMINDER)
    if not exists_event(event_id):
        raise ValueError(ErrorType.EVENT_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
             INSERT INTO meets (title, notes, reminder, status, role, person_id, event_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
             """
            cursor.execute(query, (title, notes, reminder, 'pending', 'member', member, event_id))
            connection.commit()
            return {'title': title, 'notes': notes, 'reminder': reminder, 'member': member, 'event_id': event_id, 'status': 'pending', 'role': 'member'}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection:
            connection.close()