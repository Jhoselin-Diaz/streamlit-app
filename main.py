import altair as alt
import streamlit as st
import pandas as pd
import numpy as np

# CONFIGURACIÓN GENERAL

st.set_page_config(
    page_title="Sistema Predictivo Cardiaco",
    layout="wide"
)

st.title("Sistema Predictivo de Enfermedad Cardíaca")
st.write("Aplicación en entorno controlado | Grupo 04")


tab1, tab2, tab3 = st.tabs(["Registro manual", "Cargar Excel", "Gráficos"])

# REGISTRO MANUAL
with tab1:
    st.subheader("Registro manual de datos del paciente")

    col1, col2, col3 = st.columns(3)

    with col1:
        edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
        presion = st.number_input("Presión arterial en reposo", min_value=50, max_value=250)
        colesterol = st.number_input("Colesterol (mg/dL)", min_value=50, max_value=800)

    with col2:
        azucar = st.selectbox("Azúcar en ayunas > 120 mg/dL", ["No", "Sí"])
        ecg = st.selectbox("ECG en reposo", ["Normal", "Anormal", "Hipertrofia"])
        fcmax = st.number_input("Frecuencia cardiaca (lpm)", min_value=60, max_value=250)
        angina = st.selectbox("Angina inducida por ejercicio", ["No", "Sí"])

    with col3:
        oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, step=0.1)
        slope = st.selectbox("Slope", ["Ascendente", "Plana", "Descendente"])
        imc = st.number_input("Índice de Masa Corporal (IMC)", min_value=10.0, max_value=60.0, step=0.1)
        estres = st.slider("Nivel de estrés", 1, 10)
        horas_sueno = st.slider("Horas de sueño", 1, 12)

    # Botón de predicción manual
    if st.button("Predecir con datos ingresados"):

        puntos_riesgo = 0

        # --- Reglas de riesgo --- #
        if colesterol > 240:
            puntos_riesgo += 1
        if presion > 140:
            puntos_riesgo += 1
        if oldpeak > 2.5:
            puntos_riesgo += 1
        if imc > 30:
            puntos_riesgo += 1
        if estres >= 8:
            puntos_riesgo += 1
        if fcmax < 120:
            puntos_riesgo += 1
        if horas_sueno < 5:
            puntos_riesgo += 1

        # Clasificación del riesgo
        if puntos_riesgo >= 3:
            riesgo = "🔴 Riesgo ALTO"
        elif puntos_riesgo >= 1:
            riesgo = "🟡 Riesgo MODERADO"
        else:
            riesgo = "🟢 Riesgo BAJO"

        st.success(f"Resultado del análisis: **{riesgo}**")


# CARGA DATABASE

with tab2:
    st.subheader("Cargar archivo Excel con pacientes")

    archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        df["diagnostico"] = df["diagnostico"].replace({
            "Positivo": 1,
            "Negativo": 0,
            "positivo": 1,
            "negativo": 0,
            "Sí": 1, "Si": 1, "si": 1,
            "No": 0, "no": 0
        }).astype(int)

        st.success("Archivo cargado correctamente ✔")

        st.write("### Vista previa de los datos")
        st.dataframe(df, use_container_width=True)

        # Selección de fila
        idx = st.number_input("Fila del paciente", min_value=0, max_value=len(df)-1, step=1)

        seleccionado = df.iloc[idx]
        st.write("Paciente seleccionado:")
        st.dataframe(seleccionado.to_frame().T)

        if st.button("Predecir paciente seleccionado"):

            puntos_riesgo = 0
            if seleccionado["colesterol"] > 240:
                puntos_riesgo += 1
            if seleccionado["presion_arterial_en_reposo"] > 140:
                puntos_riesgo += 1
            if seleccionado["antiguedad_oldpeak"] > 2.5:
                puntos_riesgo += 1
            if seleccionado["indice_de_masa_corporal_imc"] > 30:
                puntos_riesgo += 1
            if seleccionado["nivel_de_estres"] >= 8:
                puntos_riesgo += 1
            if seleccionado["frecuencia_cardiaca_maxima"] < 120:
                puntos_riesgo += 1
            if seleccionado["horas_de_sueno"] < 5:
                puntos_riesgo += 1

            if puntos_riesgo >= 3:
                riesgo = "🔴 Riesgo ALTO"
            elif puntos_riesgo >= 1:
                riesgo = "🟡 Riesgo MODERADO"
            else:
                riesgo = "🟢 Riesgo BAJO"

            st.success(f"Resultado del análisis: **{riesgo}**")


# GRAFICOS

