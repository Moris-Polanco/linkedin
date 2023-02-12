import streamlit as st
import openai
from linkedin_api import Linkedin

# Configuración de API
openai.api_key = "tu_api_key_de_openai"

# Configuración de LinkedIn
linkedin_email = "mpolanco@feylibertad.org"
linkedin_password = "Mita1962!"
linkedin = Linkedin(linkedin_email, linkedin_password)

# Definir función para obtener información del perfil de LinkedIn
def get_linkedin_profile(url):
    profile_id = linkedin.find_profile_id(url)
    profile_data = linkedin.get_profile(profile_id)
    return profile_data

# Definir función para generar la carta de propuesta de negocios
def generate_business_proposal(profile_data, project_description):
    # Combinar información del perfil y la descripción del proyecto
    text = f"Estimado/a {profile_data['firstName']} {profile_data['lastName']},\n\nMe complace presentarle mi propuesta para {project_description}. {profile_data['firstName']}, con su experiencia en {', '.join(profile_data['experience'])}, usted sería el socio perfecto para este proyecto. En particular, sus habilidades en {', '.join(profile_data['skills'])} y su educación en {profile_data['education']} lo hacen ideal para ayudarme a llevar esta idea al siguiente nivel.\n\nSinceramente,\nTu nombre"

    # Generar la carta de propuesta de negocios con GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    business_proposal = response.choices[0].text
    return business_proposal

# Configuración de la aplicación de Streamlit
st.title("Generador de cartas de propuestas de negocios con GPT-3")

# Obtener URL del perfil de LinkedIn y descripción del proyecto del usuario
url = st.text_input("Introduce la URL de tu perfil de LinkedIn:")
project_description = st.text_input("Describe brevemente tu proyecto:")

# Generar la carta de propuesta de negocios y mostrarla al usuario
if url and project_description:
    profile_data = get_linkedin_profile(url)
    business_proposal = generate_business_proposal(profile_data, project_description)
    st.subheader("Carta de propuesta de negocios generada:")
    st.write(business_proposal)

