import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.read_events_group.read_events_group import lambda_handler as update_event

class TestReadEventsGroup(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_events_group.read_events_group.get_db_connection')
    @patch('events_management.read_events_group.read_events_group.get_cognito_ids')
    @patch('events_management.read_events_group.read_events_group.exists_group')
    def test_create_event_success(self, mock_exists_group, mock_get_cognito_ids, mock_get_db_connection):
        mock_exists_group.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {'id': 1}
        result = update_event({'pathParameters': event}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_events_group.read_events_group.get_cognito_ids')
    @patch('events_management.read_events_group.read_events_group.exists_group')
    def test_create_event_group_not_found(self, mock_exists_group, mock_get_cognito_ids):
        mock_exists_group.return_value = False
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        event = {'id': 1}
        result = update_event({'pathParameters': event}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.read_events_group.read_events_group.get_db_connection')
    @patch('events_management.read_events_group.read_events_group.get_cognito_ids')
    @patch('events_management.read_events_group.read_events_group.exists_group')
    def test_create_event_internal_server_error(self, mock_exists_group, mock_get_cognito_ids, mock_get_db_connection):
        mock_exists_group.return_value = True
        mock_get_cognito_ids.return_value = ('user_pool_id', 'user_pool_client_id')

        mock_get_db_connection.side_effect = RuntimeError(ErrorType.CONNECTION_ERROR)

        event = {'id': 1}
        result = update_event({'pathParameters': event}, {})

        expected_result = response_500(ErrorType.INTERNAL_SERVER_ERROR)
        self.assertEqual(result, expected_result)
