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
    pdf.cell(0, 10, "RELATORIO DIARIO DE OBRA (RDO)", ln=True, align="C")
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
            pdf.cell(60, 6, f"{texto_chave}:")
            pdf.cell(0, 6, texto_valor, ln=True)
            
    # Retorna o buffer de bytes do PDF (fpdf2)
    return pdf.output()


# Criando as abas da aplicação
aba_formulario, aba_admin = st.tabs(["📝 Novo RDO (Lançamento)", "🔐 Painel Administrador"])


# ==========================================
# ABA 1: FORMULÁRIO ORIGINAL
# ==========================================
with aba_formulario:
    st.title("🚧 Sistema de Relatório Diário de Obra (RDO)")
    st.markdown("### Módulo de Lançamento de Serviços e Estaques")

    with st.form("form_rdo"):
        st.subheader("1. Localização e Referência")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rodovia = st.text_input("Rodovia (ex: SP-280)", placeholder="Ex: SP-300")
        with col2:
            km_inicial = st.number_input("Km Inicial", min_value=0.0, format="%.3f", value=0.0)
        with col3:
            data_servico = st.date_input("Data do Serviço", value=datetime.today())

        st.markdown("---")
        st.subheader("2. Estaqueamento e Extensão")
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
        st.subheader("3. Detalhamento do Serviço")
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
            placeholder="Descreva as atividades executadas, equipamentos utilizados, condições climáticas e observações relevantes..."
        )

        st.markdown("---")
        st.subheader("4. Responsáveis Técnicos e Assinaturas")
        col8, col9 = st.columns(2)
        
        with col8:
            fiscal = st.text_input("Nome do Fiscal / Supervisor", placeholder="Nome completo do Fiscal")
            crea_fiscal = st.text_input("CREA / Órgão do Fiscal", placeholder="Ex: CREA 123456-D")
        with col9:
            engenheiro = st.text_input("Nome do Engenheiro Responsável", placeholder="Nome completo do Engenheiro")
            crea_engenheiro = st.text_input("CREA do Engenheiro", placeholder="Ex: CREA 654321-S")

        # Botão de submissão
        submitted = st.form_submit_button("Gerar e Validar RDO")

    if submitted:
        # Validações básicas
        if not rodovia or not descricao or not fiscal or not engenheiro:
            st.error("⚠️ Por favor, preencha todos os campos obrigatórios (Rodovia, Descrição e Responsáveis).")
        else:
            # Cálculo de extensão (Considerando 1 estaca = 20 metros)
            posicao_inicial_m = (estaca_inicial * 20) + fracao_inicial
            posicao_final_m = (estaca_final * 20) + fracao_final
            extensao_total_m = posicao_final_m - posicao_inicial_m

            if extensao_total_m < 0:
                st.error("Erro: A estaca/fração final não pode ser menor que a inicial.")
            else:
                st.success("✅ RDO validado e processado com sucesso!")
                
                # Montagem do dicionário estruturado para salvar e exportar
                registro_rdo = {
                    "Data": data_servico.strftime('%d/%m/%Y'),
                    "Rodovia": rodovia,
                    "Km Inicial": f"Km {km_inicial:.3f}",
                    "Trecho Executado": f"Est. {estaca_inicial}+{fracao_inicial:.2f} até Est. {estaca_final}+{fracao_final:.2f}",
                    "Extensão Total (m)": f"{extensao_total_m:.2f} m",
                    "Tipo de Serviço": servico,
                    "Descrição": descricao,
                    "Fiscal Responsável": f"{fiscal} ({crea_fiscal})",
                    "Engenheiro Responsável": f"{engenheiro} ({crea_engenheiro})"
                }
                
                # Salva o registro no Session State (Histórico da Sessão)
                st.session_state["rdos_db"].append(registro_rdo)

                st.markdown("---")
                st.subheader("📄 Resumo do Relatório Gerado")
                
                # Exibição dos dados consolidados em formato amigável
                resumo_dados = {
                    "Parâmetro": list(registro_rdo.keys()),
                    "Detalhe": list(registro_rdo.values())
                }
                
                df_resumo = pd.DataFrame(resumo_dados)
                st.table(df_resumo)

                # Opção de exportação para CSV
                csv_data = df_resumo.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Relatório (CSV)",
                    data=csv_data,
                    file_name=f"RDO_{rodovia.replace(' ', '_')}_{data_servico.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )


# ==========================================
# ABA 2: PAINEL DE ADMINISTRAÇÃO
# ==========================================
with aba_admin:
    st.title("🔐 Painel do Administrador")
    st.markdown("### Gestão e Download de Formulários Preenchidos")

    # Controle de Acesso Simples via Senha
    senha_admin = st.text_input("Digite a Senha de Administrador", type="password")
    
    if senha_admin == "admin123":  # Altere para a senha de sua preferência
        st.success("Acesso autorizado.")
        
        total_registros = len(st.session_state["rdos_db"])
        st.metric(label="Total de RDOs Enviados nesta Sessão", value=total_registros)
        
        if total_registros == 0:
            st.info("Nenhum RDO foi preenchido até o momento nesta sessão.")
        else:
            st.markdown("---")
            st.subheader("📋 Lista de Relatórios Cadastrados")
            
            # Tabela geral consolidada
            df_admin = pd.DataFrame(st.session_state["rdos_db"])
            st.dataframe(df_admin, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📄 Exportar RDO Individual em PDF")
            
            # Seleção do RDO individual para geração de PDF
            opcoes_rdo = [f"ID #{i+1} | {rdo['Rodovia']} - {rdo['Data']} ({rdo['Tipo de Serviço']})" for i, rdo in enumerate(st.session_state["rdos_db"])]
            rdo_selecionado_idx = st.selectbox("Selecione um RDO para baixar o PDF", range(total_registros), format_func=lambda x: opcoes_rdo[x])
            
            rdo_escolhido = st.session_state["rdos_db"][rdo_selecionado_idx]
            
            # Gerar o arquivo PDF
            bytes_pdf = gerar_pdf_rdo(rdo_escolhido)
            
            st.download_button(
                label=f"📥 Baixar PDF do RDO #{rdo_selecionado_idx + 1}",
                data=bytes_pdf,
                file_name=f"RDO_ID{rdo_selecionado_idx + 1}_{rdo_escolhido['Rodovia']}.pdf",
                mime="application/pdf"
            )
    elif senha_admin != "":
        st.error("Senha incorreta. Tente novamente.")
