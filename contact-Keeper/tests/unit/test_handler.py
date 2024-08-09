import datetime
import json
import unittest
from unittest.mock import patch, MagicMock

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_400, response_500
from events_management.read_event.read_event import lambda_handler as read_event


class TestReadEvent(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_event.read_event.get_db_connection')
    @patch('events_management.read_event.read_event.validate_id')
    @patch('events_management.read_event.read_event.exists_by_id')
    def test_read_event_success(self, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, 'Test Event', '2024-08-09')
        mock_cursor.description = [('id',), ('name',), ('date',)]

        result = read_event({'pathParameters': {'id': 1}}, {})

        expected_result = {'id': 1, 'name': 'Test Event', 'date': '2024-08-09'}
        self.assertEqual(json.loads(result['body'])['data'], expected_result)

        mock_validate_id.assert_called_once_with(1)
        mock_exists_by_id.assert_called_once_with(1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM events WHERE id = %s", 1)
        mock_cursor.fetchone.assert_called_once()

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_event.read_event.get_db_connection')
    @patch('events_management.read_event.read_event.validate_id')
    @patch('events_management.read_event.read_event.exists_by_id')
    def test_read_event_not_found(self, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = False

        result = read_event({'pathParameters': {'id': 1}}, {})

        self.assertEqual(result['statusCode'], 400)

        error_message = json.loads(result['body'])['message']
        self.assertEqual(error_message, ErrorType.english(ErrorType.EVENT_NOT_FOUND))

        mock_validate_id.assert_called_once_with(1)
        mock_exists_by_id.assert_called_once_with(1)
        mock_get_db_connection.assert_not_called()

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_event.read_event.get_db_connection')
    @patch('events_management.read_event.read_event.validate_id')
    @patch('events_management.read_event.read_event.exists_by_id')
    def test_read_event_database_error(self, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True

        mock_get_db_connection.side_effect = RuntimeError("Database connection failed")

        result = read_event({'pathParameters': {'id': 1}}, {})

        self.assertEqual(result['statusCode'], 500)

        error_message = json.loads(result['body'])['message']
        self.assertEqual(error_message, ErrorType.english(str(RuntimeError("Database connection failed"))))

        mock_validate_id.assert_called_once_with(1)
        mock_exists_by_id.assert_called_once_with(1)
        mock_get_db_connection.assert_called_once()