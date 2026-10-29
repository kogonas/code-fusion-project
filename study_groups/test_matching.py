import unittest
from matching import calculate_compatibility


class TestCompatibilityMatching(unittest.TestCase):

    # Test 1: All five preferences match
    def test_all_preferences_match(self):
        student = {
            "study_style": "collaborative",
            "meeting_format": "online",
            "preferred_group_size": "small",
            "course": "CSC 4350",
            "availability": ["Monday 3-5 PM"]
        }

        group = {
            "study_style": "collaborative",
            "meeting_format": "online",
            "preferred_group_size": "small",
            "course": "CSC 4350",
            "availability": ["Monday 3-5 PM"]
        }

        result = calculate_compatibility(student, group)

        self.assertEqual(result, 100.0)

    # Test 2: Three out of five preferences match
    def test_partial_preferences_match(self):
        student = {
            "study_style": "independent",
            "meeting_format": "online",
            "preferred_group_size": "small",
            "course": "CSC 4350",
            "availability": ["Monday 3-5 PM"]
        }

        group = {
            "study_style": "collaborative",
            "meeting_format": "in-person",
            "preferred_group_size": "small",
            "course": "CSC 4350",
            "availability": ["Monday 3-5 PM"]
        }

        result = calculate_compatibility(student, group)

        self.assertEqual(result, 60.0)


if __name__ == "__main__":
    score = calculate_compatibility(student, group)
    print("Compatibility Score:", score)
    unittest.main()