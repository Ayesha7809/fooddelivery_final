import streamlit as st
import requests
from utils.config import BASE_URL

def run():
    st.subheader("💳 Payments")

    user_type = st.session_state.get("user_type", "user")

    if user_type == "user":
        st.info("Make a Payment")

        order_id = st.number_input("Order ID", min_value=1, step=1, key="pay_order_id")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="pay_amount")
        payment_method = st.selectbox("Payment Method", ["Credit Card", "Easypaisa", "JazzCash", "Cash"], key="pay_method")
        payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid"], key="pay_status")
        transaction_id = st.text_input("Transaction ID", key="pay_txn_id")

        if st.button("Submit Payment", key="submit_payment"):
            payload = {
                "order_id": order_id,
                "amount": amount,
                "payment_method": payment_method,
                "payment_status": payment_status,
                "transaction_id": transaction_id
            }
            headers = {
                "Authorization": f"Bearer {st.session_state.access_token}"
            }

            res = requests.post(f"{BASE_URL}/payments/", json=payload, headers=headers)
            if res.status_code == 200:
                st.success("Payment recorded successfully!")
            else:
                st.error(f"Failed to record payment: {res.text}")

    elif user_type == "admin":
        st.info("📋 All Payments")
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
        res = requests.get(f"{BASE_URL}/payments/", headers=headers)
        if res.status_code == 200:
            payments = res.json()
            for p in payments:
                st.markdown("---")
                st.write(f"💵 Amount: {p['amount']}")
                st.write(f"🧾 Transaction ID: {p['transaction_id']}")
                st.write(f"📦 Order ID: {p['order_id']}")
                st.write(f"💳 Method: {p['payment_method']}")
                st.write(f"✅ Status: {p['payment_status']}")
        else:
            st.error("Failed to fetch payments.")
