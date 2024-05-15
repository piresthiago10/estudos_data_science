import os

import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

sns.set_theme()


def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return st.pyplot(fig=plt)


caminho_pasta = os.getcwd() + "/modulo_15_streamlit"

st.set_page_config(
    page_title="Análise SINASC",
    page_icon=f"{caminho_pasta}/brasil.png",
    layout="wide"
)

@st.experimental_dialog("Sobre o estado de Rondônia", width="large")
def show_state_info():
    st.text(
        """
        Rondônia é uma das 27 unidades federativas do Brasil. Está localizado na região Norte e 
        tem como limites os estados de Mato Grosso a leste, Amazonas a norte, Acre a oeste e o 
        Estado Plurinacional da Bolívia a oeste e sul. O estado possui 52 municípios e ocupa uma
        área de 237 590,547 km², equivalente ao território da Romênia e quase cinco vezes maior 
        que a Croácia. Sua capital e município mais populoso é Porto Velho, banhada pelo rio 
        Madeira. Além desta, há outras cidades importantes como Ariquemes, Cacoal, 
        Guajará-Mirim, Ji-Paraná, Rolim de Moura e Vilhena.    
        """
    )
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Rondonia_in_Brazil.svg/300px-Rondonia_in_Brazil.svg.png",
        caption='Mapa do estado de Rondônia'
    )
    st.text(
    """
        É o terceiro estado mais populoso da Região Norte com 1 815 278 habitantes, segundo 
        estimativa do IBGE para 2021, sendo superado apenas pelo Pará e Amazonas. Quatro de seus 
        municípios possuem população acima de 100 mil habitantes, sendo estes Porto Velho, 
        Ji-Paraná, Ariquemes e Vilhena. A população rondoniense é uma das mais diversificadas do 
        Brasil, composta de migrantes oriundos de todas as regiões do país, dentre os quais 
        destacam-se os paranaenses, paulistas, mineiros e gaúchos, que fixaram-se na capital, 
        preservando-se ainda os fortes traços amazônicos da população nativa nas cidades banhadas 
        por grandes rios, sobretudo em Porto Velho e Guajará-Mirim, as duas cidades mais antigas 
        do estado.
    """
    )

@st.cache_data
def load_data(caminho):
    with st.spinner(text='In progress'):
        dados_sinasc = pd.read_csv(f'{caminho}/input_M15_SINASC_RO_2019.csv')
        st.success('Base de dados carregada')
    return dados_sinasc


sinasc = load_data(caminho_pasta)

sinasc["DTNASC"] = pd.to_datetime(sinasc["DTNASC"])

min_date = sinasc["DTNASC"].min()
max_date = sinasc["DTNASC"].max()

with st.container():
    st.title("Sinasc 2019")
    st.header("Análise de dados do estado de Rondônia")
    st.text(
        """
        Visualize os dados sobre os nascimentos do ano de 2019 navegando entre as abas abaixo.
        Selecione entre data inicial e data final para filtrar os dados exibidos nas tabelas.
        """
    )
    if st.button("Sobre Rondônia"):
        with st.spinner(text='Aguarde...'):
            show_state_info()

    col1, col2 = st.columns(2)

    with col1:
        data_incial = st.date_input(
            "Data Inicial",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with col2:
        data_final = st.date_input(
            "Data Final",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    st.write(f"Data Incial: {data_incial}   Data Final: {data_final}")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Base SINASC",
            "IDADEMAE X DTNASC",
            "IDADEMAE X DTNASC, SEXO",
            "PESO X DTNASC, SEXO",
            "PESO, ESCMAE",
            "APGAR1, GESTACAO",
            "APGAR5, GESTACAO"
        ]
    )

    sinasc = sinasc[
        (sinasc["DTNASC"] <= pd.to_datetime(data_final))
        & (sinasc["DTNASC"] >= pd.to_datetime(data_incial))
    ]

    with tab1:
        st.write("Base sinasc")
        st.dataframe(sinasc)

    with tab2:
        plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count',
                          'quantidade de nascimento', 'data de nascimento')

    with tab3:
        plota_pivot_table(sinasc, 'IDADEMAE', [
            'DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')

    with tab4:
        plota_pivot_table(sinasc, 'PESO', [
            'DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')

    with tab5:
        plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median',
                          'apgar1 mediano', 'gestacao', 'sort')

    with tab6:
        plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean',
                          'apgar1 medio', 'gestacao', 'sort')

    with tab7:
        plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean',
                          'apgar5 medio', 'gestacao', 'sort')
