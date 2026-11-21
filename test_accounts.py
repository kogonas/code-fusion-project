"""Sprint 2 tests for the Sprint 1 registration and login routes.

Run with: python -m unittest -v test_accounts.py
These tests use a fake database connection, so MySQL does not need to be running.
"""
import unittest
from unittest.mock import MagicMock, patch

from werkzeug.security import generate_password_hash
from app import app


class AccountTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY='sprint2-test-key')
        self.client = app.test_client()

    @patch('app.db_connection')
    def test_register_creates_account(self, mock_db):
        """A student can register using a name, email, and valid password."""
        connection = MagicMock()
        mock_db.return_value = connection

        response = self.client.post('/register', data={
            'name': 'Test Student',
            'email': 'student@school.edu',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/login'))
        connection.commit.assert_called_once()
        query, values = connection.cursor.return_value.execute.call_args.args
        self.assertIn('INSERT INTO users', query)
        self.assertEqual(values[0], 'Test Student')
        self.assertEqual(values[1], 'student@school.edu')
        self.assertNotEqual(values[2], 'password123')  # password is hashed

    @patch('app.db_connection')
    def test_login_accepts_correct_password(self, mock_db):
        """A registered student can log in with the correct password."""
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchone.return_value = {
            'id': 1,
            'name': 'Test Student',
            'password_hash': generate_password_hash('password123'),
        }

        response = self.client.post('/login', data={
            'email': 'student@school.edu',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/dashboard'))
        with self.client.session_transaction() as session:
            self.assertEqual(session['user_id'], 1)
            self.assertEqual(session['name'], 'Test Student')


if __name__ == '__main__':
    unittest.main()
