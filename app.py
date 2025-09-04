import streamlit as st
import random
import google.generativeai as genai

# --- Configuración de la Página Web y Estilo ---
st.set_page_config(page_title="Simulador de Renovaciones", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container { background: #F3E5F5; }
    .css-1d391kg { background-color: #EDE7F6; }
    .stButton>button { background-color: #9C27B0; color: white; border-radius: 10px; padding: 10px 24px; border: none; }
    .stButton>button:hover { background-color: #BA68C8; }
    .st-d { font-family: 'Arial'; }
    .st-emotion-cache-183n41b p { background-color: #E1BEE7; padding: 10px; border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configura tu clave de API de forma segura ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- Listas de datos para la simulación aleatoria ---
perfiles_brokers = [
    {'nombre': 'Carlos Ruiz', 'tipo': 'broker', 'personalidad': 'Orientado a resultados.', 'motivacion': 'Busca una renovación rápida y con buena comisión.'},
    {'nombre': 'Laura Gómez', 'tipo': 'broker', 'personalidad': 'Meticulosa, se preocupa por los detalles.', 'motivacion': 'Quiere estar segura de que la póliza cubre todo sin fallos.'},
    {'nombre': 'Diego López', 'tipo': 'broker', 'personalidad': 'Amistoso y conversador.', 'motivacion': 'Se basa en la relación de confianza que tiene con el propietario.'},
    {'nombre': 'Fernanda Torres', 'tipo': 'broker', 'personalidad': 'Escéptica, se enfoca en el valor.', 'motivacion': 'Necesita ver el retorno de inversión y que el producto valga el costo.'},
    {'nombre': 'Andrés Mora', 'tipo': 'broker', 'personalidad': 'Joven, quiere aprender.', 'motivacion': 'Se siente inseguro y busca la mejor opción para no equivocarse.'},
]

perfiles_propietarios = [
    {'nombre': 'Alicia Mendoza', 'tipo': 'propietario', 'personalidad': 'Ahorradora, se fija en los precios.', 'motivacion': 'Busca el mejor precio para renovar sin perder beneficios.'},
    {'nombre': 'Ricardo Solís', 'tipo': 'propietario', 'personalidad': 'Exigente, le gusta el control.', 'motivacion': 'Le preocupa la puntualidad de los pagos de renta y los contratos.'},
    {'nombre': 'Isabel Castro', 'tipo': 'propietario', 'personalidad': 'Relajada y ocupada.', 'motivacion': 'Quiere el proceso más sencillo y rápido posible, sin complicaciones.'},
    {'nombre': 'Juan Vargas', 'tipo': 'propietario', 'personalidad': 'Experimentado en rentas.', 'motivacion': 'Se cree experto y tiene sus propias ideas sobre el mercado inmobiliario.'},
    {'nombre': 'Sofía Hernández', 'tipo': 'propietario', 'personalidad': 'Primeriza, se asusta fácilmente.', 'motivacion': 'Quiere la mayor protección posible y que le expliquen todo con calma.'},
]

perfiles_de_simulacion = perfiles_brokers + perfiles_propietarios

tipos_de_producto = [
    'M12 Habitacional', 'M12 Comercial',
    'M3 Habitacional', 'M3 Comercial',
    'MLegal Habitacional', 'MLegal Comercial',
    'M3 Light Habitacional', 'M3 Light Comercial'
]
rango_renta = (1000, 100000)

# --- Lógica de la Simulación ---
def generar_instruccion_ia(perfil, detalles_del_caso):
    reglas_generales = f"""
    Eres el/la {perfil['tipo']} llamado/a {perfil['nombre']}. Tu personalidad es '{perfil['personalidad']}' y tu motivación principal es: '{perfil['motivacion']}'.
    
    Detalles de la renovación:
    - Producto actual: {detalles_del_caso['producto_actual']}
    - Uso de suelo: {detalles_del_caso['uso_suelo']}
    - Monto de renta: ${detalles_del_caso['monto_renta']:,} MXN
    
    Reglas del juego:
    - Debes poner objeciones lógicas basadas en tu perfil.
    - Puedes preguntar en ocasiones si la renovación tendrá algún descuento y si puede tener algún descuento adicional.
    - Puedes pedir en ocasiones cambios de productos por otro diferente al que tienes.
    """
    if perfil['tipo'] == 'broker':
        reglas_especificas = "Como broker, obtienes una comisión por la renovación. Tu motivación es también lograr la renovación por la comisión."
    else:
        reglas_especificas = "Eres el/la propietario/a directo/a. No obtienes ninguna comisión."
    
    return f"{reglas_generales}\n{reglas_especificas}\nTu objetivo es ser persuadido/a para renovar. Responde de forma natural y realista."

def iniciar_simulacion():
    perfil_aleatorio = random.choice(perfiles_de_simulacion)
    monto_renta_aleatorio = random.randint(rango_renta[0], rango_renta[1])
    producto_elegido = random.choice(tipos_de_producto)
    uso_suelo_elegido = 'Habitacional' if 'Habitacional' in producto_elegido else 'Comercial'
    
    detalles_del_caso = {
        'producto_actual': producto_elegido,
        'uso_suelo': uso_suelo_elegido,
        'monto_renta': monto_renta_aleatorio
    }
    
    st.session_state.perfil_actual = perfil_aleatorio
    st.session_state.detalles_del_caso = detalles_del_caso
    
    instruccion = generar_instruccion_ia(perfil_aleatorio, detalles_del_caso)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat_history = model.start_chat(history=[{"role": "user", "parts": [instruccion]}])
    
    objecion_inicial = st.session_state.chat_history.send_message("Da tu objeción inicial para que el agente te convenza.").text
    
    st.session_state.mensajes.append({"role": "assistant", "content": f"**Perfil:** {perfil_aleatorio['nombre']} ({perfil_aleatorio['tipo']})\n\n**Detalles del Caso:**\n- **Producto:** {detalles_del_caso['producto_actual']}\n- **Renta:** ${detalles_del_caso['monto_renta']:,}\n\n**{perfil_aleatorio['nombre']}:** {objecion_inicial}"})

# --- Interfaz de Usuario de Streamlit ---
st.title("Simulador de Negociación para Renovaciones")

st.markdown("""
    Este simulador te ayuda a practicar el manejo de objeciones con brokers y propietarios inmobiliarios.
    Cada vez que inicies una simulación, te enfrentarás a un perfil aleatorio con sus propias motivaciones y reglas de negocio.

    **Instrucciones:**
    1. Presiona el botón **"Iniciar Simulación"** para comenzar.
    2. Lee la objeción del broker o propietario y escribe tu respuesta en el chat.
    3. Tu objetivo es convencerlo de renovar, abordando sus objeciones de forma lógica y persuasiva.
    4. Escribe la palabra **"terminar"** en el chat para finalizar la simulación en cualquier momento.
""")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    
if st.button("Iniciar Simulación"):
    st.session_state.mensajes = []
    iniciar_simulacion()
    
for msg in st.session_state.mensajes:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Escribe tu respuesta aquí..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    if prompt.lower() == "terminar":
        st.session_state.mensajes.append({"role": "assistant", "content": "Simulación finalizada. ¡Buen trabajo!"})
    else:
        with st.spinner("Pensando..."):
            response = st.session_state.chat_history.send_message(prompt)
            st.session_state.mensajes.append({"role": "assistant", "content": response.text})
    st.experimental_rerun()
