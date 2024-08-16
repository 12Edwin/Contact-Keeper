import json
import os
import sys
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import validate_name, validate_start_date, validate_end_date, validate_event_type, exists_group, validate_id, exists_by_id, get_db_connection, response_200, response_400, response_500, ErrorType, validate_status_event


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        data = update_event(body)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def update_event(event):
    id_event = event.get('id')
    status = event.get('status')

    # Validate the attributes
    if not validate_id(id_event):
        raise ValueError(ErrorType.INVALID_ID)
    if not validate_status_event(status):
        raise ValueError(ErrorType.INVALID_EVENT_STATUS)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            UPDATE events SET status = %s WHERE id = %s
            """
            cursor.execute(query, (status, id_event))
            connection.commit()
            return {"message": "Event updated successfully"}
    except pymysql.OperationalError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()