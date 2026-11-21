"""Final sprint unit tests. Database calls are mocked (no live MySQL needed)."""
import unittest
from unittest.mock import MagicMock, patch
from app import app

class FinalFeatureTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY='final-sprint-tests')
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess['user_id'] = 7
            sess['name'] = 'Student'

    @patch('app.db_connection')
    def test_profile_update(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchone.return_value = {'name': 'Updated Student', 'email': 'new@school.edu'}
        response = self.client.post('/profile', data={'name': 'Updated Student', 'email': 'new@school.edu'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated', response.data)
        connection.commit.assert_called_once()
        query, values = connection.cursor.return_value.execute.call_args_list[0].args
        self.assertIn('UPDATE users', query)
        self.assertEqual(values, ('Updated Student', 'new@school.edu', 7))

    @patch('app.db_connection')
    def test_add_course(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchall.return_value = [{'id': 1, 'course_code': 'CSC 4350'}]
        response = self.client.post('/courses', data={'course_code': 'csc 4350'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CSC 4350', response.data)
        query, values = connection.cursor.return_value.execute.call_args_list[0].args
        self.assertIn('INSERT INTO user_courses', query)
        self.assertEqual(values, (7, 'CSC 4350'))

    @patch('app.db_connection')
    def test_save_preferences(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchone.return_value = {'study_style': 'Quiet', 'meeting_type': 'Online', 'group_size': 'Small'}
        response = self.client.post('/preferences', data={'study_style': 'Quiet', 'meeting_type': 'Online', 'group_size': 'Small'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Preferences saved', response.data)
        query, values = connection.cursor.return_value.execute.call_args_list[0].args
        self.assertIn('INSERT INTO study_preferences', query)
        self.assertEqual(values, (7, 'Quiet', 'Online', 'Small'))

    @patch('app.db_connection')
    def test_add_availability(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchall.return_value = []
        response = self.client.post('/availability', data={'day': 'Monday', 'start_time': '10:00', 'end_time': '12:00'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Availability added', response.data)
        query, values = connection.cursor.return_value.execute.call_args_list[0].args
        self.assertIn('INSERT INTO user_availability', query)
        self.assertEqual(values, (7, 'Monday', '10:00', '12:00'))

    @patch('app.db_connection')
    def test_reject_invalid_availability(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        connection.cursor.return_value.fetchall.return_value = []
        response = self.client.post('/availability', data={'day': 'Monday', 'start_time': '13:00', 'end_time': '10:00'})
        self.assertIn(b'Choose a day and a valid start/end time', response.data)
        connection.commit.assert_not_called()

    @patch('app.db_connection')
    def test_remove_course_only_for_current_user(self, mock_db):
        connection = MagicMock()
        mock_db.return_value = connection
        response = self.client.post('/courses/22/delete')
        self.assertEqual(response.status_code, 302)
        query, values = connection.cursor.return_value.execute.call_args.args
        self.assertIn('user_id=%s', query)
        self.assertEqual(values, (22, 7))

    def test_profile_requires_login(self):
        with self.client.session_transaction() as sess:
            sess.clear()
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/login'))

if __name__ == '__main__':
    unittest.main()
