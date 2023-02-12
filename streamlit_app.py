import streamlit as st
import openai

# Configurar OpenAI API 
openai.api_key = "YOUR_API_KEY" 

# Crear interfaz de usuario con Streamlit 
st.title("Generador de Cartas de Negocios") 
st.header("Proporciona la URL del perfil de LinkedIn y el nombre de tu propuesta") 

 # Obtener información del usuario y almacenarla en variables  
linkedInURL = st.text_input("URL del perfil de LinkedIn:")  
proposalName = st.text_input("Nombre de tu propuesta:")  

 # Generar carta usando GPT-3 y la información proporcionada por el usuario   
prompt = f"Hola, estoy escribiendo para presentarte mi idea llamada '{proposalName}'. Me enteré que {linkedInURL} es uno de tus intereses principales, y me gustaría compartir contigo cómo puedo ayudarte en este área."    

completion = openai.Completion(engine="davinci", prompt=prompt, max_tokens=150)    							    
response = completion.get()['choices'][0]['text'] 

#Mostrar carta generada en pantalla    
st.write(response)
