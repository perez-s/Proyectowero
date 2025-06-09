import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from modules.nav import MenuButtons
import yaml
from yaml.loader import SafeLoader
import os
from datetime import datetime
from zipfile import ZipFile
import io

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

    st.title("Reportes")

    folder_path = 'informes'
    zip_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.zip'):
            file_path = os.path.join(folder_path, filename)
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            zip_files.append({'Reporte': filename, 'Fecha': file_date.strftime('%m/%d/%Y - %H:%M'), 'Descargar': False})

    dataset = pd.DataFrame(zip_files)

    @st.cache_data(show_spinner=False)
    def split_frame(input_df, rows):
        df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
        return df

    if not dataset.empty:

        top_menu = st.columns(3)
        with top_menu[0]:
            sort = st.radio("Ordenar tabla", options=["Si", "No"], horizontal=1, index=1)
        if sort == "Si":
            with top_menu[1]:
                sort_field = st.selectbox("Ordenar por", options=dataset.columns)
            with top_menu[2]:
                sort_direction = st.radio(
                    "Dirección", options=["⬆️", "⬇️"], horizontal=True
                )
            dataset = dataset.sort_values(
                by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
            )
        pagination = st.container()

        bottom_menu = st.columns((4, 1, 1))
        with bottom_menu[2]:
            batch_size = st.selectbox("Registros", options=[10, 25, 50, 100])
        with bottom_menu[1]:
            total_pages = (
                int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
            )
            if ( batch_size * total_pages ) < len(dataset):
                total_pages += 1
            page_numbers = list(range(1, total_pages + 1))
            current_page = st.selectbox(
                'Página', options=page_numbers, index=0, key="page_selector"
            )
        with bottom_menu[0]:
            st.markdown(f"Página **{current_page}** de **{total_pages}** ")

        pages = split_frame(dataset, batch_size) 
        
        result2 = pagination.data_editor(data=pages[current_page - 1], use_container_width=True, hide_index=False, disabled=('Reporte', 'Fecha'))
        selected_reports = result2[result2['Descargar'] == True]['Reporte'].tolist()

        def consolidate_informacion_transaccional_all(folder_path):
            consolidated_data = []
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.zip'):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        with ZipFile(file_path, 'r') as zipf:
                            for name in zipf.namelist():
                                if 'excel_validados/informacion_transaccional.xlsx' in name:
                                    with zipf.open(name) as xlsx_file:
                                        df = pd.read_excel(xlsx_file, skiprows=3)  # Skip first 4 rows
                                        consolidated_data.append(df)
            if consolidated_data:
                return pd.concat(consolidated_data, ignore_index=True)

        data_to_download = consolidate_informacion_transaccional_all(folder_path)
        
        if data_to_download is not None and not data_to_download.empty:
            st.download_button(
                label="Descargar información transaccional consolidada",
                data=data_to_download.to_csv(index=False).encode('latin1'),
                file_name="consolidado_informacion_transaccional.csv",
                mime="text/csv"
            )


    else:
        selected_reports = []
        st.error("No hay reportes disponibles.")

    if selected_reports:

        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zipf:
            for report in selected_reports:
                file_path = os.path.join(folder_path, report)
                if os.path.isfile(file_path):
                    zipf.write(file_path, arcname=report)
        zip_buffer.seek(0)
        st.download_button(
            label="Descargar seleccionados como ZIP",
            data=zip_buffer,
            file_name="reportes_seleccionados.zip",
            mime="application/zip"
        )

    st.divider()

    year_selector = st.selectbox(
        "Seleccionar año a reportar",
        options=[str(year) for year in range(2020, datetime.now().year + 1)],
        index=datetime.now().year - 2020
    )

    if st.button("Guardar año seleccionado"):
        with open('year.txt', 'w') as f:
            f.write(year_selector)
        st.toast(f"Año {year_selector} guardado correctamente.", icon="✅")



else:
    st.switch_page("./pages/Inicio.py")
