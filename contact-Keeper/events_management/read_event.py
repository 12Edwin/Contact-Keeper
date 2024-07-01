import datetime

import boto3

from commons.ErrorType import ErrorType
from commons.database import get_db_connection
from commons.type_response import response_200, response_400, response_500, response_403
from commons.utils import validate_id, exists_by_id


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def lambda_handler(event, context):
    try:
        claims = event['requestContext']['authorizer']['claims']

        cognito_client = boto3.client('cognito-idp')
        user_groups = cognito_client.admin_list_groups_for_user(
            UserPoolId='us-east-1_4uOsWbva9',
            Username=claims['cognito:username']
        )

        is_admin = any(group['GroupName'] == 'Administrators' for group in user_groups['Groups'])

        if not is_admin:
            return response_403("Access denied. Administrator role required.")
        data = read_event(event['pathParameters'])
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def read_event(parameters):
    connection = None
    try:

        _id = parameters.get('id')
        if not validate_id(_id):
            raise ValueError(ErrorType.INVALID_ID)
        if not exists_by_id(_id):
            raise ValueError(ErrorType.EVENT_NOT_FOUND)

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
