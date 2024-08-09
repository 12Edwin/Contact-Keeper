import json
import os
import sys
import boto3

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import get_cognito_ids, ErrorType, validate_email, response_200, response_500, response_400


def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')

    if not validate_email(email):
        return response_400(ErrorType.english(ErrorType.INVALID_EMAIL))

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
        print(f"Error logining: {str(e)}")
        if str(e).find("UserNotFoundException") != -1:
            return response_400(ErrorType.english(ErrorType.USER_NOT_FOUND))
        if str(e).find("NotAuthorizedException") != -1:
            return response_400(ErrorType.english(ErrorType.INVALID_PASSWORD))
        return response_500()