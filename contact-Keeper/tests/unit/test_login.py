import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from auth_management.login.login import lambda_handler


class TestLogin(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.login.login.validate_email')
    @patch('boto3.client')
    @patch('auth_management.login.login.get_cognito_ids')
    def test_login_success(self, mock_get_cognito_ids, mock_boto3_client, mock_validate_email):
        mock_validate_email.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.initiate_auth.return_value = {
            'AuthenticationResult': {
                'IdToken': 'id_token',
                'AccessToken': 'access_token',
                'RefreshToken': 'refresh_token'
            }
        }
        mock_client.admin_list_groups_for_user.return_value = {
            'Groups': [{'GroupName': 'Admin'}]
        }

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['data']['id_token'], 'id_token')
        self.assertEqual(body['data']['access_token'], 'access_token')
        self.assertEqual(body['data']['refresh_token'], 'refresh_token')
        self.assertEqual(body['data']['role'], 'Admin')

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.login.login.validate_email')
    def test_login_invalid_email(self, mock_validate_email):
        mock_validate_email.return_value = False

        event = {
            'body': json.dumps({
                'email': 'invalid_email',
                'password': 'password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_EMAIL), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.login.login.validate_email')
    @patch('boto3.client')
    @patch('auth_management.login.login.get_cognito_ids')
    def test_login_user_not_found(self, mock_get_cognito_ids, mock_boto3_client, mock_validate_email):
        mock_validate_email.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.initiate_auth.side_effect = Exception('UserNotFoundException')

        event = {
            'body': json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.USER_NOT_FOUND), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.login.login.validate_email')
    @patch('boto3.client')
    @patch('auth_management.login.login.get_cognito_ids')
    def test_login_invalid_password(self, mock_get_cognito_ids, mock_boto3_client, mock_validate_email):
        mock_validate_email.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.initiate_auth.side_effect = Exception('NotAuthorizedException')

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'wrong_password'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_PASSWORD), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.login.login.validate_email')
    @patch('boto3.client')
    @patch('auth_management.login.login.get_cognito_ids')
    def test_login_unexpected_error(self, mock_get_cognito_ids, mock_boto3_client, mock_validate_email):
        mock_validate_email.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.initiate_auth.side_effect = Exception('Unexpected error')

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 500)


if __name__ == '__main__':
    unittest.main()