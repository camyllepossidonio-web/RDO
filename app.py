import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Gerenciador de RDO - Sala Técnica",
    page_icon="🚧",
    layout="wide"
)

# Inicializa o banco de dados em memória (session_state) para salvar os RDOs
if "lista_rdos" not in st.session_state:
    st.session_state.lista_rdos = []

# Criação das abas principais
aba_formulario, aba_admin = st.tabs(["📝 Lançamento de RDO", "📊 Painel do Administrador"])

with aba_formulario:
    st.title("🚧 Sistema de Relatório Diário de Obra (RDO)")
    st.markdown("### Módulo de Lançamento de Serviços e Estaques")

    with st.form("form_rdo"):
        st.subheader("1. Localização e Referência")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rodovia = st.text_input("Rodovia (ex: SP-280)", placeholder="Ex: SP-300")
        with col2:
            km_inicial = st.number_input("Km Inicial do Trecho", min_value=0.0, format="%.3f", value=0.0)
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
        with col9:
            engenheiro = st.text_input("Nome do Engenheiro Responsável", placeholder="Nome completo do Engenheiro")

        # Botão de submissão
        submitted = st.form_submit_button("Gerar e Validar RDO")

    if submitted:
        # Validações básicas
        if not rodovia or not descricao or not fiscal or not engenheiro:
            st.error("⚠️ Por favor, preencha todos os campos obrigatórios (Rodovia, Descrição e Responsáveis).")
        else:
            # Cálculo de extensão (1 estaca = 20 metros)
            posicao_inicial_m = (estaca_inicial * 20) + fracao_inicial
            posicao_final_m = (estaca_final * 20) + fracao_final
            extensao_total_m = posicao_final_m - posicao_inicial_m

            if extensao_total_m < 0:
                st.error("Erro: A estaca/fração final não pode ser menor que a inicial.")
            else:
                km_final_calculado = km_inicial + (extensao_total_m / 1000.0)
                
                # Salva o RDO na lista da sessão
                novo_rdo = {
                    "Data": data_servico.strftime('%d/%m/%Y'),
                    "Rodovia": rodovia,
                    "Km Inicial": f"Km {km_inicial:.3f}",
                    "Km Final Calculado": f"Km {km_final_calculado:.3f}",
                    "Trecho Executado": f"Est. {estaca_inicial}+{fracao_inicial:.2f} até Est. {estaca_final}+{fracao_final:.2f}",
                    "Extensão Total (m)": f"{extensao_total_m:.2f} m",
                    "Tipo de Serviço": servico,
                    "Descrição": descricao,
                    "Fiscal Responsável": fiscal,
                    "Engenheiro Responsável": engenheiro
                }
                st.session_state.lista_rdos.append(novo_rdo)

                st.success("✅ RDO validado, processado e salvo no painel do administrador com sucesso!")
                st.markdown("---")
                
                # Indicadores Rápidos
                m1, m2, m3 = st.columns(3)
                m1.metric("Extensão Total Executada", f"{extensao_total_m:.2f} m")
                m2.metric("Km Inicial", f"Km {km_inicial:.3f}")
                m3.metric("Km Final Calculado", f"Km {km_final_calculado:.3f}")
                
                st.subheader("📄 Resumo do Relatório Gerado")
                
                # Estrutura dos dados (formato original vertical)
                resumo_dados = {
                    "Parâmetro": list(novo_rdo.keys()),
                    "Detalhe": list(novo_rdo.values())
                }
                
                df_resumo = pd.DataFrame(resumo_dados)
                st.dataframe(df_resumo, use_container_width=True, hide_index=True)

                # Opção de exportação para CSV individual
                csv_data = df_resumo.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Relatório (CSV)",
                    data=csv_data,
                    file_name=f"RDO_{rodovia.replace(' ', '_')}_{data_servico.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

with aba_admin:
    st.title("🔒 Painel do Administrador - Histórico de RDOs")
    st.markdown("### Relação de todos os formulários preenchidos nesta sessão")

    if len(st.session_state.lista_rdos) == 0:
        st.info("Nenhum RDO foi cadastrado ainda.")
    else:
        # Transforma a lista de dicionários em um DataFrame tabular completo
        df_geral = pd.DataFrame(st.session_state.lista_rdos)
        st.dataframe(df_geral, use_container_width=True, hide_index=True)

        # Botão para exportar todos os RDOs consolidados em um único CSV
        csv_geral = df_geral.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Consolidação de Todos os RDOs (CSV)",
            data=csv_geral,
            file_name=f"Consolidado_RDOs_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
