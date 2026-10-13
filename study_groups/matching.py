# Calculates how compatible a student's preferences are with a study group's preferences
def calculate_compatibility(student_preferences, group_preferences):
    #keeps track of how many preferences match
    matches = 0

    #For now, only study style is being compared
    #More cmpatibility factors will be added later
    total_factors = 1

    #Check if the student's preferred study style matches the group's study style
    if student_preferences["study_style"] == group_preferences["study_style"]:
        matches += 1

    #Convert the number of matching preferences into a percentage
    compatibility_score = (matches / total_factors) * 100

    #Return the final compatibility percentage 
    return compatibility_score

