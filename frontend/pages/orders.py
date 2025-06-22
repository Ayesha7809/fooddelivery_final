import streamlit as st
import requests
from utils.config import BASE_URL

def run():
    st.subheader("📦 Orders")

    user_type = st.session_state.get("user_type", "user")

    if user_type == "user":
        st.info("📝 Create a new order")

        # ⬇️ Only fetch restaurants if user is placing order
        restaurant_id = None
        try:
            res = requests.get(f"{BASE_URL}/restaurants/")
            restaurants = res.json()

            if res.status_code == 200 and restaurants:
                restaurant_options = [f"{r['id']} - {r['name']}" for r in restaurants]
                selected = st.selectbox("Select Restaurant", restaurant_options)
                restaurant_id = int(selected.split(" - ")[0])
            else:
                st.warning("No restaurants available. Please try again later.")
        except Exception as e:
            st.error(f"Failed to fetch restaurants: {e}")

        # 📝 Order fields
        food_item = st.text_input("Food Item", key="order_food_item")
        quantity = st.number_input("Quantity", min_value=1, step=1, key="order_quantity")
        delivery_address = st.text_input("Delivery Address", key="order_address")
        total_amount = st.number_input("Total Amount", min_value=0.0, format="%.2f", key="order_total_amount")
        status = st.selectbox("Order Status", ["Pending", "Confirmed", "Delivered"], key="order_status")
        payment_status = st.selectbox("Payment Status", ["Unpaid", "Paid"], key="order_payment_status")

        if st.button("Place Order", key="place_order_btn"):
            if restaurant_id is None:
                st.error("Please select a valid restaurant.")
            else:
                payload = {
                    "restaurant_id": restaurant_id,
                    "total_amount": total_amount,
                    "status": status,
                    "payment_status": payment_status,
                    "food_item": food_item,
                    "quantity": quantity,
                    "delivery_address": delivery_address
                    # DO NOT send ordered_by manually!
                }

                headers = {
                    "Authorization": f"Bearer {st.session_state.access_token}"
                }

                res = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
                if res.status_code == 200:
                    st.success("✅ Order placed successfully!")
                else:
                    st.error(f"❌ Failed to place order: {res.text}")

    elif user_type == "admin":
        st.info("📋 View and Delete Orders")

        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }

        res = requests.get(f"{BASE_URL}/orders/", headers=headers)
        if res.status_code == 200:
            orders = res.json()
            if not orders:
                st.warning("No orders available.")
            for order in orders:
                st.markdown("---")
                st.write(f"🆔 Order ID: {order['id']}")
                st.write(f"🍽️ Food Item: {order['food_item']}")
                st.write(f"🔢 Quantity: {order['quantity']}")
                st.write(f"📍 Address: {order['delivery_address']}")
                st.write(f"👤 Ordered By: {order['ordered_by']}")  # Use ordered_by instead of user_id

                if st.button(f"❌ Delete Order {order['id']}", key=f"delete_{order['id']}"):
                    del_res = requests.delete(f"{BASE_URL}/orders/{order['id']}", headers=headers)
                    if del_res.status_code == 200:
                        st.success(f"Order {order['id']} deleted successfully")
                    else:
                        st.error(f"Failed to delete order {order['id']}")
        else:
            st.error("Failed to load orders.")
