import openai

def generate_proposal_letter(api_key, profile_url, proposal_name):
    # Inicializar la API de OpenAI con la clave de API proporcionada
    openai.api_key = api_key

    # Obtener la información del perfil del cliente potencial
    profile_data = requests.get(profile_url).json()
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

# Probar la función
openai_api_key = "your_openai_api_key"
profile_url = "https://linkedin.com/profile_url"
proposal_name = "Proposal name"

proposal_letter = generate_proposal_letter(openai_api_key, profile_url, proposal_name)
print(proposal_letter)
