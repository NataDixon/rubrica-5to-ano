import streamlit as st
import pandas as pd
import uuid
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Evaluación Emprendimientos - 5to Año",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Evaluación de Emprendimientos")
st.caption("Exposición de Proyectos de 5to Año")

# ---------------------------------------------------------
# CONEXIÓN NATIVA A GOOGLE SHEETS
# ---------------------------------------------------------
@st.cache_resource
@st.cache_resource
def obtener_conexion_gsheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Extraemos el diccionario de secretos y limpiamos a fondo la clave privada
    secrets_dict = dict(st.secrets["connections"]["gsheets"])
    if "private_key" in secrets_dict:
        pk = secrets_dict["private_key"]
        # Limpia comillas escapadas, espacios y convierte \n de texto a saltos reales
        pk = pk.replace("\\n", "\n").strip('"').strip("'").strip()
        secrets_dict["private_key"] = pk
        
    creds = Credentials.from_service_account_info(secrets_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Abrir la planilla por URL
    url_sheet = secrets_dict["spreadsheet"]
    sheet = client.open_by_url(url_sheet).worksheet("Respuestas")
    return sheet

def cargar_datos():
    try:
        sheet = obtener_conexion_gsheets()
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

# ---------------------------------------------------------
# ESTRUCTURA DE LA RÚBRICA (25 Subcriterios)
# ---------------------------------------------------------
ESTRUCTURA_RUBRICA = {
    "1. Presentación: Pitch, comunicación y defensa del proyecto (25%)": {
        "peso_categoria": 0.25,
        "subcriterios": {
            "S1_PitchClaro": "a. Presentan un Pitch claro, organizado y atractivo.",
            "S2_ComunicacionFluida": "b. Comunican las ideas de manera fluida y comprensible.",
            "S3_SeguridadDominio": "c. Demuestran seguridad, convicción y dominio del emprendimiento.",
            "S4_FundamentoDecisiones": "d. Fundamentan y justifican las decisiones tomadas.",
            "S5_RecursosIdentidad": "e. Utilizan adecuadamente recursos visuales, identidad de marca (logo, paleta de colores) y prototipo/producto en el stand para reforzar la presentación."
        }
    },
    "2. Idea de negocio, innovación y propuesta de valor (20%)": {
        "peso_categoria": 0.20,
        "subcriterios": {
            "S6_IdeaPropuestaValor": "a. Presentan claramente la idea de negocio y comunican con claridad su propuesta de valor.",
            "S7_NecesidadReal": "b. Identifican una necesidad, problema u oportunidad real.",
            "S8_RespuestaNecesidad": "c. Explican cómo su producto/servicio responde a esa necesidad.",
            "S9_CreatividadInnovacion": "d. Demuestran creatividad e innovación.",
            "S10_Diferenciación": "e. Identifican qué diferencia a su emprendimiento de otras propuestas."
        }
    },
    "3. Mercado y estrategia de comercialización (15%)": {
        "peso_categoria": 0.15,
        "subcriterios": {
            "S11_ClienteObjetivo": "a. Identifican claramente el cliente o público objetivo.",
            "S12_NecesidadesCliente": "b. Reconocen las características y necesidades de sus potenciales clientes.",
            "S13_AnalisisCompetencia": "c. Identifican competidores y reconocen fortalezas/debilidades frente a ellos.",
            "S14_PromocionEstrategia": "d. Definen estrategias de promoción y comunicación (diseño de marca, logo y material publicitario digital/impreso).",
            "S15_CanalesVenta": "e. Identifican canales de venta adecuados."
        }
    },
    "4. Planificación financiera y uso de Excel (25%)": {
        "peso_categoria": 0.25,
        "subcriterios": {
            "S16_CostosFijosVariables": "a. Identifican y clasifican correctamente costos fijos y variables.",
            "S17_PrecioVenta": "b. Determinan adecuadamente el precio de venta.",
            "S18_InversionInicial": "c. Identifican la inversión/capital inicial necesario.",
            "S19_PuntoEquilibrio": "d. Calculan correctamente el punto de equilibrio e interpretan qué representa.",
            "S20_UsoExcelFormulas": "e. Utilizan correctamente las planillas de Excel, fórmulas y herramientas trabajadas, presentando la información financiera de forma clara y ordenada."
        }
    },
    "5. Producción, gestión e impacto (15%)": {
        "peso_categoria": 0.15,
        "subcriterios": {
            "S21_ProcesoProduccion": "a. Explican claramente el proceso de producción o prestación del servicio.",
            "S22_RecursosNecesarios": "b. Identifican los recursos necesarios para llevar adelante el emprendimiento.",
            "S23_OrganizacionTareas": "c. Organizan adecuadamente tareas, tiempos y materiales.",
            "S24_ImpactoEcoSocAmb": "d. Reconocen el impacto económico, social y/o ambiental de su propuesta.",
            "S25_ResoluciónProblemas": "e. Demuestran capacidad para resolver dificultades y tomar decisiones."
        }
    }
}

tab_evaluar, tab_historial, tab_dashboard = st.tabs([
    "📝 Evaluar Proyectos", 
    "🔍 Ver / Editar Registros", 
    "📊 Resultados en Vivo"
])

# ---------------------------------------------------------
# PESTAÑA 1: EVALUAR
# ---------------------------------------------------------
with tab_evaluar:
    st.info("Califique de 1 (Ausencia del factor / Muy flojo) a 5 (Cumple satisfactoriamente).")
    
    with st.form("form_evaluacion", clear_on_submit=True):
        jurado = st.text_input("Nombre del Jurado Evaluador:")
        emprendimiento = st.selectbox("Seleccione el Emprendimiento:", [
            "Grupo 1 - KAIRÓS",
            "Grupo 2 - 4PATYS",
            "Grupo 3 - BIOSTICK",
            "Grupo 4 - DELICIA",
            "Grupo 5 - MY KEY",
            "Grupo 6 - SUEÑO DECORADO",
            "Grupo 7 - CHATARREROS",
            "Grupo 8 - RED LILY",
            "Grupo 9 - TENTACIÓN EXTREMA",
            "Grupo 10 - EL RINCON DE LA MADERA",
            "Grupo 11 - ARTE EN MASA",
            "Grupo 12 - ESTAMPAAMIGOS",
            "Grupo 13 - BATIPOWER",
            "Grupo 14 - DELICIAS SALUDABLES",
            "Grupo 15 - MAKEUP LAIMIL",
            "Grupo 16 - ECOFLOWERS",
            "Grupo 17 - ASTERIA",
            "Grupo 18 - GOATS",
            "Grupo 19 - EL RINCÓN DE MYA"
        ])
        
        respuestas = {}
        
        for cat_nombre, cat_data in ESTRUCTURA_RUBRICA.items():
            st.markdown(f"### {cat_nombre}")
            for key_id, label_texto in cat_data["subcriterios"].items():
                respuestas[key_id] = st.slider(label_texto, 1, 5, 3, key=f"inp_{key_id}")
                
        observaciones = st.text_area("Observaciones del Jurado:")
        btn_enviar = st.form_submit_button("💾 Enviar Evaluación", use_container_width=True)
        
        if btn_enviar:
            if not jurado.strip():
                st.error("⚠️ Por favor, ingrese su nombre de jurado.")
            else:
                puntaje_acumulado = 0.0
                factores_criticos = 0
                
                for cat_nombre, cat_data in ESTRUCTURA_RUBRICA.items():
                    sub_keys = list(cat_data["subcriterios"].keys())
                    cant_items = len(sub_keys)
                    peso_categoria = cat_data["peso_categoria"]
                    
                    for k in sub_keys:
                        val = respuestas[k]
                        if val <= 2:
                            factores_criticos += 1
                        puntaje_acumulado += (val * (peso_categoria / cant_items) * 20)
                
                puntaje_total = round(puntaje_acumulado, 2)
                
                if puntaje_total >= 90:
                    dictamen = "El esquema es muy bueno"
                elif puntaje_total >= 75:
                    dictamen = "Oportunidad es buena y existen actividades posibles para apoyar la iniciativa empresarial"
                elif puntaje_total >= 61:
                    dictamen = "Existen oportunidades"
                elif puntaje_total >= 46:
                    dictamen = "Existen algunas oportunidades pero se debe estudiar mejor la Innovación y el valor agregado"
                elif puntaje_total >= 31:
                    dictamen = "Oportunidad baja"
                else:
                    dictamen = "Oportunidad muy baja"
                
                nuevo_registro = [
                    str(uuid.uuid4())[:8],
                    jurado.strip(),
                    emprendimiento,
                    puntaje_total,
                    dictamen,
                    factores_criticos,
                    observaciones,
                    *[respuestas[k] for k in respuestas]
                ]
                
                try:
                    sheet = obtener_conexion_gsheets()
                    sheet.append_row(nuevo_registro)
                    st.success(f"✅ Evaluación guardada con éxito. Puntaje final: **{puntaje_total}/100 pts** ({dictamen})")
                except Exception as ex:
                    st.error(f"Error al guardar los datos en Google Sheets: {ex}")

# ---------------------------------------------------------
# PESTAÑA 2: MODIFICAR / BORRAR
# ---------------------------------------------------------
with tab_historial:
    st.subheader("Historial de Evaluaciones Cargadas")
    df_reg = cargar_datos()
    
    if df_reg.empty or "ID" not in df_reg.columns:
        st.write("Aún no hay evaluaciones registradas.")
    else:
        st.dataframe(df_reg[["ID", "Jurado", "Emprendimiento", "Puntaje_Total", "Dictamen", "Factores_Criticos"]], use_container_width=True)
        
        st.divider()
        opciones = df_reg.apply(lambda x: f"{x['ID']} - {x['Jurado']} ({x['Emprendimiento']})", axis=1).tolist()
        sel = st.selectbox("Seleccione la evaluación a eliminar:", opciones)
        
        if sel:
            id_sel = sel.split(" - ")[0]
            if st.button("🗑️ Eliminar Registro", type="secondary"):
                try:
                    sheet = obtener_conexion_gsheets()
                    cell = sheet.find(id_sel)
                    if cell:
                        sheet.delete_rows(cell.row)
                        st.warning("Registro borrado correctamente.")
                        st.rerun()
                except Exception as ex:
                    st.error(f"No se pudo eliminar el registro: {ex}")

# ---------------------------------------------------------
# PESTAÑA 3: RESULTADOS EN TIEMPO REAL
# ---------------------------------------------------------
with tab_dashboard:
    st.subheader("🏆 Ranking y Resultados en Tiempo Real")
    df_dash = cargar_datos()
    
    if not df_dash.empty and "Emprendimiento" in df_dash.columns:
        df_dash["Puntaje_Total"] = pd.to_numeric(df_dash["Puntaje_Total"], errors='coerce')
        df_dash["Factores_Criticos"] = pd.to_numeric(df_dash["Factores_Criticos"], errors='coerce')
        
        resumen = df_dash.groupby("Emprendimiento").agg(
            Promedio_Ponderado=("Puntaje_Total", "mean"),
            Cant_Evaluaciones=("Jurado", "count"),
            Total_Factores_Criticos=("Factores_Criticos", "sum")
        ).reset_index()
        
        resumen["Promedio_Ponderado"] = resumen["Promedio_Ponderado"].round(2)
        resumen = resumen.sort_values(by="Promedio_Ponderado", ascending=False).reset_index(drop=True)
        resumen.index += 1
        
        st.dataframe(resumen, use_container_width=True)
        st.bar_chart(data=resumen, x="Emprendimiento", y="Promedio_Ponderado")
