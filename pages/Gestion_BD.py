import random
import string
import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
import geonamescache
import pathlib
import shutil
import os
import re
import time
import yaml
from yaml.loader import SafeLoader
import base64
from pathlib import Path
from datetime import datetime

CONFIG_FILENAME = 'config.yaml'

def get_roles():
    """Gets user roles based on config file."""
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    if config is not None:
        cred = config['credentials']
    else:
        cred = {}

    return {username: user_info['role'] for username, user_info in cred['usernames'].items() if 'role' in user_info}

if 'authentication_status' not in ss:
    st.switch_page('./pages/Inicio.py')
if ss["authentication_status"]:

    authenticator = ss.get('authapp')
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
    authenticator.logout(button_name='Cerrar sesión', location='sidebar', use_container_width=True, key='logoutformats')
    #################################   Main section code   ###################################################

    

    st.title('Gestión de Base de Datos')
    st.subheader('Informe comparativo recolección/caracterización')
    año = st.selectbox('Seleccione un año', options=['2022', '2023', '2024', '2025'], key='year_select')
    meses = {
        'Enero': '1', 'Febrero': '2', 'Marzo': '3', 'Abril': '4',
        'Mayo': '5', 'Junio': '6', 'Julio': '7', 'Agosto': '8',
        'Septiembre': '9', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'
    }
    mes = st.selectbox('Seleccione un mes', options=list(meses.keys()), key='month_select')
    if st.button("Generar Reporte", key="generate_report2", use_container_width=True):
            with st.spinner(f"Generando reporte de {mes}-{año}...", show_time=True):
                if os.path.exists(f"reporte_comparativo_{mes}-{año}.pdf"):
                    os.remove(f"reporte_comparativo_{mes}-{año}.pdf")
                os.system(f"quarto render reporte_comparativo.qmd -P año:{año} -P mes:{meses[mes]} --output reporte_comparativo_{mes}-{año}.pdf")
                try:    
                    with open(f"reporte_comparativo_{mes}-{año}.pdf", "rb") as file:
                        st.download_button(
                            label="Descargar Reporte",
                            data=file,
                            file_name=f"reporte_comparativo_{mes}-{año}.pdf",
                            mime="application/pdf",
                            key="download_report",
                            use_container_width=True,
                            type="primary",
                        )
                except:
                    st.toast("Error al generar el reporte. Por favor, verifica los datos ingresados.", icon="🚨")


else:
    st.switch_page("./pages/Inicio.py")
