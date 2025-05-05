import streamlit as st
from streamlit import session_state as ss
from modules.nav import MenuButtons
from pages.account import get_roles
from pages.account import authenticator


logo1 = 'Logo1.png'
logo2 = 'Logo2.png'
st.logo(logo2, icon_image=logo2, size='large')


# If the user reloads or refreshes the page while still logged in,
# go to the account page to restore the login status. Note reloading
# the page changes the session id and previous state values are lost.
# What we are doing is only to relogin the user.



MenuButtons(get_roles())




# Protected content in home page.
if ss.get('authentication_status'):
    with st.sidebar:
        st.write(f'Bienvenido/a *{ss["name"]}*')
    authenticator.logout(button_name='Cerrar sesión', location='sidebar')
    logo1 = 'Logo1.png'
    logo2 = 'Logo2.png'
    st.logo(logo2, icon_image=logo2, size='large')
        
    st.image('Logo1.png')
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
    st.switch_page('./pages/account.py')
    #st.write('Please log in on login page.')
