import streamlit as st

# Configuração da página principal
st.set_page_config(
    page_title="Análise Socioambiental na Amazônia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e introdução na página principal
st.title("Análise de Impactos Socioambientais na Amazônia")

st.markdown("""
Esta aplicação interativa foi desenvolvida para analisar os dados climáticos e socioeconômicos
de comunidades na região amazônica. O objetivo é transformar dados brutos em insights que possam
apoiar a tomada de decisão local frente aos desafios hídricos e de segurança alimentar.

**Use o menu na barra lateral para navegar pelas diferentes etapas da análise.**
""")

st.sidebar.success("Selecione uma página acima para começar.")

st.markdown("---")
st.markdown("### Contexto do Desafio")
st.info("""
A região amazônica enfrenta um problema crescente relacionado à gestão dos recursos hídricos e seus impactos diretos na segurança alimentar de comunidades ribeirinhas e agricultores familiares. Episódios de estiagens prolongadas e enchentes severas alteraram drasticamente os ciclos naturais, afetando a disponibilidade de água e a produtividade agrícola.

Este projeto visa sair do campo da percepção e trabalhar com dados reais para fortalecer as tomadas de decisão comunitárias.
""")

st.image("https://cdn-v2.theculturetrip.com/1280x713/wp-content/uploads/2021/03/2bf8jfw-e1618056235626.webp", 
         caption="Floresta Amazônica -  | © Curioso.Photography / Alamy Stock Photo",
         use_container_width=True)