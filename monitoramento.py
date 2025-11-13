import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Monitor de Sensores", layout="wide")
st.title("📊 Monitoramento de Sensores com Gráficos e Alertas")

# --- Limites configuráveis ---
st.sidebar.header("⚙️ Limites de Operação por Sensor")
limites = {
    "Temperatura": {
        "min": st.sidebar.number_input("Temperatura - mínimo", value=25.0),
        "max": st.sidebar.number_input("Temperatura - máximo", value=80.0)
    },
    "Carga": {
        "min": st.sidebar.number_input("Carga - mínimo", value=30.0),
        "max": st.sidebar.number_input("Carga - máximo", value=70.0)
    },
    "Tensão": {
        "min": st.sidebar.number_input("Tensão - mínimo", value=200.0),
        "max": st.sidebar.number_input("Tensão - máximo", value=240.0)
    },
    "Corrosão": {
        "min": st.sidebar.number_input("Corrosão - mínimo", value=5.0),
        "max": st.sidebar.number_input("Corrosão - máximo", value=40.0)
    },
}

# --- Inicialização ---
if "dados" not in st.session_state:
    st.session_state.dados = {
        "Temperatura": np.random.uniform(40, 50),
        "Carga": np.random.uniform(45, 55),
        "Tensão": np.random.uniform(210, 225),
        "Corrosão": np.random.uniform(15, 25)
    }

if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=["Tempo", "Temperatura", "Carga", "Tensão", "Corrosão"])

# --- Função de atualização ---
def atualizar_valores():
    for sensor in st.session_state.dados:
        variacao = np.random.uniform(-2, 2)
        st.session_state.dados[sensor] = round(st.session_state.dados[sensor] + variacao, 2)

# --- Área principal ---
placeholder = st.empty()
tempo = 0

while True:
    atualizar_valores()
    tempo += 1

    # Atualiza histórico
    novo_dado = {"Tempo": tempo}
    novo_dado.update(st.session_state.dados)
    st.session_state.historico = pd.concat(
        [st.session_state.historico, pd.DataFrame([novo_dado])],
        ignore_index=True
    )

    # Mantém apenas os últimos 50 pontos
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico.iloc[-50:]

    with placeholder.container():
        st.subheader(" Leituras Atuais")
        cols = st.columns(4)
        alerta_geral = False

        for i, (sensor, valor) in enumerate(st.session_state.dados.items()):
            lim_min = limites[sensor]["min"]
            lim_max = limites[sensor]["max"]

            if valor < lim_min:
                cor = "orange"
                status = f"⚠️ Abaixo ({valor})"
                alerta_geral = True
            elif valor > lim_max:
                cor = "red"
                status = f"🚨 Acima ({valor})"
                alerta_geral = True
            else:
                cor = "green"
                status = f"✅ Normal ({valor})"

            cols[i].markdown(f"### {sensor}")
            cols[i].progress(min((valor - lim_min) / (lim_max - lim_min), 1.0))
            cols[i].write(f"**Status:** {status}")
            cols[i].write(f"**Limites:** {lim_min} - {lim_max}")

        if alerta_geral:
            st.error("⚠️ ALERTA: Um ou mais sensores estão fora dos limites definidos!")
            st.audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg")

        # --- Gráficos ---
        st.subheader("📊 Histórico dos Sensores")
        fig, ax = plt.subplots(2, 2, figsize=(10, 6))
        sensores = ["Temperatura", "Carga", "Tensão", "Corrosão"]

        for i, sensor in enumerate(sensores):
            linha = i // 2
            coluna = i % 2
            ax[linha, coluna].plot(
                st.session_state.historico["Tempo"],
                st.session_state.historico[sensor],
                label=sensor
            )
            ax[linha, coluna].set_title(sensor)
            ax[linha, coluna].grid(True)
            ax[linha, coluna].legend()

        st.pyplot(fig)

    time.sleep(1)
