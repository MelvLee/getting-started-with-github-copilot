import pytest


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Art Club"
    email = "newstudent@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")

    # Verify participant was added
    resp2 = client.get("/activities")
    participants = resp2.json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent"
    email = "someone@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Gym Class"
    email = "john@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify participant removed
    resp2 = client.get("/activities")
    participants = resp2.json()[activity]["participants"]
    assert email not in participants


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Drama Club"
    email = "notregistered@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student not signed up for this activity"
