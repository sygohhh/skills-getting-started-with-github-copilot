def test_get_activities_returns_known_activity(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"].startswith("Learn strategies")


def test_signup_creates_participant(client):
    activity_name = "Chess Club"
    email = "signup-test-student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    activity_name = "Chess Club"
    email = "duplicate-test-student@mergington.edu"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first.status_code == 200

    duplicate = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_from_activity(client):
    activity_name = "Chess Club"
    email = "unregister-test-student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_not_signed_up_returns_404(client):
    activity_name = "Chess Club"
    email = "not-signed-up@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    activity_name = "Nonexistent Club"
    email = "unknown@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unknown_activity_returns_404(client):
    activity_name = "Nonexistent Club"
    email = "unknown@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
