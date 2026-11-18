# Availability Matching Module
# Compares a student's availability with a study group's availability

def compare_availability(student_time, group_time):
    """
    Returns True if the student's availability
    matches the group's availability.
    """
    return student_time == group_time


def calculate_availability_score(student_time, group_time):
    """
    Returns a compatibility score based on availability.
    """
    if student_time == group_time:
        return 100
    else:
        return 0


# Example usage
student_availability = "evening"
group_availability = "evening"

is_match = compare_availability(
    student_availability,
    group_availability
)

score = calculate_availability_score(
    student_availability,
    group_availability
)

print("Availability Match:", is_match)
print("Compatibility Score:", score)
