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
rango_renta_light = (20000, 100000)

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
    
    objeciones_iniciales = [
        "El inquilino se retira, por lo que ya no vamos a necesitar el servicio.",
        "El servicio me parece muy caro, no estoy seguro si vale la pena seguir pagando.",
        "No hemos tenido problemas con los pagos, por lo que no veo la necesidad de seguir pagando la protección.",
        "No estoy seguro de qué tan completo es el servicio, ¿podrías explicarme qué cubre exactamente?",
        "Mi inquilino siempre ha sido muy puntual, tengo mucha confianza en él.",
        "Vamos a vender el inmueble, entonces no es necesario renovar el contrato.",
        "Considero que existen otras formas de proteger mis ingresos, ¿por qué debería elegir MoradaUno?",
    ]
    
    objecion_inicial_elegida = random.choice(objeciones_iniciales)

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
    - Tu primera respuesta debe ser la siguiente objeción: "{objecion_inicial_elegida}"
    - A partir de ahí, debes mantener la conversación y generar nuevas objeciones lógicas basadas en tu perfil.
    - Puedes preguntar por descuentos o cambios en la figura del inquilino o el obligado solidario.
    - Puedes preguntar cómo funcionan las protecciones para tener un mejor entendimiento del servicio.
    
    Además, debes ser capaz de responder a estas preguntas de manera realista:
    - Si te preguntan si habrá un incremento en la renta, elige una de las siguientes respuestas de forma aleatoria:
      - "Sí, me gustaría que la renta subiera conforme al INPC. ¿Cuánto podría subir?"
      - "No, queremos mantener la misma renta."
    - Si se llega a un acuerdo y te preguntan por el nuevo monto de renta, responde con un monto de renta aleatorio dentro de los rangos establecidos. Usa el formato "$[cantidad con comas] MXN", por ejemplo: "$15,500 MXN".
    - Si te preguntan qué producto se contratará, responde con el nombre del producto que se acordó o que tienes actualmente.
    - Si te preguntan quién pagará el servicio, elige una de las siguientes opciones al azar: "100% propietario", "100% inquilino", "50% propietario, 50% inquilino".
    - Si te preguntan por la firma, elige una de las siguientes opciones al azar: "digital" o "presencial".
    - Si te preguntan si quieren hacer un cambio en el contrato, responde de forma aleatoria con "sí" o "no". Si la respuesta es sí, menciona una cláusula aleatoria (por ejemplo: "Sí, me gustaría revisar la cláusula de mascotas" o "Sí, me gustaría ver la cláusula de reparaciones y mantenimiento").
    
    Reglas de formato:
    - **Siempre usa texto plano.** No uses negritas, cursivas, o cualquier otro tipo de formato a menos que sea necesario para resaltar una palabra.
    - **Separa las palabras con espacios.** Asegúrate de que no haya texto corrido como `Esosonaproximadamente`.
    - **Usa el formato numérico correcto.** Cuando menciones una cantidad de dinero, usa el formato con comas y el signo de pesos, por ejemplo: `$73,013 MXN`.
    """
    if perfil['tipo'] == 'broker':
        reglas_especificas = "Como broker, obtienes una comisión por la renovación. Tu motivación es también lograr la renovación por la comisión."
    else:
        reglas_especificas = "Eres el/la propietario/a directo/a. No obtienes ninguna comisión."
    
    return f"{reglas_generales}\n{reglas_especificas}\nTu objetivo es ser persuadido/a para renovar. Responde de forma natural y realista."

def iniciar_simulacion():
    # Inicializa el historial de chat y el estado de la simulación
    perfil_aleatorio = random.choice(perfiles_de_simulacion)
    producto_elegido = random.choice(tipos_de_producto)
    uso_suelo_elegido = 'Habitacional' if 'Habitacional' in producto_elegido else 'Comercial'

    # Lógica para balancear las rentas
    if 'M3 Light' in producto_elegido:
        # Si el producto es M3 Light, la renta siempre será > $20,000
        monto_renta_aleatorio = random.randint(20001, 100000)
    elif random.random() < 0.5:
        # 50% de probabilidad de tener una renta baja (< $20,000) para otros productos
        monto_renta_aleatorio = random.randint(1000, 20000)
    else:
        # 50% de probabilidad de tener una renta alta (> $20,000) para otros productos
        monto_renta_aleatorio = random.randint(20001, 100000)
    
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
    
    objecion_inicial = st.session_state.chat_history.send_message("Inicia la conversación.").text
    
    monto_formateado = f"{detalles_del_caso['monto_renta']:,}"
    
    st.session_state.mensajes = [{"role": "assistant", "content": f"**Perfil:** {perfil_aleatorio['nombre']} ({perfil_aleatorio['tipo']})\n\n**Detalles del Caso:**\n- **Producto:** {detalles_del_caso['producto_actual']}\n- **Renta:** ${monto_formateado}\n\n**{perfil_aleatorio['nombre']}:** {objecion_inicial}"}]

# --- Lógica de Interacción del Chat ---
def handle_chat_input():
    if st.session_state.prompt:
        user_prompt = st.session_state.prompt
        st.session_state.mensajes.append({"role": "user", "content": user_prompt})
        
        if user_prompt.lower() == "terminar":
            st.session_state.mensajes.append({"role
