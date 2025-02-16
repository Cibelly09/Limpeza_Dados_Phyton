# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 08:21:33 2025

@author: Cibelly Viegas
"""

pip install openpyxl
pip install xlrd

import pandas as pd
import math
import numpy as np
import openpyxl
import xlrd

df = pd.read_excel ("eleitorado.xlsx", engine="openpyxl")

print(df.head())
print(df.columns)
print(df.info ())

#quantas linhas tem no bd
print(df.shape[0])

# quantas colunas tem no bd
print(df.shape [1])

#quantas observações tem na bd
print(df.shape)

#selecionando variáveis

df_def = df[['SG_UF','QT_ELEITORES_DEFICIENCIA', 'DS_RACA_COR', 'DS_GRAU_ESCOLARIDADE', 'DS_FAIXA_ETARIA', 'DS_ESTADO_CIVIL', 'DS_GENERO']]

#separando as bd para análises diferentes

qtd_comp = df[['SG_UF','QT_ELEITORES_PERFIL','QT_ELEITORES_DEFICIENCIA']]

# limpando a base para acm 
# tirando as linhas nulas

df_def = df_def[df_def['QT_ELEITORES_DEFICIENCIA'].notna() &
                (df_def['QT_ELEITORES_DEFICIENCIA']>0)]
print(df_def)
print(df_def.head())
print(df_def.info ())
print(df_def.shape)

#Tirando o prefere não informar e não informado

df_def = df_def[~df_def.applymap(lambda x:x in ['Prefere nAo informar', 'NAO INFORMADO', 'Inválida']).any(axis=1)]

print(df_def.info())
print(df_def.head())
print(df_def.shape)

#Tabela de estatísticas descritivas para variáveis quantitativas

df_def[['QT_ELEITORES_DEFICIENCIA']].describe()

#Tabela de frequências para variável qualitativa por coluna
df_def['DS_RACA_COR'].value_counts()
df_def['DS_GRAU_ESCOLARIDADE'].value_counts()
df_def['DS_FAIXA_ETARIA'].value_counts()
df_def['DS_ESTADO_CIVIL'].value_counts()
df_def['DS_GENERO'].value_counts()

# Normalizando a BD - isinstance (x,str) verifica se é string para não ter erros

df_def = df_def.applymap(lambda x: x.upper()
                         if isinstance(x,str) else x)

print(df_def)
# Visualização dos dados em gráficos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'
import plotly.graph_objects as go

#Gráfico de contagem para gênero    
ax= sns.countplot(data=df_def, x='DS_GENERO', palette= 'viridis')
plt.title('Distribuição por Gênero')  #título do gráfico
ax.bar_label (ax.containers[0],fontsize=8) #rótulos
plt.xlabel('Gênero', fontsize=12) #rótulo do eixo x
plt.ylabel('Eleitores Deficientes', fontsize=12) #rótulo do eixo y

#para aparecer rótulo em todas as categorias
for container in ax.containers:
    ax.bar_label(container,fontsize=8)
    
plt.show() #mostrar o gráfico

# Gráfico de contagem para faixas etárias
import matplotlib.pyplot as plt

#Ordenando

df_def['DS_FAIXA_ETARIA'] = pd.Categorical(df_def['DS_FAIXA_ETARIA'],categories=[
    '16 ANOS', '17 ANOS', '18 A 20 ANOS', '21 A 24 ANOS', '25 A 34 ANOS', 
    '35 A 44 ANOS', '45 A 59 ANOS', '60 A 69 ANOS', '70 A 79 ANOS', 'SUPERIOR A 79 ANOS'],ordered=True)

# gerando o gráfico
plt.Figure(figsize=(12,6))
ax= sns.countplot(data=df_def, x='DS_FAIXA_ETARIA', palette= 'viridis',order=df_def
                  ['DS_FAIXA_ETARIA'].cat.categories)
plt.title('Distribuição por Faixa Etária', fontsize=12)  #título do gráfico
plt.xlabel('Faixa Etária', fontsize=10) #rótulo do eixo x
plt.ylabel('Eleitores Deficientes', fontsize=8) #rótulo do eixo y

#Criando rótulos
for container in ax.containers:
    ax.bar_label(container,fontsize=8)

#rotacionando os rótulos do eixo x
plt.xticks(rotation=45, ha='right', fontsize=8)

#Ajustando layout
plt.tight_layout()

plt.show()

# Grafico de pizza para Raça
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Criando o gráfico
pizza = pd.crosstab (index=df_def['DS_RACA_COR'], columns=df_def ['SG_UF'], normalize=True)

#Plotando o gráfico
plt.pie(pizza.sum (axis=1), #soma os valores de raça
        labels= pizza.index,#RÓTULO COM ÍNDICES DAS SÉRIES
        colors= sns.color_palette('rocket'),
        autopct= '%.1f%%', #valores em percentual
        textprops={'fontsize':10}, #tamanho da fonte dos rotulos
        pctdistance=0.7) #distancia dos percentuais em relaçao ao centro
       
# Adicionando titulo 
 plt.title ('Deficientes por Raça') #FORMATEI O TITULO

# Mostrar o gráfico
 plt.show()

# Analisando quantidade de eleitores perfil e qtd de eleitores def 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#agrupando por estado 
agrupado_por_estado = df.groupby('SG_UF').agg({ #agg cria agregação, nesse caso o sum as colunas
    'QT_ELEITORES_PERFIL':'sum',
    'QT_ELEITORES_DEFICIENCIA':'sum'}).reset_index() #reseta o indice do DF transformando o indice do grupo em coluna normal

#Calculando a proporção de eleitores def
agrupado_por_estado['Proporcao_Deficientes'] = (agrupado_por_estado['QT_ELEITORES_DEFICIENCIA'] / (agrupado_por_estado['QT_ELEITORES_PERFIL'] + agrupado_por_estado['QT_ELEITORES_DEFICIENCIA']))*100

#gráfico de linhas para proporção de aptos e deficientes
plt.figure(figsize=(10,6))
plt.plot(agrupado_por_estado['SG_UF'],agrupado_por_estado['Proporcao_Deficientes'],marker=0, color='#2ecc71',label='Proporção de Eleitores com Deficiência')

#adicionando rótulos nos pontos
for i, proporcao in enumerate(agrupado_por_estado['Proporcao_Deficientes']):
    plt.text(i, proporcao, f'{proporcao:.1f}%', ha='center', va='bottom', fontsize=10) #rotulo para aptos

#f'{aptos:.1f}%' formata em percentual com uma casa dec
#ha= alinha o texto 
#Ajustando ao layout
plt.title('Proporção de Eleitores com Deficiência por Estado', fontsize=12,pad=20)    
plt.xlabel('Estado', fontsize=10)
plt.ylabel('Proporção (%)', fontsize=10)
plt.yticks(fontsize=8)
plt.xticks(fontsize=8)
plt.legend(fontsize=8)
plt.grid(True,linestyle='--', alpha=0.1)
plt.tight_layout()
#mostrar gráfico
plt.show()

-----------------
