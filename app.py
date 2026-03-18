import streamlit as st
import random
import google.generativeai as genai

# --- Configuración Visual ---
st.set_page_config(page_title="Simulador MoradaUno", layout="wide")
st.markdown("<style>.stApp { background-color: #F8F9FA; }</style>", unsafe_allow_html=True)

# --- Configuración de la API ---
# Intentamos obtener la clave de los secrets
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
    monto = random.randint(10000, 35000)
    
    # IMPORTANTE: Aquí estaba el error. El nombre debe ser solo 'gemini-1.5-flash'
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt_sistema = f"""
        Eres {perfil['nombre']}, un {perfil['tipo']} {perfil['personalidad']}.
        Tu objetivo es NO renovar el servicio de MoradaUno fácilmente. 
        Monto de renta: ${monto} MXN.
        Reglas: 1. Solo texto plano. 2. Empieza con una objeción fuerte. 3. Habla como mexicano.
        """
        
        # Iniciamos el chat
        chat = model.start_chat(history=[])
        # Primer mensaje para que la IA tome su papel
        response = chat.send_message(prompt_sistema)
        # Segundo mensaje para que lance la objeción
        objecion = chat.send_message("Preséntate y dime por qué no quieres renovar.").text
        
        st.session_state.chat_history = chat
        st.session_state.mensajes = [
            {"role": "assistant", "content": f"**Simulación Iniciada**\n**Cliente:** {perfil['nombre']}\n**Renta:** ${monto:,} MXN"},
            {"role": "assistant", "content": objecion}
        ]
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
st.title("🤝 Simulador de Renovaciones")

if st.button("🔄 Iniciar Simulación"):
    iniciar_simulacion()

# Dibujar mensajes
for m in st.session_state.get("mensajes", []):
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Chat input
if "chat_history" in st.session_state:
    st.chat_input("Escribe tu respuesta aquí...", key="usuario_input", on_submit=responder)
else:
    st.info("Haz clic en el botón de arriba para comenzar.")
