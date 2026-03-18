import streamlit as st
import random
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Simulador MoradaUno", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta GOOGLE_API_KEY en Secrets.")
    st.stop()

# --- PERFILES ---
perfiles = [
    {'nombre': 'Carlos Ruiz', 'tipo': 'broker', 'objecion': 'La comisión es muy baja.'},
    {'nombre': 'Alicia Mendoza', 'tipo': 'propietario', 'objecion': 'No confío en estos servicios.'}
]

# --- LÓGICA ---
def iniciar_simulacion():
    perfil = random.choice(perfiles)
    try:
        # USAREMOS EL NOMBRE MÁS ESTÁNDAR POSIBLE
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        chat = model.start_chat(history=[])
        # Instrucción de sistema
        chat.send_message(f"Actúa como {perfil['nombre']}. Tu objeción inicial es: {perfil['objecion']}. Habla breve.")
        # Pedir primera frase
        response = chat.send_message("Preséntate y dime tu objeción.")
        
        st.session_state.chat_history = chat
        st.session_state.mensajes = [
            {"role": "assistant", "content": f"**Simulación con {perfil['nombre']}**"},
            {"role": "assistant", "content": response.text}
        ]
    except Exception as e:
        st.error(f"Error crítico de conexión: {e}")

def responder():
    if st.session_state.user_text:
        t = st.session_state.user_text
        st.session_state.mensajes.append({"role": "user", "content": t})
        try:
            r = st.session_state.chat_history.send_message(t)
            st.session_state.mensajes.append({"role": "assistant", "content": r.text})
        except Exception as e:
            st.error(f"Error en chat: {e}")

# --- INTERFAZ ---
st.title("🤝 Simulador MoradaUno")

if st.button("Iniciar"):
    iniciar_simulacion()

for m in st.session_state.get("mensajes", []):
    with st.chat_message(m["role"]):
        st.write(m["content"])

if "chat_history" in st.session_state:
    st.chat_input("Escribe...", key="user_text", on_submit=responder)
