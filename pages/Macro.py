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

    #################################       TEMPLATE       ###################################################
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

    ####################################################################################################
    df = pd.read_csv('bd_cocacola.csv')

    
    
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
        # First define specific validation functions
    
    def validate_index(value):
        """Valida que el índice sea un número entero positivo"""
        try:
            if pd.isna(value):
                return False
            return float(value).is_integer() and float(value) > 0
        except:
            return False
    
    def validate_date_yeartxt(value):
        """Valida que la fecha esté en formato dd/MM/DD y sea del año especificado en year.YYYYt"""
        try:
            # Leer el año desde year.txt
            with open('year.txt', 'r') as f:
                valid_year = int(f.read().strip())
            if pd.isna(value):
                return False
            if isinstance(value, datetime):
                return value.year == valid_year
            if isinstance(value, str):
                dt = datetime.strptime(value, '%d/%m/%Y')
                return dt.year == valid_year
            return False
        except:
            return False

    def validate_invoice(value):
        """Valida que el número de factura sea alfanumérico y permita símbolos"""
        try:
            if pd.isna(value):
                return False
            return len(str(value).strip()) > 0
        except:
            return False

    # Lista de materiales válidos
    VALID_MATERIALS = [
        'Papel', 'Cartón', 'Vidrio', 'Metales Ferrosos', 
        'Metales No Ferrosos', 'Multimaterial', 'Plástico PET', 
        'Plástico PEAD', 'Plástico PVC', 'Plástico PEBD', 
        'Plástico PP', 'Plástico PS', 'Otros plásticos'
    ]

    def validate_material(value):
        """Valida el tipo de material contra la lista permitida"""
        try:
            if pd.isna(value):
                return False
            return str(value).strip() in VALID_MATERIALS
        except:
            return False

    VALID_CONDITIONS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'NO APLICA']

    def validate_conditions(value):
        """Valida las condiciones contra la lista permitida"""
        try:
            if pd.isna(value):
                return False
            return str(value).strip() in VALID_CONDITIONS
        except:
            return False

    def validate_quantity(value):
        """Valida que la cantidad sea un número positivo"""
        try:
            if pd.isna(value):
                return False
            return float(value) > 0
        except:
            return False

    def validate_company_name(value):
        """Valida el formato del nombre de la empresa"""
        try:
            if pd.isna(value):
                return False
            # Elimina espacios al inicio/final y verifica espacios múltiples
            cleaned = ' '.join(str(value).strip().split())
            # Verifica que contenga al menos una letra
            has_letter = any(c.isalpha() for c in cleaned)
            return has_letter and '  ' not in cleaned
        except:
            return False

    def validate_municipality(value):
        """Valida el nombre del municipio (solo letras, no vacío)"""
        try:
            if pd.isna(value):
                return False
            # Elimina espacios y verifica que los caracteres sean letras
            cleaned = str(value).strip()
            return bool(cleaned) and all(c.isalpha() or c.isspace() for c in cleaned)
        except:
            return False

    def validate_municipality_category(value):
        """Valida la categoría del municipio (1-6 o ESP)"""
        VALID_CATEGORIES = [1, 2, 3, 4, 5, 6, 'ESP']
        try:
            if pd.isna(value):
                return False
            # Permite entradas tipo string o numéricas
            if isinstance(value, str):
                return value.strip().upper() == 'ESP'
            return int(value) in VALID_CATEGORIES
        except:
            return False

    def validate_mechanism_count(value):
        """Valida el número de mecanismos equivalentes (entero positivo)"""
        try:
            if pd.isna(value):
                return False
            num = float(value)
            return num.is_integer() and num > 0
        except:
            return False

    def validate_collected_material(value):
        """Valida la cantidad total de material recolectado (número positivo)"""
        try:
            if pd.isna(value):
                return False
            return float(value) > 0
        except:
            return False

    # Create validators dictionary
    municipal_validators = {
        'Municipio': validate_municipality,
        'Categoria del municipio': validate_municipality_category,
        'Número de mecanismos equivalentes': validate_mechanism_count,
        'Cantidad total de material recolectado (ton)': validate_collected_material
    }   

    def validate_form1(a, b, c, d, e, f, g):
        errors = []  
        
        # Validate each field
        a_error = validate_none(a)
        if a_error:
            errors.append('Usuario: ' + a_error)
        
        b_error = validate_none(b)
        if b_error:
            errors.append('Etapa: ' + b_error)
        
        c_error = validate_none(c)
        if c_error:
            errors.append('Fuente: ' +c_error)
        
        d_error = validate_none(d)
        if d_error:
            errors.append('Ciudad: ' + d_error)

        e_error = validate_none(e)
        if e_error:
            errors.append('Sucursal: ' + e_error)

        f_error = validate_none(f)
        if f_error:
            errors.append('Fecha: ' + f_error)

        g_error = validate_none(g)
        if g_error:
            errors.append('Gestor: ' + g_error)
        
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
        num_acto_error = validate_empty(num_acto)
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
        num_acto_error = validate_empty(num_acto)
        if num_acto_error:
            errors.append('Número de acto administrativo: ' + num_acto_error)
            
        # Validate cities coverage
        if ciudades == 0:
            errors.append('Ciudades de cobertura: Debe seleccionar al menos una ciudad')

        cap_transporte_error = validate_none(cap_transporte)
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

    def validate_form4(anexo4, anexo5, anexo6, anexo7, anexo8, anexo9, anexo10, metasypro, anexo11):
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
        
        anexo11_error = validate_none(anexo11)
        if anexo11_error:
            errors.append('Anexo 9: ' + anexo11_error)

        if errors:
            return errors

        return True
    
    def validate_excel_data(file_path, validators=None):
        """
        Reads and validates Excel data starting from row 5
        
        Args:
            file_path (str): Path to Excel file 
            validators (dict): Dictionary of column names and validation functions
            
        Returns:
            tuple: (is_valid (bool), errors (list), validated_data (pd.DataFrame))
        """
        try:
            # Read Excel file starting from row 5 (index 4)
            df = pd.read_excel(file_path, header=3)
            errors = []
            
            # Check if dataframe is empty
            if df.empty:
                errors.append("Excel file is empty or has no data after row 5")
                return False, errors, None
    
            # Apply validators to each column
            if validators:
                for col, validator_func in validators.items():
                    if col in df.columns:
                        # Track invalid rows for this column
                        invalid_rows = []
                        # Validate each cell in the column
                        for index, value in df[col].items():
                            try:
                                if pd.isna(value) or not validator_func(value):
                                    # Add 5 to index to match Excel row numbers (1-based + 4 skipped rows)
                                    invalid_rows.append(index + 1)
                            except Exception as e:
                                invalid_rows.append(index + 1)
                                
                        if invalid_rows:
                            errors.append(f"Valores no validos en la columna '{col}' registro: {invalid_rows}")
                    else:
                        errors.append(f"Columna '{col}' no encontrada en el archivo Excel")
    
            return len(errors) == 0, errors, df
    
        except Exception as e:
            return False, [f"Error leyendo el archivo Excel  \n  {str(e)}"], None
   
    def validate_x_or_empty(value):
        """Validate that a value is either empty/NaN or 'x'"""
        try:
            if pd.isna(value):
                return True
            return str(value).strip().lower() == 'x'
        except:
            return False

    def validate_row_has_x(row, columns_to_check):
        """Validate that at least one 'x' exists in the specified columns of the row"""
        try:
            return any(str(row[col]).strip().lower() == 'x' for col in columns_to_check if not pd.isna(row[col]))
        except:
            return False
    # Columns that need x or empty validation
    x_columns = [
        'Papel', 'Cartón', 1, 2, 3, 
        'Rígido', 'Flexible', 'Vidrio',
        'Ferrosos', 'No ferrosos',
        'Multimateriales 1', 'Multimateriales n'
    ]  
