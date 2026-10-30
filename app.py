import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io

# Configuração da página
st.set_page_config(
    page_title="Gerenciador de RDO - Sala Técnica",
    page_icon="🚧",
    layout="wide"
)

# Inicialização do banco de dados na sessão (Session State)
if "rdos_db" not in st.session_state:
    st.session_state["rdos_db"] = []


# Função para gerar o PDF formatado do RDO
def gerar_pdf_rdo(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Cabeçalho
    pdf.cell(0, 10, "RELATÓRIO DIÁRIO DE OBRA (RDO)", ln=True, align="C")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(5)
    
    # Tabela/Campos do RDO
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Detalhes do Registro:", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 10)
    for chave, valor in dados.items():
        # Trata o texto para evitar problemas de codificação no FPDF
        texto_chave = str(chave).encode('latin-1', 'replace').decode('latin-1')
        texto_valor = str(valor).encode('latin-1', 'replace').decode('latin-1')
        
        if chave == "Descrição":
            pdf.ln(3)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 6, f"{texto_chave}:", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 6, texto_valor)
            pdf.ln(3)
        else:
            pdf.cell(60, 6, f"{texto_chave}:", b=0)
            pdf.cell(0, 6, texto_valor,
