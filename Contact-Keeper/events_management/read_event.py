import json
import datetime
from commons.database import get_db_connection


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def lambda_handler(event, context):
    data = read_event(event['pathParameters']['id'])
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": data
        }, default=datetime_handler),
    }


def read_event(id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT * FROM events WHERE id = %s"""
            cursor.execute(query, id)
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
