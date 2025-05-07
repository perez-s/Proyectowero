import streamlit as st
from streamlit import session_state as ss
from modules.nav import MenuButtons
from pages.Cuenta import get_roles
from pages.Cuenta import authenticator

# st.set_page_config(
#     page_title="Inicio",
#     page_icon="Logo2.png",
#     initial_sidebar_state="expanded"
# )


logo1 = 'Logo1.png'
logo2 = 'Logo2.png'
logo3 = 'Logo3.png'
logo4 = 'Logo4.png'
st.logo(logo4, icon_image=logo2, size='large')


# If the user reloads or refreshes the page while still logged in,
# go to the Cuenta page to restore the login status. Note reloading
# the page changes the session id and previous state values are lost.
# What we are doing is only to relogin the user.

# Protected content in home page.
if ss.get('authentication_status'):
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #31d3ae;
        }
    </style>
    """, unsafe_allow_html=True)
    st.html("""
  <style>
    [alt=Logo] {
      height: 3.5rem;
    }
  </style>
        """)
    with st.sidebar:
        st.write(f'Bienvenido/a *{ss["name"]}*')
    MenuButtons(get_roles())
    authenticator.logout(button_name='Cerrar sesión', location='sidebar', use_container_width=True)
        
    st.image('Logo1.png')
    st.write(st.session_state.get('authentication_status'))

    st.markdown("""
# ¡Bienvenido a **Weroapp**!

¡Hola y bienvenido a **Weroapp**, la forma más sencilla de ingresar, gestionar y enviar tus datos!

- **Formularios Intuitivos**    
- **Guardado y Borradores**  
- **Exportación de Datos**  

---

## ¿Necesitas ayuda?

- Escribe a nuestro equipo de soporte: [soporte@Wero.com.co](mailto:soporte@Wero.com.co).

¡Hagamos que la entrada de datos sea sencilla! 🚀
""")

else:
    st.switch_page('./pages/Cuenta.py')
    #st.write('Please log in on login page.')
