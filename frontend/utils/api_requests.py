import requests
import streamlit as st

BASE_URL = "http://backend:8000"  # Use service name from docker-compose

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('access_token')}"}

def get(endpoint):
    return requests.get(f"{BASE_URL}{endpoint}", headers=get_headers())

def post(endpoint, data):
    return requests.post(f"{BASE_URL}{endpoint}", json=data, headers=get_headers())

def put(endpoint, data):
    return requests.put(f"{BASE_URL}{endpoint}", json=data, headers=get_headers())

def delete(endpoint):
    return requests.delete(f"{BASE_URL}{endpoint}", headers=get_headers())
