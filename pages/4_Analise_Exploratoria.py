import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

st.set_page_config(layout="wide")
st.markdown("# 4. Análise Exploratória de Dados")
st.markdown("---")

if 'df_final' in st.session_state and st.session_state['df_final'] is not None:
    df = st.session_state['df_final']
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'])
    st.info("Análise sendo realizada com os dados processados na Página 3.")
else:
    st.error("Nenhum dado limpo foi encontrado. Por favor, processe ou carregue os dados na 'Página 3' primeiro.")
    st.stop()

st.header("Análise Univariada: Distribuição das Variáveis")
col_options = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
selected_col = st.selectbox("Selecione uma variável para ver sua distribuição:", col_options)
if selected_col:
    fig_hist = px.histogram(df, x=selected_col, nbins=30, title=f"Distribuição de '{selected_col}'")
    st.plotly_chart(fig_hist, use_container_width=True)

st.header("Análise de Séries Temporais")
ts_cols = st.multiselect("Selecione as variáveis para visualizar ao longo do tempo:", options=col_options, default=[col for col in ['chuvas_reais_mm', 'volume_producao_tons'] if col in df.columns])
if ts_cols and 'data' in df.columns:
    fig_ts = px.line(df, x='data', y=ts_cols, title="Séries Temporais das Variáveis Selecionadas")
    st.plotly_chart(fig_ts, use_container_width=True)

st.header("Análise Sazonal (Decomposição de Série Temporal)")
if STATSMODELS_AVAILABLE:
    decomp_col = st.selectbox("Selecione a variável para decompor:", options=col_options)
    if decomp_col and 'data' in df.columns:
        ts_data = df.set_index('data')[decomp_col].dropna()
        periodo = 7
        if len(ts_data) > 2 * periodo:
            result = seasonal_decompose(ts_data, model='additive', period=periodo)
            st.subheader(f"Decomposição de '{decomp_col}'")
            fig_trend = px.line(x=result.trend.index, y=result.trend, title="Tendência").update_traces(line_color='blue')
            st.plotly_chart(fig_trend, use_container_width=True)
            fig_seasonal = px.line(x=result.seasonal.index, y=result.seasonal, title="Sazonalidade").update_traces(line_color='green')
            st.plotly_chart(fig_seasonal, use_container_width=True)
            fig_resid = px.scatter(x=result.resid.index, y=result.resid, title="Resíduos (Ruído)").update_traces(marker_color='red')
            st.plotly_chart(fig_resid, use_container_width=True)
else:
    st.warning("A biblioteca `statsmodels` não foi encontrada. Para habilitar esta análise, instale-a: pip install statsmodels scipy")

st.header("Análise Bivariada: Investigando Relações")
if 'chuvas_reais_mm' in df.columns and 'volume_producao_tons' in df.columns:
    fig_scatter = px.scatter(df, x='chuvas_reais_mm', y='volume_producao_tons', log_y=True, title="Chuvas Reais (mm) vs. Volume de Produção (tons)")
    st.plotly_chart(fig_scatter, use_container_width=True)
if 'acesso_agua_potavel' in df.columns and 'incidencia_doencas' in df.columns:
    fig_box = px.box(df, x='acesso_agua_potavel', y='incidencia_doencas', color='acesso_agua_potavel', log_y=True, notched=True, title="Incidência de Doenças por Acesso à Água Potável")
    
    st.plotly_chart(fig_box, use_container_width=True)

st.header("Visão Geral: Matriz de Correlação")
numeric_cols_for_corr = df.select_dtypes(include=np.number).columns.tolist()
if len(numeric_cols_for_corr) > 1:
    corr_matrix = df[numeric_cols_for_corr].corr()
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Mapa de Calor da Correlação")
    st.plotly_chart(fig_corr, use_container_width=True)