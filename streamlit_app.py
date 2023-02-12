import streamlit as st
import requests
import openai

# Crear la interfaz de usuario con Streamlit
st.title("Generador de Cartas de Propuestas de Negocios")

openai_api_key = st.text_input("Ingrese su clave de API de OpenAI:")
profile_url = st.text_input("Ingrese la URL del perfil de LinkedIn:")
proposal_name = st.text_input("Ingrese el nombre de su propuesta:")

def generate_proposal_letter(api_key, profile_url, proposal_name):
    # Inicializar la API de OpenAI con la clave de API proporcionada
    openai.api_key = api_key

    # Obtener información del perfil del cliente potencial a partir de la URL de LinkedIn
    profile_data = requests.get(profile_url).json()
    client_name = profile_data['name']
    client_interests = profile_data['interests']

    # Generar la carta de propuesta usando GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Estimado/a {client_name}, me gustaría proponerle una oportunidad de negocios relacionada con sus intereses en {client_interests}. Nuestra propuesta, llamada '{proposal_name}', implica...",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    proposal_letter = response['choices'][0]['text']

    return proposal_letter

if st.button("Generar Carta de Propuesta"):
    proposal_letter = generate_proposal_letter(openai_api_key, profile_url, proposal_name)
    st.success("¡Carta de propuesta generada exitosamente!")
    st.write("\n\n")
    st.write(proposal_letter)
