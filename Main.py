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

if "chat" not in st.session_state or st.session_state.chat is None:
    # this stores the chat
    try:
        st.session_state.chat = xata.query(
            "comments", {"page": {"size": 10}, "sort": {"xata.createdAt": "desc"}}
        )
    except Exception as e:
        st.error(e)
        st.session_state.chat = []

if "chatmessage" not in st.session_state:
    st.session_state.chatmessage = None

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

def update_chat():
    # this updates the chat to get the latest messages
    try:
        st.session_state.chat = xata.query(
            "comments", {"page": {"size": 10}, "sort": {"xata.createdAt": "desc"}}
        )
    # trunk-ignore(ruff/E722)
    except:
        st.session_state.chat = []


def add_comment():
    # this adds the comment to the database
    if st.session_state.chatmessage is not None and st.session_state.chatmessage != "":
        try:
            xata.insert(
                "comments",
                {
                    "user": st.session_state.username,
                    "comment": st.session_state.chatmessage,
                },
            )

        except Exception as e:
            st.error("Something went wrong try again")
            st.write(e)




def chat_room(loged: bool = False):
    def read_chat():
        for i in st.session_state.chat["records"][::-1]:
            with st.chat_message("user", avatar="🦋"):
                st.write(":blue[user] : " + i["user"]["id"])
                st.write(i["comment"])
                st.write(i["xata"]["createdAt"][:19])

    st.title("Chat Room")
    read_chat()
    cols = st.columns([0.2, 0.3, 0.3, 0.2])
    if cols[1].button("Previous Page"):
        st.session_state.chat = xata.prev_page(
            "comments", st.session_state.chat, pagesize=10
        )
        st.rerun()
    if cols[2].button("Next Page"):
        st.session_state.chat = xata.next_page(
            "comments", st.session_state.chat, pagesize=10
        )
        st.rerun()
    if cols[3].button("🔄"):
        update_chat()
        st.rerun()

    chat_input = st.chat_input(
        "Type here", key="chat_input", max_chars=250, disabled=not loged
    )
    if chat_input:
        st.session_state.chatmessage = chat_input
        add_comment()
        update_chat()
        st.rerun()


def app():
    if st.session_state.login_status:
        st.title("Welcome")
        if st.button("Logout"):
            st.session_state.login_status = False
            st.session_state.username = None
            st.rerun()

    chat_room(st.session_state.login_status)

    st.caption("Para ver nuevos mensajes refresca el chat")


if __name__ == "__main__":
    app()
