import streamlit as st
from streamlit import session_state as ss
from modules.nav import MenuButtons
from pages.account import get_roles

# If the user reloads or refreshes the page while still logged in,
# go to the account page to restore the login status. Note reloading
# the page changes the session id and previous state values are lost.
# What we are doing is only to relogin the user.
if 'authentication_status' not in ss:
    st.switch_page('./pages/account.py')


MenuButtons(get_roles())


# Protected content in home page.
if ss.get('authentication_status'):
    st.markdown("""
# ¡Bienvenido a **Weroapp**!

¡Hola y bienvenido a **Weroapp**, la forma más sencilla de ingresar, gestionar y enviar tus datos!

Ya sea que recopiles respuestas de encuestas, registres detalles de inventario o hagas seguimiento de hitos de proyectos, Weroapp te ofrece:

- **Constructor de Formularios Intuitivo**  
  Crea y personaliza campos en segundos — sin necesidad de programar.

- **Validación en Tiempo Real**  
  Obtén retroalimentación inmediata sobre campos obligatorios, formatos y rangos para garantizar datos limpios.

- **Guardado Automático y Borradores**  
  Nunca pierdas tu progreso: tus entradas se guardan automáticamente mientras escribes.

- **Exportación de Datos Potente**  
  Descarga tus envíos en CSV o JSON para un análisis e informes sencillos.

---

## Primeros pasos

1. **Regístrate**  
   Crea tu cuenta gratuita en menos de 30 segundos.  
2. **Crea un Nuevo Formulario**  
   Haz clic en **“Nuevo Formulario”**, arrastra los campos que necesites y presiona **“Guardar”**.  
3. **Comparte y Recopila**  
   Copia el enlace de tu formulario y compártelo por correo, chat o incrústalo en tu sitio web.  
4. **Revisa y Exporta**  
   Dirígete a la pestaña **“Envíos”** para ver las entradas o exportar tus datos cuando quieras.

---

## ¿Necesitas ayuda?

- Consulta nuestra [Documentación](#) para guías paso a paso.  
- Visita el [Foro de la Comunidad](#) para hacer preguntas y compartir consejos.  
- Escribe a nuestro equipo de soporte: [support@Weroapp.app](mailto:support@Weroapp.app).

¡Hagamos que la entrada de datos sea sencilla! 🚀
""")

else:
    st.switch_page('./pages/account.py')
    #st.write('Please log in on login page.')
