import streamlit as st
import random
import google.generativeai as genai
from IPython.display import display, HTML

# Esta configuración de Streamlit no funcionará en Colab,
# pero el resto del código es compatible.

# --- Configura tu clave de API ---
GOOGLE_API_KEY = "TU_CLAVE_API"
genai.configure(api_key=GOOGLE_API_KEY)

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
    
    instruccion = generar_instruccion_ia(perfil_aleatorio, detalles_del_caso)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_history = model.start_chat(history=[{"role": "user", "parts": [instruccion]}])
    
    objecion_inicial = chat_history.send_message("Da tu objeción inicial para que el agente te convenza.").text
    
    display(HTML(f"<b>--- SIMULACIÓN INICIADA ---</b><br><b>Perfil:</b> {perfil_aleatorio['nombre']} ({perfil_aleatorio['tipo']})<br><b>Producto:</b> {detalles_del_caso['producto_actual']}<br><b>Renta:</b> ${detalles_del_caso['monto_renta']:,}<br><br><b>{perfil_aleatorio['nombre']}:</b> {objecion_inicial}"))

    while True:
        tu_respuesta = input("\nTu respuesta: ")
        if tu_respuesta.lower() in ["terminar", "fin", "finalizar"]:
            print("\n--- SIMULACIÓN FINALIZADA ---")
            break
        
        response = chat_history.send_message(tu_respuesta).text
        print(f"\n{perfil_aleatorio['nombre']}: {response}")