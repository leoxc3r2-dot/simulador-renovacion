import streamlit as st
import google.generativeai as genai
import os

# --- Configuración Visual ---
st.set_page_config(page_title="Simulador MoradaUno", layout="centered")

# --- Conexión Manual y Forzada ---
if "GOOGLE_API_KEY" in st.secrets:
    # FORZAMOS LA CONFIGURACIÓN SIN BETA
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("No se encontró la llave en Secrets.")
    st.stop()

st.title("🤝 Simulador de Negociación")

# --- Lógica con Selección de Modelo Automática ---
if "chat" not in st.session_state:
    try:
        # Intentamos con el nombre que SÍ estaba en tu lista: gemini-2.0-flash
        # Si este falla, el sistema saltará al siguiente automáticamente
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        st.session_state.chat = model.start_chat(history=[])
        # Mensaje de inicialización
        st.session_state.chat.send_message("Eres un cliente de MoradaUno. No quieres renovar. Sé breve y habla como mexicano.")
        
        st.session_state.mensajes = [{"role": "assistant", "content": "Hola, soy tu cliente. Estaba revisando el presupuesto y la verdad no creo que renovemos la protección este año. ¿Qué me puedes decir?"}]
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Intentando reconectar con modelo alternativo...")
        # Intento de rescate con otro modelo de tu lista
        try:
            model = genai.GenerativeModel('gemini-pro')
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.mensajes = [{"role": "assistant", "content": "Hola, ¿me escuchas? Soy tu cliente. Cuéntame por qué debería renovar."}]
        except:
            st.error("No se pudo conectar con ningún modelo. Revisa tu API Key.")

# --- Interfaz de Chat ---
if "mensajes" in st.session_state:
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
        st.error(f"Error en la respuesta: {e}")
