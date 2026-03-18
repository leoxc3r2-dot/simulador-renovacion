import streamlit as st
import random
import google.generativeai as genai

# --- Configuración de la Página ---
st.set_page_config(page_title="Simulador de Renovaciones", layout="wide")

# Estilo visual MoradaUno
st.markdown(
    """
    <style>
    .stApp { background-color: #F8F9FA; }
    .stButton>button { background-color: #9C27B0; color: white; border-radius: 10px; border: none; }
    .stButton>button:hover { background-color: #BA68C8; border: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configuración de API ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Error: No se encontró 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- Datos de la Simulación ---
perfiles_brokers = [
    {'nombre': 'Carlos Ruiz', 'tipo': 'broker', 'personalidad': 'Orientado a resultados.', 'motivacion': 'Busca una renovación rápida y con buena comisión.'},
    {'nombre': 'Laura Gómez', 'tipo': 'broker', 'personalidad': 'Meticulosa, se preocupa por los detalles.', 'motivacion': 'Quiere seguridad total en la cobertura.'},
    {'nombre': 'Diego López', 'tipo': 'broker', 'personalidad': 'Amistoso y conversador.', 'motivacion': 'Se basa en la relación de confianza.'},
]

perfiles_propietarios = [
    {'nombre': 'Alicia Mendoza', 'tipo': 'propietario', 'personalidad': 'Ahorradora, se fija en los precios.', 'motivacion': 'Busca el mejor precio sin perder beneficios.'},
    {'nombre': 'Ricardo Solís', 'tipo': 'propietario', 'personalidad': 'Exigente, le gusta el control.', 'motivacion': 'Le preocupa la puntualidad de los pagos.'},
    {'nombre': 'Sofía Hernández', 'tipo': 'propietario', 'personalidad': 'Primeriza, se asusta fácilmente.', 'motivacion': 'Quiere protección y explicaciones claras.'},
]

perfiles_de_simulacion = perfiles_brokers + perfiles_propietarios

tipos_de_producto = ['M12 Habitacional', 'M12 Comercial', 'M3 Habitacional', 'M3 Comercial', 'MLegal Habitacional', 'M3 Light Habitacional']

informacion_productos = {
    'M12 Habitacional': "12 meses de protección de renta + protección legal del inmueble.",
    'M12 Comercial': "12 meses de protección de renta + protección legal del inmueble.",
    'M3 Habitacional': "3 meses de protección de renta + servicio anual de protección legal.",
    'M3 Comercial': "3 meses de protección de renta + servicio anual de protección legal.",
    'MLegal Habitacional': "Enfoque total en defensa legal y recuperación de la propiedad.",
    'M3 Light Habitacional': "Producto anterior (no disponible), cubría 3 meses para rentas >$20,000."
}

# --- Funciones Lógicas ---
def generar_instruccion_ia(perfil, detalles):
    return f"""
    Eres {perfil['nombre']}, un {perfil['tipo']} con personalidad '{perfil['personalidad']}'. 
    Motivación: {perfil['motivacion']}.
    Contexto: Estás negociando la renovación de protección de renta de MoradaUno.
    Detalles: Producto actual {detalles['producto_actual']}, Renta ${detalles['monto_renta']:,} MXN.
    
    REGLAS:
    1. Responde SIEMPRE en texto plano, sin negritas ni formatos raros.
    2. Tu primera respuesta debe ser una objeción difícil basada en tu perfil.
    3. Si te convencen con buenos argumentos de MoradaUno, acepta la renovación al final.
    4. Usa un tono natural de México.
    """

def iniciar_simulacion():
    perfil = random.choice(perfiles_de_simulacion)
    producto = random.choice(tipos_de_producto)
    monto = random.randint(8000, 45000)
    
    detalles = {'producto_actual': producto, 'monto_renta': monto}
    instruccion = generar_instruccion_ia(perfil, detalles)
    
    try:
        # Usamos el modelo más reciente y estable
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])
        
        # Enviamos el contexto y obtenemos la primera objeción
        response = chat.send_message(instruccion)
        objecion_inicial = chat.send_message("Preséntate brevemente y lanza tu primera objeción.").text
        
        st.session_state.chat_history = chat
        st.session_state.mensajes = [
            {"role": "assistant", "content": f"**CASO NUEVO:**\n- **Cliente:** {perfil['nombre']} ({perfil['tipo']})\n- **Producto:** {producto}\n- **Renta:** ${monto:,} MXN"},
            {"role": "assistant", "content": objecion_inicial}
        ]
    except Exception as e:
        st.error(f"Error al conectar con Gemini: {e}")

def handle_chat():
    if st.session_state.user_input:
        user_text = st.session_state.user_input
        st.session_state.mensajes.append({"role": "user", "content": user_text})
        
        try:
            response = st.session_state.chat_history.send_message(user_text)
            st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error en la respuesta: {e}")

# --- Interfaz Principal ---
st.title("🤝 Simulador de Negociación MoradaUno")

if st.button("🚀 Iniciar Nueva Simulación"):
    iniciar_simulacion()

# Mostrar Chat
for msg in st.session_state.get("mensajes", []):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if "chat_history" in st.session_state:
    st.chat_input("Escribe tu respuesta aquí...", key="user_input", on_submit=handle_chat)
else:
    st.info("Haz clic en 'Iniciar Nueva Simulación' para comenzar.")
