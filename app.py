'''
Flask Application
'''
from dataclasses import asdict
import re
import os
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from dataclasses import asdict

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

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
        return jsonify(data["experience"])
    if request.method == "POST":
        if request.is_json:
            request_body = request.get_json()

            new_experience = Experience(
                request_body["title"],
                request_body["company"],
                request_body["start_date"],
                request_body["end_date"],
                request_body["description"],
                request_body.get("logo", "default-logo.png")
            )
        else:
            request_body = request.form

            logo_filename = "default-logo.png"
            if "logo" in request.files:
                logo_file = request.files["logo"]
                logo_filename = logo_file.filename
                logo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], logo_filename))

            new_experience = Experience(
                request_body["title"],
                request_body["company"],
                request_body["start_date"],
                request_body["end_date"],
                request_body["description"],
                logo_filename
            )

        data["experience"].append(new_experience)
        new_experience_id = len(data["experience"]) - 1

        return jsonify({"id": new_experience_id}), 201

    return jsonify({})

@app.route('/resume/experience/<int:exp_id>', methods=['GET'])
def get_experience(exp_id):
    '''
    Return a specific experience by ID
    '''
    if exp_id < 0 or exp_id >= len(data["experience"]):
        return jsonify({"error": "Experience not found"}), 404

    return jsonify(asdict(data["experience"][exp_id]))

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


@app.route('/resume/skill', methods=['GET', 'POST', 'PUT', 'DELETE'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        index = request.args.get('id', type=int)
        if index is not None:
            if 0 <= index < len(data["skill"]):
                return jsonify(data["skill"][index].__dict__)
            return jsonify({"error": "Invalid skill ID"}), 400
        
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
    
    if request.method == 'PUT':
        request_body = request.get_json()
        if not request_body:
            return jsonify({"error": "Request must be JSON"}), 400

        index = request_body.get("id")
        if index is None or not isinstance(index, int) or not 0 <= index < len(data["skill"]):
            return jsonify({"error": "Invalid skill ID"}), 400

        existing_skill = data["skill"][index]
        updated_skill = Skill(
            request_body.get("name", existing_skill.name),
            request_body.get("proficiency", existing_skill.proficiency),
            request_body.get("logo", existing_skill.logo),
        )
        data["skill"][index] = updated_skill

        return jsonify({
            "message": "Skill updated successfully",
            "id": index,
            "skill": updated_skill.__dict__
        }), 200

    if request.method == 'DELETE':
        index = request.json.get('id')
        if index is not None and 0 <= index < len(data['skill']):
            deleted_skill = data['skill'].pop(index)
            return jsonify({"message": "Skill deleted successfully"}), 200
        return jsonify({"error": "Invalid skill ID"}), 400

    return jsonify({})
