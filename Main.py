# trunk-ignore-all(isort)
import streamlit as st
from st_xatadb_connection import XataConnection
import bcrypt

st.set_page_config(page_title="Xata Demo", page_icon="🦋", layout="wide",initial_sidebar_state="collapsed")
# Set the connection to the database
xata = st.connection("xata", type=XataConnection)

st.markdown('''
<style>
    .bg-image {
        background-color: #ffffff;
        opacity: 0.3;
        background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #ffffff 10px ), repeating-linear-gradient( #444cf755, #444cf7 );
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

st.image("banner.gif",use_column_width=True)
