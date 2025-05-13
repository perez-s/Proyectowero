import streamlit as st
from streamlit import session_state as ss
import yaml
import time
from yaml.loader import SafeLoader
from modules.nav import MenuButtons
import streamlit_authenticator as stauth
import base64
from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html


authenticator = stauth.Authenticate('config.yaml')


if 'authapp' not in ss:
    ss.authapp = authenticator

    # st.set_page_config(
    #     page_title="Cuenta",
    #     page_icon="🔐",
    #     initial_sidebar_state="collapsed"
    # )

# logo1 = 'Logo1.png'
# logo2 = 'Logo2.png'
# logo3 = 'Logo3.png'
# logo4 = 'Logo4.png'
# logo5 = 'Logo5.png'
# st.logo(logo4 ,icon_image=logo2, size='large')


st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


CONFIG_FILENAME = 'config.yaml'

# with open(CONFIG_FILENAME) as file:
#     config = yaml.load(file, Loader=SafeLoader)

def get_roles():
    """Gets user roles based on config file."""
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    if config is not None:
        cred = config['credentials']
    else:
        cred = {}

    return {username: user_info['role'] for username, user_info in cred['usernames'].items() if 'role' in user_info}



# col1, col2, col3 = st.columns(3)
# with col2:
#     st.image('Logo2.png', use_container_width=True)

# authenticator.login(location='main', fields={'Form name':'Iniciar sesión', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar', 'Captcha':'Captcha'})

css="""
<style>
    [data-testid="stForm"] {
        background: #ffffff;

    }
</style>
"""
st.write(css, unsafe_allow_html=True)

# authenticator.login(location='unrendered', fields={'Form name':'Iniciar sesión', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar', 'Captcha':'Captcha'}, key='loginhome1')

# if ss["authentication_status"] is False:
#     col1, col2, col3 = st.columns(3)
#     with col2:
#         st.image('Logo2.png', use_container_width=True)
# elif ss["authentication_status"] is None:
#     col1, col2, col3 = st.columns(3)
#     with col2:
#         st.image('Logo2.png', use_container_width=True)

authenticator.login(location='main', fields={'Form name':'Iniciar sesión', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar', 'Captcha':'Captcha'}, key='loginhome1')

if ss["authentication_status"]:
    with st.sidebar:
        st.write(f'Benvenido/a *{ss["name"]}*i')
    MenuButtons(get_roles())
    authenticator.logout(button_name='Cerrar sesión', location='sidebar', use_container_width=True, key='logouthome')
    time.sleep(0.5)
    st.toast('Sesion iniciada exitosamente!', icon='✅')
    time.sleep(0.5)
    st.markdown("""
        <style>
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: initial;
            }
        </style>
        """, unsafe_allow_html=True
        )
    logo1 = 'Logo1.png'
    logo2 = 'Logo2.png'
    logo3 = 'Logo3.png'
    logo4 = 'Logo4.png'
    st.logo(logo4, icon_image=logo2, size='large')
    st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #31d3ae;
            }
        </style>
        """, unsafe_allow_html=True
        )
    st.html("""
        <style>
            [alt=Logo] {
            height: 3.5rem;
            }
        </style>
                """
            )
    # st.image('Logo1.png')
    st.markdown(img_to_html('banner4.jpg'), unsafe_allow_html=True)
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
        """
        )
    # st.markdown(img_to_html('banner2.jpg'), unsafe_allow_html=True)


if ss["authentication_status"] is False:
    st.toast('Usuario/contraseña incorrecta', icon="🚫")
    def set_bg_hack(main_bg):
        '''
        A function to unpack an image from root folder and set as bg.
    
        Returns
        -------
        The background.
        '''
        # set bg name
        main_bg_ext = "png"
            
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack('homepage1.jpg')

elif ss["authentication_status"] is None:
    st.toast('Por favor ingresa usuario y contraseña', icon="⚠️")
    def set_bg_hack(main_bg):
        '''
        A function to unpack an image from root folder and set as bg.
    
        Returns
        -------
        The background.
        '''
        # set bg name
        main_bg_ext = "png"
            
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack('homepage1.jpg')


