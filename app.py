# Import Flask so Python can create a web application
from flask import Flask, render_template, request

# Import our compatibility matching function
from study_groups.matching import calculate_compatibility

# Create Flask application
app = Flask(__name__)
# Sample study groups used to test the recommendation feature
study_groups = [
    {
        "name": "Software Engineering Study Group",
        "course": "CSC 4350",
        "study_style": "collaborative",
        "meeting_format": "online",
        "preferred_group_size": "small",
        "availability": ["Monday 3-5 PM", "Wednesday 1-3 PM"]
    },
    {
        "name": "Computer Networks Study Group",
        "course": "CSC 4220",
        "study_style": "independent",
        "meeting_format": "in-person",
        "preferred_group_size": "small",
        "availability": ["Tuesday 2-4 PM"]
    },
    {
        "name": "Software Engineering Evening Group",
        "course": "CSC 4350",
        "study_style": "independent",
        "meeting_format": "online",
        "preferred_group_size": "large",
        "availability": ["Wednesday 1-3 PM"]
    }
]

# Define the route for the home page
@app.route('/')
def home():
    # Display the application home page
    return render_template('index.html')

# Process student preferences and recommend compatible study groups
@app.route('/recommend', methods=['POST'])
def recommend():

    # Get the student's preferences from the HTML form
    student_preferences = {
        "course": request.form.get("course"),
        "study_style": request.form.get("study_style"),
        "meeting_format": request.form.get("meeting_format"),
        "preferred_group_size": request.form.get("preferred_group_size"),
        "availability": request.form.getlist("availability")
    }

    # Store recommended study groups
    recommendations = []

    # Compare student preferences against each study group
    for group in study_groups:

        # Only recommend groups for the student's selected course
        if group["course"] != student_preferences["course"]:
            continue

        # Calculate compatibility using our existing matching function
        score = calculate_compatibility(student_preferences, group)

        # Save the group and its compatibility score
        recommendations.append({
            "name": group["name"],
            "course": group["course"],
            "score": score
        })

    # Sort groups from highest to lowest compatibility
    recommendations.sort(
        key=lambda group: group["score"],
        reverse=True
    )

    # Display the recommendations on the homepage
    return render_template(
        'index.html',
        recommendations=recommendations
    )

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
