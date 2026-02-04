'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == "POST":
        request_body = request.get_json()
        if not request_body:
            return jsonify({"error": "Request must be JSON or include form data"}), 400

        new_experience = Experience(
            request_body["title"],
            request_body["company"],
            request_body["start_date"],
            request_body["end_date"],
            request_body["description"],
        )
        data["experience"].append(new_experience)

        new_experience_id = len(data["experience"]) - 1

        return jsonify({"message": "Experience added successfully ", "id": new_experience_id}), 201

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        request_body = request.get_json()

        if not request_body:
            return jsonify({"error": "Request must be valid JSON"}), 400

        try:
            new_education = Education(
                request_body["course"],
                request_body["school"],
                request_body["start_date"],
                request_body["end_date"],
                request_body["grade"],
            )
        except KeyError as missing:
            return jsonify({"error": "Missing required field: " + missing.args[0]}), 400

        if "logo" in request_body:
            new_education.logo = request_body["logo"]

        data["education"].append(new_education)

        new_education_id = len(data["education"]) - 1

        return jsonify({"message": "Education added successfully ", "id": new_education_id}), 201

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST', 'DELETE'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    if request.method == 'DELETE':
        index = request.json.get('id')
        if index is not None and 0 <= index < len(data['skill']):
            deleted_skill = data['skill'].pop(index)
            return jsonify({"message": "Skill deleted successfully"}), 204
        return jsonify({"error": "Invalid skill ID"}), 400

    return jsonify({})
