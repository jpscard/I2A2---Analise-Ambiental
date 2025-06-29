import streamlit as st

st.set_page_config(layout="wide")

st.markdown("# 1. Introdução ao Desafio")
st.markdown("---")

st.header("🎯 Objetivos")
st.write("""
Analisar a relação entre as variações climáticas e hídricas e seus impactos na segurança alimentar e saúde de comunidades amazônicas, transformando dados brutos em informações confiáveis para apoiar a tomada de decisão local.
""")

st.header("⚖️ Critérios de Avaliação")
st.markdown("""
* **Clareza na definição do problema.**
* **Coerência na análise dos dados.**
* **Qualidade dos insights gerados.**
* **Organização e apresentação da solução.**
""")

st.header("💾 Descrição das Variáveis Originais")
st.write("Os dados estão divididos em duas bases que se conectam pela data do registro.")

tab1, tab2 = st.tabs(["Base Climática", "Base Socioeconômica"])

with tab1:
    st.subheader("🌦️ Base Climática")
    st.markdown("""
    - `data`: Data do registro.
    - `chuvas_previstas_mm`: Precipitação prevista em mm.
    - `chuvas_reais_mm`: Precipitação real medida em mm.
    - `temperatura_media_C`: Temperatura média diária em °C.
    - `variacao_climatica`: Indicador de variação climática incomum.
    - `indice_umidade_solo`: Umidade do solo em percentual (%).
    """)

with tab2:
    st.subheader("🧑‍🤝‍🧑 Base Socioeconômica")
    st.markdown("""
    - `data`: Data do registro.
    - `volume_producao_tons`: Volume de produção agrícola em toneladas.
    - `incidencia_doencas`: Número de casos de doenças hídricas.
    - `acesso_agua_potavel`: Acesso da comunidade à água potável.
    - `indicador_seguranca_alimentar`: Índice de segurança alimentar (0–100).
    """)