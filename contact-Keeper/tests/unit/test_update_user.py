import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from user_management.update_user.update_user import lambda_handler as update_user


class TestUpdateUser(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.update_user.update_user.get_db_connection')
    @patch('user_management.update_user.update_user.get_cognito_ids')
    @patch('boto3.client')
    @patch('user_management.update_user.update_user.exists_user')
    @patch('user_management.update_user.update_user.validate_name')
    @patch('user_management.update_user.update_user.validate_birthday')
    @patch('user_management.update_user.update_user.validate_phone')
    def test_update_user_success(self, mock_validate_phone, mock_validate_birthday, mock_validate_name, mock_exists_user, mock_boto3_client, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_cognito_client = MagicMock()
        mock_boto3_client.return_value = mock_cognito_client
        mock_cognito_client.admin_list_groups_for_user.return_value = {
            'Groups': [{'GroupName': 'Administrators'}]
        }
        mock_exists_user.return_value = True
        mock_validate_name.return_value = True
        mock_validate_birthday.return_value = True
        mock_validate_phone.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        data = {
            'id': 1,
            'name': 'user name',
            'surname': 'user surname',
            'last_name': 'user last_name',
            'birthday': '2000-01-01',
            'phone': '1234567890'
        }
        result = update_user({'requestContext':{'authorizer':{'claims': mock_cognito_client}}, 'body': json.dumps(data), 'pathParameters': {'id': '1'}}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)
