import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from auth_management.confirm_password.confirm_password import lambda_handler


class TestConfirmPassword(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    @patch('auth_management.confirm_password.confirm_password.validate_password')
    @patch('boto3.client')
    @patch('auth_management.confirm_password.confirm_password.get_cognito_ids')
    def test_confirm_password_success(self, mock_get_cognito_ids, mock_boto3_client,
                                      mock_validate_password, mock_validate_email):
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': 'session_token'
        }
        mock_client.respond_to_auth_challenge.return_value = {'success': True}

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'old_password',
                'new_password': 'new_password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        mock_client.admin_initiate_auth.assert_called_once()
        mock_client.respond_to_auth_challenge.assert_called_once()

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    def test_confirm_password_invalid_email(self, mock_validate_email):
        mock_validate_email.return_value = False

        event = {
            'body': json.dumps({
                'email': 'invalid_email',
                'password': 'old_password',
                'new_password': 'new_password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_USERNAME), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    @patch('auth_management.confirm_password.confirm_password.validate_password')
    def test_confirm_password_invalid_new_password(self, mock_validate_password, mock_validate_email):
        mock_validate_email.return_value = True
        mock_validate_password.return_value = False

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'old_password',
                'new_password': 'weak'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_PASSWORD), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    @patch('auth_management.confirm_password.confirm_password.validate_password')
    @patch('boto3.client')
    @patch('auth_management.confirm_password.confirm_password.get_cognito_ids')
    def test_confirm_password_user_not_found(self, mock_get_cognito_ids, mock_boto3_client,
                                             mock_validate_password, mock_validate_email):
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_initiate_auth.side_effect = Exception('UserNotFoundException')

        event = {
            'body': json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'old_password',
                'new_password': 'new_password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.USER_NOT_FOUND), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    @patch('auth_management.confirm_password.confirm_password.validate_password')
    @patch('boto3.client')
    @patch('auth_management.confirm_password.confirm_password.get_cognito_ids')
    def test_confirm_password_invalid_old_password(self, mock_get_cognito_ids, mock_boto3_client,
                                                   mock_validate_password, mock_validate_email):
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_initiate_auth.side_effect = Exception('NotAuthorizedException')

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'wrong_password',
                'new_password': 'new_password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_PASSWORD), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.confirm_password.confirm_password.validate_email')
    @patch('auth_management.confirm_password.confirm_password.validate_password')
    @patch('boto3.client')
    @patch('auth_management.confirm_password.confirm_password.get_cognito_ids')
    def test_confirm_password_unexpected_challenge(self, mock_get_cognito_ids, mock_boto3_client,
                                                   mock_validate_password, mock_validate_email):
        mock_validate_email.return_value = True
        mock_validate_password.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'UNEXPECTED_CHALLENGE',
            'Session': 'session_token'
        }

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'old_password',
                'new_password': 'new_password123'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn("Error setting password: ChallengeName is not NEW_PASSWORD_REQUIRED", response['body'])


if __name__ == '__main__':
    unittest.main()