# trunk-ignore-all(isort)
import streamlit as st
from st_xatadb_connection import XataConnection
from streamlit_extras.switch_page_button import switch_page
import bcrypt

xata = st.connection("xata", type=XataConnection)

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
