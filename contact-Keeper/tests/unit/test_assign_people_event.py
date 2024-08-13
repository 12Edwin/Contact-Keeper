import unittest
import os
import sys
from unittest.mock import patch, MagicMock

import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.assign_people_event.assign_people_event import lambda_handler as assign_people_event


class TestAssignPeopleEvent(unittest.TestCase):

        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('events_management.assign_people_event.assign_people_event.get_db_connection')
        @patch('events_management.assign_people_event.assign_people_event.get_cognito_ids')
        @patch('events_management.assign_people_event.assign_people_event.exists_user')
        @patch('events_management.assign_people_event.assign_people_event.validate_name')
        @patch('events_management.assign_people_event.assign_people_event.validate_opt_name')
        @patch('events_management.assign_people_event.assign_people_event.exists_event')
        def test_assign_people_event_success(self, mock_exists_event, mock_validate_opt_name, mock_validate_name, mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = True
            mock_validate_name.return_value = True
            mock_validate_opt_name.return_value = True
            mock_exists_event.return_value = True
            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_get_db_connection.return_value = mock_connection
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
            event = {'body': '{"title": "title", "notes": "notes", "reminder": "reminder", "member": "member", "event_id": "event_id"}'}
            result = assign_people_event(event, {})
            expected_result = 200
            self.assertEqual(result['statusCode'], expected_result)

        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('events_management.assign_people_event.assign_people_event.get_cognito_ids')
        @patch('events_management.assign_people_event.assign_people_event.exists_user')
        def test_assign_people_event_user_not_found(self, mock_exists_user, mock_get_cognito_ids):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = False
            event = {'body': '{"title": "title", "notes": "notes", "reminder": "reminder", "member": "member", "event_id": "event_id"}'}
            result = assign_people_event(event, {})
            expected_result = 400
            self.assertEqual(result['statusCode'], expected_result)

        @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
        @patch('events_management.assign_people_event.assign_people_event.get_db_connection')
        @patch('events_management.assign_people_event.assign_people_event.get_cognito_ids')
        @patch('events_management.assign_people_event.assign_people_event.exists_user')
        @patch('events_management.assign_people_event.assign_people_event.validate_name')
        @patch('events_management.assign_people_event.assign_people_event.validate_opt_name')
        @patch('events_management.assign_people_event.assign_people_event.exists_event')
        def test_assign_people_event_invalid_title(self, mock_exists_event, mock_validate_opt_name, mock_validate_name, mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
            mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')
            mock_exists_user.return_value = True
            mock_validate_name.return_value = True
            mock_validate_opt_name.return_value = True
            mock_exists_event.return_value = True

            mock_get_db_connection.side_effect = pymysql.MySQLError('Mocked error message')
            event = {'body': '{"title": "", "notes": "notes", "reminder": "reminder", "member": "member", "event_id": "event_id"}'}
            result = assign_people_event(event, {})
            expected_result = response_500(ErrorType.CONNECTION_ERROR)
            self.assertEqual(result, expected_result)