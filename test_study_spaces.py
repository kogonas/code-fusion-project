
import unittest
import study_spaces as ss

# Small fixed set of reviews so the tests never touch reviews.json
REVIEWS = [
    {"space_id": 1, "author": "A", "rating": 5, "text": "great", "flagged": False},
    {"space_id": 1, "author": "B", "rating": 3, "text": "ok", "flagged": False},
    {"space_id": 4, "author": "C", "rating": 2, "text": "loud", "flagged": False},
]


class TestSpaceData(unittest.TestCase):
    def test_every_space_has_required_fields_and_unique_ids(self):
        required = ["id", "name", "location", "kind", "noise", "seating",
                    "hours", "eats", "blurb", "site"] + list(ss.FLAGS)
        ids = [s["id"] for s in ss.SPACES]
        self.assertEqual(len(ids), len(set(ids)))
        for s in ss.SPACES:
            for key in required:
                self.assertIn(key, s)

    def test_four_spaces_are_not_owned_by_gsu(self):
        off = [s for s in ss.SPACES if s["offcampus"]]
        self.assertEqual(len(off), 4)


class TestSearchAndFilter(unittest.TestCase):
    def test_search_matches_name_case_insensitive(self):
        names = [s["name"] for s in ss.search("LIBRARY SOUTH", reviews=REVIEWS)]
        self.assertIn("Library South", names)

    def test_search_with_no_match_returns_empty_list(self):
        self.assertEqual(ss.search("zzzz-not-a-place", reviews=REVIEWS), [])

    def test_offcampus_filter_only_returns_non_gsu_spaces(self):
        results = ss.search("", ["offcampus"], reviews=REVIEWS)
        self.assertTrue(results)
        self.assertTrue(all(s["offcampus"] == 1 for s in results))

    def test_multiple_filters_must_all_match(self):
        results = ss.search("", ["offcampus", "quiet"], reviews=REVIEWS)
        self.assertEqual([s["name"] for s in results], ["Atlanta-Fulton Central Library"])

    def test_sort_by_name_is_alphabetical(self):
        names = [s["name"] for s in ss.search("", sort="name", reviews=REVIEWS)]
        self.assertEqual(names, sorted(names))


class TestReviews(unittest.TestCase):
    def test_average_rating(self):
        self.assertEqual(ss.average(REVIEWS, 1), 4.0)
        self.assertEqual(ss.average(REVIEWS, 99), 0.0)

    def test_highest_rated_sort_puts_best_space_first(self):
        first = ss.search("", sort="rating", reviews=REVIEWS)[0]
        self.assertEqual(first["id"], 1)

    def test_space_reviews_only_returns_that_space(self):
        self.assertEqual(len(ss.space_reviews(REVIEWS, 1)), 2)
        self.assertEqual(len(ss.space_reviews(REVIEWS, 4)), 1)

    def test_stars_output(self):
        self.assertEqual(ss.stars(4), "★★★★☆")
        self.assertEqual(ss.stars(0), "☆☆☆☆☆")


if __name__ == "__main__":
    unittest.main()
