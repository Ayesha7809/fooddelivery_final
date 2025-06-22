import streamlit as st
import requests
from utils.config import BASE_URL
import re

def run():
    st.subheader("🏪 Manage Restaurants")

    user_type = st.session_state.get("user_type", "user")  # default to 'user'

    # Only admin sees full CRUD options
    if user_type == "admin":
        action = st.selectbox("Select Action", ["Create", "Read", "Update", "Delete"], key="restaurant_crud_action")
    else:
        st.info("You are logged in as a regular user. You can only view restaurants.")
        action = "Read"  # force only Read action for normal users

    if action == "Create":
        name = st.text_input("Restaurant Name", key="restaurant_name_input")
        location = st.text_input("Location", key="restaurant_location_input")
        address = st.text_input("Address", key="restaurant_address_input")
        phone = st.text_input("Phone", key="restaurant_phone_input")

        if st.button("Add Restaurant", key="add_restaurant_button"):
            if not re.fullmatch(r"03[0-9]{9}", phone):
             st.warning("❗ Please enter a valid Pakistani phone number (e.g., 03112233445).")
            else:
                payload = {
                    "name": name,
                    "location": location,
                    "address": address,
                    "phone": phone
                }

            res = requests.post(f"{BASE_URL}/restaurants/", json=payload)
            if res.status_code == 200:
                st.success("Restaurant added successfully!")
            else:
                st.error(f"Failed to add restaurant: {res.text}")

    elif action == "Read":
        st.write("📋 List of Restaurants")
        res = requests.get(f"{BASE_URL}/restaurants/")
        if res.status_code == 200:
            restaurants = res.json()
            if restaurants:
                for r in restaurants:
                    st.write(f"🍽️ {r.get('name')} - 📍 {r.get('location', 'N/A')} - 🏠 {r.get('address', 'N/A')} - 📞 {r.get('phone', 'N/A')}")
            else:
                st.info("No restaurants found.")
        else:
            st.error("Could not fetch restaurants.")

    elif action == "Update":
        res = requests.get(f"{BASE_URL}/restaurants/")
        if res.status_code == 200:
            restaurants = res.json()
            if restaurants:
                restaurant_map = {f"{r['id']} - {r['name']}": r for r in restaurants}
                selected = st.selectbox("Select Restaurant to Update", list(restaurant_map.keys()), key="update_select")
                selected_restaurant = restaurant_map[selected]

                new_name = st.text_input("New Name", value=selected_restaurant["name"], key="update_name")
                new_location = st.text_input("New Location", value=selected_restaurant["location"], key="update_location")
                new_address = st.text_input("New Address", value=selected_restaurant["address"], key="update_address")
                new_phone = st.text_input("New Phone", value=selected_restaurant["phone"], key="update_phone")

                if st.button("Update", key="update_button"):
                    payload = {
                        "name": new_name,
                        "location": new_location,
                        "address": new_address,
                        "phone": new_phone
                    }
                    res = requests.put(f"{BASE_URL}/restaurants/{selected_restaurant['id']}", json=payload)
                    if res.status_code == 200:
                        st.success("Restaurant updated successfully!")
                    else:
                        st.error(f"Failed to update: {res.text}")
            else:
                st.info("No restaurants available to update.")
        else:
            st.error("Failed to fetch restaurant list.")

    elif action == "Delete":
        res = requests.get(f"{BASE_URL}/restaurants/")
        if res.status_code == 200:
            restaurants = res.json()
            if restaurants:
                restaurant_map = {f"{r['id']} - {r['name']}": r for r in restaurants}
                selected = st.selectbox("Select Restaurant to Delete", list(restaurant_map.keys()), key="delete_select")
                selected_restaurant = restaurant_map[selected]

                if st.button("Delete", key="delete_button"):
                    res = requests.delete(f"{BASE_URL}/restaurants/{selected_restaurant['id']}")
                    if res.status_code == 200:
                        st.success("Restaurant deleted successfully!")
                    else:
                        st.error(f"Failed to delete: {res.text}")
            else:
                st.info("No restaurants available to delete.")
        else:
            st.error("Failed to fetch restaurant list.")
