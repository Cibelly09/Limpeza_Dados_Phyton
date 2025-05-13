# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 08:21:33 2025

@author: Cibelly Viegas
"""
# Importando as bibliotecas necessárias
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

# Defina o diretório correto
os.chdir(r"C:\Users\Cibelly Viegas\Desktop\TCC 24\TCC\PROJECT OFICIAL")

#Nome do arquivo
arquivo_nome = "perfil_eleitorado_2024.original.csv"

#verificando se o caminho existe
caminho_arquivo = os.path.join(os.getcwd(), arquivo_nome)
print("\nVerificando o caminho do arquivo:", caminho_arquivo)

if os.path.exists(caminho_arquivo):
    # Lendo o arquivo
    df = pd.read_csv(caminho_arquivo, delimiter=";",encoding="latin1")
    print("\nArquivo encontrado e carregado com sucesso.")
    print (df.head())
else:
    print("Arquivo não encontrado.", caminho_arquivo)
    
# Visualizando as primeiras linhas do DataFrame
print(df.head())

# Checando informações sobre as colunas e o tipo de dados
print(df.columns)
print(df.info())

# Quantas linhas e colunas tem no DataFrame
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

# Selecionando variáveis de interesse para análise
df_def = df[['SG_UF', 'QT_ELEITORES_DEFICIENCIA', 'DS_RACA_COR', 'DS_GRAU_ESCOLARIDADE', 
             'DS_FAIXA_ETARIA', 'DS_ESTADO_CIVIL', 'DS_GENERO']]

# Limpando a base de dados (removendo valores nulos e indesejados)
df_def = df_def[df_def['QT_ELEITORES_DEFICIENCIA'].notna() & (df_def['QT_ELEITORES_DEFICIENCIA'] > 0)]
df_def = df_def[~df_def.applymap(lambda x: x in ['Prefere nAo informar', 'NAO INFORMADO', 'Inválida']).any(axis=1)]

# Verificando a estrutura da base após a limpeza
print(df_def.info())
print(df_def.head())

# Estatísticas descritivas para a variável quantitativa 'QT_ELEITORES_DEFICIENCIA'
print(df_def[['QT_ELEITORES_DEFICIENCIA']].describe())

# Tabelas de frequência para variáveis qualitativas
print(df_def['DS_RACA_COR'].value_counts())
print(df_def['DS_GRAU_ESCOLARIDADE'].value_counts())
print(df_def['DS_FAIXA_ETARIA'].value_counts())
print(df_def['DS_ESTADO_CIVIL'].value_counts())
print(df_def['DS_GENERO'].value_counts())

# Normalizando a base para maiúsculas nas variáveis qualitativas
df_def = df_def.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Visualização dos dados em gráficos
pio.renderers.default = 'browser'

# Gráfico de contagem por Gênero
plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df_def, x='DS_GENERO', palette='viridis')
plt.title('Distribuição por Gênero')
ax.bar_label(ax.containers[0], fontsize=8)
plt.xlabel('Gênero')
plt.ylabel('Eleitores Deficientes')
plt.show()

# Gráfico de contagem por Faixa Etária
df_def['DS_FAIXA_ETARIA'] = pd.Categorical(df_def['DS_FAIXA_ETARIA'], categories=[
    '16 ANOS', '17 ANOS', '18 A 20 ANOS', '21 A 24 ANOS', '25 A 34 ANOS', 
    '35 A 44 ANOS', '45 A 59 ANOS', '60 A 69 ANOS', '70 A 79 ANOS', 'SUPERIOR A 79 ANOS'], ordered=True)

plt.figure(figsize=(12, 6))
ax = sns.countplot(data=df_def, x='DS_FAIXA_ETARIA', palette='viridis', order=df_def['DS_FAIXA_ETARIA'].cat.categories)
plt.title('Distribuição por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Eleitores Deficientes')
for container in ax.containers:
    ax.bar_label(container, fontsize=8)
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()
plt.show()

# Gráfico de Pizza para Raça
pizza = pd.crosstab(index=df_def['DS_RACA_COR'], columns=df_def['SG_UF'], normalize=True)
plt.pie(pizza.sum(axis=1), labels=pizza.index, colors=sns.color_palette('rocket'),
        autopct='%.1f%%', textprops={'fontsize': 10}, pctdistance=0.7)
plt.title('Deficientes por Raça')
plt.show()

# Analisando a quantidade de eleitores por estado e a proporção de deficientes
agrupado_por_estado = df.groupby('SG_UF').agg({
    'QT_ELEITORES_PERFIL': 'sum',
    'QT_ELEITORES_DEFICIENCIA': 'sum'}).reset_index()

# Calculando a proporção de deficientes
agrupado_por_estado['Proporcao_Deficientes'] = (
    agrupado_por_estado['QT_ELEITORES_DEFICIENCIA'] / 
    (agrupado_por_estado['QT_ELEITORES_PERFIL'] + agrupado_por_estado['QT_ELEITORES_DEFICIENCIA'])) * 100

# Gráfico de linhas para proporção de deficientes por estado
plt.figure(figsize=(10, 6))
plt.plot(agrupado_por_estado['SG_UF'], agrupado_por_estado['Proporcao_Deficientes'], marker='o', color='#2ecc71', label='Proporção de Eleitores com Deficiência')
for i, proporcao in enumerate(agrupado_por_estado['Proporcao_Deficientes']):
    plt.text(i, proporcao, f'{proporcao:.1f}%', ha='center', va='bottom', fontsize=10)
plt.title('Proporção de Eleitores com Deficiência por Estado')
plt.xlabel('Estado')
plt.ylabel('Proporção (%)')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.1)
plt.tight_layout()
plt.show()

