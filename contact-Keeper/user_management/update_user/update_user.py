import json

import boto3
import os
import sys

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_user, validate_name, validate_birthday, validate_phone


def lambda_handler(event, context):
    try:
        claims = event['requestContext']['authorizer']['claims']
        user_pool_id, user_pool_client_id = get_cognito_ids()
        cognito_client = boto3.client('cognito-idp')
        user_groups = cognito_client.admin_list_groups_for_user(
            UserPoolId=user_pool_id,
            Username=claims['cognito:username']
        )

        is_admin = any(group['GroupName'] == 'Administrators' for group in user_groups['Groups'])

        if not is_admin:
            return response_403("Access denied. Administrator role required.")
        body = json.loads(event['body'])
        data = update_user(event['pathParameters'], body)
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def update_user(parameters, body):
    connection = None
    try:
        _id = parameters.get('id')
        _name = body.get('name')
        _surname = body.get('surname')
        _last_name = body.get('last_name')
        _birthday = body.get('birthday')
        _phone = body.get('phone')

        if not exists_user(_id):
            raise ValueError(ErrorType.USER_NOT_FOUND)
        if not validate_name(_name):
            raise ValueError(ErrorType.INVALID_NAME)
        if not validate_name(_surname):
            raise ValueError(ErrorType.INVALID_SURNAME)
        if not validate_name(_last_name):
            raise ValueError(ErrorType.INVALID_LAST_NAME)
        if not validate_birthday(_birthday):
            raise ValueError(ErrorType.INVALID_BIRTHDAY)
        if not validate_phone(_phone):
            raise ValueError(ErrorType.INVALID_PHONE)

        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """UPDATE people SET name = %s, surname = %s, last_name = %s, birthday = %s, phone = %s WHERE id = %s"""
            cursor.execute(query, (_name, _surname, _last_name, _birthday, _phone, _id))
            connection.commit()
            return None
    finally:
        if connection is not None:
            connection.close()
