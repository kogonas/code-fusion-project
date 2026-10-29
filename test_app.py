import unittest
from app import app


class TestStudyGroupRecommendations(unittest.TestCase):

    def setUp(self):
        # Create a test client to simulate requests to the website
        self.client = app.test_client()

    def test_homepage_loads(self):
        # Check that the Studyly homepage loads successfully
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Studyly!", response.data)

    def test_recommendations(self):
        # Student preferences used to test the matching feature
        student_preferences = {
            "course": "CSC 4350",
            "study_style": "collaborative",
            "meeting_format": "online",
            "preferred_group_size": "small",
            "availability": ["Monday 3-5 PM"]
        }

        # Submit the preferences to the recommendation route
        response = self.client.post(
            "/recommend",
            data=student_preferences
        )

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)

        # Verify the correct group receives 100% compatibility
        self.assertIn(b"Software Engineering Study Group", response.data)
        self.assertIn(b"100.0%", response.data)

        # Verify groups from other courses are excluded
        self.assertNotIn(b"Computer Networks Study Group", response.data)


if __name__ == "__main__":
    unittest.main()