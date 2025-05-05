import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from modules.nav import MenuButtons


logo1 = 'Logo1.png'
logo2 = 'Logo2.png'
st.logo(logo2, icon_image=logo2, size='large')




CONFIG_FILENAME = 'config.yaml'


with open(CONFIG_FILENAME) as file:
    config = yaml.load(file, Loader=SafeLoader)


def get_roles():
    """Gets user roles based on config file."""
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    if config is not None:
        cred = config['credentials']
    else:
        cred = {}

    return {username: user_info['role'] for username, user_info in cred['usernames'].items() if 'role' in user_info}


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


authenticator.login(location='main', fields={'Form name':'Iniciar sesión', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar', 'Captcha':'Captcha'})
if ss["authentication_status"]:
    st.switch_page('streamlit_app.py')

elif ss["authentication_status"] is False:
    st.error('Usuario/contraseña incorrecta')
elif ss["authentication_status"] is None:
    st.warning('Por favor ingresa usuario y contraseña')

# We call below code in case of registration, reset password, etc.
with open(CONFIG_FILENAME, 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

# Call this late because we show the page navigator depending on who logged in.
MenuButtons(get_roles())
