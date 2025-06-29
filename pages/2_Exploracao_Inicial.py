import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

st.markdown("# 2. Carga e Exploração Inicial dos Dados")
st.markdown("---")
st.header("Faça o upload das duas bases de dados")

col1, col2 = st.columns(2)
with col1:
    clima_file = st.file_uploader("Carregue a Base Climática (.csv)", type="csv")
with col2:
    socio_file = st.file_uploader("Carregue a Base Socioeconômica (.csv)", type="csv")

if clima_file and socio_file:
    st.success("Arquivos carregados com sucesso! Iniciando diagnóstico...")
    df_clima = pd.read_csv(clima_file)
    df_socio = pd.read_csv(socio_file)
    
    st.session_state['dados_brutos'] = (df_clima.copy(), df_socio.copy())
    st.markdown("---")

    st.header("🌦️ Análise da Base Climática")
    st.dataframe(df_clima.head())
    st.warning(f"Diagnóstico Rápido: {df_clima.duplicated().sum()} duplicatas e {df_clima.isnull().sum().sum()} valores nulos encontrados.")
    
    with st.expander("Ver detalhes da Base Climática"):
        buffer = io.StringIO()
        df_clima.info(buf=buffer)
        st.text(buffer.getvalue())
        st.write("Valores Nulos:", df_clima.isnull().sum())

    st.header("🧑‍🤝‍🧑 Análise da Base Socioeconômica")
    st.dataframe(df_socio.head())
    st.warning(f"Diagnóstico Rápido: {df_socio.duplicated().sum()} duplicatas e {df_socio.isnull().sum().sum()} valores nulos encontrados.")

    with st.expander("Ver detalhes da Base Socioeconômica"):
        buffer = io.StringIO()
        df_socio.info(buf=buffer)
        st.text(buffer.getvalue())
        st.write("Valores Nulos:", df_socio.isnull().sum())
        
    st.success("Diagnóstico concluído. Prossiga para a página de Limpeza e Preparação.")
else:
    st.info("Aguardando o upload de ambos os arquivos CSV para iniciar a análise.")