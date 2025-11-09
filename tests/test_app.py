import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400


def test_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
