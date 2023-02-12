import openai
import streamlit as st

# Autenticación en OpenAI
openai.api_key = "YOUR_API_KEY_HERE"

# Configuración del modelo GPT-3
model_engine = "text-davinci-003"

# Función para generar el correo
def generate_email(name, company, role, linkedin_url, proposal):
    prompt = (f"Hola {name},\n\n" 
              "He estado investigando tu perfil en LinkedIn y me ha impresionado mucho tu experiencia en {role} en {company}. "
              "Me gustaría saber si estarías interesado en hablar sobre una posible colaboración en un proyecto relacionado con {role} en nuestra empresa. "
              f"A continuación, te proporciono más información sobre nuestra propuesta:\n\n{proposal}\n\n"
              "Te he enviado una solicitud de conexión en LinkedIn para que podamos mantenernos en contacto.\n\n"
              "Saludos cordiales,\n"
              "Tu nombre")
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
        user=dict(linkedin_url=linkedin_url)
    )
    return response.choices[0].text

# Interfaz de usuario de Streamlit
st.title("Generador de Correos Personalizados")
name = st.text_input("Ingresa el nombre de la persona:")
company = st.text_input("Ingresa la empresa en la que trabaja la persona:")
role = st.text_input("Ingresa el puesto de la persona:")
linkedin_url = st.text_input("Ingresa la URL del perfil de LinkedIn de la persona:")
proposal = st.text_area("Ingresa la descripción de la propuesta de negocio:")

if st.button("Generar correo"):
    # Generar el correo y mostrar el resultado en la interfaz de usuario
    email = generate_email(name, company, role, linkedin_url, proposal)
    st.text_area("Correo generado:", value=email, height=200, max_chars=None)
