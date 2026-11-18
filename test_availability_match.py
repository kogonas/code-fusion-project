from availability_match import compare_availability

assert compare_availability("evening", "evening") == True
assert compare_availability("morning", "evening") == False

print("Availability comparison tests passed.")
