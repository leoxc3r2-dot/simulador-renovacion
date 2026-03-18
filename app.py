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
    
    # CAMBIO CLAVE: Usamos gemini-1.5-flash para mayor estabilidad y cuota
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt_sistema = f"""
        Eres {perfil['nombre']}, un {perfil['tipo']} {perfil['personalidad']}.
        Contexto: Negociación de renovación de MoradaUno. Renta: ${monto} MXN.
        Reglas: 1. Texto plano. 2. Empieza con una objeción fuerte. 3. Habla como mexicano de CDMX.
        """
        
        chat = model.start_chat(history=[])
        # Configuramos el personaje
        chat.send_message(prompt_sistema)
        # Lanzamos la primera objeción
        response = chat.send_message("Preséntate brevemente y lanza tu primera objeción sobre por qué NO quieres renovar con MoradaUno.")
        
        st.session_state.chat_history = chat
        st.session_state.mensajes = [
            {"role": "assistant", "content": f"**Simulación: {perfil['nombre']} ({perfil['tipo']})**\n**Renta:** ${monto:,} MXN"},
            {"role": "assistant", "content": response.text}
        ]
        st.session_state.ready = True
    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ Cuota agotada. Espera 60 segundos y vuelve a intentar.")
        else:
            st.
