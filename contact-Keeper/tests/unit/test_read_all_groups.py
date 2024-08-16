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
from group_management.read_all_groups.read_all_groups import lambda_handler as read_all_groups


class TestReadAllGroups(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.read_all_groups.read_all_groups.get_db_connection')
    @patch('group_management.read_all_groups.read_all_groups.get_cognito_ids')
    def test_read_all_groups_success(self, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'group name', 'group description', 'group title', 'group notes', 'group reminder', 1)]

        result = read_all_groups({}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)


    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('group_management.read_all_groups.read_all_groups.get_db_connection')
    @patch('group_management.read_all_groups.read_all_groups.get_cognito_ids')
    def test_read_all_groups_error_connection(self, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
        mock_get_db_connection.side_effect = pymysql.MySQLError('Error connection')

        result = read_all_groups({}, {})

        expected_result = response_500(ErrorType.CONNECTION_ERROR)
        self.assertEqual(result, expected_result)
