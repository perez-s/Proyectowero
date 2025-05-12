import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
# from pages.Inicio import get_roles, authenticator
import geonamescache
import pathlib
import shutil
import os
import re
import time
import yaml
from yaml.loader import SafeLoader

steps = 0

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

if "uploader_key2" not in st.session_state:
    st.session_state.uploader_key2 = 0

if "uploader_key3" not in st.session_state:
    st.session_state.uploader_key3 = 0

if "uploader_key4" not in st.session_state:
    st.session_state.uploader_key4 = 0



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
    # authenticator.logout(button_name='Cerrar sesión', location='sidebar', use_container_width=True)

    #################################       Country and City lists      ###################################################

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

    ####################################################################################################
    def validate_name(name):
        # Check if name is empty or None
        if not name or name.isspace():
            return "El nombre no puede estar vacío"
        
        # Remove leading/trailing spaces
        name = name.strip()
        
        # Check if name contains only letters and spaces
        if not all(char.isalpha() or char.isspace() for char in name):
            return " debe contener solo letras y espacios"
        
        # Check for multiple consecutive spaces
        if "  " in name:
            return " no puede contener espacios múltiples"
        
        # Check minimum length (e.g., 2 characters)
        if len(name) < 2:
            return " debe tener al menos 2 caracteres"
        
        # Check maximum length (e.g., 50 characters)
        if len(name) > 50:
            return " no puede exceder los 50 caracteres"
        
        # If all validations pass
        return None

    def validate_email(email):
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if valid:
            return None
        return "Ingresa un correo valido."
    
    def validate_number(number):
        if not number.isdigit():
            return "Ingresa un valor numerico."
    
    def validate_phone(phone):
        # Check if phone is empty or None
        if not phone or phone is None:
            return " teléfono no puede estar vacío"
        
        # Convert to string if it's a number
        phone = str(phone)
        
        # Remove any spaces
        phone = phone.strip()
        
        # Check if it contains only digits
        if not phone.isdigit():
            return " debe contener solo dígitos"
        
        # Check length (only 7 or 10 digits allowed)
        length = len(phone)
        if length != 7 and length != 10:
            return " debe tener 7 dígitos (fijo) o 10 dígitos (celular)"
        
        # If all validations pass
        return None

    def validate_none(element):
        if element == None:
            return "Campo obligtorio."
        return None

    def validate_empty(element):
        if element == '':
            return "Ingresa un valor valido."
        return None

    def validate_form1(a, b, c, d, e, f, g, h):
        errors = []
        
        # Validate each field
        a_error = validate_name(a)
        if a_error:
            errors.append('Nombre: ' + a_error)
        
        b_error = validate_none(b)
        if b_error:
            errors.append('Nacionalidad: ' + b_error)
        
        c_error = validate_none(c)
        if c_error:
            errors.append('NIT: ' +c_error)
        
        d_error = validate_email(d)
        if d_error:
            errors.append('Correo electrónico: ' + d_error)

        e_error = validate_phone(e)
        if e_error:
            errors.append('Teléfono: ' + e_error)

        f_error = validate_empty(f)
        if f_error:
            errors.append('Dirección: ' + f_error)

        g_error = validate_none(g)
        if g_error:
            errors.append('Ciudad: ' + g_error)

        h_error = validate_empty(h)
        if h_error:
            errors.append('Observaciones: ' + h_error)
        
        # If there are errors, return them
        if errors:
            return errors

        return True

    def validate_form2(razon_social, nit, correo, telefono, direccion, ciudad, forma_participacion, num_involucrados, num_acto, ciudades, logo, proceso, tipo_producto, destino_final, cap_transformacion):
        errors = []
        
        # Validate business name
        razon_error = validate_empty(razon_social)
        if razon_error:
            errors.append('Razón social: ' + razon_error)
        
        # Validate NIT
        nit_error = validate_none(nit)
        if nit_error:
            errors.append('CC o NIT: ' + nit_error)
        
        # Validate email
        correo_error = validate_email(correo)
        if correo_error:
            errors.append('Correo electrónico: ' + correo_error)

        # Validate phone
        telefono_error = validate_phone(telefono)
        if telefono_error:
            errors.append('Teléfono: ' + telefono_error)

        # Validate address
        direccion_error = validate_empty(direccion)
        if direccion_error:
            errors.append('Dirección: ' + direccion_error)

        # Validate city
        ciudad_error = validate_none(ciudad)
        if ciudad_error:
            errors.append('Ciudad: ' + ciudad_error)
            
        # Validate participation form
        forma_error = validate_empty(forma_participacion)
        if forma_error:
            errors.append('Forma de participación: ' + forma_error)
            
        # Validate number of people involved
        num_inv_error = validate_none(num_involucrados)
        if num_inv_error:
            errors.append('Número de personas involucradas: ' + num_inv_error)
            
        # Validate administrative act number
        num_acto_error = validate_none(num_acto)
        if num_acto_error:
            errors.append('Número de acto administrativo: ' + num_acto_error)
            
        # Validate cities coverage
        if not ciudades:
            errors.append('Ciudades de cobertura: Debe seleccionar al menos una ciudad')

        # Validate logo upload
        logo_error = validate_none(logo)
        if logo_error:
            errors.append('Logo:'+ logo_error)          

        # Validate transformation process
        proceso_error = validate_empty(proceso)
        if proceso_error:
            errors.append('Proceso de transformación: ' + proceso_error)
            
        # Validate product type
        tipo_error = validate_empty(tipo_producto)
        if tipo_error:
            errors.append('Tipo de producto: ' + tipo_error)
            
        # Validate final destination
        destino_error = validate_none(destino_final)
        if destino_error:
            errors.append('Destino final: ' + destino_error)
            
        # Validate transformation capacity
        cap_error = validate_none(cap_transformacion)
        if cap_error:
            errors.append('Capacidad de transformación: ' + cap_error)
            
        # If there are errors, return them
        if errors:
            return errors

        return True

    def validate_form3(razon_social, nit, correo, telefono, direccion, ciudad, forma_participacion, num_involucrados, num_acto, ciudades, cap_transporte, logo):
        errors = []
        
        # Validate business name
        razon_error = validate_empty(razon_social)
        if razon_error:
            errors.append('Razón social: ' + razon_error)
        
        # Validate NIT
        nit_error = validate_none(nit)
        if nit_error:
            errors.append('CC o NIT: ' + nit_error)
        
        # Validate email
        correo_error = validate_email(correo)
        if correo_error:
            errors.append('Correo electrónico: ' + correo_error)

        # Validate phone
        telefono_error = validate_phone(telefono)
        if telefono_error:
            errors.append('Teléfono: ' + telefono_error)

        # Validate address
        direccion_error = validate_empty(direccion)
        if direccion_error:
            errors.append('Dirección: ' + direccion_error)

        # Validate city
        ciudad_error = validate_none(ciudad)
        if ciudad_error:
            errors.append('Ciudad: ' + ciudad_error)
            
        # Validate participation form
        forma_error = validate_empty(forma_participacion)
        if forma_error:
            errors.append('Forma de participación: ' + forma_error)
            
        # Validate number of people involved
        num_inv_error = validate_none(num_involucrados)
        if num_inv_error:
            errors.append('Número de personas involucradas: ' + num_inv_error)
            
        # Validate administrative act number
        num_acto_error = validate_none(num_acto)
        if num_acto_error:
            errors.append('Número de acto administrativo: ' + num_acto_error)
            
        # Validate cities coverage
        if ciudades == 0:
            errors.append('Ciudades de cobertura: Debe seleccionar al menos una ciudad')

        cap_transporte_error = validate_empty(cap_transporte)
        if cap_transporte_error:
            errors.append('Capacidad de transporte: ' + cap_transporte_error)

        # Validate logo upload
        logo_error = validate_none(logo)
        if logo_error:
            errors.append('Logo:'+ logo_error)          
            
        # If there are errors, return them
        if errors:
            return errors

        return True

    def validate_form4(anexo4, anexo5, anexo6, anexo7, anexo8, anexo9, anexo10, metasypro):
        errors = []

        # Validate NIT
        anexo4_error = validate_none(anexo4)
        if anexo4_error:
            errors.append('Anexo 1: ' + anexo4_error)

        anexo5_error = validate_none(anexo5)
        if anexo5_error:
            errors.append('Anexo 2: ' + anexo5_error)

        anexo6_error = validate_none(anexo6)
        if anexo6_error:
            errors.append('Anexo 3: ' + anexo6_error)

        anexo7_error = validate_none(anexo7)
        if anexo7_error:
            errors.append('Anexo 4: ' + anexo7_error)
        
        anexo8_error = validate_none(anexo8)
        if anexo8_error:
            errors.append('Anexo 5: ' + anexo8_error)

        anexo9_error = validate_none(anexo9)
        if anexo9_error:
            errors.append('Anexo 6: ' + anexo9_error)
        
        anexo10_error = validate_none(anexo10)
        if anexo10_error:
            errors.append('Anexo 7: ' + anexo10_error)
        
        metasypro_error = validate_none(metasypro)
        if metasypro_error:
            errors.append('Anexo 8: ' + metasypro_error)
        
        if errors:
            return errors

        return True
    ####################################################################################################


    tab1, tab2, tab4 = st.tabs(["Operadores del Plan", "Actores", 'Soportes'])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            nombre_input = st.text_input('Nombre',key='nombre_input_key')
            nacionalidad_input = st.selectbox('Nacionalidad', countrieslist, index=None, placeholder='Seleccione un país',accept_new_options=False, key='nacionalidad_input_key')
            nit_input=st.number_input("NIT", value=None, placeholder=None, key='nit_input_key', step=1)
            correo_input = st.text_input('Correo electrónico', key='correo_input_key')
        with col2:  
            telefono_input = st.number_input('Teléfono', placeholder=None, key='telefono_input_key', value=None, step=1)
            direccion_input = st.text_input('Dirección física', key='direccion_input_key')
            
            citieslist = [k for k, v in citiesdict.items() if v == nacionalidad_input]
            citieslist.sort()
            
            ciudad_input = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False, key='ciudad_input_key')

            observaciones_input = st.text_area('Obsevaciones', key='observaciones_input_key')

        # col3, col4 = st.columns(2)
        # with col3:
            # col5, col6 = st.columns(2)        
            # with col5:
        validcheck=validate_form1(nombre_input,nacionalidad_input,nit_input,correo_input,telefono_input,direccion_input,ciudad_input,observaciones_input)  
        def on_click():
                with open('informes/admin/notes.csv', 'a+') as f:    #Append & read mode
                    f.write(f"{nombre_input},{nacionalidad_input},{nit_input},{correo_input},{telefono_input},{direccion_input},{ciudad_input},{observaciones_input}\n")
                    st.toast('Registro añadido exitosamente', icon='✅')  

                st.session_state.nombre_input_key = ""
                st.session_state.nacionalidad_input_key = None
                st.session_state.nit_input_key = None
                st.session_state.correo_input_key = ""
                st.session_state.telefono_input_key = None
                st.session_state.direccion_input_key = ""
                st.session_state.ciudad_input_key = None
                st.session_state.observaciones_input_key = ''

        if validcheck != True:
            if st.button('Añadir', type='secondary', key='añadirfalse'):
                s = ''
                for i in validcheck:
                    st.toast(i, icon='⚠️')
                #     s += "-" + i + "  \n"
                # st.error(s)

        elif validcheck == True:
                st.button('Añadir', type='secondary', on_click=on_click, key='añadirtrue')
        if st.button('Limpiar formato', type='tertiary'):
            f = open('informes/admin/notes.csv', "w+")
            f.close()
            st.toast('Formato limpiado exitosamente', icon='ℹ️')


        st.info("Previsualización del formato")
        
        st.dataframe(pd.read_csv("informes/admin/notes.csv",names=["Nombre","Nacionalidad","NIT","Correo","Telefono","Dirección","Ciudad","Observaciones"],encoding='latin1'),height=300)

    with tab2:
        tab1, tab2 = st.tabs(["Transformadores", "Gestores"])
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                razonsocial_input2 = st.text_input('Razón social', key='razonsocial_input2')
                nit_input2=st.number_input("CC o NIT", value=None, placeholder=None, min_value=0, step=1, key='nit_input2')
                correo_input2 = st.text_input('Correo electrónico', key='correo_input2')
                telefono_input2 = st.number_input('Teléfono', value=None, placeholder=None, step=1, key='telefono_input2')
                direccion_input2 = st.text_input('Dirección física', key='direccion_input2')
                citieslist = [k for k, v in citiesdict.items() if v == 'Colombia']
                citieslist.sort()
                ciudad_input2 = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False, key='ciudad_input2')
                formaparticipacion_input2 = st.text_input('Forma de participación y responsabilidades (*)', key='formaparticipacion_input2')
                numinvolucrados_input2 = st.number_input('Número de personas involucradas', value=None, placeholder=None, min_value=0, help='(personas asociadas y/o con vinculación laboral)', step=1, key='numinvolucrados_input2')
                numacto_input2 = st.number_input('Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique', value=None, placeholder=None, min_value=0, step=1, key='numacto_input2')

            with col2:
                ciudades_input2 = st.multiselect("Ciudades donde tienes cobertura normalmente en el año", citieslist, placeholder='Seleccione una ciudad o más', accept_new_options=False, key='ciudades_input2')
                capacidadtransporte_input2 = st.text_input('Capacidad de transporte y almacenamiento', disabled=True, key='capacidadtransporte_input2')
                logo_input2 = st.file_uploader('Logo en alta resolución', type=["jpg", "jpeg", "png"], key=f"uploader_{st.session_state.uploader_key2}")
                procesotransformacion_input2 = st.text_input('Proceso de transformación de la ET', key='procesotransformacion_input2')
                tipoproducto_input2 = st.text_input('Tipo de producto obtenido', key='tipoproducto_input2')
                destinofinal_input2 = st.selectbox("Destino final de producto obtenido", ['fabricante', 'productor', 'distribuidor', 'comercializador'], placeholder='Seleccione una opción', accept_new_options=False, index=None, key='destinofinal_input2')
                captransformacion_input2 = st.number_input('Capacidad de transformación (ton/año)', value=None, placeholder=None, min_value=0, step=1, key='captransformacion_input2')

            validcheck=validate_form2(razonsocial_input2,nit_input2,correo_input2,telefono_input2,direccion_input2,ciudad_input2,formaparticipacion_input2,numinvolucrados_input2,numacto_input2,ciudades_input2,logo_input2,procesotransformacion_input2,tipoproducto_input2,destinofinal_input2,captransformacion_input2)  
            def on_click2():
                if os.path.isdir('informes/admin/logos_transformadores/') == False:
                    os.mkdir('informes/admin/logos_transformadores')
                logopath=f'informes/admin/logos_transformadores/{nit_input2}-logo'+f'.{pathlib.Path(logo_input2.name).suffix}'      
                with open(logopath, mode='wb') as w:
                    w.write(logo_input2.getvalue())

                with open('informes/admin/notes2.csv', 'a+') as f:    #Append & read mode
                    f.write(f"{razonsocial_input2};{nit_input2};{correo_input2};{telefono_input2};{direccion_input2};{ciudad_input2};{formaparticipacion_input2};{numinvolucrados_input2};{numacto_input2};{ciudades_input2};{'N/A'};{logopath};{procesotransformacion_input2};{tipoproducto_input2};{destinofinal_input2};{captransformacion_input2}\n")
                    st.toast('Registro añadido exitosamente', icon='✅')  
                st.session_state.razonsocial_input2 = ""
                st.session_state.nit_input2 = None 
                st.session_state.correo_input2 = ""
                st.session_state.telefono_input2 = None
                st.session_state.direccion_input2 = ""
                st.session_state.ciudad_input2 = None
                st.session_state.formaparticipacion_input2 = ""
                st.session_state.numinvolucrados_input2 = None
                st.session_state.numacto_input2 = None
                st.session_state.ciudades_input2 = []
                st.session_state.procesotransformacion_input2 = ""
                st.session_state.tipoproducto_input2 = ""
                st.session_state.destinofinal_input2 = None
                st.session_state.captransformacion_input2 = None
                st.session_state.uploader_key2 += 1

                    
            if validcheck != True:
                if st.button('Añadir', type='secondary', key='añadirfalse2'):
                    s = ''
                    for i in validcheck:
                        st.toast(i, icon='⚠️')
                    #     s += "-" + i + "  \n"
                    # st.error(s)

            elif validcheck == True:
                st.button('Añadir', type='secondary', on_click=on_click2, key='añadirtrue2')

            if st.button('Limpiar formato', key='limpiar2', type='tertiary'):
                f = open('informes/admin/notes2.csv', "w+")
                f.close()
                if os.path.isdir('informes/admin/logos_transformadores/'):
                    shutil.rmtree('informes/admin/logos_transformadores/')
                st.toast('Formato limpiado exitosamente', icon='ℹ️')
                    
            st.warning("(*) Forma de participación y responsabilidades: orientación de opciones por actor: \n"
            "- Gestores: Campañas de comunicación, recolección, mecanismos de recolección equivalentes, puntos de recolección, almacenamiento y transporte \n" \
            "- Empresas Transformadoras: Tipo de aprovechamiento, tipo de material de envases y empaques, campañas de comunicación, inversión en infraestructura y/o ecodiseño")
                        
            st.info("Previsualización del formato")
            
            st.dataframe(pd.read_csv("informes/admin/notes2.csv",delimiter=';',names=["Razón social","CC o NIT","Correo electrónico","Teléfono","Dirección física","Ciudad","Forma de participación y responsabilidades","Número de personas involucradas (personas asociadas y/o con vinculación laboral)","Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique","Ciudades donde tienes cobertura normalmente en el año","Capacidad de transporte y almacenamiento","Logo en alta resolución","Proceso de transformación de la ET","Tipo de producto obtenido","Destino final de producto obtenido","Capacidad de transformación (ton/año)"],encoding='latin1'),height=300)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                razonsocial_input3 = st.text_input('Razón social', key='razonsocial_input3')
                nit_input3=st.number_input("CC o NIT", value=None, placeholder=None, min_value=0, step=1, key='nit_input3')
                correo_input3 = st.text_input('Correo electrónico', key='correo_input3')
                telefono_input3 = st.number_input('Teléfono', value=None, placeholder=None, step=1, key='telefono_input3')
                direccion_input3 = st.text_input('Dirección física', key='direccion_input3')
                citieslist = [k for k, v in citiesdict.items() if v == 'Colombia']
                citieslist.sort()
                ciudad_input3 = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False, key='ciudad_input3')
                formaparticipacion_input3 = st.text_input('Forma de participación y responsabilidades (*)', key='formaparticipacion_input3')
                numinvolucrados_input3 = st.number_input('Número de personas involucradas', value=None, placeholder=None, min_value=0, help='(personas asociadas y/o con vinculación laboral)', step=1, key='numinvolucrados_input3')
                numacto_input3 = st.number_input('Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique', value=None, placeholder=None, min_value=0, step=1, key='numacto_input3')

            with col2:
                ciudades_input3 = st.multiselect("Ciudades donde tienes cobertura normalmente en el año", citieslist, placeholder='Seleccione una ciudad o más', accept_new_options=False, key='ciudades_input3')
                capacidadtransporte_input3 = st.text_input('Capacidad de transporte y almacenamiento', disabled=False, key='capacidadtransporte_input3')
                logo_input3 = st.file_uploader('Logo en alta resolución', type=["jpg", "jpeg", "png"], key=f"uploader9_{st.session_state.uploader_key3}")
                procesotransformacion_input3 = st.text_input('Proceso de transformación de la ET', key='procesotransformacion_input3', disabled=True)
                tipoproducto_input3 = st.text_input('Tipo de producto obtenido', key='tipoproducto_input3', disabled=True)
                destinofinal_input3 = st.selectbox("Destino final de producto obtenido", ['fabricante', 'productor', 'distribuidor', 'comercializador'], placeholder='Seleccione una opción', accept_new_options=False, index=None, key='destinofinal_input3', disabled=True)
                captransformacion_input3 = st.number_input('Capacidad de transformación (ton/año)', value=None, placeholder=None, min_value=0, step=1, key='captransformacion_input3', disabled=True)

            validcheck=validate_form3(razonsocial_input3,nit_input3,correo_input3,telefono_input3,direccion_input3,ciudad_input3,formaparticipacion_input3,numinvolucrados_input3,numacto_input3,len(ciudades_input3),capacidadtransporte_input3,logo_input3)  
            def on_click3():
                if os.path.isdir('informes/admin/logos_gestores/') == False:
                    os.mkdir('informes/admin/logos_gestores')
                logopath=f'informes/admin/logos_gestores/{nit_input3}-logo'+f'.{pathlib.Path(logo_input3.name).suffix}'      
                with open(logopath, mode='wb') as w:
                    w.write(logo_input3.getvalue())

                with open('informes/admin/notes3.csv', 'a+') as f:    #Append & read mode
                    f.write(f"{razonsocial_input3};{nit_input3};{correo_input3};{telefono_input3};{direccion_input3};{ciudad_input3};{formaparticipacion_input3};{numinvolucrados_input3};{numacto_input3};{ciudades_input3};{capacidadtransporte_input3};{logopath};{'N/A'};{'N/A'};{'N/A'};{'N/A'}\n")
                    st.toast('Registro añadido exitosamente', icon='✅')  
                st.session_state.razonsocial_input3 = ""
                st.session_state.nit_input3 = None 
                st.session_state.correo_input3 = ""
                st.session_state.telefono_input3 = None
                st.session_state.direccion_input3 = ""
                st.session_state.ciudad_input3 = None
                st.session_state.formaparticipacion_input3 = ""
                st.session_state.numinvolucrados_input3 = None
                st.session_state.numacto_input3 = None
                st.session_state.ciudades_input3 = []
                st.session_state.capacidadtransporte_input3 = ""
                st.session_state.uploader_key3 += 1
                
                    
            if validcheck != True:
                if st.button('Añadir', type='secondary', key='añadirfalse3'):
                    s = ''
                    for i in validcheck:
                        st.toast(i, icon='⚠️')
                    #     s += "-" + i + "  \n"
                    # st.error(s)

            elif validcheck == True:
                st.button('Añadir', type='secondary', on_click=on_click3, key='añadirtrue3')

            if st.button('Limpiar formato', key='limpiar3', type='tertiary'):
                f = open('informes/admin/notes3.csv', "w+")
                f.close()
                if os.path.isdir('informes/admin/logos_gestores/'):
                    shutil.rmtree('informes/admin/logos_gestores/')
                st.toast('Formato limpiado exitosamente', icon='ℹ️')
                    
            st.warning("(*) Forma de participación y responsabilidades: orientación de opciones por actor: \n"
            "- Gestores: Campañas de comunicación, recolección, mecanismos de recolección equivalentes, puntos de recolección, almacenamiento y transporte \n" \
            "- Empresas Transformadoras: Tipo de aprovechamiento, tipo de material de envases y empaques, campañas de comunicación, inversión en infraestructura y/o ecodiseño")

            st.warning("(**) Tipos de Gestores: \n"
                "1. Asosicaciones de recicladores en proceso de formalización como prestadores del servicio público de aseo en la actividad de aprovechamiento \n"
                "2. Asociaciones de recicladores formalizadas \n"
                "3, Empresas únicamente que compran y venden materiales (\"intermediarios\") \n"
                "4. Empresas de servicios públicos de aseo en la actividad de aprovechamiento \n"
                "5. Otras entidades solidarias como ONG´S, fundaciones que canjean residuos por bienes y/o servicios \n"
                )

            st.info("Previsualización del formato")
            
            st.dataframe(pd.read_csv("informes/admin/notes3.csv",delimiter=';',names=["Razón social","CC o NIT","Correo electrónico","Teléfono","Dirección física","Ciudad","Forma de participación y responsabilidades","Número de personas involucradas (personas asociadas y/o con vinculación laboral)","Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique","Ciudades donde tienes cobertura normalmente en el año","Capacidad de transporte y almacenamiento","Logo en alta resolución","Proceso de transformación de la ET","Tipo de producto obtenido","Destino final de producto obtenido","Capacidad de transformación (ton/año)"],encoding='latin1'),height=300)

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            anexo4_input4 = st.file_uploader('Anexo 1: Inscripción de las empresas transformadoras', type='pdf', key=f"uploader1_{st.session_state.uploader_key4}")
            anexo5_input4 = st.file_uploader('Anexo 2: Copia de los soportes anexados a la solicitud de inscripción de las empresas transformadoras ante la autoridad ambiental competente de su jurisdicción', type='pdf', key=f"uploader2_{st.session_state.uploader_key4}")
            anexo6_input4 = st.file_uploader('Anexo 3: Copia de la respuesta de la CAR al radicado de inscripción como empresa transformadora', type='pdf', key=f"uploader3_{st.session_state.uploader_key4}")
            anexo7_input4 = st.file_uploader('Anexo 4: Tabla I-a. Certificación de toneladas aprovechadas y contenido mínimo de material reciclado', type='pdf', key=f"uploader4_{st.session_state.uploader_key4}")
        with col2:
            anexo8_input4 = st.file_uploader('Anexo 5: Tabla I-b. Certificación de toneladas recolectadas', type='pdf', key=f"uploader5_{st.session_state.uploader_key4}")
            anexo9_input4 = st.file_uploader('Anexo 6: Copia de las facturas mediante las cuales se realizó la venta a la empresa transformadora, que demuestre la transacción comercial', type='pdf', key=f"uploader6_{st.session_state.uploader_key4}")
            anexo10_input4 = st.file_uploader('Anexo 7: Informe mecanismos equivalentes gestores - ASOCAÑA', type='pdf', key=f"uploader7_{st.session_state.uploader_key4}")
            metasypro_input4 = st.file_uploader('Anexo 8: Informe de avance en el cumplimiento de metas y proyección', type='pdf', key=f"uploader8_{st.session_state.uploader_key4}")

        validcheck=validate_form4(anexo4_input4,anexo5_input4,anexo6_input4,anexo7_input4,anexo8_input4,anexo9_input4,anexo10_input4,metasypro_input4)

        def on_click4():
            if os.path.isdir('informes/admin/anexos/') == False:
                os.mkdir('informes/admin/anexos')

            anexospath=f'informes/admin/anexos/anexo1'+f'.{pathlib.Path(anexo4_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo4_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo2'+f'.{pathlib.Path(anexo5_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo5_input4.getvalue())
            
            anexospath=f'informes/admin/anexos/anexo3'+f'.{pathlib.Path(anexo6_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo6_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo4'+f'.{pathlib.Path(anexo7_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo7_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo5'+f'.{pathlib.Path(anexo8_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo8_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo6'+f'.{pathlib.Path(anexo9_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo9_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo7'+f'.{pathlib.Path(anexo10_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo10_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo8'+f'.{pathlib.Path(metasypro_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(metasypro_input4.getvalue())
            
            st.session_state.uploader_key4 += 1

            st.toast('Anexos añadidos exitosamente', icon='✅')
             

        if validcheck != True:
            if st.button('Añadir', type='secondary', key='añadirfalse4'):
                s = ''
                for i in validcheck:
                    st.toast(i, icon='⚠️')
                #     s += "-" + i + "  \n"
                # st.error(s)
        
        elif validcheck == True:
            st.button('Añadir', type='secondary', key='añadirtrue4', on_click=on_click4)
        
            
        if st.button('Limpiar anexos', key='limpiar4', type='tertiary'):
            if os.path.isdir('informes/admin/anexos/'):
                shutil.rmtree('informes/admin/anexos/')
            st.info('Anexos limpiados exitosamente')

    st.divider()

    @st.dialog('Confirmar')
    def dialog():
        st.write('¿Estas seguro que deseas enviar el reporte?')
        st.write('Recuerda que una vez enviado no podrás editar el formato.')
        if st.button('Enviar', key='enviar', type='primary'):
            timestr = time.strftime("%Y-%m-%d")
            shutil.make_archive(f'informes/reporte_{timestr}', 'zip', './informes/admin')
            f = open('informes/admin/notes.csv', "w+")
            f.close()
            f = open('informes/admin/notes2.csv', "w+")
            f.close()
            f = open('informes/admin/notes3.csv', "w+")
            f.close()
            st.rerun()
            if os.path.isdir('informes/admin/anexos/'):
                shutil.rmtree('informes/admin/anexos/')

            st.success(f'Reporte {timestr} generado exitosamente')
    if "vote" not in st.session_state:
        if st.button("Enviar reporte", type='primary', key='enviar_reporte'):
            dialog()
    
else:
    st.switch_page("./pages/Inicio.py")
