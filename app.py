import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import uuid

st.set_page_config(
    page_title="Evaluación Emprendimientos - 5to Año",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Evaluación de Emprendimientos")
st.caption("Feria de Proyectos de 5to Año")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos():
    try:
        return conn.read(worksheet="Respuestas", ttl=0)
    except Exception:
        return pd.DataFrame()

# Mapeo exacto de Criterios, Porcentajes y Subcriterios según imagen
ESTRUCTURA_RUBRICA = {
    "Entrevista y presentación (10%)": {
        "peso_categoria": 0.10,
        "subcriterios": {
            "S1_ClaridadExposicion": "1. Claridad en tema expuesto",
            "S2_SeguridadDominio": "2. Seguridad y dominio del tema",
            "S3_CreerIdea": "3. Proyecta creer en la idea de negocio"
        }
    },
    "Idea de negocio e innovación (20%)": {
        "peso_categoria": 0.20,
        "subcriterios": {
            "S4_IdeaClaraCoherente": "4. Idea de negocio definida, clara y coherente",
            "S5_ResuelveProblema": "5. La idea de negocio resuelve un problema o satisface una necesidad",
            "S6_DiferenteExistente": "6. Ofrece algo diferente a lo existente en el mercado u ofrece adicionalidades significativas",
            "S7_ValorAgregado": "7. El producto/servicio da beneficios o valor agregado al cliente y puede tener acogida en el mercado",
            "S8_EntornoDesarrollo": "8. Idea de negocio coherente con el entorno donde se pretende desarrollar"
        }
    },
    "Mercadeo (20%)": {
        "peso_categoria": 0.20,
        "subcriterios": {
            "S9_ClientesDefinidos": "9. Define quienes son y donde estan los clientes",
            "S10_ProductosClaros": "10. Define con claridad los productos y servicios a vender",
            "S11_IdentificaCompetencia": "11. Conocen e identifican a su competencia",
            "S12_VentajasCompetitivas": "12. Presenta ventajas competitivas claras y definidas",
            "S13_EstrategiasPublicidad": "13. Las estrategias de publicidad y promocion son claras y coherentes"
        }
    },
    "Producción y administración (15%)": {
        "peso_categoria": 0.15,
        "subcriterios": {
            "S14_ProcesoProduccion": "14. El proceso de producción del producto/servicio es claro y definido",
            "S15_GeneracionEmpleo": "15. Tiene capacidad de generación de empleo directo y/o indirecto",
            "S16_ImpactosPositivos": "16. Genera impactos económico, social y ambiental positivos en su entorno"
        }
    },
    "Finanzas (20%)": {
        "peso_categoria": 0.20,
        "subcriterios": {
            "S17_CostosGastos": "17. Se han considerado todos los costos y gastos de operación",
            "S18_InversionCoherente": "18. La inversión requerida es coherente con el negocio"
        }
    },
    "Equipo de emprendedores (15%)": {
        "peso_categoria": 0.15,
        "subcriterios": {
            "S19_ExperienciaEquipo": "19. La experiencia y conocimientos del equipo de emprendedores es adecuada",
            "S20_AporteFinanciero": "20. Hay aporte financiero y/o recursos de parte del grupo emprendedor"
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
    st.info("Puntaje de 1 (Ausencia del factor) a 5 (Se cumple satisfactoriamente).")
    
    with st.form("form_evaluacion", clear_on_submit=True):
        jurado = st.text_input("Nombre del Jurado Evaluador:")
        emprendimiento = st.selectbox("Seleccione el Emprendimiento:", [
            "Grupo 1 - Proyecto Alpha",
            "Grupo 2 - Proyecto Beta",
            "Grupo 3 - Proyecto Gamma"
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
                st.error("⚠️ Ingrese su nombre de jurado.")
            else:
                # Cálculo de puntaje ponderado exacto
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
                        # Cada punto asignado (1 a 5) aporta proporcionalmente al % del criterio sobre 100
                        puntaje_acumulado += (val * (peso_categoria / cant_items) * 20)
                
                puntaje_total = round(puntaje_acumulado, 2)
                
                # Dictamen según tabla de instrucciones
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
                
                nuevo_registro = {
                    "ID": str(uuid.uuid4())[:8],
                    "Jurado": jurado.strip(),
                    "Emprendimiento": emprendimiento,
                    "Puntaje_Total": puntaje_total,
                    "Dictamen": dictamen,
                    "Factores_Criticos": factores_criticos,
                    "Observaciones": observaciones,
                    **respuestas
                }
                
                df_actual = cargar_datos()
                df_nuevo = pd.concat([df_actual, pd.DataFrame([nuevo_registro])], ignore_index=True)
                conn.update(worksheet="Respuestas", data=df_nuevo)
                
                st.success(f"✅ Guardado. Puntaje: **{puntaje_total}/100** ({dictamen})")

# ---------------------------------------------------------
# PESTAÑA 2: MODIFICAR / BORRAR
# ---------------------------------------------------------
with tab_historial:
    st.subheader("Historial de Evaluaciones Cargadas")
    df_reg = cargar_datos()
    
    if df_reg.empty or "ID" not in df_reg.columns:
        st.write("Sin evaluaciones aún.")
    else:
        st.dataframe(df_reg[["ID", "Jurado", "Emprendimiento", "Puntaje_Total", "Dictamen"]], use_container_width=True)
        
        st.divider()
        opciones = df_reg.apply(lambda x: f"{x['ID']} - {x['Jurado']} ({x['Emprendimiento']})", axis=1).tolist()
        sel = st.selectbox("Seleccione evaluación a corregir:", opciones)
        
        if sel:
            id_sel = sel.split(" - ")[0]
            idx = df_reg[df_reg["ID"] == id_sel].index[0]
            
            if st.button("🗑️ Eliminar Registro", type="secondary"):
                df_mod = df_reg.drop(idx).reset_index(drop=True)
                conn.update(worksheet="Respuestas", data=df_mod)
                st.warning("Registro borrado.")
                st.rerun()

# ---------------------------------------------------------
# PESTAÑA 3: RESULTADOS EN TIEMPO REAL
# ---------------------------------------------------------
with tab_dashboard:
    st.subheader("🏆 Posiciones en Tiempo Real")
    df_dash = cargar_datos()
    
    if not df_dash.empty and "Emprendimiento" in df_dash.columns:
        df_dash["Puntaje_Total"] = pd.to_numeric(df_dash["Puntaje_Total"], errors='coerce')
        
        resumen = df_dash.groupby("Emprendimiento").agg(
            Promedio_Ponderado=("Puntaje_Total", "mean"),
            Cant_Evaluaciones=("Jurado", "count")
        ).reset_index()
        
        resumen["Promedio_Ponderado"] = resumen["Promedio_Ponderado"].round(2)
        resumen = resumen.sort_values(by="Promedio_Ponderado", ascending=False).reset_index(drop=True)
        resumen.index += 1
        
        st.dataframe(resumen, use_container_width=True)
        st.bar_chart(data=resumen, x="Emprendimiento", y="Promedio_Ponderado")
