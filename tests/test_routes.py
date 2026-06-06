from pathlib import Path

import pytest

from backend import create_app
from backend.services.db_service import init_db


@pytest.fixture()
def client(tmp_path: Path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test_app.db")

    with app.app_context():
        init_db()

    with app.test_client() as client:
        yield client


def test_home_redirects_to_login_when_logged_out(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_signup_and_login_flow(client):
    signup_response = client.post(
        "/signup",
        data={
            "name": "Anjali",
            "email": "anjali@example.com",
            "password": "pass123",
            "confirm_password": "pass123",
        },
        follow_redirects=True,
    )
    assert signup_response.status_code == 200
    assert b"Account created successfully" in signup_response.data

    login_response = client.post(
        "/login",
        data={
            "email": "anjali@example.com",
            "password": "pass123",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"Paste Your Code" in login_response.data
