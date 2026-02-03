'''
Flask Application
'''
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

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})
