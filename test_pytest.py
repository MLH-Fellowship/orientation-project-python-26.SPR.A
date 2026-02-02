'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill


def test_delete_skill():
    '''
    Test deleting a skill by its index position.
    
    Add a skill, delete it, and verify it was removed.
    '''
    # Add a new skill first
    example_skill = {
        "name": "TypeScript",
        "proficiency": "1-2 years",
        "logo": "example-logo.png"
    }
    
    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']
    
    # Delete the skill using its index
    delete_response = app.test_client().delete('/resume/skill',
                                               json={"id": item_id})
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == "Skill deleted successfully"
    
    # Verify the skill was deleted by getting all skills
    response = app.test_client().get('/resume/skill')
    assert item_id not in response.json or response.json[item_id] != example_skill
