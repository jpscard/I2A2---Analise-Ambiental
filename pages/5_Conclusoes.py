import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

st.set_page_config(layout="wide")
st.markdown("# 5. Conclusões e Recomendações")
st.markdown("---")

if 'df_final' in st.session_state and st.session_state['df_final'] is not None:
    df = st.session_state['df_final']
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'])
else:
    st.error("Nenhum dado limpo foi encontrado. Por favor, processe ou carregue os dados na 'Página 3' primeiro.")
    st.stop()

st.header("Resumo dos Principais Achados")
st.info("""
A análise dos dados revelou pontos cruciais para a tomada de decisão da comunidade:
1.  **Impacto Direto:** O acesso à água potável está diretamente ligado a uma menor incidência de doenças.
2.  **Relação Complexa:** A produção agrícola é influenciada pelas chuvas, mas a relação não é linear.
3.  **Vulnerabilidade Sazonal:** Existem períodos do ano com maior fragilidade na segurança alimentar.
""")

st.header("Análise Detalhada dos Insights")

if 'acesso_agua_potavel' in df.columns and 'incidencia_doencas' in df.columns:
    st.subheader("Insight 1: Acesso à água potável como fator de proteção")
    fig_box = px.box(df, x='acesso_agua_potavel', y='incidencia_doencas', color='acesso_agua_potavel', log_y=True, notched=True, title="Incidência de Doenças por Acesso à Água Potável", labels={'acesso_agua_potavel': 'Acesso à Água Potável', 'incidencia_doencas': 'Casos de Doenças Hídricas'})
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.subheader("Teste de Significância Estatística (Teste t)")
    grupo_com_acesso = df[df['acesso_agua_potavel'] == 'sim']['incidencia_doencas'].dropna()
    grupo_sem_acesso = df[df['acesso_agua_potavel'] == 'não']['incidencia_doencas'].dropna()

    if len(grupo_com_acesso) > 1 and len(grupo_sem_acesso) > 1:
        t_stat, p_value = stats.ttest_ind(grupo_com_acesso, grupo_sem_acesso, equal_var=False)
        st.metric(label="P-valor do Teste", value=f"{p_value:.4f}")
        if p_value < 0.05:
            st.success("**Conclusão:** O resultado é estatisticamente significativo. A diferença na incidência de doenças não é obra do acaso.")
        else:
            st.warning("**Conclusão:** O resultado não é estatisticamente significativo. A diferença observada pode ser fruto de variação aleatória.")
    else:
        st.warning("Não foi possível realizar o teste estatístico por falta de dados em um dos grupos.")

if 'chuvas_reais_mm' in df.columns and 'volume_producao_tons' in df.columns:
    st.markdown("---")
    st.subheader("Insight 2: Produção agrícola e o equilíbrio hídrico")
    fig_scatter = px.scatter(df, x='chuvas_reais_mm', y='volume_producao_tons', log_y=True, title="Chuvas Reais (mm) vs. Volume de Produção (toneladas)", labels={'chuvas_reais_mm': 'Chuvas Reais (mm)', 'volume_producao_tons': 'Volume de Produção (toneladas)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.header("Recomendações para Ação")
st.warning("""
- **Prioridade Máxima:** Investir em saneamento e acesso universal à água potável.
- **Resiliência Agrícola:** Fomentar técnicas de manejo de solo e o uso de culturas mais resistentes.
- **Monitoramento Contínuo:** Manter a coleta de dados para criar alertas precoces e medir o impacto de novas ações.
""")
