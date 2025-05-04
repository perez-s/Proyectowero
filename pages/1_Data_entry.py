import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
from pages.account import get_roles
import geonamescache

if 'authentication_status' not in ss:
    st.switch_page('./pages/account.py')

MenuButtons(get_roles())

countrieslist = []
citiesdict = {}

gc = geonamescache.GeonamesCache()
countries = dict(gc.get_countries())
countriesabv = list(countries.keys())

# print countries dictionary

for i in countriesabv:
    countrieslist.append(countries[i]['name'])
countrieslist.sort()

cities = dict(gc.get_cities())
citiesabv = list(cities.keys())

for i in citiesabv:
    citiesdict.update({cities[i]['name']:countries[cities[i]['countrycode']]['name']})


tab1, tab2, tab3 = st.tabs(["Tabla II-C", "Tabla II-B", "Tabla II-D"])

with tab1:

    st.write("TABLA II-B. IDENTIFICACIÓN DE OPERADORES Y/O ADMINISTRADORES DEL PLAN")

    col1, col2 = st.columns(2)
    with col1:
        nombre_input = st.text_input('Nombre',key='nombre_input_key')
        nacionalidad_input = st.selectbox('Nacionalidad', countrieslist, index=None, placeholder='Seleccione un país',accept_new_options=False, key='nacionalidad_input_key')
        
        nit_input=st.number_input("NIT", value=None, placeholder=None, key='nit_input_key')
        correo_input = st.text_input('Correo electrónico', key='correo_input_key')
    with col2:
        telefono_input = st.text_input('Teléfono', key='telefono_input_key')
        direccion_input = st.text_input('Dirección física', key='direccion_input_key')
        
        citieslist = [k for k, v in citiesdict.items() if v == nacionalidad_input]
        citieslist.sort()
        
        ciudad_input = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False, key='ciudad_input_key')
        observaciones_input = st.text_area('Obsevaciones', key='observaciones_input_key')

    st.write(ciudad_input)

    if st.button('Registrar'):
        with open('pages/notes.csv', 'a+') as f:    #Append & read mode
            f.write(f"{nombre_input},{nacionalidad_input},{nit_input},{correo_input},{telefono_input},{direccion_input},{ciudad_input},{observaciones_input}\n")
    
    st.info("Previsualización")
    
    st.dataframe(pd.read_csv("pages/notes.csv",names=["Nombre","Nacionalidad","NIT","Correo","Telefono","Dirección","Ciudad","Observaciones"],encoding='latin1'),height=300)
