# Calculates how compatible a student's preferences are with a study group's preferences
def calculate_compatibility(student_preferences, group_preferences):
    #keeps track of how many preferences match
    matches = 0

    # Five factors are used to calculate compatibility
    # Course, availability, study style, meeting format, and preferred group size
    total_factors = 5

    # Compare study style
    if (student_preferences.get("study_style") is not None and
            student_preferences.get("study_style") == group_preferences.get("study_style")):
        matches += 1

    # Compare meeting format
    if (student_preferences.get("meeting_format") is not None and
            student_preferences.get("meeting_format") == group_preferences.get("meeting_format")):
        matches += 1

    # Compare preferred group size
    if (student_preferences.get("preferred_group_size") is not None and
            student_preferences.get("preferred_group_size") == group_preferences.get("preferred_group_size")):
        matches += 1

    # Compare course
    if (student_preferences.get("course") is not None and
            student_preferences.get("course") == group_preferences.get("course")):
        matches += 1

    # Compare availability
    student_availability = student_preferences.get("availability") or []
    group_availability = group_preferences.get("availability") or []

    for time in student_availability:
        if time in group_availability:
            matches += 1
            break

    # Convert the number of matching preferences into a percentage
    compatibility_score = round((matches / total_factors) * 100, 2)

    # Return the final compatibility percentage
    return compatibility_score

# Run this example only when matching.py is executed directly
if __name__ == "__main__":

    student = {
        "study_style": "independent",
        "meeting_format": "online",
        "preferred_group_size": "small",
        "course": "CSC 4350",
        "availability": ["Monday 3-5 PM", "Wednesday 1-3 PM"]
    }

    group = {
        "study_style": "collaborative",
        "meeting_format": "in-person",
        "preferred_group_size": "small",
        "course": "CSC 4350",
        "availability": ["Monday 3-5 PM", "Tuesday 2-4 PM"]
    }

    score = calculate_compatibility(student, group)

    print("Compatibility Score:", score)
