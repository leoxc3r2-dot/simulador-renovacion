import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# --- 1. Configuración Visual ---
st.set_page_config(page_title="Simulador MoradaUno", layout="centered")

# --- 2. Conexión Forzada a Producción ---
if "GOOGLE_API_KEY" in st.secrets:
    # Esta línea es la CLAVE: obliga a usar la API v1 estable, no la beta
    options = client_options.ClientOptions(api_version="v1")
    genai.configure(
        api_key=st.secrets["GOOGLE_API_KEY"],
        client_options=options
    )
else:
    st.error("Falta la clave GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.title("🤝 Simulador de Negociación")

# --- 3. Lógica del Chat ---
if "chat" not in st.session_state:
    try:
        # Usamos el nombre completo del modelo para evitar confusiones
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        st.session_state.chat = model.start_chat(history=[])
        
        # Configuramos al cliente Ricardo
        instruccion = "Eres Ricardo, un cliente de MoradaUno. No quieres renovar. Habla como mexicano de forma breve."
        response = st.session_state.chat.send_message(instruccion)
        
        st.session_state.mensajes = [{"role": "assistant", "content": response.text}]
    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.info("Si ves un 429, espera 1 minuto. Si ves un 404, revisa que la API Key sea la correcta.")
        st.stop()

# --- 4. Interfaz ---
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Escribe tu argumento..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
