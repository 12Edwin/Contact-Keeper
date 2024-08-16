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
from group_management.assign_member.assign_member import lambda_handler as assign_member


class TestAssignMember(unittest.TestCase):

        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('group_management.assign_member.assign_member.get_db_connection')
        @patch('group_management.assign_member.assign_member.get_cognito_ids')
        @patch('group_management.assign_member.assign_member.exists_user')
        @patch('group_management.assign_member.assign_member.validate_name')
        @patch('group_management.assign_member.assign_member.validate_opt_name')
        @patch('group_management.assign_member.assign_member.exists_group')
        def test_assign_member_success(self, mock_exists_group, mock_validate_opt_name, mock_validate_name,
                                       mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = True
            mock_validate_name.return_value = True
            mock_validate_opt_name.return_value = True
            mock_exists_group.return_value = True

            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_get_db_connection.return_value = mock_connection
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.return_value = None

            data = {
                'title': 'title',
                'notes': 'notes',
                'group_id': 1,
                'member': 1
            }
            result = assign_member({'body': json.dumps(data)}, {})

            expected_result = 200
            self.assertEqual(result['statusCode'], expected_result)


        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('group_management.assign_member.assign_member.get_cognito_ids')
        @patch('group_management.assign_member.assign_member.exists_user')
        def test_assign_member_invalid_user(self, mock_exists_user, mock_get_cognito_ids):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = False

            data = {
                'title': 'title',
                'notes': 'notes',
                'group_id': 1,
                'member': 1
            }
            result = assign_member({'body': json.dumps(data)}, {})

            expected_result = 400
            self.assertEqual(result['statusCode'], expected_result)
            self.assertEqual(json.loads(result['body'])['message'], ErrorType.english(ErrorType.USER_NOT_FOUND))


        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('group_management.assign_member.assign_member.get_db_connection')
        @patch('group_management.assign_member.assign_member.get_cognito_ids')
        @patch('group_management.assign_member.assign_member.exists_user')
        @patch('group_management.assign_member.assign_member.validate_name')
        @patch('group_management.assign_member.assign_member.validate_opt_name')
        @patch('group_management.assign_member.assign_member.exists_group')
        def test_assign_member_invalid_title(self, mock_exists_group, mock_validate_opt_name, mock_validate_name,
                                            mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = True
            mock_validate_name.return_value = True
            mock_validate_opt_name.return_value = True
            mock_exists_group.return_value = True

            mock_get_db_connection.side_effect = pymysql.MySQLError('Error connection')

            data = {
                'title': 'title',
                'notes': 'notes',
                'group_id': 1,
                'member': 1
            }
            result = assign_member({'body': json.dumps(data)}, {})

            expected_result = response_500(ErrorType.CONNECTION_ERROR)
            self.assertEqual(result, expected_result)