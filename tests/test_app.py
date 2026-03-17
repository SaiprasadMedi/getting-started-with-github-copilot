def test_root_redirects_to_index(client):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange / Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "test.user@example.com"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_returns_400_if_already_signed_up(client):
    # Arrange
    activity = "Chess Club"
    already_signed_up = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": already_signed_up})

    # Assert
    assert response.status_code == 400


def test_remove_participant_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_nonexistent_participant_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "not.signed.up@example.com"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 400
