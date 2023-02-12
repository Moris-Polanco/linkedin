import openai
import streamlit as st

# Autenticación en OpenAI
openai.api_key = "YOUR_API_KEY_HERE"

# Configuración del modelo GPT-3
model_engine = "text-davinci-003"
prompt = (
    "Hola {nombre}, \n\n"
    "He estado investigando tu perfil en linkedit.com y me ha impresionado mucho tu experiencia en {area}. "
    "Me gustaría saber si estarías interesado en hablar sobre una posible colaboración en {proyecto}. "
    "Quedo a la espera de tu respuesta.\n\n"
    "Saludos cordiales,\n"
    "{tu_nombre}"
)

# Interfaz de usuario de Streamlit
st.title("Generador de Correos Personalizados")
nombre = st.text_input("Ingresa el nombre de la persona:")
area = st.text_input("Ingresa el área de experiencia de la persona:")
proyecto = st.text_input("Ingresa el proyecto específico que te interesa:")

if st.button("Generar correo"):
    # Solicitud de generación de texto a OpenAI
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt.format(nombre=nombre, area=area, proyecto=proyecto, tu_nombre="Tu Nombre"),
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Mostrar el resultado en la interfaz de usuario
    st.text_area("Correo generado:", value=response.choices[0].text, height=200, max_chars=None)
