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

# Inicializar o histórico de RDOs no session_state para persistência na sessão
if 'lista_rdos' not in st.session_state:
    st.session_state.lista_rdos = []

st.title("🚧 Sistema de Relatório Diário de Obra (RDO)")
st.markdown("### Módulo de Lançamento de Serviços e Estaques")

# Criação de abas para separar o Lançamento e o Painel do Administrador
aba_lancamento, aba_admin = st.tabs(["📝 Lançamento de RDO", "🔒 Painel do Administrador"])

with aba_lancamento:
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
        with col9:
            engenheiro = st.text_input("Nome do Engenheiro Responsável", placeholder="Nome completo do Engenheiro")

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
                
                # Salvar no histórico global da sessão
                novo_registro = {
                    "Data": data_servico.strftime('%d/%m/%Y'),
                    "Rodovia": rodovia,
                    "Km Inicial": f"Km {km_inicial:.3f}",
                    "Trecho Executado": f"Est. {estaca_inicial}+{fracao_inicial:.2f} até Est. {estaca_final}+{fracao_final:.2f}",
                    "Extensão Total (m)": f"{extensao_total_m:.2f} m",
                    "Tipo de Serviço": servico,
                    "Descrição": descricao,
                    "Fiscal Responsável": fiscal,
                    "Engenheiro Responsável": engenheiro
                }
                st.session_state.lista_rdos.append(novo_registro)
                
                st.markdown("---")
                st.subheader("📄 Resumo do Relatório Gerado")
                
                df_resumo = pd.DataFrame([novo_registro])
                st.dataframe(df_resumo, use_container_width=True)

                # Opção de exportação individual para XLSX com dados em linha
                output_ind = io.BytesIO()
                with pd.ExcelWriter(output_ind, engine='openpyxl') as writer:
                    df_resumo.to_excel(writer, index=False, sheet_name='RDO')
                excel_data_ind = output_ind.getvalue()

                st.download_button(
                    label="📥 Baixar Relatório (Excel .xlsx)",
                    data=excel_data_ind,
                    file_name=f"RDO_{rodovia.replace(' ', '_')}_{data_servico.strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

with aba_admin:
    st.subheader("🔒 Painel do Administrador - RDOs Registrados")
    senha_admin = st.text_input("Senha de Acesso", type="password", placeholder="Digite a senha de administrador")
    
    # Senha padrão de exemplo configurada como 'admin123'
    if senha_admin == "admin123":
        st.success("Acesso autorizado com sucesso!")
        
        if len(st.session_state.lista_rdos) > 0:
            df_admin = pd.DataFrame(st.session_state.lista_rdos)
            st.dataframe(df_admin, use_container_width=True)
            
            # Botão para baixar todos os relatórios consolidados em XLSX
            output_todos = io.BytesIO()
            with pd.ExcelWriter(output_todos, engine='openpyxl') as writer:
                df_admin.to_excel(writer, index=False, sheet_name='Consolidado_RDOs')
            excel_data_todos = output_todos.getvalue()

            st.download_button(
                label="📥 Baixar Todos os Relatórios (Consolidado Excel .xlsx)",
                data=excel_data_todos,
                file_name=f"Consolidado_RDOs_{datetime.today().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Nenhum RDO cadastrado nesta sessão até o momento.")
    elif senha_admin != "":
        st.error("Senha incorreta. Tente novamente.")
    else:
        st.info("🔑 Insira a senha de administrador para visualizar os dados. (Senha padrão de teste: `admin123`)")
