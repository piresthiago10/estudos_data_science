import pandas as pd
import matplotlib.pyplot as plt

import sys
import os

def verifica_meses(argumentos):
    meses_disponíveis = [
        'JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'
    ]
    meses = [mes.upper() for mes in argumentos if mes.upper() in meses_disponíveis]
    return meses

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
    return None

argumentos = sys.argv[1:]
meses = verifica_meses(argumentos)
caminho_pasta = os.getcwd() + "/modulo_14_scripting/Support_Exercise_M14"

for mes in meses:
    sinasc = pd.read_csv(f'{caminho_pasta}/input/SINASC_RO_2019_'+mes+'.csv')
    print('Data minima: ', sinasc.DTNASC.min())
    print('Data máxima: ', sinasc.DTNASC.max())

    max_data = sinasc.DTNASC.max()[:7]
    print(max_data)

    os.makedirs(f'{caminho_pasta}/output/figs/'+max_data, exist_ok=True)

    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count',
                    'quantidade de nascimento', 'data de nascimento')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/quantidade de nascimento_'+max_data+'.png')

    plota_pivot_table(sinasc, 'IDADEMAE', [
                    'DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/media idade mae por sexo_'+max_data+'.png')

    plota_pivot_table(sinasc, 'PESO', [
                    'DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/media peso bebe por sexo_'+max_data+'.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median',
                    'apgar1 mediano', 'gestacao', 'sort')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/apgar1 mediano por escolaridade mae_'+max_data+'.png')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean',
                    'apgar1 medio', 'gestacao', 'sort')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/media apgar1 por gestacao_'+max_data+'.png')

    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean',
                    'apgar5 medio', 'gestacao', 'sort')
    plt.savefig(f'{caminho_pasta}/output/figs/{max_data}/media apgar5 por gestacao_'+max_data+'.png')
