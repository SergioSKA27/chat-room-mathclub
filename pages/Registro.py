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
        opacity: 0.1;
        background-image: radial-gradient(circle at center center, #444cf7, #ffffff), repeating-radial-gradient(circle at center center, #444cf7, #444cf7, 10px, transparent 20px, transparent 10px);
        background-blend-mode: multiply;
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
def user_register():
    st.title("Registro de Usuario 👾")
    with st.form(key="register_form"):
        username = st.text_input("Nombre de Usuario")
        name = st.text_input("Nombre Completo (opcional)")
        password = st.text_input("Contaseña", type="password")
        password2 = st.text_input("Confirmar Contraseña", type="password")

        submit_button = st.form_submit_button(label="Registrar Usuario 🚀")

        if submit_button and username != "" and password != "":
            if password.strip() == password2.strip():
                try:
                    xata.get("Users", username.strip())
                    st.error("El usuario ya existe 😢")
                except Exception as e:
                    if e.status_code == 404:
                        try:
                            result = xata.insert(
                                "Users",
                                {
                                    "password": bcrypt.hashpw(
                                        password.strip().encode(), bcrypt.gensalt()
                                    ).decode(),
                                    "name": name
                                },
                                record_id=username.strip(),
                                if_version=0,
                            )
                            st.toast("Usuario registrado con éxito",icon="😄")
                            st.write(result)
                        except Exception as e:
                            st.error("Something went wrong")
                            st.write(e)
            else:
                st.error("Las contraseñas no coinciden 😢")


if __name__ == "__main__":
    user_register()
    if st.button("Iniciar Sesión"):
        switch_page("Iniciar_Sesion")
