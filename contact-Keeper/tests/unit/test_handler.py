import datetime
import unittest
from unittest.mock import patch, MagicMock

from events_management.commons import ErrorType
from events_management.commons.type_response import response_400, response_500
from events_management.read_event.read_event import lambda_handler as read_event


class TestReadEvent(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('events_management.commons.database.pymysql')
    @patch('events_management.commons.utils.validate_id')
    @patch('events_management.commons.utils.exists_by_id')
    def test_read_event_success(self, mock_exists_by_id, mock_validate_id, mock_pymysql):
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('1', 'Test Event', datetime.datetime(2024, 6, 12, 15, 0), datetime.datetime(2024, 6, 12, 16, 0),
                                            'Test Location', 'This is a test event', 'session', 1, 1, datetime.datetime(2024, 6, 5, 14, 28, 25), 'canceled')

        mock_cursor.description = [('id',), ('name',), ('start_date',), ('end_date',), ('location',), ('description',),
                                   ('type',), ('id_group_member',), ('status',), ('created_at',), ('status',)]

        mock_pymysql.connect.return_value = mock_connection

        parameters = {'pathParameters': {'id': '1'}}
        result = read_event(parameters, {})

        expected_result = {'id': '1', 'name': 'Unit Test', 'start_date': datetime.datetime(2024, 6, 12, 15, 0),
                           'end_date': datetime.datetime(2024, 6, 12, 16, 0), 'location': 'Test Location',
                           'description': 'This is a test event', 'type': 'session', 'id_group_member': 1, 'status': 'canceled',
                           'created_at': datetime.datetime(2024, 6, 5, 14, 28, 25)}
        self.assertEqual(result, expected_result)

    @patch('path.to.module.validate_id')
    def test_read_event_invalid_id(self, mock_validate_id):
        # Configurar mock
        mock_validate_id.return_value = False

        # Llamar a la función
        parameters = {'id': 'invalid'}
        with self.assertRaises(ValueError) as context:
            read_event(parameters)

        # Verificar excepción
        self.assertEqual(str(context.exception), ErrorType.INVALID_ID)

    @patch('path.to.module.exists_by_id')
    @patch('path.to.module.validate_id')
    def test_read_event_not_found(self, mock_validate_id, mock_exists_by_id):
        # Configurar mocks
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = False

        # Llamar a la función
        parameters = {'id': '1'}
        with self.assertRaises(ValueError) as context:
            read_event(parameters)

        # Verificar excepción
        self.assertEqual(str(context.exception), ErrorType.EVENT_NOT_FOUND)

    @patch('path.to.module.get_db_connection')
    @patch('path.to.module.validate_id')
    @patch('path.to.module.exists_by_id')
    def test_read_event_database_error(self, mock_exists_by_id, mock_validate_id, mock_get_db_connection):
        # Configurar mocks
        mock_validate_id.return_value = True
        mock_exists_by_id.return_value = True
        mock_get_db_connection.side_effect = RuntimeError('Database error')

        # Llamar a la función
        parameters = {'id': '1'}
        with self.assertRaises(RuntimeError) as context:
            read_event(parameters)

        # Verificar excepción
        self.assertEqual(str(context.exception), 'Database error')

    @patch('path.to.module.lambda_handler')
    @patch('path.to.module.read_event')
    def test_response_400(self, mock_read_event, mock_lambda_handler):
        # Configurar mock
        mock_read_event.side_effect = ValueError('Error message')

        # Llamar a la función
        event = {'pathParameters': {'id': '1'}}
        context = None
        result = lambda_handler(event, context)

        # Verificar resultado
        expected_result = response_400(ErrorType.english('Error message'))
        self.assertEqual(result, expected_result)

    @patch('path.to.module.lambda_handler')
    @patch('path.to.module.read_event')
    def test_response_500(self, mock_read_event, mock_lambda_handler):
        # Configurar mock
        mock_read_event.side_effect = RuntimeError('Error message')

        # Llamar a la función
        event = {'pathParameters': {'id': '1'}}
        context = None
        result = lambda_handler(event, context)

        # Verificar resultado
        expected_result = response_500(ErrorType.english('Error message'))
        self.assertEqual(result, expected_result)