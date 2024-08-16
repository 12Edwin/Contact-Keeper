import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from group_management.update_group.update_group import lambda_handler as update_group


class TestUpdateGroup(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.update_group.update_group.get_db_connection')
    @patch('group_management.update_group.update_group.get_cognito_ids')
    @patch('group_management.update_group.update_group.exists_group')
    @patch('group_management.update_group.update_group.validate_name')
    @patch('group_management.update_group.update_group.validate_opt_name')
    def test_update_group_success(self, mock_validate_opt_name, mock_validate_name, mock_exists_group, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_validate_opt_name.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        data = {
            'id': 1,
            'name': 'group name',
            'description': 'group description'
        }
        result = update_group({'body': json.dumps(data)}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)


    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.update_group.update_group.get_cognito_ids')
    @patch('group_management.update_group.update_group.exists_group')
    def test_update_group_invalid_name(self, mock_exists_group, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_exists_group.return_value = False

        data = {
            'id': 1,
            'name': 'group name',
            'description': 'group description'
        }
        result = update_group({'body': json.dumps(data)}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['message'], ErrorType.english(ErrorType.GROUP_NOT_FOUND))


    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.update_group.update_group.get_db_connection')
    @patch('group_management.update_group.update_group.get_cognito_ids')
    @patch('group_management.update_group.update_group.exists_group')
    @patch('group_management.update_group.update_group.validate_name')
    @patch('group_management.update_group.update_group.validate_opt_name')
    def test_update_group_error_connection(self, mock_validate_opt_name, mock_validate_name, mock_exists_group, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_validate_opt_name.return_value = True

        mock_get_db_connection.side_effect = pymysql.MySQLError('Error connection')

        data = {
            'id': 1,
            'name': 'group name',
            'description': 'group description'
        }
        result = update_group({'body': json.dumps(data)}, {})

        expected_result = response_500(ErrorType.CONNECTION_ERROR)
        self.assertEqual(result, expected_result)