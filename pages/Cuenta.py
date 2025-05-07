import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from modules.nav import MenuButtons

st.set_page_config(
    page_title="Cuenta",
    page_icon="🔐",
)

# logo1 = 'Logo1.png'
# logo2 = 'Logo2.png'
# logo3 = 'Logo3.png'
# logo4 = 'Logo4.png'
# logo5 = 'Logo5.png'
# st.logo(logo4 ,icon_image=logo2, size='large')




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

authenticator = stauth.Authenticate('config.yaml')
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )
col1, col2, col3 = st.columns(3)
with col2:
    st.image('Logo2.png', use_container_width=True)

st.write(st.session_state.get('authentication_status'))

authenticator.login(location='main', fields={'Form name':'Iniciar sesión', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Ingresar', 'Captcha':'Captcha'})

css="""
<style>
    [data-testid="stForm"] {
        background: #31d3ae;

    }
</style>
"""
st.write(css, unsafe_allow_html=True)

if ss["authentication_status"]:
    st.switch_page('Inicio.py')
elif ss["authentication_status"] is False:
#     st.markdown("""
#     <style>
#         [data-testid=stSidebar] {
#             background-color: #31d3ae;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.html("""
#   <style>
#     [alt=Logo] {
#       height: 3.5rem;
#     }
#   </style>
#         """)
#     with st.sidebar:
#         st.write('')
    st.error('Usuario/contraseña incorrecta')
elif ss["authentication_status"] is None:
#     st.markdown("""
#     <style>
#         [data-testid=stSidebar] {
#             background-color: #31d3ae;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.html("""
#   <style>
#     [alt=Logo] {
#       height: 3.5rem;
#     }
#   </style>
#         """)
#     with st.sidebar:
#         st.write('')
    st.warning('Por favor ingresa usuario y contraseña')

# We call below code in case of registration, reset password, etc.

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

# if 'authenticator' not in st.session_state:
#     st.session_state.authenticator = authenticator
st.session_state.authenticator = authenticator

# Call this late because we show the page navigator depending on who logged in.
MenuButtons(get_roles())
