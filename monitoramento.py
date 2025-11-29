import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# CONFIGURAÇÃO DO APLICATIVO
# ==============================
st.set_page_config(page_title="Monitor de Sensores", layout="wide")
st.title("📊 Monitoramento de Sensores com Gráficos e Alertas")

# Atualização automática (a cada 1 segundo)
st_autorefresh = st.runtime.legacy_caching.clear_cache  # placeholder antigo
st.experimental_rerun

# ==============================
# LIMITE DOS SENSORES (SIDEBAR)
# ==============================
st.sidebar.header("⚙️ Limites de Operação")

limites = {
    "Temperatura": {
        "min": st.sidebar.number_input("Temperatura - mínimo (°C)", value=15.0),
        "max": st.sidebar.number_input("Temperatura - máximo (°C)", value=45.0)
    },
    "Carga Móvel": {
        "min": st.sidebar.number_input("Carga Móvel - mínimo (kN)", value=0.0),
        "max": st.sidebar.number_input("Carga Móvel - máximo (kN)", value=450.0)
    },
    "Carga Distribuída": {
        "min": st.sidebar.number_input("Carga Distribuída - mínimo (kN/m²)", value=0.0),
        "max": st.sidebar.number_input("Carga Distribuída - máximo (kN/m²)", value=5.0)
    },
    "Reação de Apoio": {
        "min": st.sidebar.number_input("Reação de Apoio - mínimo (kN)", value=315.0),
        "max": st.sidebar.number_input("Reação de Apoio - máximo (kN)", value=365.0)
    },
}

# ==============================
# ESTADO DA APLICAÇÃO
# ==============================
if "tempo" not in st.session_state:
    st.session_state.tempo = 0

if "dados" not in st.session_state:
    st.session_state.dados = {
        "Temperatura": np.random.uniform(20, 40),
        "Carga Móvel": np.random.uniform(100, 400),
        "Carga Distribuída": np.random.uniform(1, 4),
        "Reação de Apoio": np.random.uniform(320, 360)
    }

if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=["Tempo"] + list(st.session_state.dados.keys())
    )


# ==============================
# ATUALIZA DADOS
# ==============================
def atualizar_dados():
    for sensor in st.session_state.dados:
        variacao = np.random.uniform(-4, 4)  # variação menor = mais estável
        st.session_state.dados[sensor] = round(st.session_state.dados[sensor] + variacao, 2)


atualizar_dados()
st.session_state.tempo += 1

# salvar histórico
novo_registro = {"Tempo": st.session_state.tempo}
novo_registro.update(st.session_state.dados)

st.session_state.historico = pd.concat(
    [st.session_state.historico, pd.DataFrame([novo_registro])],
    ignore_index=True
)

# mantém só 50 últimos
st.session_state.historico = st.session_state.historico.tail(50)


# ==============================
# TABELA DE STATUS (ATUAL)
# ==============================
st.subheader("📡 Leituras Atuais")
cols = st.columns(4)
houve_alerta = False

for i, (sensor, valor) in enumerate(st.session_state.dados.items()):
    lim_min = limites[sensor]["min"]
    lim_max = limites[sensor]["max"]

    if valor < lim_min:
        status = f"⚠️ Abaixo ({valor})"
        houve_alerta = True
    elif valor > lim_max:
        status = f"🚨 Acima ({valor})"
        houve_alerta = True
    else:
        status = f"✅ Normal ({valor})"

    progresso = (valor - lim_min) / (lim_max - lim_min)
    progresso = max(0, min(1, progresso))

    cols[i].markdown(f"### {sensor}")
    cols[i].progress(progresso)
    cols[i].write(f"**Status:** {status}")
    cols[i].write(f"**Limites:** {lim_min} - {lim_max}")

if houve_alerta:
    st.error("⚠️ ALERTA: Um ou mais sensores estão fora dos limites!")
    st.markdown(
        """
        <audio autoplay style="display:none">
            <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True
    )


# ==============================
# GRÁFICOS
# ==============================
st.subheader("📊 Histórico dos Sensores")
fig, ax = plt.subplots(2, 2, figsize=(10, 6))

sensores = list(st.session_state.dados.keys())

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

st.pyplot(fig)

# força atualização a cada execução
st.experimental_rerun()
