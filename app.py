import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da página
st.set_page_config(
    page_title="Gerenciador de RDO - Sala Técnica",
    page_icon="🚧",
    layout="wide"
)

# Estilização CSS customizada e moderna (com ajuste para exibir imagens por completo)
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    div[data-testid="stForm"] {
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        background-color: var(--background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .rdo-header-box {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        background-color: #fafafa;
        color: #111111;
        margin-bottom: 20px;
    }
    /* Garante que o logo apareça por completo e centralizado verticalmente */
    [data-testid="column"] img {
        object-fit: contain;
        max-height: 70px;
        width: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados em memória (session_state) para salvar os RDOs
if "lista_rdos" not in st.session_state:
    st.session_state.lista_rdos = []

# Cabeçalho global com o Logo ajustado na parte superior esquerda
col_logo, col_titulo = st.columns([1.2, 5.8])
with col_logo:
    try:
        st.image("logo-ellenco.jpg", use_column_width=True)
    except Exception:
        st.warning("⚠️ Logo 'logo-ellenco.jpg' não encontrada.")
with col_titulo:
    st.title("🚧 Sistema de Relatório Diário de Obra (RDO)")
    st.markdown("##### *Sala Técnica — Gestão Integrada de Campo e Escritório*")

st.markdown("---")

# Criação das abas principais com um design mais limpo
aba_formulario, aba_admin = st.tabs(["📝 Lançamento de RDO", "📊 Painel do Administrador"])

with aba_formulario:
    with st.form("form_rdo"):
        st.markdown("##### 👤 Informações Gerais e Contrato")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            cliente = st.text_input("Cliente", placeholder="Nome do Cliente / Contratante")
        with col_g2:
            obra = st.text_input("Obra", placeholder="Nome ou Código da Obra")
        with col_g3:
            centro_custo = st.text_input("Centro de Custo", placeholder="Ex: CC-102030")

        st.markdown("---")
        st.markdown("##### 🌦️ Condições Climáticas e Período")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            tempo = st.selectbox(
                "Condição do Tempo",
                ["Sol", "Nublado", "Chuvoso"]
            )
        with col_c2:
            periodo = st.selectbox(
                "Período",
                ["Integral (Manhã e Tarde)", "Manhã", "Tarde", "Noite"]
            )

        st.markdown("---")
        st.markdown("##### 👤 Responsável pelo Registro")
        responsavel_preenchimento = st.text_input("Nome do Responsável pelo Preenchimento", placeholder="Seu nome completo")
        
        st.markdown("---")
        st.markdown("##### 📍 1. Localização e Referência")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rodovia = st.text_input("Rodovia (ex: SP-280)", placeholder="Ex: SP-300")
        with col2:
            km_inicial = st.number_input("Km Inicial do Trecho", min_value=0.0, format="%.3f", value=0.0)
        with col3:
            data_servico = st.date_input("Data do Serviço", value=datetime.today())

        st.markdown("---")
        st.markdown("##### 📏 2. Estaqueamento e Extensão")
        col4, col5
