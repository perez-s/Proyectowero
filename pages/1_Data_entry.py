import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
from pages.account import get_roles
import geonamescache
import time
import pathlib
import shutil
import os
from pages.account import authenticator

directory = pathlib.Path("informes/admin")

timestr = time.strftime("%Y%m%d")
print(timestr) 

logo1 = 'Logo1.png'
logo2 = 'Logo2.png'
st.logo(logo2, icon_image=logo2, size='large')

if ss.get('authentication_status'):

    MenuButtons(get_roles())
    with st.sidebar:
        st.write(f'Bienvenido/a *{ss["name"]}*')
    authenticator.logout(button_name='Cerrar sesión', location='sidebar')

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


    tab1, tab2, tab3, tab4 = st.tabs(["TABLA II-B", "TABLA II-C", "INVERSIÓN DE RECURSOS ACTORES", 'CARGAR PDF'])

    with tab1:

        st.write("TABLA II-B. IDENTIFICACIÓN DE OPERADORES Y/O ADMINISTRADORES DEL PLAN")

        col1, col2 = st.columns(2)
        with col1:
            nombre_input = st.text_input('Nombre',key='nombre_input_key')
            nacionalidad_input = st.selectbox('Nacionalidad', countrieslist, index=None, placeholder='Seleccione un país',accept_new_options=False, key='nacionalidad_input_key')
            
            nit_input=st.number_input("NIT", value=None, placeholder=None, key='nit_input_key')
            correo_input = st.text_input('Correo electrónico', key='correo_input_key')
        with col2:
            telefono_input = st.number_input('Teléfono', placeholder=None, key='telefono_input_key', value=None)
            direccion_input = st.text_input('Dirección física', key='direccion_input_key')
            
            citieslist = [k for k, v in citiesdict.items() if v == nacionalidad_input]
            citieslist.sort()
            
            ciudad_input = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False, key='ciudad_input_key')
            observaciones_input = st.text_area('Obsevaciones', key='observaciones_input_key')

        col3, col4 = st.columns(2)
        with col3:
            col5, col6 = st.columns(2)        
            with col5:      
                if st.button('Añadir', type='secondary'):
                    with open('informes/admin/notes.csv', 'a+') as f:    #Append & read mode
                        f.write(f"{nombre_input},{nacionalidad_input},{nit_input},{correo_input},{telefono_input},{direccion_input},{ciudad_input},{observaciones_input}\n")
                    st.success('Registro añadido exitosamente')
            with col6:
                if st.button('Limpiar formato', type='tertiary'):
                    f = open('informes/admin/notes.csv', "w+")
                    f.close()
                    st.info('Formato limpiado exitosamente')


        st.info("Previsualización del formato")
        
        st.dataframe(pd.read_csv("informes/admin/notes.csv",names=["Nombre","Nacionalidad","NIT","Correo","Telefono","Dirección","Ciudad","Observaciones"],encoding='latin1'),height=300)

    with tab2:

        st.write("TABLA II-C. IDENTIFICACIÓN DE LOS ACTORES")

        col1, col2 = st.columns(2)
        with col1:
            razonsocial_input2 = st.text_input('Razón social')
            nit_input2=st.number_input("CC o NIT", value=None, placeholder=None, min_value=0)
            correo_input2 = st.text_input('Correo electrónico')
            telefono_input2 = st.number_input('Teléfono', value=None, placeholder=None)
            direccion_input2 = st.text_input('Dirección física')

            citieslist = [k for k, v in citiesdict.items() if v == 'Colombia']
            citieslist.sort()

            ciudad_input2 = st.selectbox("Ciudad", citieslist, index=None, placeholder='Seleccione una ciudad', accept_new_options=False)
            formaparticipacion_input2 = st.text_input('Forma de participación y responsabilidades (*)')
            numinvolucrados_input2 = st.number_input('Número de personas involucradas', value=None, placeholder=None, min_value=0, help='(personas asociadas y/o con vinculación laboral)')
            numacto_input2 = st.number_input('Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique', value=None, placeholder=None, min_value=0)

        with col2:
            ciudades_input2 = st.multiselect("Ciudades donde tienes cobertura normalmente en el año", citieslist, placeholder='Seleccione una ciudad o más', accept_new_options=False)
            capacidadtransporte_input2 = st.text_input('Capacidad de transporte y almacenamiento', disabled=True)
            logo_input2 = st.file_uploader('Logo en alta resolución', type=["jpg", "jpeg", "png"])
            procesotransformacion_input2 = st.text_input('Proceso de transformación de la ET')
            tipoproducto_input2 = st.text_input('Tipo de producto obtenido')
            destinofinal_input2 = st.selectbox("Destino final de producto obtenido", ['fabricante', 'productor', 'distribuidor', 'comercializador'], placeholder='Seleccione una opción', accept_new_options=False, index=None)
            captransformacion_input2 = st.number_input('Capacidad de transformación (ton/año)', value=None, placeholder=None, min_value=0)
            observaciones_input = st.text_area('Obsevaciones')
        
        col3, col4 = st.columns(2)
        with col3:
            col5, col6 = st.columns(2)        
            with col5:
                if st.button('Añadir', key='registrar2', type='secondary'):
                    if os.path.isdir('informes/admin/logos/') == False:
                        os.mkdir('informes/admin/logos')
                    
                    logopath=f'informes/admin/logos/{nit_input2}-logo'+f'.{pathlib.Path(logo_input2.name).suffix}'      
                    with open(logopath, mode='wb') as w:
                        w.write(logo_input2.getvalue())
                    with open('informes/admin/notes2.csv', 'a+') as f:    #Append & read mode
                        f.write(f"{razonsocial_input2};{nit_input2};{correo_input2};{telefono_input2};{direccion_input2};{ciudad_input2};{formaparticipacion_input2};{numinvolucrados_input2};{numacto_input2};{ciudades_input2};{'N/A'};{logopath};{procesotransformacion_input2};{tipoproducto_input2};{destinofinal_input2};{captransformacion_input2}\n")
                    st.success('Registro añadido exitosamente')

            with col6:
                if st.button('Limpiar formato', key='limpiar2', type='tertiary'):
                    f = open('informes/admin/notes2.csv', "w+")
                    f.close()
                    if os.path.isdir('informes/admin/logos/'):
                        shutil.rmtree('informes/admin/logos/')
                    st.info('Formato limpiado exitosamente')

        st.warning("(*) Forma de participación y responsabilidades: orientación de opciones por actor: \n"
        "- Gestores: Campañas de comunicación, recolección, mecanismos de recolección equivalentes, puntos de recolección, almacenamiento y transporte \n" \
        "- Empresas Transformadoras: Tipo de aprovechamiento, tipo de material de envases y empaques, campañas de comunicación, inversión en infraestructura y/o ecodiseño")
        
        st.info("Previsualización del formato")
        
        st.dataframe(pd.read_csv("informes/admin/notes2.csv",delimiter=';',names=["Razón social","CC o NIT","Correo electrónico","Teléfono","Dirección física","Ciudad","Forma de participación y responsabilidades","Número de personas involucradas (personas asociadas y/o con vinculación laboral)","Número de acto administrativo de las autorizaciones ambientales, permisos, concesiones cuando aplique","Ciudades donde tienes cobertura normalmente en el año","Capacidad de transporte y almacenamiento","Logo en alta resolución","Proceso de transformación de la ET","Tipo de producto obtenido","Destino final de producto obtenido","Capacidad de transformación (ton/año)"],encoding='latin1'),height=300)

    with tab3:

        st.write("INVERSIÓN DE RECURSOS ACTORES")

        col1, col2 = st.columns(2)
        with col1:
            acciones_input3 = st.text_input('Acciones adelantadas')
            objetivo_input3 = st.text_input('Objetivo')
            estrategia_input3 = st.text_area('Descripción de la estrategia')
            local_input3 = st.text_input('Localización geográfica')
            actores_input3 = st.text_input('Actores beneficiados', help=': gestores, recicladores, empresas transformadoras (personas naturales y/o empresas)')
        with col2:
            tipoinv_input3 = st.selectbox('Tipo de inversión', options=['Dinero','Especie'], index=None, placeholder= 'Seleccione una opción')
            if tipoinv_input3 == 'Dinero':
                tipoinvmod = 'D'
            elif tipoinv_input3 == 'Especie':
                tipoinvmod = 'E'
            else:
                tipoinvmod = ''
            valor_input3 = st.number_input("Valor recursos destinados ($ COP)", value=None, placeholder=None, min_value=0)
            actoresben_input3 = st.number_input("Número de actores beneficiados", value=None, placeholder=None, min_value=0)
            orgben_input3 = st.number_input("Cantidad de organizaciones beneficiadas", value=None, placeholder=None, min_value=0)
            soporte_input3 = st.file_uploader('Registro fotográfico soporte', type=["jpg", "jpeg", "png"])

        col3, col4 = st.columns(2)
        with col3:
            col5, col6 = st.columns(2)        
            with col5:
                logopath=''      
                if st.button('Añadir', key='registrar3', type='secondary'):
                    if os.path.isdir('informes/admin/fotos_registro/') == False:
                        os.mkdir('informes/admin/fotos_registro')
                    
                    fotospath=f'informes/admin/fotos_registro/{actores_input3}-foto'+f'.{pathlib.Path(soporte_input3.name).suffix}'      
                    with open(fotospath, mode='wb') as w:
                        w.write(soporte_input3.getvalue())
                    with open('informes/admin/notes3.csv', 'a+') as f:    #Append & read mode
                        f.write(f"{acciones_input3};{objetivo_input3};{estrategia_input3};{local_input3};{actores_input3};{tipoinvmod};{valor_input3};{actoresben_input3};{orgben_input3};{fotospath}\n")
                    st.success('Registro añadido exitosamente')
            with col6:
                if st.button('Limpiar', key='limpiar3', type='tertiary'):
                    f = open('informes/admin/notes3.csv', "w+")
                    f.close()
                    if os.path.isdir('informes/admin/fotos_registro/'):
                        shutil.rmtree('informes/admin/fotos_registro/')
                    st.info('Formato limpiado exitosamente')

        st.info("Previsualización del formato")
        
        st.dataframe(pd.read_csv("informes/admin/notes3.csv",delimiter=';',names=["Acciones adelantadas","Objetivo","Descripción de la estrategia","Localización geográfica","Actores beneficiados: gestores, recicladores empresas transformadoras (personas naturales y/o empresas)","Tipo de inversión (Dinero=D / Especie=E)","Valor recursos destinados ($ COP)","Número de actores beneficiados","Cantidad de organizaciones beneficiadas","Registro fotográfico soporte"], encoding='latin1'),height=300)

    with tab4:
        anexo4_input4 = st.file_uploader('Anexo IV. Inscripción de las empresas transformadoras', type='pdf')
        anexo5_input4 = st.file_uploader('Copia de los soportes anexados a la solicitud de inscripción de las empresas transformadoras ante la autoridad ambiental competente de su jurisdicción', type='pdf')
        anexo6_input4 = st.file_uploader('Copia de la respuesta de la CAR al radicado de inscripción como empresa transformadora', type='pdf')
        anexo7_input4 = st.file_uploader('Anexo I. Tabla I-a. Certificación de toneladas aprovechadas y contenido mínimo de material reciclado', type='pdf')
        metasypro_input4 = st.file_uploader('Informe de avance en el cumplimiento de metas y proyección', type='pdf')
        
        if st.button('Añadir', key='registrar4', type='secondary'):
            if os.path.isdir('informes/admin/anexos/') == False:
                os.mkdir('informes/admin/anexos')

            anexospath=f'informes/admin/anexos/anexo4'+f'.{pathlib.Path(anexo4_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo4_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo5'+f'.{pathlib.Path(anexo5_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo5_input4.getvalue())
            
            anexospath=f'informes/admin/anexos/anexo6'+f'.{pathlib.Path(anexo6_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo6_input4.getvalue())

            anexospath=f'informes/admin/anexos/anexo7'+f'.{pathlib.Path(anexo7_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(anexo7_input4.getvalue()) 
            
            anexospath=f'informes/admin/anexos/anexo8'+f'.{pathlib.Path(metasypro_input4.name).suffix}'      
            with open(anexospath, mode='wb') as w:
                        w.write(metasypro_input4.getvalue()) 
            
        if st.button('Limpiar anexos', key='limpiar4', type='tertiary'):
            if os.path.isdir('informes/admin/anexos/'):
                shutil.rmtree('informes/admin/anexos/')
            st.info('Anexos limpiados exitosamente')



    st.divider()

    if st.button('Enviar', key='enviar', type='primary'):
        shutil.make_archive(f'informes/admin/reporte_{timestr}', 'zip', directory)
        # with zipfile.ZipFile(f"{timestr}-directory.zip", mode="w") as archive:
        #     for file_path in directory.iterdir():
        #          archive.write(file_path)
        st.success('Reporte generado exitosamente')
else:
    st.switch_page('./pages/account.py')

