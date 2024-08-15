import boto3
import os
import sys

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import ErrorType, get_db_connection, response_200, response_400, response_500, response_403, get_cognito_ids


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
        cognito_users = get_cognito_users(cognito_client, user_pool_id)
        data = read_users()
        result = compare_users(cognito_users, data)
        return response_200(result)
    except ValueError as e:
        return response_400(ErrorType.english(str(e)))
    except RuntimeError as e:
        return response_500(ErrorType.english(str(e)))


def get_cognito_users(cognito_client, user_pool_id):
    users = []
    pagination_token = None
    while True:
        if pagination_token:
            response = cognito_client.list_users(
                UserPoolId=user_pool_id,
                PaginationToken=pagination_token
            )
        else:
            response = cognito_client.list_users(UserPoolId=user_pool_id)

        users.extend(response['Users'])

        if 'PaginationToken' in response:
            pagination_token = response['PaginationToken']
        else:
            break

    return {user['Username']: user for user in users}


def read_users():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """SELECT * FROM people"""
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows is not None:
                column_names = [desc[0] for desc in cursor.description]
                data = []
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    data.append(row_dict)
                return data
            else:
                return {}
    finally:
        if connection is not None:
            connection.close()


def compare_users(cognito_users, db_users):
    matched_users = []

    for username, cognito_user in cognito_users.items():
        for db_user in db_users:
            if db_user.get('id') == username:
                matched_users.append({
                    'email': cognito_user['Attributes'][0]['Value'],
                    'id': db_user.get('id'),
                    'name': db_user.get('name'),
                    'surname': db_user.get('surname'),
                    'last_name': db_user.get('last_name'),
                    'birthday': db_user.get('birthday'),
                    'phone': db_user.get('phone')
                })
                break

    return matched_users
