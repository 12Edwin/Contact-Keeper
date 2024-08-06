import json
import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_group, validate_name, exists_user, validate_opt_name

def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        body = json.loads(event['body'])
        result = create_meet_member(body)
        return response_200(result)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def create_meet_member(body):
    title = body.get('title')
    notes = body.get('notes')
    group_id = body.get('group_id')
    member = body.get('member')

    # Validate the attributes
    if not exists_user(member):
        raise ValueError(ErrorType.USER_NOT_FOUND)
    if not validate_name(title):
        raise ValueError(ErrorType.INVALID_TITLE)
    if not validate_opt_name(notes):
        raise ValueError(ErrorType.INVALID_NOTES)
    if not exists_group(group_id):
        raise ValueError(ErrorType.GROUP_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO meets (title, notes, group_id, person_id, status, role) VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (title, notes, group_id, member, 'pending', 'member'))
            connection.commit()
            return {'title': title, 'notes': notes, 'group_id': group_id, 'member': member, 'status': 'pending', 'role': 'member'}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.DATABASE_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        connection.close()
