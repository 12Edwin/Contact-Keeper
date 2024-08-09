import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, validate_id, exists_by_id, get_cognito_ids, exists_group, validate_name, validate_start_date, validate_end_date, validate_event_type, exists_user, validate_opt_name, exists_event

def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        path_parameters = event['pathParameters']
        id_person = path_parameters.get('id_person')
        id_event = path_parameters.get('id_event')
        data = unassign_people_event(id_person, id_event)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def unassign_people_event(id_person, id_event):
    if not exists_user(id_person):
        raise ValueError(ErrorType.USER_NOT_FOUND)
    if not exists_event(id_event):
        raise ValueError(ErrorType.EVENT_NOT_FOUND)

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
             DELETE FROM meets WHERE person_id = %s AND event_id = %s
             """
            cursor.execute(query, (id_person, id_event))
            connection.commit()
            return {'message': 'Meet deleted', 'person_id': id_person, 'event_id': id_event}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.DATABASE_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()