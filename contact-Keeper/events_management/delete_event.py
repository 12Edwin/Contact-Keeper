import datetime
import pymysql
from .commons.utils import validate_id, exists_by_id
from .commons.database import get_db_connection
from .commons.type_response import response_200, response_400, response_500
from .commons.ErrorType import ErrorType
from .read_event import read_event


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def lambda_handler(event, context):
    try:
        data = delete_event(event['pathParameters'])
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def delete_event(parameters):
    connection = None
    try:
        _id = parameters.get('id')
        if not validate_id(_id):
            raise ValueError(ErrorType.INVALID_ID)
        if not exists_by_id(_id):
            raise ValueError(ErrorType.EVENT_NOT_FOUND)
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
