import pandas as pd
from datetime import datetime
import numpy as np


print('Iniciando a leitura do arquivo Excel...')   
#lê o arquivo Excel
df = pd.read_excel('prova/dio.xlsx')
nintendo = df.copy()

print('leitura concluída')


#altera a coluna 'Game' para separar o nome do jogo e a plataforma
nintendo[['Game', 'Platform']] = nintendo['Game'].str.rsplit(' - ', n=1, expand=True)

#remove o prefixo 'Batch-' da coluna 'Batch' e espaços em branco
nintendo['Batch'] = nintendo['Batch'].str.removeprefix('Batch-').str.strip()


#substitui os valores '----', '---', '-----' por NaN
nintendo = nintendo.replace(['----', '---', '-----'], np.nan)


#remove linhas onde todas as colunas são NaN
nintendo = nintendo.dropna(how='all')

#altera a coluna 'Send Date' para o formato datetime
nintendo['Send Date'] = pd.to_datetime(nintendo['Send Date'], dayfirst=True, errors='coerce')

#mapeia os valores da coluna 'Region' para nomes completos
TRADUCAO = {
    'PT': 'Português',
    'EN': 'Inglês',
    'JP': 'Japonês'
} 


nintendo['Region'] = nintendo['Region'].map(TRADUCAO)


#remove o símbolo de moeda e converte a coluna 'Preço Unit Price' para float
nintendo['Preço Unit Price'] = nintendo['Preço Unit Price'].apply(lambda x : float(str(x).replace('$', '').replace('R$','').replace(',','.').strip())if isinstance(x, str) else x )

#cria a coluna 'preco_total' como o produto da 'Stock Quantity' e 'Preço Unit Price'
nintendo['preco_total'] = nintendo ['Stock Quantity'] * nintendo ['Preço Unit Price']



print('Iniciando a exportação do arquivo Excel...')
#exporta o DataFrame limpo para um novo arquivo Excel
nintendo.to_excel('prova/nitendo.xlsx', index=False)

print('Arquivo exportado com sucesso!')
