import study_spaces as ss
from db import execute


def seed():
    for space in ss.SPACES:
        keys = ["id", "name", "location", "kind", "wifi", "outlets", "quiet", "groups", "food", "reserve", "offcampus", "noise", "seating", "hours", "eats", "blurb", "site"]
        fields = ", ".join("`" + key + "`" for key in keys)
        marks = ", ".join(["%s"] * len(keys))
        updates = ", ".join("`" + key + "` = VALUES(`" + key + "`)" for key in keys if key != "id")
        execute("INSERT INTO study_spaces (" + fields + ") VALUES (" + marks + ") ON DUPLICATE KEY UPDATE " + updates, tuple(space[key] for key in keys))
    print("Loaded", len(ss.SPACES), "study spaces")


if __name__ == "__main__":
    seed()
