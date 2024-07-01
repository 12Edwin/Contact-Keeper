import json
import random
import string

import boto3
from commons.read_pool import get_cognito_ids
from commons.utils import validate_username, validate_email, validate_password, validate_user_type
from commons.type_response import response_200, response_400, response_500
from commons.ErrorType import ErrorType


def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body.get('username')
    email = body.get('email')
    password = generate_temporary_password(8)
    user_type = body.get('user_type')

    if not validate_username(username):
        return response_400(ErrorType.english(ErrorType.INVALID_USERNAME))
    if not validate_email(email):
        return response_400(ErrorType.english(ErrorType.INVALID_EMAIL))
    if not validate_password(password):
        return response_400(ErrorType.english(ErrorType.INVALID_PASSWORD))
    if not validate_user_type(user_type):
        return response_400(ErrorType.english(ErrorType.INVALID_USER_TYPE))

    client = boto3.client('cognito-idp')
    user_pool_id, user_pool_client_id = get_cognito_ids()
    try:
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'false'},
                {'Name': 'name', 'Value': username}
            ],
            TemporaryPassword=password
        )

        if user_type == 'admin':
            client.admin_add_user_to_group(
                UserPoolId=user_pool_id,
                Username=email,
                GroupName='Administrators'
            )
        else:
            client.admin_add_user_to_group(
                UserPoolId=user_pool_id,
                Username=email,
                GroupName='NormalUsers'
            )

        return response_200(response)
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return response_500()


def generate_temporary_password(length=12):
    special_characters = '^$*.[]{}()?-"!@#%&/\\,><\':;|_~`+= '
    characters = string.ascii_letters + string.digits + special_characters

    while True:
        # Genera una contraseña aleatoria
        password = ''.join(random.choice(characters) for _ in range(length))

        # Verifica los criterios
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_special = any(char in special_characters for char in password)

        if has_digit and has_upper and has_lower and has_special and len(password) >= 8:
            return password