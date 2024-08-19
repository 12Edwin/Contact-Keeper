import json
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

if 'AWS_LAMBDA_FUNCTION_NAME' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from commons.python.ErrorType import ErrorType
from user_management.read_users.read_users import lambda_handler, compare_users, get_cognito_users, read_users


class TestLambdaHandler(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.read_users.read_users.get_cognito_ids')
    @patch('boto3.client')
    @patch('user_management.read_users.read_users.get_cognito_users')
    @patch('user_management.read_users.read_users.read_users')
    @patch('user_management.read_users.read_users.compare_users')
    def test_lambda_handler_success(self, mock_compare_users, mock_read_users,
                                    mock_get_cognito_users, mock_boto3_client, mock_get_cognito_ids):
        mock_get_cognito_ids.return_value = ('pool_id', 'client_id')
        mock_cognito_client = MagicMock()
        mock_boto3_client.return_value = mock_cognito_client
        mock_get_cognito_users.return_value = {'user1': {'Attributes': [{'Name': 'email', 'Value': 'user1@example.com'}]}}
        mock_read_users.return_value = [{'id': 'user1', 'name': 'John'}]
        mock_compare_users.return_value = [{'id': 'user1', 'name': 'John', 'email': 'user1@example.com'}]

        result = lambda_handler({}, None)

        expected_result = 200
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['data'], [{'id': 'user1', 'name': 'John', 'email': 'user1@example.com'}])

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.read_users.read_users.get_cognito_ids')
    def test_lambda_handler_value_error(self, mock_get_cognito_ids):
        mock_get_cognito_ids.side_effect = ValueError("Test error")

        result = lambda_handler({}, None)

        expected_result = 400
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['message'], ErrorType.english("Test error"))

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.read_users.read_users.get_cognito_ids')
    def test_lambda_handler_runtime_error(self, mock_get_cognito_ids):
        mock_get_cognito_ids.side_effect = RuntimeError("Test error")

        result = lambda_handler({}, None)

        expected_result = 500
        self.assertEqual(result['statusCode'], expected_result)
        self.assertEqual(json.loads(result['body'])['message'], ErrorType.english("Test error"))

class TestGetCognitoUsers(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    def test_get_cognito_users_single_page(self):
        mock_client = MagicMock()
        mock_client.list_users.return_value = {
            'Users': [
                {'Username': 'user1', 'Attributes': [{'Name': 'email', 'Value': 'user1@example.com'}]},
                {'Username': 'user2', 'Attributes': [{'Name': 'email', 'Value': 'user2@example.com'}]}
            ]
        }

        result = get_cognito_users(mock_client, 'test_pool_id')

        self.assertEqual(len(result), 2)
        self.assertIn('user1', result)
        self.assertIn('user2', result)
        self.assertEqual(result['user1']['Attributes'][0]['Value'], 'user1@example.com')
        self.assertEqual(result['user2']['Attributes'][0]['Value'], 'user2@example.com')

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    def test_get_cognito_users_multiple_pages(self):
        mock_client = MagicMock()
        mock_client.list_users.side_effect = [
            {
                'Users': [{'Username': 'user1', 'Attributes': [{'Name': 'email', 'Value': 'user1@example.com'}]}],
                'PaginationToken': 'token'
            },
            {
                'Users': [{'Username': 'user2', 'Attributes': [{'Name': 'email', 'Value': 'user2@example.com'}]}]
            }
        ]

        result = get_cognito_users(mock_client, 'test_pool_id')

        self.assertEqual(len(result), 2)
        self.assertIn('user1', result)
        self.assertIn('user2', result)
        self.assertEqual(result['user1']['Attributes'][0]['Value'], 'user1@example.com')
        self.assertEqual(result['user2']['Attributes'][0]['Value'], 'user2@example.com')

class TestReadUsers(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.read_users.read_users.get_db_connection')
    def test_read_users_success(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [(1, 'John', 'Doe', 'Smith', '1990-01-01', '1234567890')]
        mock_cursor.description = [('id',), ('name',), ('surname',), ('last_name',), ('birthday',), ('phone',)]

        result = read_users()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], 'John')
        self.assertEqual(result[0]['surname'], 'Doe')
        self.assertEqual(result[0]['last_name'], 'Smith')
        self.assertEqual(result[0]['birthday'], '1990-01-01')
        self.assertEqual(result[0]['phone'], '1234567890')

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    @patch('user_management.read_users.read_users.get_db_connection')
    def test_read_users_empty(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = None

        result = read_users()

        self.assertEqual(result, {})

class TestCompareUsers(unittest.TestCase):

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    def test_compare_users_match(self):
        cognito_users = {
            'user1': {'Attributes': [{'Name': 'email', 'Value': 'user1@example.com'}]}
        }
        db_users = [
            {'id': 'user1', 'name': 'John', 'surname': 'Doe', 'last_name': 'Smith',
             'birthday': '1990-01-01', 'phone': '1234567890'}
        ]

        result = compare_users(cognito_users, db_users)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['email'], 'user1@example.com')
        self.assertEqual(result[0]['name'], 'John')
        self.assertEqual(result[0]['surname'], 'Doe')
        self.assertEqual(result[0]['last_name'], 'Smith')
        self.assertEqual(result[0]['birthday'], '1990-01-01')
        self.assertEqual(result[0]['phone'], '1234567890')

    @patch.dict('os.environ', {'DB_HOST': 'HOST', 'DB_NAME': 'NAME', 'SECRET_NAME': 'SECRET'})
    def test_compare_users_no_match(self):
        cognito_users = {
            'user1': {'Attributes': [{'Name': 'email', 'Value': 'user1@example.com'}]}
        }
        db_users = [
            {'id': 'user2', 'name': 'Jane'}
        ]

        result = compare_users(cognito_users, db_users)

        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()

