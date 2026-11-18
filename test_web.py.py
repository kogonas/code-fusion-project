import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SECRET_KEY", "test-key-only")
from app import app


class TestPages(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.query")
    def test_home_page(self, mocked):
        mocked.return_value = []
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Find a study space", response.data)

    @patch("app.query")
    def test_missing_space(self, mocked):
        mocked.return_value = None
        self.assertEqual(self.client.get("/spaces/9999").status_code, 404)

    @patch("app.query")
    def test_filters_use_all_selected_fields(self, mocked):
        mocked.return_value = []
        self.client.get("/?offcampus=1&quiet=1")
        sql = mocked.call_args.args[0]
        self.assertIn("s.`offcampus` = 1", sql)
        self.assertIn("s.`quiet` = 1", sql)

    def test_guest_cannot_review(self):
        self.assertEqual(self.client.post("/reviews/1", data={"rating": "5", "text": "Good"}).status_code, 400)

    def test_guest_cannot_open_admin(self):
        self.assertEqual(self.client.get("/admin").status_code, 403)

    def test_guest_cannot_submit_without_csrf(self):
        self.assertEqual(self.client.post("/login", data={"password": "anything"}).status_code, 400)

    @patch("app.query")
    def test_closing_times(self, mocked):
        mocked.return_value = []
        self.assertEqual(self.client.get("/closing-times").status_code, 200)


if __name__ == "__main__":
    unittest.main()
