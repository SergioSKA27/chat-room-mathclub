# trunk-ignore-all(isort)
import streamlit as st
from st_xatadb_connection import XataConnection
import bcrypt

xata = st.connection("xata", type=XataConnection)

def login():
    st.title("Login")
    # this is the login form
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

        if username != "" and password != "":
            user_info = None

            try:
                user_info = xata.get("Users", username.strip())
            except Exception as e:
                if e.status_code == 404:
                    # this means that the user does not exist
                    st.error("No users found")

        if submit_button:
            if user_info is not None:
                if bcrypt.checkpw(
                    password.strip().encode(), user_info["password"].encode()
                ):
                    st.toast("Logged in as {}".format(username.strip()), icon="😄")
                    st.session_state.login_status = True
                    st.session_state.username = username.strip()
                    st.rerun()

                else:
                    st.error("Incorrect password")
            else:
                st.error("No users found")

