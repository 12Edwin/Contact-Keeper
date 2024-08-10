import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.update_event.update_event import lambda_handler as update_event

class TestUpdateEvent(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event.update_event.get_db_connection')
    @patch('events_management.update_event.update_event.validate_id')
    @patch('events_management.update_event.update_event.exists_by_id')
    @patch('events_management.update_event.update_event.exists_group')
    @patch('events_management.update_event.update_event.validate_name')
    @patch('events_management.update_event.update_event.validate_start_date')
    @patch('events_management.update_event.update_event.validate_end_date')
    @patch('events_management.update_event.update_event.validate_event_type')
    def test_create_event_success(self, mock_validate_event_type, mock_validate_end_date, mock_validate_start_date,
                                  mock_validate_name, mock_exists_group, mock_exists_by_id, mock_validate_id,
                                  mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_exists_by_id.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {
            'id': 1,
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event.update_event.get_db_connection')
    @patch('events_management.update_event.update_event.validate_id')
    def test_create_event_invalid_id(self,mock_validate_id, mock_get_db_connection):
        mock_validate_id.return_value = False

        event = {
            'id': 1,
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.update_event.update_event.get_db_connection')
    @patch('events_management.update_event.update_event.validate_id')
    @patch('events_management.update_event.update_event.exists_by_id')
    @patch('events_management.update_event.update_event.exists_group')
    @patch('events_management.update_event.update_event.validate_name')
    @patch('events_management.update_event.update_event.validate_start_date')
    @patch('events_management.update_event.update_event.validate_end_date')
    @patch('events_management.update_event.update_event.validate_event_type')
    def test_create_event_internal_server_error(self, mock_validate_event_type, mock_validate_end_date, mock_validate_start_date,
                                  mock_validate_name, mock_exists_group, mock_exists_by_id, mock_validate_id,
                                  mock_get_db_connection):
        mock_validate_id.return_value = True
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_exists_by_id.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True

        mock_get_db_connection.side_effect = RuntimeError(ErrorType.CONNECTION_ERROR)

        event = {
            'id': 1,
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = update_event({'body': json.dumps(event)}, {})

        expected_result = response_500(ErrorType.INTERNAL_SERVER_ERROR)
        self.assertEqual(result, expected_result)