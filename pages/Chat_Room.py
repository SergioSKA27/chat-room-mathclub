import io
import streamlit as st
from PIL import Image
from st_xatadb_connection import XataConnection
from streamlit_drawable_canvas import st_canvas

xata = st.connection("xata", type=XataConnection)

st.markdown('''
<style>
    .bg-image {
        background-color: #ffffff;
        opacity: 0.1;
        background-size: 20px 20px;
        background-image:  repeating-linear-gradient(0deg, #444cf7, #444cf7 1px, #ffffff 1px, #ffffff);

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

if "chat" not in st.session_state:
    # this stores the chat
    try:
        st.session_state.chat = [xata.query(
            "comments", {"page": {"size": 20}, "sort": {"xata.createdAt": "desc"}}
        )]
    except Exception as e:
        st.error(e)
        st.session_state.chat = []

if 'page' not in st.session_state:
    st.session_state.page = 0

if "chatmessage" not in st.session_state:
    st.session_state.chatmessage = None



def update_chat():
    # this updates the chat to get the latest messages
    try:
        st.session_state.chat = [xata.query(
            "comments", {"page": {"size": 10}, "sort": {"xata.createdAt": "desc"}}
        )]
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

def extract_code_from_graphviz(text):
    return text.split('$')[1]

def drawable_canvas():
    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:",("Libre", "Linea", "Rectangulo", "Circulo", "Transformar")
    )
    tools =  dict(zip(("Libre", "Linea", "Rectangulo", "Circulo", "Transformar"),("freedraw", "line", "rect", "circle", "transform")))
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=tools[drawing_mode],
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )

    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:
        if st.button("Subir",key="upload_canvas"):
            comment = 'Canvas'
            c = xata.insert("comments",{"user":st.session_state.username,"comment":comment})
            im = Image.fromarray(canvas_result.image_data)
            im.convert("RGB")
            buf = io.BytesIO()
            im.save(buf, format='PNG')
            byte_im = buf.getvalue()

            xata.upload_file("comments",c["id"],"file",byte_im,"image/png")
            update_chat()
            st.rerun()

def upload_image():
    url =  st.text_input("URL")
    if st.button("Subir",key="upload_image"):
        if url != "":
            comm = f'<img src="{url}" height=400px>'
            xata.insert("comments",{"user":st.session_state.username,"comment":comm})
        update_chat()
        st.rerun()

def chat_room(loged: bool = False):

    def read_chat():
        for i in st.session_state.chat[st.session_state.page]["records"][::-1]:
            with st.chat_message("user", avatar="🦋"):
                try:
                    st.write(":blue[user] : " + i["user"]["id"])
                    if "graphviz" in i["comment"]:
                        code = extract_code_from_graphviz(i["comment"])
                        with st.expander("Ver Código de Graphviz 🖧"):
                            st.code(code, language="dot")
                        if code is not None:
                            st.graphviz_chart(code)
                    if "file" in i and "url" in i["file"]:
                        st.image(i["file"]["url"])
                    else:
                        st.markdown(i["comment"],unsafe_allow_html=True)
                    st.write(i["xata"]["createdAt"][:19])
                except Exception as e:
                    st.write("Error al leer el mensaje")
                    print(e)

    ct = st.columns([0.9,0.1])
    with ct[0]:
        st.title("💬 Chat Room")
    with ct[1]:
        if st.button("Resetear"):
            st.session_state.chat = [xata.query("comments", {"page": {"size": 20}, "sort": {"xata.createdAt": "desc"}})]
            st.session_state.page = 0
    read_chat()

    cols = st.columns([0.7, 0.1, 0.1, 0.1])


    if cols[1].button("⏮️",use_container_width=True):
        if st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()

    if cols[2].button("⏭️",use_container_width=True):
        st.session_state.chat.append(xata.next_page(
            "comments", st.session_state.chat[st.session_state.page], pagesize=10
        ))
        st.session_state.page += 1

        if st.session_state.chat[st.session_state.page] is None:
            del st.session_state.chat[st.session_state.page]
            st.session_state.page  = 0
        st.rerun()
    if cols[3].button("🔄",use_container_width=True):
        update_chat()
        st.rerun()

    colsops = st.columns(4)

    with colsops[0]:
        img = st.checkbox("🖼️")

    with colsops[1]:
        graph = st.checkbox("🖧")

    with colsops[2]:
        canvas = st.checkbox("🎨")

    if graph:
        code = st.text_area("Codigo de Graphviz",height=200)
        if st.button("Subir"):
            comm = f'graphviz${code}'
            xata.insert("comments",{"user":st.session_state.username,"comment":comm})
            update_chat()
            st.rerun()
    if img:
        upload_image()

    chat_input = st.chat_input(
        "Escribe tu mensaje", key="chat_input", max_chars=250, disabled=not loged
    )
    if canvas:
        drawable_canvas()


    if chat_input:
        st.session_state.chatmessage = chat_input
        add_comment()
        update_chat()
        st.rerun()

def app():
    if st.session_state.login_status:
        with st.sidebar:
            if st.button("Cerrar Sesión"):
                st.session_state.login_status = False
                st.session_state.username = None
                st.rerun()

    chat_room(st.session_state.login_status)

    st.caption("Para ver nuevos mensajes refresca el chat")



if __name__ == "__main__":
    app()
