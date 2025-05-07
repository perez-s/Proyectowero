import streamlit as st
from streamlit import session_state as ss


def HomeNav():
    st.sidebar.page_link("Inicio.py", label="Inicio", icon='🏠')


def LoginNav():
    st.sidebar.page_link("./pages/Cuenta.py", label="Ingresar", icon='🔐')

def DataEntryAdmin():
    st.sidebar.page_link("pages/Formatos.py", label="Formatos", icon='📚')


def MenuButtons(user_roles=None):
    if user_roles is None:
        user_roles = {}

    if 'authentication_status' not in ss:
        ss.authentication_status = False

    # Always show the home and login navigators.
    #HomeNav()
    

    # Show the other page navigators depending on the users' role.
    if ss["authentication_status"]:

        # (1) Only the admin role can access page 1 and other pages.
        # In a user roles get all the usernames with admin role.
        admins = [k for k, v in user_roles.items() if v == 'admin']
        users = [k for k, v in user_roles.items() if v == 'user']

        HomeNav()

        # Show page 1 if the username that logged in is an admin.
        if ss.username in admins:
            DataEntryAdmin()
        if ss.username in users:
            DataEntryAdmin()            
        # (2) users with user and admin roles have access to page 2.     
