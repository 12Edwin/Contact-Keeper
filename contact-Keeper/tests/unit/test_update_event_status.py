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
from events_management.update_event_status.update_event_status import lambda_handler as update_event


class TestUpdateEventStatus(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event_status.update_event_status.get_db_connection')
    @patch('events_management.update_event_status.update_event_status.exists_event')
    @patch('events_management.update_event_status.update_event_status.validate_status_event')
    def test_update_event_status_success(self, mock_validate_status_event, mock_exists_event, mock_get_db_connection):
        mock_exists_event.return_value = True
        mock_validate_status_event.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {
            'id': 1,
            'status': 'active'
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event_status.update_event_status.exists_event')
    def test_update_event_status_invalid_id(self, mock_exists_event):
        mock_exists_event.return_value = False

        event = {
            'id': 1,
            'status': 'active'
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['message'], ErrorType.english(ErrorType.INVALID_ID))

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event_status.update_event_status.get_db_connection')
    @patch('events_management.update_event_status.update_event_status.exists_event')
    @patch('events_management.update_event_status.update_event_status.validate_status_event')
    def test_update_event_status_invalid_status(self, mock_validate_status_event, mock_exists_event, mock_get_db_connection):
        mock_exists_event.return_value = True
        mock_validate_status_event.return_value = True

        mock_get_db_connection.side_effect = pymysql.OperationalError('Error connection')

        event = {
            'id': 1,
            'status': 'invalid'
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = response_500(ErrorType.CONNECTION_ERROR)
        self.assertEqual(result, expected_result)