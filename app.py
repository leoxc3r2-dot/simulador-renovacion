import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnóstico MoradaUno", layout="wide")

# 1. Configuración de API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ No se encontró GOOGLE_API_KEY en Secrets.")
    st.stop()

st.title("🛠 Panel de Diagnóstico y Simulación")

# --- BLOQUE DE DIAGNÓSTICO ---
# Esto nos dirá exactamente qué modelos ve tu cuenta
with st.expander("Ver modelos disponibles en tu cuenta"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write(models)
    except Exception as e:
        st.error(f"No se pudo listar los modelos: {e}")

# --- LÓGICA DE LA IA ---
def probar_conexion():
    # Intentaremos con el nombre más genérico posible
    # Si falla, prueba cambiar 'gemini-1.5-flash' por 'gemini-pro' aquí abajo
    nombre_modelo = 'gemini-1.5-flash' 
    
    try:
        model = genai.GenerativeModel(nombre_modelo)
        # Prueba de vida simple
        response = model.generate_content("Hola, responde solo con la palabra 'CONECTADO'")
        
        st.success(f"✅ ¡Conexión exitosa con {nombre_modelo}!")
        st.info(f"Respuesta de la IA: {response.text}")
        
        # Guardar en sesión para el simulador
        st.session_state.model_ready = True
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.mensajes = [{"role": "assistant", "content": "¡Listo! ¿En qué puedo ayudarte con la renovación?"}]
        
    except Exception as e:
        st.error("❌ Error de conexión todavía activo.")
        st.warning(f"Detalle técnico: {e}")
        st.info("Sugerencia: Si en la lista de arriba aparece 'models/gemini-pro', intenta usar ese.")

# --- INTERFAZ ---
if st.button("🔌 Probar Conexión y Despertar IA"):
    probar_conexion()

# Mostrar chat solo si la conexión funciona
if st.session_state.get("model_ready"):
    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    if prompt := st.chat_input("Escribe tu respuesta..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        response = st.session_state.chat.send_message(prompt)
        st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"): st.write(response.text)
