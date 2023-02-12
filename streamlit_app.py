import openai
import json
import streamlit as st
import os

# Autenticación en OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configuración del modelo GPT-3
model_engine = "text-davinci-003"

# Función para generar el correo
def generate_email(name, linkedin_url):
    prompt = (f"Hola {name},\n\n" 
              "He estado investigando tu perfil en LinkedIn y me ha impresionado mucho tu experiencia y habilidades. "
              "Me gustaría saber si estarías interesado en hablar sobre una posible colaboración en un proyecto relacionado con tus áreas de experiencia. "
              "Permíteme proporcionarte más detalles sobre la propuesta de negocio:\n\n"
              "Nuestra empresa se dedica a [descripción de la empresa]. Actualmente estamos trabajando en un proyecto relacionado con [descripción del proyecto]."
              "Creemos que tu experiencia y habilidades podrían ser de gran valor para el proyecto, y nos gustaría discutir una posible colaboración contigo. "
              "Por favor, háznos saber si estarías interesado en saber más sobre el proyecto y cómo podrías contribuir.\n\n"
              "Te he enviado una solicitud de conexión en LinkedIn para que podamos mantenernos en contacto.\n\n"
              "Saludos cordiales,\n"
              "Tu nombre")
    user_data = {"linkedin_url": linkedin_url}
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
        user=json.dumps(user_data)
    )
    return response.choices[0].text

# Interfaz de usuario de Streamlit
st.title("Generador de Correos Personalizados")
name = st.text_input("Ingresa el nombre de la persona:")
linkedin_url = st.text_input("Ingresa la URL del perfil de LinkedIn de la persona:")

if st.button("Generar correo"):
    # Generar la propuesta de negocio
    prompt = "Nuestra empresa se dedica a "
    company_description = st.text_input("Describe tu empresa:")
    if company_description:
        prompt += company_description + ". "
    else:
        prompt += "[descripción de la empresa]. "

    prompt += "Actualmente estamos trabajando en un proyecto relacionado con "
    project_description = st.text_input("Describe el proyecto:")
    if project_description:
        prompt += project_description + ". "
    else:
        prompt += "[descripción del proyecto]. "

    proposal_response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )
    proposal = proposal_response.choices[0].text

    # Generar el correo y mostrar el resultado en la interfaz de usuario
    email = generate_email(name, linkedin_url)
    email = email.replace("[descripción de la empresa]", company_description)
    email = email.replace("[descripción del proyecto]", project_description)
    email = email.replace("[propuesta de negocio]", proposal)
    st.text_area("Correo generado:", value=email, height=200, max_chars=None)
