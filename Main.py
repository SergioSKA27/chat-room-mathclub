# trunk-ignore-all(isort)
import streamlit as st
from st_xatadb_connection import XataConnection
import bcrypt

st.set_page_config(page_title="Xata Demo", page_icon="🦋", layout="wide",initial_sidebar_state="collapsed")
# Set the connection to the database
xata = st.connection("xata", type=XataConnection)


# Set the title of the app
st.title("Club de Matemáticas Acatlán 👾")
st.divider()
# Set the variables for the app
if "login_status" not in st.session_state:
    # we can use this to check if the user is logged in or not
    st.session_state.login_status = False

if "username" not in st.session_state:
    # we can use this to check the username of the user
    st.session_state.username = None


if not st.session_state.login_status:
    passw = st.text_input("Contraseña", type="password")

    if bcrypt.checkpw(passw.strip().encode(),st.secrets["PASSWORD"].encode()):
        st.toast("Bienvenido", icon="😄")
    else:
        st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
