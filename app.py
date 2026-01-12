import streamlit as st
from database import init_db, add_offer, match_offers, get_active_offers
from ai import parse_ngo_query, generate_match_summary
from datetime import datetime

init_db()  # Run once

st.title("Food Connect: Linking Excess Food to Those in Need")

role = st.selectbox("Select your role:", ["Restaurant (Donate Food)", "NGO (Search for Food)"])

if role == "Restaurant (Donate Food)":
    st.header("Submit Excess Food Offer")
    food_type = st.text_input("Food Type (e.g., vegetarian pizza)")
    quantity = st.number_input("Quantity (portions)", min_value=1)
    expiration = st.datetime_input("Expiration Date/Time", min_value=datetime.now())
    location = st.text_input("Location (e.g., Abuja Garki)")
    email = st.text_input("Your Email")
    if st.button("Submit Offer"):
        add_offer(food_type, quantity, expiration.isoformat(), location, email)
        st.success("Offer submitted!")

    st.subheader("Current Active Offers (for testing)")
    offers = get_active_offers()
    for offer in offers:
        st.write(offer)

elif role == "NGO (Search for Food)":
    st.header("Smart Search for Food")
    query = st.text_area("Describe what you need (e.g., 'Rice meals for 20 people in Abuja tonight')")
    if st.button("Search with AI"):
        criteria = parse_ngo_query(query)
        st.write("AI-extracted criteria:", criteria)  # For demo/debug
        matches = match_offers(criteria)
        summary = generate_match_summary(matches)
        st.markdown(summary)