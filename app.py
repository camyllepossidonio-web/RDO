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

# Estilização CSS customizada simulando o formato A4 e fundo azul corporativo
st.markdown("""
    <style>
    /* Fundo geral da aplicação em azul corporativo */
    .stApp {
        background-color: #f0f4f8;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        background-color: #f0f4f8;
    }
    
    /* Formulário principal */
    div[data-testid="stForm"] {
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 6px 16px rgba(11, 37, 69, 0.08);
        background-color: #ffffff;
        border: 1px solid #d9e2ec;
    }
    
    /* Botões */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #102a43;
        color: white;
    }
    
    .stButton button:hover {
        background-color: #243b53;
        color: white;
    }

    /* Formato de Folha A4 para a visualização do relatório gerado */
    .a4-page {
        background-color: #ffffff;
        width: 100%;
        max-width: 800px;
        margin: 20px auto;
        padding: 40px;
        border-radius: 4px;
        box-shadow: 0 8px 24px rgba(16, 42, 67, 0.15);
        border: 1px solid #cbd5e1;
        color: #102a43;
    }
    
    /* Abas customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
        color: #334e68;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #102a43 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados em memória e controle de autenticação
if "lista_rdos" not in st.session_state:
    st.session_state.lista_rdos = []

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False

# Cabeçalho global com o Logo ajustado na parte superior esquerda
col_logo, col_titulo = st.columns([2, 5])
with col_logo:
    try:
        st.image("logo-ellenco.jpg", width=220)
    except Exception:
        st.warning("⚠️ Logo 'logo-ellenco.jpg' não encontrada.")
with col_titulo:
    st.title("🚧 Sistema de Relatório Diário de Obra (RDO)")
    st.markdown("##### *Sala Técnica — Gestão Integrada de Campo e Escritório*")

st.markdown("---")

# Criação das abas principais
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
        col4, col5, col6, col7 = st.columns(4)
        
        with col4:
            estaca_inicial = st.number_input("Estaca Inicial", min_value=0, step=1, value=0)
        with col5:
            fracao_inicial = st.number_input("Fração Inicial (m)", min_value=0.0, max_value=19.99, step=0.01, value=0.0)
        with col6:
            estaca_final = st.number_input("Estaca Final", min_value=0, step=1, value=0)
        with col7:
            fracao_final = st.number_input("Fração Final (m)", min_value=0.0, max_value=19.99, step=0.01, value=0.0)

        st.markdown("---")
        st.markdown("##### ⚙️ 3. Detalhamento do Serviço")
        servico = st.selectbox(
            "Tipo de Serviço",
            [
                "Terraplenagem / Corte",
                "Terraplenagem / Aterro",
                "Camada de Pavimentação (BGS / CBUQ)",
                "Drenagem / OAE",
                "Sinalização Rodoviária",
                "Serviços Preliminares"
            ]
        )
        
        descricao = st.text_area(
            "Descrição Detalhada do Serviço",
            placeholder="Descreva as atividades executadas, equipamentos utilizados e observações relevantes..."
        )

        st.markdown("---")
        st.markdown("##### 👥 4. Responsáveis Técnicos")
        col8, col9 = st.columns(2)
        
        with col8:
            fiscal = st.text_input("Nome do Fiscal / Supervisor", placeholder="Nome completo do Fiscal")
        with col9:
            engenheiro = st.text_input("Nome do Engenheiro Responsável", placeholder="Nome completo do Engenheiro")

        st.markdown("")
        submitted = st.form_submit_button("🚀 Gerar e Validar RDO", use_container_width=True)

    if submitted:
        if not cliente or not obra or not centro_custo or not rodovia or not descricao or not fiscal or not engenheiro or not responsavel_preenchimento:
            st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
        else:
            posicao_inicial_m = (estaca_inicial * 20) + fracao_inicial
            posicao_final_m = (estaca_final * 20) + fracao_final
            extensao_total_m = posicao_final_m - posicao_inicial_m

            if extensao_total_m < 0:
                st.error("Erro: A estaca/fração final não pode ser menor que a inicial.")
            else:
                km_final_calculado = km_inicial + (extensao_total_m / 1000.0)
                
                num_rdo = len(st.session_state.lista_rdos) + 1
                data_formatada = data_servico.strftime('%d %b %Y').capitalize()
                
                novo_rdo = {
                    "Data": data_servico.strftime('%d/%m/%Y'),
                    "Cliente": cliente,
                    "Obra": obra,
                    "Centro de Custo": centro_custo,
                    "Condição do Tempo": tempo,
                    "Período": periodo,
                    "Rodovia": rodovia,
                    "Km Inicial": f"Km {km_inicial:.3f}",
                    "Km Final Calculado": f"Km {km_final_calculado:.3f}",
                    "Trecho Executado": f"Est. {estaca_inicial}+{fracao_inicial:.2f} até Est. {estaca_final}+{fracao_final:.2f}",
                    "Extensão Total (m)": f"{extensao_total_m:.2f} m",
                    "Tipo de Serviço": servico,
                    "Descrição": descricao,
                    "Responsável pelo Preenchimento": responsavel_preenchimento,
                    "Fiscal Responsável": fiscal,
                    "Engenheiro Responsável": engenheiro
                }
                st.session_state.lista_rdos.append(novo_rdo)

                st.success("✅ RDO validado, processado e salvo no painel do administrador com sucesso!")
                
                # --- VISUALIZAÇÃO EM FORMATO DE FOLHA A4 ---
                st.markdown(f"""
                <div class="a4-page">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #102a43; padding-bottom: 10px; margin-bottom: 15px;">
                        <h2 style="margin: 0; color: #102a43; font-size: 1.4rem;">RELATÓRIO DIÁRIO DE OBRA (RDO)</h2>
                        <span style="font-size: 0.9rem; font-weight: bold; color: #555;">#{num_rdo}</span>
                    </div>
                    <div style="font-size: 0.95rem; line-height: 1.6; margin-bottom: 15px;">
                        <b>Data:</b> {data_formatada} ({data_servico.strftime('%A').capitalize()})<br>
                        <b>Cliente:</b> {cliente} &nbsp;|&nbsp; <b>Obra:</b> {obra}<br>
                        <b>Centro de Custo:</b> {centro_custo} &nbsp;|&nbsp; <b>Rodovia:</b> {rodovia}<br>
                        <b>Período:</b> {periodo} &nbsp;|&nbsp; <b>Condição do Tempo:</b> {tempo} ☀️<br>
                        <b>Responsável:</b> {responsavel_preenchimento}
                    </div>
                    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
                    <div style="font-size: 0.95rem; line-height: 1.6;">
                        <b>
