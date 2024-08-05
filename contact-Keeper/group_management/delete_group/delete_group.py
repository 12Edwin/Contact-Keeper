import json
import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_group, validate_name, exists_user, validate_opt_name


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        params = event['pathParameters']
        group_status = get_group_status(params)
        result = delete_group(params['id'], group_status)
        return response_200(result)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def get_group_status(params):
    group_id = params.get('id')
    if not exists_group(group_id):
        raise ValueError(ErrorType.GROUP_NOT_FOUND)
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            SELECT `status` FROM `group_members` WHERE `id` = %s
            """
            cursor.execute(query, (group_id))
            result = cursor.fetchone()
            return result[0] if result else None
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)


def delete_group(group_id, status):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            UPDATE `group_members` SET status = %s WHERE `id` = %s
            """
            cursor.execute(query, (not status, group_id))
            connection.commit()
            return {'id': group_id}
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)