from app.models import User


def test_login_success(client):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "Admin123!"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Compliance Dashboard" in response.data


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_user_password_hash(app):
    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        assert user.check_password("Admin123!") is True
