import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.create_event_for_group.create_event_for_group import lambda_handler as create_event


class TestCreateEventGroup(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.create_event_for_group.create_event_for_group.get_cognito_ids')
    @patch('events_management.create_event_for_group.create_event_for_group.get_db_connection')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_id')
    @patch('events_management.create_event_for_group.create_event_for_group.exists_group')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_name')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_start_date')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_end_date')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_event_type')
    def test_create_event_success(self, mock_validate_event_type, mock_validate_end_date, mock_validate_start_date,
                                  mock_validate_name, mock_exists_group, mock_validate_id, mock_get_db_connection, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_validate_id.return_value = True
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = create_event({'body': json.dumps(event)}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.create_event_for_group.create_event_for_group.get_cognito_ids')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_id')
    def test_create_event_invalid_id(self, mock_validate_id, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_validate_id.return_value = False

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = create_event({'body': json.dumps(event)}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.create_event_for_group.create_event_for_group.get_cognito_ids')
    @patch('events_management.create_event_for_group.create_event_for_group.get_db_connection')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_id')
    @patch('events_management.create_event_for_group.create_event_for_group.exists_group')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_name')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_start_date')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_end_date')
    @patch('events_management.create_event_for_group.create_event_for_group.validate_event_type')
    def test_create_event_internal_error(self, mock_validate_event_type, mock_validate_end_date, mock_validate_start_date,
                                  mock_validate_name, mock_exists_group, mock_validate_id, mock_get_db_connection,
                                  mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_validate_id.return_value = True
        mock_exists_group.return_value = True
        mock_validate_name.return_value = True
        mock_validate_start_date.return_value = True
        mock_validate_end_date.return_value = True
        mock_validate_event_type.return_value = True

        mock_get_db_connection.side_effect = RuntimeError(ErrorType.CONNECTION_ERROR)

        event = {
            'name': 'Test Event',
            'description': 'Description',
            'start_date': '2024-08-10',
            'end_date': '2024-08-11',
            'type': 'meeting',
            'location': 'Online',
            'id_group_member': 1
        }
        result = create_event({'body': json.dumps(event)}, {})
        expected_result = response_500(ErrorType.english(ErrorType.INTERNAL_SERVER_ERROR))
        self.assertEqual(result, expected_result)