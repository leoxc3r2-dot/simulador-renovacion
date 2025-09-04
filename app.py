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
    
    reglas_generales = f"""
    Eres el/la {perfil['tipo']} llamado/a {perfil['nombre']}. Tu personalidad es '{perfil
