'''
Flask Application
'''
from dataclasses import asdict
import re
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

########### Helper functions ###########
def validate_email(email):
    '''validate email'''
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    return False

def validate_phone(phone):
    '''validate phone number'''
    if re.match(r'^\+[1-9]\d{7,14}$', phone):
        return True
    return False
########################################


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


@app.route('/resume/personal-info', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_info():
    '''
    Handle user personal info requests
    '''
    if request.method == 'GET':
        return jsonify(data["personal_info"])

    if request.method == 'POST':
        body = request.json
        if not body:
            return jsonify({"error": "Invalid JSON"}), 400

        required = ("name", "email", "phone")
        if not all(key in body for key in required):
            return jsonify({"error": "Missing required fields"}), 400

        if not validate_email(body["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        if not validate_phone(body["phone"]):
            return jsonify({"error": "Invalid phone number format"}), 400

        data["personal_info"] = body
        return jsonify(body), 201

    if request.method == 'PUT':
        body = request.json
        if not body:
            return jsonify({"error": "Invalid JSON"}), 400

        if "email" in body and not validate_email(body["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        if "phone" in body and not validate_phone(body["phone"]):
            return jsonify({"error": "Invalid phone number format"}), 400

        data["personal_info"].update(body)
        return jsonify(data["personal_info"])

    if request.method == 'DELETE':
        data["personal_info"] = {}
        return jsonify({"message": "Personal info deleted"})

    return jsonify({"error": "Method not allowed"}), 405

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
        return jsonify([asdict(education) for education in data["education"]])

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

@app.route('/resume/education/<int:index>', methods=['DELETE'])
def delete_education(index):
    '''
    Delete an education entry by index
    '''
    try:
        if 0 <= index < len(data['education']):
            deleted_education = data['education'].pop(index)
            return jsonify({
                'message': 'Education deleted successfully',
                'deleted': deleted_education.__dict__
            }), 204
        return jsonify({'error': 'Education not found'}), 404
    except IndexError:
        return jsonify({'error': 'Education not found'}), 404


@app.route('/resume/skill', methods=['GET', 'POST', 'DELETE'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        skills_as_dicts = [skill.__dict__ for skill in data["skill"]]
        return jsonify(skills_as_dicts)

    if request.method == 'POST':
        request_body = request.get_json()
        if not request_body:
            return jsonify({"error": "Request must be JSON"}), 400

        try:
            new_skill = Skill(
                request_body["name"],
                request_body["proficiency"],
                request_body["logo"]
            )
        except KeyError as missing:
            return jsonify({"error": f"Missing field: {missing.args[0]}"}), 400

        data["skill"].append(new_skill)
        new_skill_id = len(data["skill"]) - 1
        return jsonify({"message": "Skill added successfully", "id": new_skill_id}), 201

    if request.method == 'DELETE':
        index = request.json.get('id')
        if index is not None and 0 <= index < len(data['skill']):
            deleted_skill = data['skill'].pop(index)
            return jsonify({"message": "Skill deleted successfully"}), 204
        return jsonify({"error": "Invalid skill ID"}), 400

    return jsonify({})
