import streamlit as st
import requests
from pages import users, restaurants, orders, payments
from utils.auth import login_user
from utils.config import BASE_URL
import re  



BASE_URL = "http://backend:8000"

st.set_page_config(page_title="Food Delivery Dashboard", layout="wide")
st.title("🍽️ Food Delivery ")

if "access_token" not in st.session_state:
    st.session_state.access_token = None


def is_strong_password(password):
    """At least 8 characters, includes lowercase, uppercase, number, and special character"""
    return (
        len(password) >= 8
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"\d", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def register():
    st.subheader("📝 Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    email = st.text_input("Email", key="register_email")
    user_type = st.selectbox("User Type", ["admin", "user"], key="register_user_type")

    if st.button("Register", key="register_button"):
        if len(username) > 30:
            st.warning("❗ Username cannot exceed 30 characters.")
        elif "@" not in email or "." not in email:
            st.warning("❗ Please enter a valid email address.")
        elif not is_strong_password(password):
            st.warning("❗ Password must contain atleast 8 characters, includes lowercase, uppercase, number, and special character")
        else:
            payload = {
                "username": username,
                "password": password,
                "email": email,
                "user_type": user_type
            }
            res = requests.post(f"{BASE_URL}/users/register", json=payload)
            if res.status_code == 200:
                st.success("✅ Registered successfully")
            else:
                st.error(f"❌ Error: {res.text}")

def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        res = login_user(username, password)
        if res.status_code == 200:
            user_data = res.json()
            st.session_state.access_token = user_data["access_token"]
            st.session_state.user_type = user_data["user_type"]  # <-- add this line

            st.success("Login successful!")
        else:
            st.error("Invalid credentials")



# Logout Button
def logout():
    if st.button("Logout"):
        st.session_state.access_token = None
        st.success("Logged out")

# MAIN LOGIC
if st.session_state.access_token:
    logout()
    menu = st.sidebar.selectbox("📂 Select Section", ["Users", "Restaurants", "Orders", "Payments"])

    if menu == "Users":
        users.run()
    elif menu == "Restaurants":
        restaurants.run()
    elif menu == "Orders":
        orders.run()
    elif menu == "Payments":
        payments.run()
else:
    auth_choice = st.radio("Select Option", ["Login", "Register"])
    if auth_choice == "Login":
        login()
    else:
        register()
