import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from events_management.create_event_for_meet.create_event_for_meet import create_event, create_meet_admin, lambda_handler as create_event_meet


class TestCreateEvent(unittest.TestCase):

    @patch('events_management.create_event_for_meet.create_event_for_meet.get_cognito_ids')
    @patch('events_management.create_event_for_meet.create_event_for_meet.create_event')
    @patch('events_management.create_event_for_meet.create_event_for_meet.create_meet_admin')
    def test_lambda_handler_success(self, mock_create_meet_admin, mock_create_event, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_create_event.return_value = {'id': 1}
        mock_create_meet_admin.return_value = {'message': 'event created successfully', 'id': 1}

        event = {
            'body': json.dumps({
                'name': 'Test Event',
                'description': 'Description',
                'start_date': '2024-08-10',
                'end_date': '2024-08-11',
                'type': 'meeting',
                'location': 'Online',
                'moderator': 'user123',
                'title': 'Test Title',
                'notes': 'Some notes',
                'reminder': '1 hour before'
            })
        }

        result = create_event_meet(event, {})
        self.assertEqual(result['statusCode'], 200)

    @patch('events_management.create_event_for_meet.create_event_for_meet.get_cognito_ids')
    @patch('events_management.create_event_for_meet.create_event_for_meet.create_event')
    def test_lambda_handler_value_error(self, mock_create_event, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_create_event.side_effect = ValueError(ErrorType.INVALID_NAME)

        event = {
            'body': json.dumps({
                'name': '',  # Invalid name
                'description': 'Description',
                'start_date': '2024-08-10',
                'end_date': '2024-08-11',
                'type': 'meeting',
                'location': 'Online',
                'moderator': 'user123',
                'title': 'Test Title',
                'notes': 'Some notes',
                'reminder': '1 hour before'
            })
        }

        result = create_event_meet(event, {})
        self.assertEqual(result['statusCode'], 400)

    @patch('events_management.create_event_for_meet.create_event_for_meet.get_cognito_ids')
    @patch('events_management.create_event_for_meet.create_event_for_meet.create_event')
    def test_lambda_handler_runtime_error(self, mock_create_event, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_create_event.side_effect = RuntimeError(ErrorType.CONNECTION_ERROR)

        event = {
            'body': json.dumps({
                'name': 'Test Event',
                'description': 'Description',
                'start_date': '2024-08-10',
                'end_date': '2024-08-11',
                'type': 'meeting',
                'location': 'Online',
                'moderator': 'user123',
                'title': 'Test Title',
                'notes': 'Some notes',
                'reminder': '1 hour before'
            })
        }

        result = create_event_meet(event, {})
        self.assertEqual(result['statusCode'], 500)

    @patch('events_management.create_event_for_meet.create_event_for_meet.exists_user')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_name')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_start_date')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_end_date')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_event_type')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_opt_name')
    @patch('events_management.create_event_for_meet.create_event_for_meet.get_db_connection')
    def test_create_event_success(self, mock_db_connection, mock_validate_opt_name, mock_validate_event_type,
                                  mock_validate_end_date, mock_validate_start_date, mock_validate_name, mock_exists_user):
        mock_exists_user.return_value = True
        mock_validate_name.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True
        mock_validate_opt_name.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.lastrowid = 1

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'moderator': 'user123',
            'title': 'Test Title',
            'notes': 'Some notes',
            'reminder': '1 hour before'
        }

        result = create_event(event)
        self.assertEqual(result['id'], 1)

    @patch('events_management.create_event_for_meet.create_event_for_meet.exists_user')
    def test_create_event_user_not_found(self, mock_exists_user):
        mock_exists_user.return_value = False

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'moderator': 'user123',
            'title': 'Test Title',
            'notes': 'Some notes',
            'reminder': '1 hour before'
        }

        with self.assertRaises(ValueError) as context:
            create_event(event)
        self.assertTrue(ErrorType.USER_NOT_FOUND in str(context.exception))

    @patch('events_management.create_event_for_meet.create_event_for_meet.get_db_connection')
    def test_create_meet_admin_success(self, mock_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.lastrowid = 1

        event = {
            'title': 'Test Title',
            'notes': 'Some notes',
            'reminder': '1 hour before',
            'moderator': 'user123'
        }
        event_id = 1

        result = create_meet_admin(event, event_id)
        self.assertEqual(result['id'], 1)

    @patch('events_management.create_event_for_meet.create_event_for_meet.get_db_connection')
    def test_create_meet_admin_connection_error(self, mock_db_connection):
        mock_db_connection.side_effect = pymysql.OperationalError("Connection error")

        event = {
            'title': 'Test Title',
            'notes': 'Some notes',
            'reminder': '1 hour before',
            'moderator': 'user123'
        }
        event_id = 1

        with self.assertRaises(RuntimeError) as context:
            create_meet_admin(event, event_id)
        self.assertTrue(ErrorType.CONNECTION_ERROR in str(context.exception))

    @patch('events_management.create_event_for_meet.create_event_for_meet.exists_user')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_name')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_start_date')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_end_date')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_event_type')
    @patch('events_management.create_event_for_meet.create_event_for_meet.validate_opt_name')
    @patch('events_management.create_event_for_meet.create_event_for_meet.get_db_connection')
    def test_create_meet_admin_exception_error(self, mock_db_connection, mock_validate_opt_name, mock_validate_event_type,
                                  mock_validate_end_date, mock_validate_start_date, mock_validate_name, mock_exists_user):
        mock_db_connection.side_effect = pymysql.OperationalError("Connection error")
        mock_exists_user.return_value = True
        mock_validate_name.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True
        mock_validate_opt_name.return_value = True

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'moderator': 'user123',
            'title': 'Test Title',
            'notes': 'Some notes',
            'reminder': '1 hour before'
        }
        with self.assertRaises(RuntimeError) as context:
            create_event(event)
        self.assertTrue(ErrorType.CONNECTION_ERROR in str(context.exception))