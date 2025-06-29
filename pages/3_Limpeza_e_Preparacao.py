import streamlit as st
import pandas as pd
import numpy as np
import pandera as pa

st.set_page_config(layout="wide")

st.markdown("# 3. Limpeza e Preparação dos Dados")
st.markdown("---")

# Abas para escolher o fluxo de trabalho
tab_limpar, tab_carregar = st.tabs(["Limpar Dados Brutos (Interativo)", "Carregar Dados Já Limpos"])

with tab_limpar:
    st.header("Opção 1: Limpar os dados carregados passo a passo")

    if 'dados_brutos' not in st.session_state:
        st.warning("Por favor, faça o upload dos dados na 'Página 2: Carga e Exploração' primeiro.")
    else:
        df_clima_raw, df_socio_raw = st.session_state['dados_brutos']

        # --- FORMULÁRIO 1: CONFIGURAÇÃO E VALIDAÇÃO ---
        with st.form(key="validation_form"):
            st.subheader("Passo 1: Configure e Execute a Validação")
            st.info("Ajuste as regras de validação abaixo com base nas estatísticas dos seus dados brutos.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("Estatísticas da Base Climática:")
                st.dataframe(df_clima_raw.describe())
            with col2:
                st.write("Estatísticas da Base Socioeconômica:")
                st.dataframe(df_socio_raw.describe())

            temp_range = st.slider("Faixa de Temperatura (°C) aceitável:", -10, 50, (15, 45))
            umidade_range = st.slider("Faixa de Umidade do Solo (%) aceitável:", 0, 100, (0, 100))
            
            validation_submitted = st.form_submit_button("Validar e Realizar Limpeza Básica")

        if validation_submitted:
            with st.spinner("Validando e aplicando limpeza básica..."):
                schema_clima = pa.DataFrameSchema({"temperatura_media_C": pa.Column(float, pa.Check.in_range(temp_range[0], temp_range[1]), nullable=True), "indice_umidade_solo": pa.Column(float, pa.Check.in_range(umidade_range[0], umidade_range[1]), nullable=True)}, coerce=True, strict=False)
                schema_socio = pa.DataFrameSchema({"incidencia_doencas": pa.Column(float, pa.Check.greater_than_or_equal_to(0), nullable=True)}, coerce=True, strict=False)
                
                df_clima, df_socio = df_clima_raw.copy(), df_socio_raw.copy()
                df_socio['incidencia_doencas'] = pd.to_numeric(df_socio['incidencia_doencas'], errors='coerce').abs()
                
                try:
                    schema_clima.validate(df_clima, lazy=True)
                    schema_socio.validate(df_socio, lazy=True)
                    st.success("Dados validados com sucesso com as suas regras!")
                    
                    for df_temp in [df_clima, df_socio]:
                        df_temp['data'] = pd.to_datetime(df_temp['data'], errors='coerce')
                        df_temp.dropna(subset=['data'], inplace=True)
                        df_temp.drop_duplicates(inplace=True)
                    df_clima['variacao_climatica'] = df_clima['variacao_climatica'].str.lower().replace('nao', 'não')
                    df_socio['acesso_agua_potavel'] = df_socio['acesso_agua_potavel'].str.lower().replace('nao', 'não')
                    
                    st.session_state.dados_etapa1 = (df_clima, df_socio)
                    st.session_state.etapa1_ok = True
                except pa.errors.SchemaErrors as e:
                    st.error("Validação falhou! Ajuste os parâmetros ou o arquivo de origem.")
                    st.dataframe(e.failure_cases)
                    st.session_state.etapa1_ok = False
        
        # --- FORMULÁRIO 2: DECISÕES DE TRATAMENTO ---
        if st.session_state.get('etapa1_ok', False):
            st.markdown("---")
            st.subheader("Passo 2: Painel de Decisão de Tratamento")
            st.info("Agora, decida como tratar os problemas restantes nos dados.")

            with st.form(key="treatment_form"):
                df_clima_temp, df_socio_temp = (df.copy() for df in st.session_state.dados_etapa1)
                
                st.write("**Decisão sobre Outliers:**")
                estrategia_outlier = st.radio("Como tratar outliers de chuva?", ["Não tratar", "Usar método estatístico IQR"], key="strat_outlier")

                if estrategia_outlier == "Usar método estatístico IQR":
                    col_outlier = 'chuvas_reais_mm'
                    df_clima_temp[col_outlier] = pd.to_numeric(df_clima_temp[col_outlier], errors='coerce')
                    Q1 = df_clima_temp[col_outlier].quantile(0.25); Q3 = df_clima_temp[col_outlier].quantile(0.75); IQR = Q3 - Q1
                    limite_superior = Q3 + 1.5 * IQR
                    df_clima_temp.loc[df_clima_temp[col_outlier] > limite_superior, col_outlier] = np.nan
                
                cols_com_nulos = df_clima_temp.columns[df_clima_temp.isnull().any()].tolist() + df_socio_temp.columns[df_socio_temp.isnull().any()].tolist()
                
                st.write("**Decisão sobre Dados Ausentes:**")
                estrategias_nulos = {}
                if cols_com_nulos:
                    for col in set(cols_com_nulos):
                        estrategias_nulos[col] = st.selectbox(f"Estratégia para '{col}':", ['Preencher com a Mediana', 'Preencher com a Média', 'Remover Linhas'], key=f"strat_{col}")
                else:
                    st.info("Nenhum dado ausente a ser tratado.")
                
                treatment_submitted = st.form_submit_button("Aplicar Decisões e Gerar DataFrame Final")

                if treatment_submitted:
                    with st.spinner("Finalizando..."):
                        for col, strat in estrategias_nulos.items():
                            for df_temp in [df_clima_temp, df_socio_temp]:
                                if col in df_temp.columns and df_temp[col].isnull().any():
                                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')
                                    if strat == 'Preencher com a Mediana': df_temp[col].fillna(df_temp[col].median(), inplace=True)
                                    elif strat == 'Preencher com a Média': df_temp[col].fillna(df_temp[col].mean(), inplace=True)
                                    elif strat == 'Remover Linhas': df_temp.dropna(subset=[col], inplace=True)
                        
                        df_final_bruto = pd.merge(df_clima_temp, df_socio_temp, on='data', how='inner')
                        
                        # --- LINHA ADICIONADA ---
                        # Garante que os dados estejam em ordem cronológica antes de salvar
                        df_final = df_final_bruto.sort_values(by='data').reset_index(drop=True)
                        
                        st.session_state['df_final'] = df_final
                        st.success("Processo de limpeza concluído com sucesso!")
                        st.dataframe(df_final.head())

with tab_carregar:
    st.header("Opção 2: Carregar um arquivo de dados já limpo")
    cleaned_file = st.file_uploader("Carregue seu arquivo (.csv)", type="csv", key="limpo_uploader")
    if cleaned_file:
        df_carregado = pd.read_csv(cleaned_file)
        
        # --- LINHAS ADICIONADAS COMO MEDIDA DE SEGURANÇA ---
        # Garante que o arquivo carregado também seja ordenado
        df_carregado['data'] = pd.to_datetime(df_carregado['data'], errors='coerce')
        df_carregado.dropna(subset=['data'], inplace=True)
        df_carregado = df_carregado.sort_values(by='data').reset_index(drop=True)
        
        st.session_state['df_final'] = df_carregado
        st.success("Arquivo de dados limpos carregado e ordenado com sucesso!")
        st.dataframe(df_carregado.head())

if 'df_final' in st.session_state and st.session_state['df_final'] is not None:
    st.markdown("---")
    st.header("Exportar Dados Limpos")
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')
    csv = convert_df_to_csv(st.session_state['df_final'])
    st.download_button("Baixar dados limpos como CSV", csv, 'dados_processados.csv', 'text/csv')
