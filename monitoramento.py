import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Monitoramento de Sensores", layout="wide")
st.title("📊 Monitoramento de Sensores Industriais")

# --- Limites de operação ---
LIMITES = {
    "Temperatura": {"min": 30, "max": 90},
    "Carga": {"min": 50, "max": 450},
    "Tensão": {"min": 210, "max": 240},
    "Corrosão": {"min": 2, "max": 8}
}

# Dados iniciais
data = pd.DataFrame({
    "Temperatura": [np.random.uniform(20, 100)],
    "Carga": [np.random.uniform(0, 500)],
    "Tensão": [np.random.uniform(200, 250)],
    "Corrosão": [np.random.uniform(0, 10)]
})

placeholder = st.empty()

# Simulação contínua
for i in range(500):
    # Valores variando mais bruscamente
    new_data = pd.DataFrame({
        "Temperatura": [data["Temperatura"].iloc[-1] + np.random.uniform(-10, 10)],
        "Carga": [data["Carga"].iloc[-1] + np.random.uniform(-60, 60)],
        "Tensão": [data["Tensão"].iloc[-1] + np.random.uniform(-10, 10)],
        "Corrosão": [data["Corrosão"].iloc[-1] + np.random.uniform(-1.5, 1.5)]
    })

    # Limita o tamanho do histórico
    data = pd.concat([data, new_data]).tail(60)

    with placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Gráfico em tempo real")
            st.line_chart(data)
        with col2:
            st.subheader("📟 Leituras atuais e alertas")

            for sensor in data.columns:
                valor = new_data[sensor].iloc[0]
                minimo = LIMITES[sensor]["min"]
                maximo = LIMITES[sensor]["max"]

                if valor > maximo:
                    st.error(f"{sensor}: {valor:.2f} ⚠️ ACIMA do limite ({maximo})")
                elif valor < minimo:
                    st.warning(f"{sensor}: {valor:.2f} ⚠️ ABAIXO do mínimo ({minimo})")
                else:
                    st.success(f"{sensor}: {valor:.2f} dentro do normal ✅")

    time.sleep(1)
