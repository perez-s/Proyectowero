import streamlit as st
from streamlit import session_state as ss


def HomeNav():
    st.sidebar.page_link("streamlit_app.py", label="Home", icon='🏠')


def LoginNav():
    st.sidebar.page_link("./pages/account.py", label="Ingresar", icon='🔐')


def Page1Nav():
    st.sidebar.page_link("./pages/page1.py", label="Page 1", icon='✈️')


def Page2Nav():
    st.sidebar.page_link("./pages/page2.py", label="Page 2", icon='📚')

def DataEntryAdmin():
    st.sidebar.page_link("/mount/src/proyectowero/pages/1_Data_Entry.py", label="Data entry", icon='📚')


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
            Page1Nav()
            DataEntryAdmin()
        if ss.username in users:
            Page2Nav()
            DataEntryAdmin()            
        # (2) users with user and admin roles have access to page 2.
    LoginNav()     
