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

    # Verificar si la URL proporcionada es válida
    try:
        response = requests.get(profile_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.write("Error al obtener la información del perfil:", e)
        return None

    # Verificar si la respuesta es una respuesta JSON válida
    if response.headers['Content-Type'] == 'application/json':
        try:
            profile_data = response.json()
        except json.decoder.JSONDecodeError as e:
            st.write("Error al decodificar la respuesta JSON:", e)
            return None
    else:
        st.write("La respuesta no es una respuesta JSON válida.")
        return None

    client_name = profile_data['name']
    client_interests = profile_data['interests']

    # Generar la carta de propuesta usando GPT-3
    model_engine = "text-davinci-002"
    prompt = (f"Escriba una carta de propuesta para {client_name} sobre la propuesta '{proposal_name}', teniendo en cuenta sus intereses: {client_interests}")

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

if st.button("Generar Carta de Propuesta"):
    proposal_letter = generate_proposal_letter(openai_api_key, profile_url, proposal_name)
    if proposal_letter is None:
        st.write("No se pudo generar la carta de propuesta.")
    else:
        st.success("¡Carta de propuesta generada con éxito!")
        st.write("Aquí está su carta de propuesta:")
        st.write(proposal_letter)