with tab3:
    st.subheader("Gráficos del dataset")

    if "df" in locals() or "df" in globals():

        # 1. Distribución del colesterol
        st.write("### Distribución del colesterol")
        chart1 = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("colesterol", title="Colesterol (mg/dL)"),
                y=alt.Y("count()", title="Cantidad de pacientes")
            )
        )
        st.altair_chart(chart1, use_container_width=True)

        # 2. Relación IMC vs Colesterol
        st.write("### Relación IMC vs Colesterol")
        chart2 = (
            alt.Chart(df)
            .mark_circle(size=80)
            .encode(
                x=alt.X("indice_de_masa_corporal_imc", title="IMC"),
                y=alt.Y("colesterol", title="Colesterol (mg/dL)"),
                color="diagnostico:N"
            )
        )
        st.altair_chart(chart2, use_container_width=True)

        # 3. Horas de sueño vs Nivel de estrés
        st.write("### Horas de sueño vs Nivel de estrés")
        chart3 = (
            alt.Chart(df)
            .mark_circle(size=80)
            .encode(
                x=alt.X("horas_de_sueno", title="Horas de sueño"),
                y=alt.Y("nivel_de_estres", title="Nivel de estrés"),
            )
        )
        st.altair_chart(chart3, use_container_width=True)

        # 4. Tendencia de diagnóstico según actividad física
        st.write("### Tendencia de diagnóstico según actividad física")
        diag_act = df.groupby("actividad_fisica")["diagnostico"].mean().reset_index()
        diag_act["diagnostico"] *= 100

        chart4 = (
            alt.Chart(diag_act)
            .mark_line(point=True)
            .encode(
                x=alt.X("actividad_fisica:N", title="Actividad física"),
                y=alt.Y("diagnostico:Q", title="% Diagnóstico positivo")
            )
        )
        st.altair_chart(chart4, use_container_width=True)

        # 5. IMC según actividad física
        st.write("### Distribución del IMC según nivel de actividad física")
        imc_act = df.groupby("actividad_fisica")["indice_de_masa_corporal_imc"].mean().reset_index()

        chart5 = (
            alt.Chart(imc_act)
            .mark_bar()
            .encode(
                x=alt.X("actividad_fisica:N", title="Actividad física"),
                y=alt.Y("indice_de_masa_corporal_imc:Q", title="IMC promedio")
            )
        )
        st.altair_chart(chart5, use_container_width=True)

        # 6. Diagnóstico positivo según calidad de dieta
        st.write("### Diagnóstico positivo según calidad de dieta")
        diet = df.groupby("calidad_de_dieta")["diagnostico"].mean().reset_index()
        diet["diagnostico"] *= 100

        chart6 = (
            alt.Chart(diet)
            .mark_bar()
            .encode(
                x=alt.X("calidad_de_dieta:N", title="Calidad de dieta"),
                y=alt.Y("diagnostico:Q", title="% Diagnóstico positivo")
            )
        )
        st.altair_chart(chart6, use_container_width=True)

        # 7. Colesterol según calidad de dieta
        st.write("### Distribución del colesterol según calidad de dieta")
        col_diet = df.groupby("calidad_de_dieta")["colesterol"].mean().reset_index()

        chart7 = (
            alt.Chart(col_diet)
            .mark_bar()
            .encode(
                x=alt.X("calidad_de_dieta:N", title="Calidad de dieta"),
                y=alt.Y("colesterol:Q", title="Colesterol promedio")
            )
        )
        st.altair_chart(chart7, use_container_width=True)

        # 8. Diagnóstico positivo según pendiente (pie chart)
        st.write("### Diagnóstico positivo según tipo de pendiente (Slope)")
        slope = df.groupby("pendiente_slope")["diagnostico"].mean().reset_index()
        slope["diagnostico"] *= 100
        slope["LABEL"] = slope["pendiente_slope"] + " (" + slope["diagnostico"].round(1).astype(str) + "%)"

        pie = (
            alt.Chart(slope)
            .mark_arc()
            .encode(
                theta=alt.Theta("diagnostico:Q", title="% positivo"),
                color=alt.Color("LABEL:N", title="Tipo de pendiente")
            )
        )
        st.altair_chart(pie, use_container_width=True)

        # 9. Oldpeak según pendiente
        st.write("### Distribución del Oldpeak según pendiente (Slope)")
        old_slope = df.groupby("pendiente_slope")["antiguedad_oldpeak"].mean().reset_index()

        chart8 = (
            alt.Chart(old_slope)
            .mark_bar()
            .encode(
                x=alt.X("pendiente_slope:N", title="Tipo de pendiente"),
                y=alt.Y("antiguedad_oldpeak:Q", title="Oldpeak promedio")
            )
        )
        st.altair_chart(chart8, use_container_width=True)

        # 10. Nivel de estrés según diagnóstico
        st.write("### Nivel de estrés según diagnóstico")
        estres = df.groupby("diagnostico")["nivel_de_estres"].mean().reset_index()

        chart9 = (
            alt.Chart(estres)
            .mark_bar()
            .encode(
                x=alt.X("diagnostico:N", title="Diagnóstico (0 = Negativo / 1 = Positivo)"),
                y=alt.Y("nivel_de_estres:Q", title="Nivel promedio de estrés")
            )
        )
        st.altair_chart(chart9, use_container_width=True)

    else:
        st.info("⚠ Primero sube un archivo Excel en la pestaña **Cargar Excel**.")




# INFORMACIÓN FINAL

st.markdown("---")

st.write("Aplicación desarrollada en Streamlit | Entorno controlado - BPA")
st.write("Universidad | 2025")