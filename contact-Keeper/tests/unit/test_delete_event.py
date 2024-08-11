import unittest
import os
import sys
from unittest.mock import patch, MagicMock

import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.delete_event.delete_event import read_event, lambda_handler as delete_event


class TestDeleteEvent(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.delete_event.delete_event.get_db_connection')
    @patch('events_management.delete_event.delete_event.validate_id')
    @patch('events_management.delete_event.delete_event.exists_by_id')
    @patch('events_management.delete_event.delete_event.read_event')
    def test_delete_event_success(self, mock_read_event, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True
        mock_read_event.return_value = {'status': 'pending'}
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {'id': 1}
        result = delete_event({'pathParameters': event}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.delete_event.delete_event.validate_id')
    @patch('events_management.delete_event.delete_event.exists_by_id')
    def test_delete_event_event_not_found(self, mock_exists_by_id, mock_validate_id):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = False

        event = {'id': 1}
        result = delete_event({'pathParameters': event}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.delete_event.delete_event.validate_id')
    @patch('events_management.delete_event.delete_event.exists_by_id')
    @patch('events_management.delete_event.delete_event.read_event')
    def test_delete_event_internal_server_error(self, mock_read_event, mock_exists_by_id, mock_validate_id):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True
        mock_read_event.side_effect = pymysql.OperationalError('Mocked error message')
        event = {'id': 1}
        result = delete_event({'pathParameters': event}, {})
        expected_result = response_500(ErrorType.CONNECTION_ERROR)
        self.assertEqual(result, expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.delete_event.delete_event.get_db_connection')
    @patch('events_management.delete_event.delete_event.validate_id')
    @patch('events_management.delete_event.delete_event.exists_by_id')
    def test_delete_event_invalid_id(self, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'Test Event', '2024-08-09')
        mock_cursor.description = [('id',), ('name',), ('date',)]


        event = {'id': 'invalid_id'}
        result = read_event(event)
        expected_result = {'id': 1, 'name': 'Test Event', 'date': '2024-08-09'}
        self.assertEqual(result, expected_result)
