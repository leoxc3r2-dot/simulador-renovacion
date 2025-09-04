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
    {'nombre': 'Laura Gómez', 'tipo': 'broker', 'personalidad': 'Meticulosa, se preocupa por los detalles.', 'motivacion': 'Quiere estar segura de que la protección cubre todo sin fallos.'},
    {'nombre': 'Diego López', 'tipo': 'broker', 'personalidad': 'Amistoso y conversador.', 'motivacion': 'Se basa en la relación de confianza que tiene con el propietario.'},
    {'nombre': 'Fernanda Torres', 'tipo': 'broker', 'personalidad': 'Escéptica, se enfoca en el valor.', 'motivacion': 'Necesita ver el retorno de inversión y que el servicio valga el costo.'},
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

# Información de los servicios de MoradaUno
informacion_productos = {
    'M12 Habitacional': "Ofrece hasta 12 meses de protección de renta, con servicio de protección legal para el inmueble, cubriendo gastos y trámites para su recuperación.",
    'M12 Comercial': "Ofrece hasta 12 meses de protección de renta, con servicio de protección legal para el inmueble, cubriendo gastos y trámites para su recuperación.",
    'M3 Habitacional': "Ofrece hasta 3 meses de protección de renta, con servicio anual de protección legal para el inmueble.",
    'M3 Comercial': "Ofrece hasta 3 meses de protección de renta, con servicio anual de protección legal para el inmueble.",
    'MLegal Habitacional': "Se enfoca en la protección legal. Incluye la asesoría y defensa legal para su propiedad, cubriendo los gastos necesarios para su recuperación.",
    'MLegal Comercial': "Se enfoca en la protección legal. Incluye la asesoría y defensa legal para su propiedad, cubriendo los gastos necesarios para su recuperación.",
    'M3 Light Habitacional': "Actualmente no está disponible. Incluía hasta 3 meses de protección de renta con servicio de protección legal, para rentas superiores a $20,000, con un límite de pago de hasta $10,000.",
    'M3 Light Comercial': "Actualmente no está disponible. Incluía hasta 3 meses de protección de renta con servicio de protección legal, para rentas superiores a $20,000, con un límite de pago de hasta $10,000."
}

# --- Lógica de la Simulación ---
def generar_instruccion_ia(perfil, detalles_del_caso):
    numero_aleatorio = random.randint(1000, 9999)
    inmueble = f"A{numero_aleatorio}"
    
    reglas_generales = f"""
    Eres el/la {perfil['tipo']} llamado/a {perfil['nombre']}. Tu personalidad es '{perfil['personalidad']}' y tu motivación principal es: '{perfil['motivacion']}'.
    
    El contexto es el siguiente: Eres el/la propietario/a del inmueble con folio de renta {inmueble} y estás próximo/a a renovar el servicio de protección de renta con MoradaUno.
    
    Detalles de la renovación:
    - Producto actual: {detalles_del_caso['producto_actual']}
    - Uso de suelo: {detalles_del_caso['uso_suelo']}
    - Monto de renta: ${detalles_del_caso['monto_renta']:,} MXN
    - Inmueble: {inmueble}
    
    Información que tienes sobre el servicio:
    - MoradaUno ofrece un servicio de protección de rentas que cubre el impago de alquiler.
    - La protección de renta es un escudo financiero.
    - Al contratar, el propietario traslada la responsabilidad de pago a MoradaUno. Si el inquilino incumple, MoradaUno paga al propietario y se encarga de los trámites legales y cobranza.
    - El producto actual, {detalles_del_caso['producto_actual']}, se describe así: {informacion_productos[detalles_del_caso['producto_actual']]}.
    - Si tu producto es M3 Light, sabes que ya no está disponible.
    - Tu inquilino actual es el Sr. Juan Pérez y la obligada solidaria es la Sra. Ana García.
    
    Reglas del juego:
    - Debes poner objeciones lógicas basadas en tu perfil.
    - Puedes preguntar por descuentos o cambios en la figura del inquilino o el obligado solidario.
    - Puedes preguntar cómo funcionan las protecciones para tener un mejor entendimiento del servicio.
    - Objeciones comunes a mencionar:
        - "El servicio es caro, y no estoy seguro de si vale la pena seguir pagando."
        - "No he tenido problemas con el pago, por lo que no veo la necesidad de seguir pagando."
        - "Mi inquilino siempre ha sido puntual, tengo confianza en él."
        - "No estoy seguro de qué tan completo es el servicio y qué situaciones exactas cubre."
        - "Considero que existen otras formas de proteger mis ingresos de alquiler."
        - "No estoy completamente seguro de que el servicio de protección de renta funcione como promete."
        - "No quiero complicarme con un proceso de renovación largo o burocrático."
        - Puedes preguntar si la renta subirá conforme a la inflación o si se mantendrá igual.
        - "El inquilino se retira."
        - "Ya se vendió el inmueble."
        - "Vamos a renovar con otro servicio."
        - "Solo haremos los contratos, no la protección."
        - "El costo es muy caro."
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
    
    objecion_inicial = st.session_state.chat_history.send_message("Inicia la conversación como si estuvieras revisando tu próxima renovación y da una primera objeción o pregunta.").text
    
    st.session_state.mensajes.append({"role": "assistant", "content": f"**Perfil:** {perfil_aleatorio['nombre']} ({perfil_aleatorio['tipo']})\n\n**Detalles del Caso:**\n- **Producto:** {detalles_del_caso['producto_actual']}\n- **Renta:** ${detalles_del_caso['monto_renta']:,}\n\n**{perfil_aleatorio['nombre']}:** {objecion_inicial}"})

# --- Interfaz de Usuario de Streamlit ---
st.title("Simulador de Negociación de MoradaUno")

st.markdown("""
    Este simulador te ayuda a practicar el manejo de objeciones con brokers y propietarios inmobiliarios en el contexto de MoradaUno.
    Cada vez que inicies una simulación, te enfrentarás a un perfil aleatorio con sus propias motivaciones y reglas.

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
        st.session_state.mensajes.append({"role": "assistant", "content": "Simulación finalizada. ¡Buen trabajo! Presiona 'Iniciar Simulación' para comenzar de nuevo."})
        del st.session_state.chat_history
    else:
        with st.spinner("Pensando..."):
            response = st.session_state.chat_history.send_message(prompt)
            st.session_state.mensajes.append({"role": "assistant", "content": response.text})
    st.experimental_rerun()
