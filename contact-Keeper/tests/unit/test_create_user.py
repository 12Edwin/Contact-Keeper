import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from auth_management.create_user.create_user import lambda_handler, generate_temporary_password


class TestCreateUser(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.create_user.create_user.validate_nickname')
    @patch('auth_management.create_user.create_user.validate_email')
    @patch('auth_management.create_user.create_user.validate_user_type')
    @patch('auth_management.create_user.create_user.validate_name')
    @patch('auth_management.create_user.create_user.validate_birthday')
    @patch('auth_management.create_user.create_user.validate_phone')
    @patch('auth_management.create_user.create_user.exists_user_phone')
    @patch('boto3.client')
    @patch('auth_management.create_user.create_user.get_cognito_ids')
    @patch('auth_management.create_user.create_user.get_db_connection')
    def test_create_user_success(self, mock_get_db_connection, mock_get_cognito_ids, mock_boto3_client,
                                 mock_exists_user_phone, mock_validate_phone, mock_validate_birthday,
                                 mock_validate_name, mock_validate_user_type, mock_validate_email,
                                 mock_validate_nickname):
        # Configure all validation mocks to return True
        mock_validate_nickname.return_value = True
        mock_validate_email.return_value = True
        mock_validate_user_type.return_value = True
        mock_validate_name.return_value = True
        mock_validate_birthday.return_value = True
        mock_validate_phone.return_value = True
        mock_exists_user_phone.return_value = False

        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_create_user.return_value = {'User': {'Username': 'test_user'}}

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {
            'body': json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'user_type': 'normal',
                'name': 'John',
                'surname': 'Doe',
                'last_name': 'Smith',
                'birthday': '1990-01-01',
                'phone': '1234567890'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        mock_client.admin_create_user.assert_called_once()
        mock_client.admin_add_user_to_group.assert_called_once()
        mock_cursor.execute.assert_called_once()

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.create_user.create_user.validate_nickname')
    def test_create_user_invalid_username(self, mock_validate_nickname):
        mock_validate_nickname.return_value = False

        event = {
            'body': json.dumps({
                'username': 'invalid_username',
                'email': 'test@example.com'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.INVALID_USERNAME), response['body'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('auth_management.create_user.create_user.validate_nickname')
    @patch('auth_management.create_user.create_user.validate_email')
    @patch('auth_management.create_user.create_user.validate_user_type')
    @patch('auth_management.create_user.create_user.validate_name')
    @patch('auth_management.create_user.create_user.validate_birthday')
    @patch('auth_management.create_user.create_user.validate_phone')
    @patch('auth_management.create_user.create_user.exists_user_phone')
    @patch('boto3.client')
    @patch('auth_management.create_user.create_user.get_cognito_ids')
    def test_create_user_already_exists(self, mock_get_cognito_ids, mock_boto3_client,
                                        mock_exists_user_phone, mock_validate_phone, mock_validate_birthday,
                                        mock_validate_name, mock_validate_user_type, mock_validate_email,
                                        mock_validate_nickname):
        # Configure all validation mocks to return True
        mock_validate_nickname.return_value = True
        mock_validate_email.return_value = True
        mock_validate_user_type.return_value = True
        mock_validate_name.return_value = True
        mock_validate_birthday.return_value = True
        mock_validate_phone.return_value = True
        mock_exists_user_phone.return_value = False

        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_client = MagicMock()
        mock_boto3_client.return_value = mock_client

        mock_client.admin_create_user.side_effect = Exception('UsernameExistsException')

        event = {
            'body': json.dumps({
                'username': 'existinguser',
                'email': 'existing@example.com',
                'user_type': 'normal',
                'name': 'John',
                'surname': 'Doe',
                'last_name': 'Smith',
                'birthday': '1990-01-01',
                'phone': '1234567890'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn(ErrorType.english(ErrorType.USER_ALREADY_EXISTS), response['body'])

    def test_generate_temporary_password(self):
        password = generate_temporary_password()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "!@#$%^&*(),.?:{}|<>" for c in password))


if __name__ == '__main__':
    unittest.main()