# Modify your validate_excel_data function to include row validation
    def validate_excel_data2(file_path, validators=None):
        """
        Reads and validates Excel data starting from row 5
        
        Args:
            file_path (str): Path to Excel file 
            validators (dict): Dictionary of column names and validation functions
            
        Returns:
            tuple: (is_valid (bool), errors (list), validated_data (pd.DataFrame))
        """
        try:
            # Read Excel file starting from row 5 (index 4)
            df = pd.read_excel(file_path, header=6)
            print(df.columns)
            errors = []
            
            # Check if dataframe is empty
            if df.empty:
                errors.append("El archivo Excel está vacío o no contiene datos después de la fila 5")
                return False, errors, None

            # Apply validators to each column
            if validators:
                for col, validator_func in validators.items():
                    if col in df.columns:
                        # Track invalid rows for this column
                        invalid_rows = []
                        
                        # Validate each cell in the column
                        for index, value in df[col].items():
                            if not validator_func(value):
                                # Add 5 to index to match Excel row numbers
                                invalid_rows.append(index + 1)
                                
                        if invalid_rows:
                            errors.append(f"Valores no válidos en la columna '{col}' en las filas: {invalid_rows}")
                    else:
                        errors.append(f"Columna requerida '{col}' no encontrada en el archivo Excel")

            # Validate that each row has at least one 'x'
            available_x_columns = [col for col in x_columns if col in df.columns]
            for index, row in df.iterrows():
                if not validate_row_has_x(row, available_x_columns):
                    errors.append(f"La fila {index + 1} debe tener al menos una columna marcada con 'x'")

            return len(errors) == 0, errors, df

        except Exception as e:
             False, [f"Error leyendo el archivo Excel: {str(e)}"], None   
   
   
    # Example usage with validators:

    # Create the validators dictionary

    
    ####################################################################################################
    enabled_materials = True
    enabled_mezclado = True

    st.title('Macro de Registro de Materiales')
    col1, col2 = st.columns(2)
    with col1:

        usuarios_list = ['F. Ramírez', 'L. Valencia', 'Assorsa']
        usuario_input = st.selectbox('Usuario', options=usuarios_list,key='usuario_input_key', index=None)
        
        col3, col4 = st.columns(2)
        with col3:
        
            etapa_list = df['Etapa'].unique().tolist()
            etapa_input = st.selectbox('Etapa', options=etapa_list, key='etapa_input_key', index=None)
            
            if etapa_input == 'Recolección':
                enabled_materials = True
                enabled_mezclado = False
            elif etapa_input == 'Caracterización':
                enabled_materials = False
                enabled_mezclado = True

            fuente_list = df[df['Etapa'] == etapa_input]['Fuente'].unique().tolist()
            fuente_input=st.selectbox('Fuente', options=fuente_list, key='fuente_input_key', index=None)

            ciudad_list = df[(df['Fuente'] == fuente_input) & (df['Etapa'] == etapa_input)]['Ciudad'].unique().tolist()
            ciudad_input = st.selectbox('Ciudad', options=ciudad_list, key='ciudad_input_key', index=None)

            sucursal_list = df[(df['Ciudad'] == ciudad_input) & (df['Fuente'] == fuente_input) & (df['Etapa'] == etapa_input)]['Sucursal'].unique().tolist()
            sucursal_input = st.selectbox('Sucursal', options=sucursal_list, key='sucursal_input_key', index=None)    
        with col4:

            gestor_list = df['Gestor'].dropna().unique().tolist() 
            gestor_input = st.selectbox('Gestor', options=gestor_list, key='gestor_input_key', index=None)
            
            aforo_input = st.text_input("Aforo (opcional)", key='aforo_input_key')
            fecha_input = st.date_input('Fecha', key='fecha_input_key', format='MM/DD/YYYY')
    with col2:
        col5, col6 = st.columns(2)
        with col5:
            acrilico_input = st.number_input('Acrílico', key='acrilico_input_key', disabled=enabled_materials)
            aluminio_input = st.number_input('Aluminio', key='aluminio_input_key', disabled=enabled_materials)
            archivo_input = st.number_input('Archivo', key='archivo_input_key', disabled=enabled_materials)
            carton_input = st.number_input('Cartón', key='carton_input_key', disabled=enabled_materials)
            chatarra_input = st.number_input('Chatarra', key='chatarra_input_key', disabled=enabled_materials)
            organicos_input = st.number_input('Orgánicos', key='organicos_input_key', disabled=enabled_materials)
            pead_input = st.number_input('PEAD', key='pead_input_key', disabled=enabled_materials)
            pet_input = st.number_input('PET', key='pet_input_key', disabled=enabled_materials)
            mezclado_input = st.number_input('Mezclado', key='mezclado_input_key', disabled=enabled_mezclado)
        with col6:
            PEBD_input = st.number_input('PEBD', key='pebd_input_key', disabled=enabled_materials)
            plegadiza_input = st.number_input('Plegadiza', key='plegadiza_input_key', disabled=enabled_materials)
            polyboard_input = st.number_input('Polyboard', key='polyboard_input_key', disabled=enabled_materials)
            pvc_input = st.number_input('PVC', key='pvc_input_key', disabled=enabled_materials)
            rechazo_input = st.number_input('Rechazo', key='rechazo_input_key', disabled=enabled_materials)
            tgrasa_input = st.number_input('T. de grasa', key='tgrasa_input_key', disabled=enabled_materials)
            tetrapack_input = st.number_input('Tetra Pack', key='tetrapack_input_key', disabled=enabled_materials)
            vidrio_input = st.number_input('Vidrio', key='vidrio_input_key', disabled=enabled_materials)

    validcheck=validate_form1(usuario_input, etapa_input, fuente_input, ciudad_input, sucursal_input, fecha_input, gestor_input)  
    def on_click():
            with open('bd_cocacola.csv', 'a+', encoding='utf-8') as f:    #Append & read mode
                if etapa_input == 'Recolección':
                    f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Mezclado'},{mezclado_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                if etapa_input == 'Caracterización':
                    if acrilico_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Acrílico'},{acrilico_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if aluminio_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Aluminio'},{aluminio_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if archivo_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Archivo'},{archivo_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if carton_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Cartón'},{carton_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if chatarra_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Chatarra'},{chatarra_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if organicos_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Orgánicos'},{organicos_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if pead_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'PEAD'},{pead_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if pet_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'PET'},{pet_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if PEBD_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'PEBD'},{PEBD_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if plegadiza_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Plegadiza'},{plegadiza_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if polyboard_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Polyboard'},{polyboard_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if pvc_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'PVC'},{pvc_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if rechazo_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Rechazo'},{rechazo_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if tgrasa_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'T. de grasa'},{tgrasa_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if tetrapack_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Tetra Pack'},{tetrapack_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                    if vidrio_input > 0:
                        f.write(f"{ciudad_input},{fecha_input.strftime('%m/%d/%Y')},{gestor_input},{aforo_input},{etapa_input},{fuente_input},{sucursal_input},{'Vidrio'},{vidrio_input},{usuario_input},{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}\n")
                st.toast('Registro añadido exitosamente', icon='✅')  

            st.session_state.mezclado_input_key = 0
            st.session_state.acrilico_input_key = 0
            st.session_state.aluminio_input_key = 0
            st.session_state.archivo_input_key = 0
            st.session_state.carton_input_key = 0
            st.session_state.chatarra_input_key = 0
            st.session_state.organicos_input_key = 0
            st.session_state.pead_input_key = 0
            st.session_state.pet_input_key = 0
            st.session_state.pebd_input_key = 0
            st.session_state.plegadiza_input_key = 0
            st.session_state.polyboard_input_key = 0
            st.session_state.pvc_input_key = 0
            st.session_state.rechazo_input_key = 0
            st.session_state.tgrasa_input_key = 0
            st.session_state.tetrapack_input_key = 0
            st.session_state.vidrio_input_key = 0

    if validcheck != True:
        if st.button('Registrar', type='secondary', key='añadirfalse'):
            
            for i in validcheck:
                st.toast(i, icon='⚠️')
            # s = ''
            #     s += "-" + i + "  \n"
            # st.error(s)

    elif validcheck == True:
            st.button('Registrar', type='secondary', on_click=on_click, key='añadirtrue')       

else:
    st.switch_page("./pages/Inicio.py")
