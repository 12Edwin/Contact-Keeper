import json

import boto3

from commons.read_pool import get_cognito_ids
from commons.ErrorType import ErrorType
from commons.utils import validate_email, validate_password
from commons.type_response import response_200, response_500, response_400


def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')

    if not validate_email(email):
        return response_400(ErrorType.english(ErrorType.INVALID_EMAIL))
    if not validate_password(password):
        return response_400(ErrorType.english(ErrorType.INVALID_PASSWORD))

    client = boto3.client('cognito-idp')
    user_pool_id, user_pool_client_id = get_cognito_ids()
    try:
        response = client.initiate_auth(
            ClientId=user_pool_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )

        user_groups = client.admin_list_groups_for_user(
            Username=email,
            UserPoolId=user_pool_id
        )
        role = None
        if user_groups['Groups']:
            role = user_groups['Groups'][0]['GroupName']

        id_token = response['AuthenticationResult']['IdToken']
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        return response_200({
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": role
        })
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return response_500()