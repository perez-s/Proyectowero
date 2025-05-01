import streamlit as st
import pandas as pd
from streamlit import session_state as ss
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
print(citiesdict)

# you really wanna do something more useful with the data...

tab1, tab2, tab3 = st.tabs(["Tabla II-C", "Dog", "Owl"])

with tab1:

#    def form_callback(data1, data2):
#    with open('pages/notes.csv', 'a+') as f:    #Append & read mode
#        f.write(f"{data1},{data2}\n")
    
    st.write("TABLA II-B. IDENTIFICACIÓN DE OPERADORES Y/O ADMINISTRADORES DEL PLAN")

    col1, col2 = st.columns(2)
    with col1:
        nombre_input = st.text_input('Nombre')
        nacionalidad_input = st.selectbox('Nacionalidad', countrieslist, index=None, placeholder='Seleccione un país',accept_new_options=False)
        
        nit_input=st.number_input("NIT", value=None, placeholder=None)
        correo_input = st.text_input('Correo electrónico')
    with col2:
        telefono_input = st.text_input('Teléfono')
        direccion_input = st.text_input('Dirección física')
        
        citieslist = [k for k, v in citiesdict.items() if v == nacionalidad_input]
        citieslist.sort()
        
        ciudad_input = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False)
        observaciones_input = st.text_area('Obsevaciones')
    
    st.button('Registrar')


        



    st.info("Previsualización")
    st.dataframe(pd.read_csv("pages/notes.csv",names=["Stock","Note"],encoding='latin1'),height=300)
