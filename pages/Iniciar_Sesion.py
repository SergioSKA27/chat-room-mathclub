# trunk-ignore-all(isort)
import streamlit as st
from st_xatadb_connection import XataConnection
from streamlit_extras.switch_page_button import switch_page
import bcrypt

xata = st.connection("xata", type=XataConnection)

st.markdown('''
<style>
    .bg-image {
        background-color: #ffffff;
        opacity: 0.2;
        background-size: 10px 10px;
        background-image: repeating-linear-gradient(45deg, #444cf7 0, #444cf7 1px, #ffffff 0, #ffffff 50%);
        bottom:0;
        left:-50%;
        position:fixed;
        right:-50%;
        top:0;
        z-index:0;
        ackground-size: cover;
        background-position: center center;
    }
</style>
<div class="bg-image"></div>
''', unsafe_allow_html=True)


if "login_status" in st.session_state:
    if st.session_state.login_status:
        switch_page("Chat_Room")

def login():
    st.title("Iniciar Sesión")
    # this is the login form
    with st.form(key="login_form"):
        username = st.text_input("Usuario 👾",placeholder="Nombre de Usuario")
        password = st.text_input("Contraseña", type="password",placeholder="Contraseña")
        submit_button = st.form_submit_button(label="Iniciar Sesión")

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
                    switch_page("Chat_Room")

                else:
                    st.error("Incorrect password")
            else:
                st.error("No users found")

if __name__ == "__main__":
    login()
