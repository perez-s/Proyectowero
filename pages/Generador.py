import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
import yaml
from yaml.loader import SafeLoader
import os
from datetime import datetime
from zipfile import ZipFile
import os
from dateutil.relativedelta import relativedelta
import time

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

    ############################# TEMPLATE #############################
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

    #################################################################

    st.title("Generador de Reportes Coca-Cola")

    with open("bd_cocacola.csv", "rb") as file:
                st.download_button(
                    label="Descargar BD de Coca-Cola",
                    data=file,
                    file_name="bd_cocacola.csv",
                    mime="text/csv",
                    key="download_button1",
                    use_container_width=True
                )

    def delete_file(file_path):
        time.sleep(10)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

    # Read the CSV file
    df = pd.read_csv('bd_cocacola.csv')

    # Get unique values from 'Fuente' column
    fuentes = df['Fuente'].unique().tolist()

    # Create a multiselect widget
    Clientes = st.selectbox('Selecciona los clientes para reportar:', fuentes)
    enddate = st.date_input("Fecha de corte", value='today')
    meses_a_reportar = st.number_input("Meses a reportar", min_value=1, max_value=12, value=12, step=1)
    startdate = enddate - relativedelta(months=meses_a_reportar)
    nodoc = st.text_input("Número del documento")
    obsevacion = st.text_area("Observaciones adicionales")
    obsevacion2 = repr(obsevacion).replace("'", '"')
    norecomendacion = st.checkbox("Sin recomendación", value=False, key="norecomendacion")
    recomendaciones = {
        "Recomendación rechazo": "Se ha observado una continuidad en la presencia de grandes cantidades de material no aprovechable o material de rechazo en los puntos de recolección. Entre estos residuos, se incluyen plásticos contaminados con grasas y restos orgánicos de las proteínas, restos de comida preparada y no preparada, servilletas de cocina y de mesa, así como una mezcla de materiales reciclables con no reciclables que afecta la calidad del material recuperable. Esta situación limita la eficiencia del proceso de reciclaje y representa un desafío significativo en la correcta segregación de residuos. \n\n",
        "Recomendación fortalecimiento": "Los puntos de recolección implementados como parte del piloto, junto con los retos inherentes a la separación en la fuente de los residuos sólidos, evidencian la necesidad urgente de reforzar las estrategias de educación y concientización. \n\n",
        "Recomendación acciones fuente": "Desde el área de sostenibilidad se han llevado a cabo diversas acciones de comunicación y capacitación a través de WERO, lo que ha favorecido una mayor apropiación por parte de los usuarios de las pautas de clasificación. Estos esfuerzos han resultado en una mejora en la separación de materiales reciclables y no reciclables. \n\n",
        "Recomendación fortalecimiento 2": "Para fortalecer la separación en la fuente en cada punto de venta de las distintas ciudades, se recomienda enfocar la estrategia en dos acciones clave- la creación de un concurso de reciclaje y la implementación de campañas de sensibilización. El concurso deberá premiar a los puntos de venta que demuestren un alto nivel de cumplimiento en la correcta separación de residuos, fomentando la motivación tanto entre los colaboradores como entre los consumidores para que se involucren activamente en la correcta separación en la fuente. \n\n",
        "Recomendación difusión": "Se sugiere  ampliar el alcance de las campañas de sensibilización, utilizando medios digitales para llegar tanto a los colaboradores como a los consumidores, a través de videos tutoriales y mensajes interactivos que refuercen la importancia de la separación de residuos y su impacto positivo en el ambiente. Esta combinación de incentivos y educación podrá contribuir a una mayor conciencia y participación en el proceso de segregación en la fuente. \n\n"
    }
    recomendacioneslist = st.multiselect("Selecciona una recomendación:", list(recomendaciones.keys()), placeholder="Escoge una o varias recomendaciones", disabled=norecomendacion)
    recomendacionadicional = st.text_area("Recomendación adicional", placeholder="Escribe una recomendación adicional aquí...", key="recomendacionadicional", disabled=norecomendacion)
    recomendacionfinal = "Para este periodo de informe proponemos las siguientes recomendaciones. \n\n"
    for i in range(len(recomendacioneslist)):
        recomendacionfinal = recomendacionfinal + f"{i+1}. {recomendaciones[recomendacioneslist[i]]}\n\n"
    recomendacionfinal2 = recomendacionfinal + f"{len(recomendacioneslist)+1}. {recomendacionadicional}\n\n"
    recomendacionfinal2 = repr(recomendacionfinal2).replace("'", '"')
    oganicosselect = st.selectbox("Reportar residuos orgánicos?", ["Si", "No"], index=1)

    if st.button("Generar Reporte", key="generate_report", use_container_width=True):
        with st.spinner(f"Generando reporte de {Clientes}...", show_time=True):
            if os.path.exists(f"{Clientes}.pdf"):
                os.remove(f"{Clientes}.pdf")
            if oganicosselect == "Si":
                os.system(f"quarto render reporte_organicos.qmd -P obs:{obsevacion2} -P rec:{recomendacionfinal2} -P nodoc:{nodoc} -P client:\"{Clientes}\" -P startdate:{startdate} -P enddate:{enddate} --output \"{Clientes}\".pdf")    
            else:
                os.system(f"quarto render reporte_base.qmd -P obs:{obsevacion2} -P rec:{recomendacionfinal2} -P nodoc:{nodoc} -P client:\"{Clientes}\" -P startdate:{startdate} -P enddate:{enddate} --output \"{Clientes}\".pdf")
            try:    
                with open(f"{Clientes}.pdf", "rb") as file:
                    st.download_button(
                        label="Descargar Reporte",
                        data=file,
                        file_name=f"{Clientes}.pdf",
                        mime="application/pdf",
                        key="download_report",
                        use_container_width=True,
                        type="primary",
                    )
            except:
                st.toast("Error al generar el reporte. Por favor, verifica los datos ingresados.", icon="🚨")
else:
    st.switch_page("./pages/Inicio.py")
