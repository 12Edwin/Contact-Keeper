import boto3
import os
import sys

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, validate_id, exists_group, get_cognito_ids


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        data = read_events(event['pathParameters'])
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def read_events(parameters):
    connection = None
    try:
        _id = parameters.get('id')
        if not exists_group(_id):
            raise ValueError(ErrorType.GROUP_NOT_FOUND)

        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT e.* FROM meets m LEFT JOIN events e ON e.id = m.event_id WHERE group_id = %s"""
            cursor.execute(query, _id)
            row = cursor.fetchone()
            if row is not None:
                column_names = [desc[0] for desc in cursor.description]
                row_dict = dict(zip(column_names, row))
                return row_dict
            else:
                return None
    finally:
        if connection is not None:
            connection.close()
