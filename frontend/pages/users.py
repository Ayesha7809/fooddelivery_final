import streamlit as st
import requests
from utils.config import BASE_URL

def run():
    st.subheader("👥 Manage Users")

    user_type = st.session_state.get("user_type", "user")

    # Only admin can do full CRUD
    if user_type == "admin":
        action = st.selectbox("Select Action", ["Read", "Update", "Delete"], key="user_action")
    else:
        st.info("You are logged in as a regular user. You can only view users.")
        action = "Read"

    if action == "Read":
        if st.button("🔄 Load Users"):
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            res = requests.get(f"{BASE_URL}/users/", headers=headers)
            if res.status_code == 200:
                users = res.json()
                st.json(users)
            else:
                st.error("Could not load users")

    elif action == "Update":
        user_id = st.number_input("Enter User ID to update", min_value=1)
        new_username = st.text_input("New Username")
        new_email = st.text_input("New Email")
        new_user_type = st.selectbox("User Type", ["admin", "user"])

        if st.button("✅ Update User"):
            payload = {
                "username": new_username,
                "email": new_email,
                "user_type": new_user_type
            }
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            res = requests.put(f"{BASE_URL}/users/{user_id}", json=payload, headers=headers)
            if res.status_code == 200:
                st.success("User updated successfully")
            else:
                st.error(f"Failed to update user: {res.text}")

    elif action == "Delete":
        user_id = st.number_input("Enter User ID to delete", min_value=1)
        if st.button("🗑️ Delete User"):
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            res = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
            if res.status_code == 200:
                st.success("User deleted successfully")
            else:
                st.error(f"Failed to delete user: {res.text}")
