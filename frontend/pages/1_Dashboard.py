import streamlit as st
from config import page_setup, require_auth, page_title

page_setup("NitaRefund · Dashboard")
require_auth()  # bounces to login if no token

username = st.session_state.get("username", "User")
page_title(f"Welcome back, {username}", "Your dashboard is coming next.")

if st.button("Log out"):
    st.session_state.clear()
    st.switch_page("app.py")