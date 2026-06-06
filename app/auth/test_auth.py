

def test_signup_creates_user(client):
    response = client.post(
        "/auth/signup",
        data={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert len(data) == 2


def test_signup_with_existing_email_fails(client):
    client.post(
        "/auth/signup",
        data={
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/signup",
        data={
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_with_correct_password(client):
    client.post(
        "/auth/signup",
        data={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "login@example.com"

    assert data["email"] == "login@example.com"
    assert data["message"] == "Login successful"
    assert "id" in data
    assert len(data) == 3


def test_login_with_wrong_password_fails(client):
    client.post(
        "/auth/signup",
        data={
            "email": "wrong-password@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "email": "wrong-password@example.com",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

