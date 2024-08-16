import json
import os
import sys
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_group, validate_name, exists_user, validate_opt_name


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        body = json.loads(event['body'])
        data = create_group(body)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def create_group(group):
    message = group.get('message')
    id_group = group.get('id_group')
    author = group.get('author')

    # Validate the attributes
    if not validate_name(message):
        raise ValueError(ErrorType.INVALID_NAME)
    if not exists_group(id_group):
        raise ValueError(ErrorType.INVALID_REMINDER)
    if not exists_user(author):
        raise ValueError(ErrorType.USER_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO `messages` (`message`, `status`, `id_group_member`, `person_id`) VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (message, 'unread', id_group, author))
            connection.commit()
            return {'id': cursor.lastrowid, 'message': message, 'status': 'unread', 'id_group_member': id_group, 'person_id': author}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection:
            connection.close()