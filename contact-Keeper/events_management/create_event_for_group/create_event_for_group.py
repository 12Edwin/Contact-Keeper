import json
import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, validate_id, exists_by_id, get_cognito_ids, exists_group, validate_name, validate_start_date, validate_end_date, validate_event_type


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        body = json.loads(event['body'])
        data = create_event(body)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def create_event(event):
    name = event.get('name')
    description = event.get('description')
    start_date = event.get('start_date')
    end_date = event.get('end_date')
    _type = event.get('type')
    location = event.get('location')
    id_group_member = event.get('id_group_member')

    # Validate the attributes
    if not validate_id(id_group_member):
        raise ValueError(ErrorType.INVALID_ID)
    if not exists_group(id_group_member):
        raise ValueError(ErrorType.GROUP_NOT_FOUND)
    if not validate_name(name):
        raise ValueError(ErrorType.INVALID_NAME)
    if not validate_start_date(start_date):
        raise ValueError(ErrorType.INVALID_START_DATE)
    if not validate_end_date(start_date, end_date):
        raise ValueError(ErrorType.INVALID_END_DATE)
    if not validate_event_type(_type):
        raise ValueError(ErrorType.INVALID_EVENT_TYPE)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            INSERT INTO events (name, description, start_date, end_date, type, location, id_group_member)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, description, start_date, end_date, _type, location, id_group_member))
            connection.commit()
            return {"message": "Event created successfully"}
    except pymysql.OperationalError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()