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

# Estilização CSS customizada e moderna
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
aba_formulario, aba
