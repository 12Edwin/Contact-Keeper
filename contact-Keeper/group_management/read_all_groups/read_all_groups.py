import json
import os
import sys
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids, exists_group, validate_name, exists_user, validate_opt_name


def lambda_handler(event, context):
    try:
        user_pool_id, user_pool_client_id = get_cognito_ids()
        data = read_groups()
        return response_200(data)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def read_groups():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM `group_members`
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows is not None:
                column_names = [desc[0] for desc in cursor.description]
                data = []
                for row in rows:
                    data.append(dict(zip(column_names, row)))
                return data
            else:
                return []
    except pymysql.MySQLError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()