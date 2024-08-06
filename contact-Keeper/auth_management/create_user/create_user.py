import json
import os
import re
import sys
import random
import string
import boto3
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import get_cognito_ids, validate_nickname, validate_email, validate_user_type, validate_name, validate_birthday, validate_phone, response_200, response_400, response_500, ErrorType, get_db_connection


def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body.get('username')
    email = body.get('email')
    password = generate_temporary_password(8)
    user_type = body.get('user_type')
    name = body.get('name')
    surname = body.get('surname')
    last_name = body.get('last_name')
    birthday = body.get('birthday')
    phone = body.get('phone')

    if not validate_nickname(username):
        return response_400(ErrorType.english(ErrorType.INVALID_USERNAME))
    if not validate_email(email):
        return response_400(ErrorType.english(ErrorType.INVALID_EMAIL))
    if not validate_user_type(user_type):
        return response_400(ErrorType.english(ErrorType.INVALID_USER_TYPE))
    if not validate_name(name):
        return response_400(ErrorType.english(ErrorType.INVALID_NAME))
    if not validate_name(surname):
        return response_400(ErrorType.english(ErrorType.INVALID_SURNAME))
    if not validate_name(last_name):
        return response_400(ErrorType.english(ErrorType.INVALID_LAST_NAME))
    if not validate_birthday(birthday):
        return response_400(ErrorType.english(ErrorType.INVALID_BIRTHDAY))
    if not validate_phone(phone):
        return response_400(ErrorType.english(ErrorType.INVALID_PHONE))

    client = boto3.client('cognito-idp')
    user_pool_id, user_pool_client_id = get_cognito_ids()
    connection = None
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

        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                    INSERT INTO people (name, surname, last_name, birthday, phone, id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (name, surname, last_name, birthday, phone, response['User']['Username']))
            connection.commit()
            return response_200(response)
    except pymysql.OperationalError as e:
        print(e)
        raise RuntimeError(ErrorType.CONNECTION_ERROR)
    except Exception as e:
        print(e)
        raise RuntimeError(ErrorType.INTERNAL_SERVER_ERROR)
    finally:
        if connection is not None:
            connection.close()


def generate_temporary_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*(),.?:{}|<>"
    all_characters = lowercase + uppercase + digits + special_characters

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?:{}|<>]).{' + str(length) + r',}$'

    while True:
        # Aseguramos al menos un carácter de cada tipo
        password = (random.choice(lowercase) +
                    random.choice(uppercase) +
                    random.choice(digits) +
                    random.choice(special_characters) +
                    ''.join(random.choices(all_characters, k=length - 4)))

        # Mezclamos la contraseña
        password = ''.join(random.sample(password, len(password)))

        if re.match(pattern, password):
            return password
