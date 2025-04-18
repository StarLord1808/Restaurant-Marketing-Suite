import streamlit as st
from auth import create_user_table, add_user, verify_user

# Ensure user table exists
create_user_table()

def login_page():
    st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

    st.title("🍽️ Delicacy AI Agent - Login")
    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Select Option", menu)

    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("User ID")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = verify_user(username, password)
            if user:
                st.success(f"Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()  # Refresh the page after login
            else:
                st.error("Incorrect ID or Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Choose a User ID")
        new_pass = st.text_input("Choose a Password", type='password')
        if st.button("Sign Up"):
            try:
                add_user(new_user, new_pass)
                st.success("Account created! Go to Login to sign in.")
            except:
                st.error("Username already exists. Try a different one.")

# Initialize login state if not present
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# If already logged in, go to main.py (i.e., the home page)
if st.session_state.logged_in:
    st.switch_page("pages/1_Post_Generator.py")  # or whatever page makes sense
else:
    login_page()
