import unittest
import os
import sys
from unittest.mock import patch, MagicMock

import pymysql

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from commons.python.type_response import response_500
from events_management.unassign_people_event.unassign_people_event import lambda_handler as unassign_people_event


class TestUnassignPeopleEvent(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.unassign_people_event.unassign_people_event.get_db_connection')
    @patch('events_management.unassign_people_event.unassign_people_event.get_cognito_ids')
    @patch('events_management.unassign_people_event.unassign_people_event.exists_user')
    @patch('events_management.unassign_people_event.unassign_people_event.exists_event')
    def test_unassign_people_event_success(self, mock_exists_event, mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_exists_user.return_value = True
        mock_exists_event.return_value = True
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        event = {'id_person': 1, 'id_event': 1}
        result = unassign_people_event({'pathParameters': event}, {})

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.unassign_people_event.unassign_people_event.get_cognito_ids')
    @patch('events_management.unassign_people_event.unassign_people_event.exists_user')
    def test_unassign_people_event_user_not_found(self, mock_exists_user, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_exists_user.return_value = False

        event = {'id_person': 1, 'id_event': 1}
        result = unassign_people_event({'pathParameters': event}, {})

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.unassign_people_event.unassign_people_event.get_db_connection')
    @patch('events_management.unassign_people_event.unassign_people_event.get_cognito_ids')
    @patch('events_management.unassign_people_event.unassign_people_event.exists_user')
    @patch('events_management.unassign_people_event.unassign_people_event.exists_event')
    def test_unassign_people_event_event_not_found(self, mock_exists_event, mock_exists_user, mock_get_cognito_ids, mock_get_db_connection):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_exists_user.return_value = True
        mock_exists_event.return_value = True
        mock_get_db_connection.side_effect = pymysql.MySQLError('Mocked error message')

        event = {'id_person': 1, 'id_event': 1}
        result = unassign_people_event({'pathParameters': event}, {})

        expected_result = response_500(ErrorType.CONNECTION_ERROR)
        self.assertEqual(result, expected_result)