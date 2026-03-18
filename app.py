import streamlit as st
import random
import google.generativeai as genai

# --- Configuración Visual ---
st.set_page_config(page_title="Simulador MoradaUno", layout="wide")
st.markdown("<style>.stApp { background-color: #F8F9FA; }</style>", unsafe_allow_html=True)

# --- Configuración de la API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ No se encontró la clave GOOGLE_API_KEY en los Secrets.")
    st.stop()

# --- Datos de los Perfiles ---
perfiles = [
    {'nombre': 'Carlos Ruiz', 'tipo': 'broker', 'personalidad': 'Directo y enfocado en dinero.', 'motivacion': 'Quiere su comisión rápido.'},
    {'nombre': 'Alicia Mendoza', 'tipo': 'propietario', 'personalidad': 'Desconfiada y ahorradora.', 'motivacion': 'No quiere gastar de más.'},
    {'nombre': 'Diego López', 'tipo': 'broker', 'personalidad': 'Amistoso pero distraído.', 'motivacion': 'Quiere que el proceso sea fácil.'}
]

# --- Funciones de la Simulación ---
def iniciar_simulacion():
    perfil = random.choice(perfiles)
    monto = random.randint(12000, 45000)
    
    # ACTUALIZADO: Usando el modelo que aparece en tu lista
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt_sistema = f"""
        Eres {perfil['nombre']}, un {perfil['tipo']} {perfil['personalidad']}.
        Contexto: Negociación de renovación de MoradaUno. Renta: ${monto} MXN.
        Reglas: 1. Texto plano. 2. Empieza con una objeción fuerte. 3. Habla como mexicano.
        """
        
        chat = model.start_chat(history=[])
        # Configuramos el personaje
        chat.send_message(prompt_sistema)
        # Lanzamos la primera objeción
        response = chat.send_message("Preséntate y lanza tu primera objeción de renovación.")
        
        st.session_state.chat_history = chat
        st.session_state.mensajes = [
            {"role": "assistant", "content": f"**Simulación: {perfil['nombre']} ({perfil['tipo']})**\n**Renta:** ${monto:,} MXN"},
            {"role": "assistant", "content": response.text}
        ]
        st.session_state.ready = True
    except Exception as e:
        st.error(f"Error de conexión: {e}")

def responder():
    if st.session_state.usuario_input:
        texto = st.session_state.usuario_input
        st.session_state.mensajes.append({"role": "user", "content": texto})
        
        try:
            response = st.session_state.chat_history.send_message(texto)
            st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error en la IA: {e}")

# --- Interfaz ---
st.title("🤝 Simulador de Renovaciones MoradaUno")

if st.button("🔄 Iniciar Nueva Simulación"):
    iniciar_simulacion()

# Dibujar mensajes
if "mensajes" in st.session_state:
    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Chat input
if st.session_state.get("ready"):
    st.chat_input("Escribe tu respuesta aquí...", key="usuario_input", on_submit=responder)
else:
    st.info("Haz clic en el botón de arriba para comenzar la práctica.")
