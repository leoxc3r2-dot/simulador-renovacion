import streamlit as st
import google.generativeai as genai

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Simulador MoradaUno", layout="centered")

# --- 2. Conexión a la API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la clave GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.title("🤝 Simulador de Negociación")

# --- 3. Inicialización del Chat ---
# Usamos ÚNICAMENTE gemini-1.5-flash que es el más estable
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Iniciamos el chat vacío
        st.session_state.chat = model.start_chat(history=[])
        
        # El primer mensaje configura al cliente
        instruccion = (
            "Eres un cliente de MoradaUno en México. No quieres renovar tu protección de renta "
            "porque te parece cara. Saluda de forma natural y lanza tu primera objeción breve."
        )
        response = st.session_state.chat.send_message(instruccion)
        
        # Guardamos el primer mensaje en el historial visual
        st.session_state.mensajes = [{"role": "assistant", "content": response.text}]
    except Exception as e:
        st.error(f"Error de conexión inicial: {e}")
        st.stop()

# --- 4. Interfaz de Usuario (Chat) ---
# Mostrar mensajes previos
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe tu argumento aquí..."):
    # Mostrar mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Obtener respuesta de la IA
    try:
        response = st.session_state.chat.send_message(prompt)
        st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.write(response.text)
    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ Vas muy rápido. Espera 30 segundos y vuelve a intentar.")
        else:
            st.error(f"Error en la comunicación: {e}")
