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
from group_management.create_group.create_group import lambda_handler as create_group, create_group as create_group_func, create_meet_member


class TestCreateGroup(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.create_group.create_group.get_db_connection')
    @patch('group_management.create_group.create_group.get_cognito_ids')
    @patch('group_management.create_group.create_group.validate_name')
    @patch('group_management.create_group.create_group.validate_opt_name')
    @patch('group_management.create_group.create_group.exists_user')
    def test_create_group_func_success(self, mock_exists_user, mock_validate_opt_name, mock_validate_name, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_exists_user.return_value = True
        mock_validate_name.return_value = True
        mock_validate_opt_name.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = {'id': 1, 'name': 'group name', 'description': 'group description'}

        data = {
            'name': 'group name',
            'description': 'group description',
            'title': 'group title',
            'notes': 'group notes',
            'reminder': 'group reminder',
            'moderator': 1
        }
        result = create_group_func(data)

        expected_result = {'id': 1, 'name': 'group name', 'description': 'group description'}
        self.assertEqual(result['name'], expected_result['name'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.create_group.create_group.get_db_connection')
    @patch('group_management.create_group.create_group.get_cognito_ids')
    @patch('group_management.create_group.create_group.validate_name')
    @patch('group_management.create_group.create_group.validate_opt_name')
    @patch('group_management.create_group.create_group.exists_user')
    def test_create_group_func_connection_error(self, mock_exists_user, mock_validate_opt_name, mock_validate_name,
                                       mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_exists_user.return_value = True
        mock_validate_name.return_value = True
        mock_validate_opt_name.return_value = True

        mock_get_db_connection.side_effect = pymysql.MySQLError

        data = {
            'name': 'group name',
            'description': 'group description',
            'title': 'group title',
            'notes': 'group notes',
            'reminder': 'group reminder',
            'moderator': 1
        }

        try:
            create_group_func(data)
        except RuntimeError as e:
            self.assertEqual(str(e), ErrorType.CONNECTION_ERROR)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.create_group.create_group.get_db_connection')
    @patch('group_management.create_group.create_group.get_cognito_ids')
    def test_create_meet_success(self, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = {'id': 1, 'name': 'group name', 'description': 'group description'}

        data = {
            'name': 'group name',
            'description': 'group description',
            'title': 'group title',
            'notes': 'group notes',
            'reminder': 'group reminder',
            'moderator': 1
        }
        result = create_meet_member(data, 1)

        expected_result = {"message": "group created successfully"}
        self.assertEqual(result['message'], expected_result['message'])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.create_group.create_group.get_db_connection')
    @patch('group_management.create_group.create_group.get_cognito_ids')
    def test_create_meet_connection_error(self, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_get_db_connection.side_effect = pymysql.OperationalError

        data = {
            'name': 'group name',
            'description': 'group description',
            'title': 'group title',
            'notes': 'group notes',
            'reminder': 'group reminder',
            'moderator': 1
        }

        try:
            create_meet_member(data, 1)
        except RuntimeError as e:
            self.assertEqual(str(e), ErrorType.CONNECTION_ERROR)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.create_group.create_group.get_cognito_ids')
    @patch('group_management.create_group.create_group.create_group')
    def test_create_group_invalid_user(self, mock_creat_group, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_creat_group.side_effect = ValueError(ErrorType.USER_NOT_FOUND)

        data = {
            'name': 'group name',
            'description': 'group description',
            'title': 'group title',
            'notes': 'group notes',
            'reminder': 'group reminder',
            'moderator': 1
        }
        result = create_group({'body': json.dumps(data)}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['message'], ErrorType.english(ErrorType.USER_NOT_FOUND))