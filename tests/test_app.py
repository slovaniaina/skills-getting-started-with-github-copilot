import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_success():
    response = client.post("/activities/Tennis Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Tennis Club" in response.json().get("message", "")

    # Clean up: remove the test participant
    data = client.get("/activities").json()
    data["Tennis Club"]["participants"].remove("tester@mergington.edu")

def test_signup_duplicate():
    # Add a participant first
    client.post("/activities/Drama Club/signup?email=unique@mergington.edu")
    # Try to add again
    response = client.post("/activities/Drama Club/signup?email=unique@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

    # Clean up: remove the test participant
    data = client.get("/activities").json()
    data["Drama Club"]["participants"].remove("unique@mergington.edu")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
