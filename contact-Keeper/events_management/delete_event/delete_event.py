import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import validate_id, exists_by_id, get_db_connection, response_200, response_400, response_500, ErrorType


def lambda_handler(event, context):
    try:
        data = delete_event(event['pathParameters'])
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def delete_event(parameters):
    _id = parameters.get('id')
    if not validate_id(_id):
        raise ValueError(ErrorType.INVALID_ID)
    if not exists_by_id(_id):
        raise ValueError(ErrorType.EVENT_NOT_FOUND)

    connection = None
    try:
        event = read_event({'id': _id})
        status = 'canceled' if event.get('status') == 'pending' else 'pending'
        connection = get_db_connection()
        with connection.cursor() as cursor:
            update_query = """UPDATE events SET status = %s WHERE id = %s"""
            cursor.execute(update_query, (status, _id))
            connection.commit()
            message = "Event canceled successfully" if status == 'canceled' else "Event reactivated successfully"
            return {"message": message}
    except pymysql.OperationalError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()


def read_event(parameters):
    _id = parameters.get('id')
    if not validate_id(_id):
        raise ValueError(ErrorType.INVALID_ID)
    if not exists_by_id(_id):
        raise ValueError(ErrorType.EVENT_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT * FROM events WHERE id = %s"""
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
