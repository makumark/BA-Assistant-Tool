from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.crud.user import create_user

client = TestClient(app)

def test_register_user():
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_login_user():
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    # First, register the user
    create_user(UserCreate(**user_data))
    
    response = client.post("/api/v1/auth/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_invalid_credentials():
    user_data = {
        "email": "invaliduser@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=user_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"