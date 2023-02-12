import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Configuración de API
openai.api_key = "tu_api_key_de_openai"

# Definir función para obtener información del perfil de LinkedIn
def get_linkedin_profile(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    name_div = soup.find("div", {"class": "flex-1 mr5"})
    name_loc = name_div.find_all("ul")
    name = name_loc[0].find("li").get_text().strip()
    headline = name_div.find("h2").get_text().strip()
    exp_section = soup.find("section", {"id": "experience-section"})
    experience = []
    for exp in exp_section.find_all("div", {"class": "pv-entity__summary-info"}):
        title = exp.find("h3", {"class": "t-16 t-black t-bold"}).get_text().strip()
        company = exp.find("p", {"class": "pv-entity__secondary-title t-14 t-black t-normal"}).get_text().strip()
        date_range = exp.find("h4", {"class": "t-14 t-black t-normal"}).find_all("span")[1].get_text().strip()
        experience.append({"title": title, "company": company, "date_range": date_range})
    edu_section = soup.find("section", {"id": "education-section"})
    education = []
    for edu in edu_section.find_all("div", {"class": "pv-profile-section__card-item-v2 pv-profile-section pv-education-entity ember-view"}):
        school = edu.find("h3", {"class": "pv-entity__school-name t-16 t-black t-bold"}).get_text().strip()
        degree = edu.find("p", {"class": "pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"}).find_all("span")[1].get_text().strip()
        field_of_study = edu.find("p", {"class": "pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"}).find_all("span")[1].get_text().strip()
        date_range = edu.find("p", {"class": "pv-entity__dates t-14 t-black t-normal"}).find_all("span")[1].get_text().strip()
        education.append({"school": school, "degree": degree, "field_of_study": field_of_study, "date_range": date_range})
    skills_section = soup.find("section", {"class": "pv-profile-section pv-skill-categories-section artdeco-container-card ember-view"})
    skills = []
    for skill in skills_section.find_all("li", {"class": "pv-skill-category-entity__skill-wrapper"}):
        skills.append(skill.find("span", {"class": "pv-skill-category-entity__name-text t-16 t-black t-bold"}).get_text().strip())
    return {"name": name, "headline": headline, "experience": experience, "education": education, "skills": skills}

# Definir función para generar la carta de propuesta de negocios
def generate_business_proposal(profile_data, project_description):
    # Combinar información del perfil y la descripción del proyecto
    text = f"Estimado/a {profile_data['name']},\n\nMe complace presentarle mi propuesta para {project_description}. {profile_data['name']}, con su experiencia en {[exp['title'] for exp in profile_data['experience']]}, usted sería el socio perfecto para este proyecto. En particular, sus habilidades en {', '.join(profile_data['skills'])} y su educación en {profile_data['education'][0]['field_of_study']} lo hacen ideal para ayudarme a llevar esta idea al siguiente nivel.\n\nSinceramente,\nTu nombre"

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
url = st.text_input("Introduce la URL de un perfil de LinkedIn:")
project_description = st.text_input("Describe brevemente tu proyecto:")

# Generar la carta de propuesta de negocios y mostrarla al usuario
if url and project_description:
    profile_data = get_linkedin_profile(url)
    business_proposal = generate_business_proposal(profile_data, project_description)
    st.subheader("Carta de propuesta de negocios generada:")
    st.write(business_proposal)

