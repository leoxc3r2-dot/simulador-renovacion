import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Simulador MoradaUno", layout="centered")

# Configuración con la nueva llave
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("No se encontró la GOOGLE_API_KEY en los Secrets.")
    st.stop()

st.title("🤝 Simulador de Negociación")

# Inicializamos el estado si no existe
if "chat" not in st.session_state:
    try:
        # Usamos el modelo más estándar del mundo
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.chat = model.start_chat(history=[])
        # Enviamos el primer mensaje de contexto "invisible"
        st.session_state.chat.send_message("Eres un cliente de MoradaUno. No quieres renovar. Sé breve y mexicano.")
        st.session_state.mensajes = [{"role": "assistant", "content": "Hola, soy tu cliente. No estoy seguro de querer renovar la protección este año, me parece un gasto innecesario. ¿Qué me dices?"}]
    except Exception as e:
        st.error(f"Error al iniciar: {e}")

# Mostrar historial
if "mensajes" in st.session_state:
    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Input de usuario
if prompt := st.chat_input("Escribe tu argumento de venta..."):
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
