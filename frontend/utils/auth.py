import requests

BASE_URL = "http://backend:8000"  # Docker hostname

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", params={
        "username": username,
        "password": password
    })
    return response

def register_user(username, password, email, user_type):
    response = requests.post(f"{BASE_URL}/users/register", json={
        "username": username,
        "password": password,
        "email": email,
        "user_type": user_type
    })
    return response

