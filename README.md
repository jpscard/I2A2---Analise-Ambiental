# Projeto de Análise Socioambiental na Amazônia

## 1. Introdução e Contexto

Este projeto consiste em uma **aplicação web interativa** desenvolvida para analisar os impactos de variações climáticas e da gestão de recursos hídricos na segurança alimentar e na saúde de comunidades ribeirinhas na Amazônia.

A ferramenta foi criada para transformar dados brutos e "sujos" em informações visuais e estatísticas confiáveis, permitindo que líderes comunitários e analistas saiam do campo da percepção e tomem decisões estratégicas baseadas em evidências concretas. A aplicação guia o usuário através de todo o ciclo de vida de um projeto de dados, desde a carga e validação até a análise e geração de insights.

---

## 2. Funcionalidades Principais

A aplicação é construída em Python com a biblioteca Streamlit e está organizada em um fluxo de trabalho de 5 páginas:

* **Página 1: Introdução:** Apresenta o contexto do desafio, os objetivos do projeto e a descrição dos dados.
* **Página 2: Carga e Exploração Inicial:** Permite que o usuário faça o upload das bases de dados (`climática` e `socioeconômica`) e apresenta um diagnóstico inicial, mostrando duplicatas, valores ausentes e estatísticas descritivas.
* **Página 3: Limpeza e Preparação:** O coração da ferramenta. Oferece um painel de controle interativo para:
    * **Validar os dados** contra regras de qualidade configuráveis pelo usuário (ex: faixas de temperatura aceitáveis).
    * **Tomar decisões** sobre como tratar outliers e valores ausentes para cada variável.
    * Processar, unificar e ordenar os dados, gerando um conjunto de dados final e limpo.
* **Página 4: Análise Exploratória (EDA):** Apresenta visualizações interativas dos dados limpos, incluindo histogramas, séries temporais, gráficos de dispersão, box plots e uma matriz de correlação. Inclui também análises avançadas como a decomposição sazonal.
* **Página 5: Conclusões e Recomendações:** Sintetiza os principais achados da análise em uma linguagem acessível e realiza testes de significância estatística para validar as conclusões.

---

## 3. Como Executar o Projeto

Para rodar esta aplicação em sua máquina local, siga os passos abaixo.

### Pré-requisitos
* Python 3.8 ou superior instalado.

### Passos para Instalação e Execução

1.  **Clone ou baixe este repositório:**
    ```bash
    # Exemplo com git
    git clone <url-do-seu-repositorio>
    cd <nome-da-pasta-do-projeto>
    ```

2.  **Crie e ative um ambiente virtual (altamente recomendado):**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows
    .\.venv\Scripts\activate

    # Ativar no macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências necessárias:**
    Crie um arquivo chamado `requirements.txt` com o conteúdo abaixo e execute o comando `pip`.
    ```txt
    # requirements.txt
    streamlit
    pandas
    numpy
    plotly
    pandera
    scipy
    statsmodels==0.14.1
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    Na pasta raiz do projeto, execute o seguinte comando no seu terminal:
    ```bash
    streamlit run app.py
    ```
    A aplicação será aberta automaticamente no seu navegador padrão.

---

## 4. Estrutura do Projeto

O projeto está organizado da seguinte forma para facilitar a manutenção e a navegação:
