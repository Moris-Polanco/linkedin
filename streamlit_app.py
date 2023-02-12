import openai
import json
import streamlit as st
import os

# Autenticación en OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configuración del modelo GPT-3
model_engine = "text-davinci-003"

# Función para generar el correo
def generate_email(name, linkedin_url, proposal, interests):
    prompt = (f"Hola {name},\n\n" 
              "Me he dado cuenta de que compartimos intereses en común en tu perfil de LinkedIn, como [intereses]. "
              "Me gustaría saber si estarías interesado en hablar sobre una posible colaboración en un proyecto relacionado con tus áreas de experiencia. "
              "Permíteme proporcionarte más detalles sobre la propuesta de negocio:\n\n"
              f"{proposal}\n\n"
              "Te he enviado una solicitud de conexión en LinkedIn para que podamos mantenernos en contacto.\n\n"
              "Saludos cordiales,\n"
              "Tu nombre")
    user_data = {"linkedin_url": linkedin_url}
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt.replace("[intereses]", interests),
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.5,
        user=json.dumps(user_data)
    )
    print("API response:")
    print(response)
    if len(response.choices) == 0:
        return "No se pudo generar el correo. Por favor, intenta nuevamente más tarde."
    print("API response text:")
    print(response.choices[0].text)
    return str(response.choices[0].text)

# Interfaz de usuario de Streamlit
st.title("Generador de Correos Personalizados")
name = st.text_input("Ingresa el nombre de la persona:")
linkedin_url = st.text_input("Ingresa la URL del perfil de LinkedIn de la persona:")
interests = st.text_input("Ingresa los intereses que compartes con la persona:")
proposal = st.text_area("Ingresa la propuesta de negocio:")

if st.button("Generar correo"):
    # Generar el correo y mostrar el resultado en la interfaz de usuario
    email = generate_email(name, linkedin_url, proposal, interests)
    st.text_area("Correo generado:", value=email, height=200, max_chars=None)
