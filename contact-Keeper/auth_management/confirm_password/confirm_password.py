import json
import os
import sys
import boto3

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'commons', 'python'))

from app import get_cognito_ids, validate_email, validate_password, response_200, response_400, response_500, ErrorType


def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')
    new_password = body.get('new_password')

    if not validate_email(email):
        return response_400(ErrorType.english(ErrorType.INVALID_USERNAME))
    if not validate_password(new_password):
        return response_400(ErrorType.english(ErrorType.INVALID_PASSWORD))

    client = boto3.client('cognito-idp')
    user_pool_id, user_pool_client_id = get_cognito_ids()
    try:

        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=user_pool_client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )

        if response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            client.respond_to_auth_challenge(
                ClientId=user_pool_client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=response['Session'],
                ChallengeResponses={
                    'USERNAME': email,
                    'NEW_PASSWORD': new_password,
                    'email_verified': 'true'
                }
            )
            return response_200(response)
        else:
            return response_400("Error setting password: ChallengeName is not NEW_PASSWORD_REQUIRED")
    except Exception as e:
        print(f"Error setting password: {str(e)}")
        return response_500()