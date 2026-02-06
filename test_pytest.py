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



def test_user_info():
    '''
    Add a new user info and then get all user info. 

    Check that it returns the new user info in that list
    '''
    example_user_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }

    app.test_client().post('/resume/personal-info',
                          json=example_user_info)

    response = app.test_client().get('/resume/personal-info')
    assert response.json == example_user_info


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

def test_get_experience_by_valid_id():
    response = app.test_client().get("/resume/experience/0")

    assert response.status_code == 200
    data = response.get_json()

    assert "title" in data
    assert "company" in data
    assert "start_date" in data
    assert "end_date" in data
    assert "description" in data

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

def test_get_skill_by_index():
    '''
    Fetch a skill by its index via query parameter.
    '''
    response = app.test_client().get('/resume/skill', query_string={'id': 0})
    assert response.status_code == 200
    assert response.json['name'] == "Python"
    assert response.json['proficiency'] == "1-2 Years"


def test_delete_education():
    '''
    Test deleting an education entry by index.
    
    Verifies that the education is deleted and returns appropriate response.
    '''
    from app import data
    
    # Store initial count
    initial_count = len(data['education'])
    
    # Add a test education entry using POST
    example_education = {
        "course": "Test Course",
        "school": "Test University",
        "start_date": "January 2020",
        "end_date": "December 2023",
        "grade": "90%",
        "logo": "test-logo.png"
    }
    app.test_client().post('/resume/education', json=example_education)
    
    # Get the index of the newly added education (last item)
    index_to_delete = len(data['education']) - 1
    
    # Delete the education
    response = app.test_client().delete(f'/resume/education/{index_to_delete}')
    
    # Check response
    assert response.status_code == 200
    assert response.json['message'] == 'Education deleted successfully'
    assert response.json['deleted']['course'] == 'Test Course'
    
    # Verify the education was actually removed
    assert len(data['education']) == initial_count


def test_delete_education_invalid_index():
    '''
    Test deleting an education with an invalid index.
    
    Should return 404 error.
    '''
    from app import data
    
    # Try to delete with an index that doesn't exist
    invalid_index = len(data['education']) + 100
    response = app.test_client().delete(f'/resume/education/{invalid_index}')
    
    # Check that it returns 404
    assert response.status_code == 404
    assert response.json['error'] == 'Education not found'

def test_delete_education():
    '''
    Test deleting an education entry by index.
    
    Verifies that the education is deleted and returns appropriate response.
    '''
    from app import data
    
    # Store initial count
    initial_count = len(data['education'])
    
    # Add a test education entry using POST
    example_education = {
        "course": "Test Course",
        "school": "Test University",
        "start_date": "January 2020",
        "end_date": "December 2023",
        "grade": "90%",
        "logo": "test-logo.png"
    }
    app.test_client().post('/resume/education', json=example_education)
    
    # Get the index of the newly added education (last item)
    index_to_delete = len(data['education']) - 1
    
    # Delete the education
    response = app.test_client().delete(f'/resume/education/{index_to_delete}')
    
    # Check response
    assert response.status_code == 200
    assert response.json['message'] == 'Education deleted successfully'
    assert response.json['deleted']['course'] == 'Test Course'
    
    # Verify the education was actually removed
    assert len(data['education']) == initial_count


def test_delete_education_invalid_index():
    '''
    Test deleting an education with an invalid index.
    
    Should return 404 error.
    '''
    from app import data
    
    # Try to delete with an index that doesn't exist
    invalid_index = len(data['education']) + 100
    response = app.test_client().delete(f'/resume/education/{invalid_index}')
    
    # Check that it returns 404
    assert response.status_code == 404
    assert response.json['error'] == 'Education not found'
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


def test_update_skill_put():
    '''
    Update an existing skill using a PUT request and verify the change.
    '''
    # Create a skill to update
    example_skill = {
        "name": "Go",
        "proficiency": "1 year",
        "logo": "go-logo.png"
    }
    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    updated_skill = {
        "id": item_id,
        "name": "GoLang",
        "proficiency": "2 years",
        "logo": "updated-go-logo.png"
    }

    # Perform the update
    update_response = app.test_client().put('/resume/skill',
                                            json=updated_skill)
    assert update_response.status_code == 200
    assert update_response.json['message'] == "Skill updated successfully"
    assert update_response.json['skill']['name'] == "GoLang"

    # Confirm data was updated
    skills_after_update = app.test_client().get('/resume/skill').json
    assert skills_after_update[item_id]['name'] == "GoLang"
    assert skills_after_update[item_id]['proficiency'] == "2 years"
    assert skills_after_update[item_id]['logo'] == "updated-go-logo.png"
