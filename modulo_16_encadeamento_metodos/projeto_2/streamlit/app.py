import os
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from unidecode import unidecode

caminho_pasta = os.getcwd() + "/modulo_16_encadeamento_metodos"

st.set_page_config(
    page_title="Previsão de Renda",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data(caminho):
    with st.spinner(text='In progress'):
        dados_sinasc = pd.read_csv(
            f'{caminho}/projeto_2/input/previsao_de_renda.csv')
    return dados_sinasc


renda_original = load_data(caminho_pasta)
renda_classificada = renda_original.copy()

# analise dos dados


def analise_variaveis_numericas(dados):
    variaveis_numericas = []
    for i in dados.columns[1:24].tolist():
        if dados.dtypes[i] == 'int64' or dados.dtypes[i] == 'float64':
            variaveis_numericas.append(i)
    fig, axes = plt.subplots(2, 3, figsize=(14, 10), constrained_layout=True)

    linha = 0
    coluna = 0
    for i in variaveis_numericas:
        sns.boxplot(data=dados, y=i, ax=axes[linha][coluna])
        coluna += 1
        if coluna == 3:
            linha += 1
            coluna = 0
    sns.despine()
    return st.pyplot(fig=plt)


def analise_variavel_bivariada(variavel, dados):
    salario_minimo = 1_412
    dados["quant_salario_min"] = round(
        dados['renda'] / salario_minimo)
    bins_salario = [-100, 0, 3, 6, 10, 20]
    labels = [
        "0 a 3 salarios",
        "3 a 6 salarios",
        "6 a 10 salarios",
        "10 a 20 salarios",
        "mais 20 salarios"
    ]
    dados['cat_quant_salario'] = pd.cut(
        dados['quant_salario_min'], bins=bins_salario, labels=labels)

    bins_idade = [-100, 0, 1, 3, 5, 10]
    labels = [
        "0 a 1 ano",
        "1 a 3 anos",
        "3 a 5 anos",
        "5 a 10 anos",
        "mais 10 anos"
    ]
    dados['cat_tempo_emprego'] = pd.cut(
        dados['tempo_emprego'], bins=bins_idade, labels=labels)
    fig, ax = plt.subplots(figsize=(12, 5), constrained_layout=True)
    sns.countplot(data=dados, x=variavel, hue="cat_quant_salario", ax=ax)
    sns.despine()
    return st.pyplot(fig=plt)

# preparacao dos dados


columns = [
    'sexo',
    'posse_de_veiculo',
    'posse_de_imovel',
    'qtd_filhos',
    'tipo_renda',
    'educacao',
    'estado_civil',
    'tipo_residencia',
    'idade',
    'tempo_emprego',
    'qt_pessoas_residencia',
    'renda'
]
renda_dados_ajustados = pd.DataFrame(renda_original, columns=columns)

renda_dados_ajustados['tempo_emprego'] = renda_dados_ajustados['tempo_emprego'].fillna(
    (renda_dados_ajustados['tempo_emprego'].median()))

renda_dados_ajustados = renda_dados_ajustados.loc[renda_dados_ajustados['qtd_filhos'] <= 2]
renda_dados_ajustados = renda_dados_ajustados.loc[renda_dados_ajustados['qt_pessoas_residencia'] <= 4]
renda_dados_ajustados = renda_dados_ajustados.loc[renda_dados_ajustados['renda'] <= 100_000]
renda_dados_ajustados = renda_dados_ajustados.loc[renda_dados_ajustados['tempo_emprego'] <= 38]

renda_dados_ajustados_dummies = pd.get_dummies(renda_dados_ajustados, columns=[
                                               'sexo', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia'], drop_first=True)


def clean_column_name(col_name):
    col_name = unidecode(col_name)
    col_name = col_name.lower()
    col_name = col_name.replace(' ', '_')
    return col_name


renda_dados_ajustados_dummies.columns = [clean_column_name(
    col) for col in renda_dados_ajustados_dummies.columns]

df_train, df_test = train_test_split(
    renda_dados_ajustados_dummies, test_size=0.25, random_state=42)

modelo = """np.log(renda) ~ tempo_emprego
+ sexo_m
+ educacao_superior_completo
+ tipo_renda_empresario
+ qtd_filhos
+ idade
+ posse_de_imovel
+ posse_de_veiculo
"""

reg = smf.ols(modelo, data=df_test).fit()

# página do streamlit

st.write("# Previsão de Renda")

tab1, tab2, tab3 = st.tabs(["Entendimento", "Gráficos", "Previsão de Renda"])

with tab1:
    st.header("Entendimento do negócio e dados")
    st.write(
        """
       O objetivo deste projeto é desenvolver um modelo preditivo que possa estimar a renda 
       dos indivíduos com base em características demográficas e socioeconômicas.
       
       Os dados disponíveis incluem informações demográficas, posse de bens, e dados relacionados a 
       família. As limitações incluem a qualidade dos dados e as restrições de privacidade 
       e proteção de dados.
       """
    )
    st.write(
        """
        A descrição detalhada dos dados contidos na base encontra-se abaixo
        
        | Variável                | Descrição                                           | Tipo         |
        | ----------------------- |:---------------------------------------------------:| ------------:|
        | data_ref                |  Data de referência de coleta das variáveis         | Quantitativa - Contínua|
        | id_cliente              |  Código de identificação do cliente                 | Qualitativa - Nominal|
        | sexo                    |  Sexo do cliente                                    | Qualitativa - Nominal|
        | posse_de_veiculo        |  Indica se o cliente possui veículo                 | Qualitativa - Nominal|
        | posse_de_imovel         |  Indica se o cliente possui imóvel                  | Qualitativa - Nominal|
        | qtd_filhos              |  Quantidade de filhos do cliente                    | Quantitativa - Discreta|
        | tipo_renda              |  Tipo de renda do cliente                           | Qualitativa - Nominal|
        | educacao                |  Grau de instrução do cliente                       | Qualitativa - Ordinal|
        | estado_civil            |  Estado civil do cliente                            | Qualitativa - Nominal|
        | tipo_residencia         |  Tipo de residência do cliente (própria, alugada etc)| Qualitativa - Nominal|
        | idade                   |  Idade do cliente                                   | Quantitativa - Discreta|
        | tempo_emprego           |  Tempo no emprego atual                             | Quantitativa - Contínua|
        | qt_pessoas_residencia   |  Quantidade de pessoas que moram na residência      | Quantitativa - Discreta|
        | renda                   |  Renda em reais                                     | Quantitativa - Contínua|
        """
    )
    st.write("### Exemplo dos dados disponíveis:")
    st.dataframe(renda_classificada)

with tab2:
    st.header("Análise dos Gráficos")
    st.write("### Entendimento dos dados - Univariada")
    analise_variaveis_numericas(renda_original)
    st.write("### Entendimento dos dados - Bivariada")

    for item in ["sexo", "educacao", "posse_de_imovel", "posse_de_veiculo", "tipo_renda", "cat_tempo_emprego"]:
        analise_variavel_bivariada(item, renda_classificada)

with tab3:
    st.header("Formulário de Previsão de Renda")

    with st.form("dados_form"):
        tempo_emprego = st.number_input("Tempo de Emprego (meses)")
        sexo_m = st.checkbox("Sexo Masculino")
        educacao_superior_completo = st.checkbox("Educação Superior Completa")
        tipo_renda_empresario = st.checkbox("Tipo de Renda Empresário")
        qtd_filhos = st.number_input("Quantidade de Filhos")
        idade = st.number_input("Idade")
        posse_de_imovel = st.checkbox("Posse de Imóvel")
        posse_de_veiculo = st.checkbox("Posse de Veículo")

        submit_button = st.form_submit_button("Enviar")
    with st.spinner(text='Aguarde...'):
        if submit_button:
            dados_novos_df = {
                "tempo_emprego": tempo_emprego,
                "sexo_m": sexo_m,
                "educacao_superior_completo": educacao_superior_completo,
                "tipo_renda_empresario": tipo_renda_empresario,
                "qtd_filhos": qtd_filhos,
                "idade": idade,
                "posse_de_imovel": posse_de_imovel,
                "posse_de_veiculo": posse_de_veiculo
            }

            dados_novos_df = pd.DataFrame(dados_novos_df, index=["Prev_Renda_Cliente"])

            resultado = np.exp(reg.predict(dados_novos_df))

            st.subheader("Dados Preenchidos")
            st.write(dados_novos_df)

            st.subheader("Resultado da Predição")
            st.write(f"### R$ {resultado[0]:.2f}")

