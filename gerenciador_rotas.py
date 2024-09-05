import streamlit as st
import pandas as pd
import json
from datetime import datetime
from datetime import date
import os
import numpy as np

# Inicializar o estado da sessão para dataframes
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['nome_cliente',
                                                'Consumo Médio',
                                                'Preço_litro',
                                                'km_inicial',
                                                'km_final',
                                                'data_viagem'])


# Criar um dataframe para armazenar as entregas
deliveries = pd.DataFrame(columns=['nome_cliente',
                                   'Consumo Médio',
                                   'Preço_litro',
                                   'km_inicial', 
                                   'km_final', 
                                   'data_viagem'])

# Convert the 'data' column to datetime format
deliveries['data_viagem'] = pd.to_datetime(deliveries['data_viagem'])

caminho = 'deliveries.csv'
caminho_nomes = 'nomes.csv'
caminho_config = 'config.csv'
caminho_inicio = 'inicio.csv'
caminho_fim = 'fim.csv'

#Novo banco de dados
dados = []

# Função para definir o nome do cliente
def nome_cliente():
    nome_cliente = st.text_input('Nome_Cliente')
    

    dados.extend([
        {"Nome do Cliente" : [nome_cliente]}
    ])
        
    if st.button("Salvar Configurações"):
        new_row = pd.DataFrame({
            "Nome_Cliente": [nome_cliente]})
        # Escrever os dados no arquivo CSV
        if os.path.isfile(caminho_nomes):
            new_row.to_csv('nomes.csv', mode='a', header=False, index=False)
        else:
            new_row.to_csv('nomes.csv', mode='a', header=True, index=False)
        st.success("Cliente adicionado com sucesso!")

# Função para definir o consumo médio
def consumo():
    consumo_medio = st.number_input('Consumo Médio')
    preco_litro = st.number_input('Preço por Litro')
    
    dados.extend([
        {"consumo" : [consumo_medio], "preco_litro" : [preco_litro]}
    ])
    
    if st.button("Salvar Configurações"):
        new_row = pd.DataFrame({
            "consumo" : [consumo_medio], 
            "preco_litro" : [preco_litro]})

        # Escrever os dados no arquivo CSV
        if os.path.isfile(caminho_config):
            new_row.to_csv('config.csv', mode='a', header=False, index=False)
        else:
            new_row.to_csv('config.csv', mode='a', header=True, index=False) 
        st.success("Configurações adicionadas com sucesso!")

def iniciar_entrega():
    km_inicial = st.number_input('Km Inicial')
    data_viagem = st.date_input("Data da entrega:", value=date.today())
    
    # Verificar se o arquivo nomes.csv existe
    if not os.path.isfile(caminho_nomes):
        # Criar o arquivo se ele não existir
        with open(caminho_nomes, 'w') as f:
            f.write('Nome_Cliente\n')
            
    # Ler os dados do arquivo nomes.csv
    nomes_df = pd.read_csv(caminho_nomes)
    
    # Verificar se o arquivo inicio.csv existe
    if not os.path.isfile(caminho_inicio):
        # Criar o arquivo se ele não existir
        with open(caminho_inicio, 'w') as f:
            f.write('Nome_Cliente,data_entrega,Km Inicial\n')    
            
    # Selecionar o nome do cliente
    nome_cliente = st.selectbox('Nome do Cliente', nomes_df['Nome_Cliente'].unique())
    
    # Ler os dados do arquivo inicio.csv
    inicio_df = pd.read_csv(caminho_inicio)
    
    # Botão para salvar os dados
    if st.button("Salvar"):
        # Criar uma nova linha com os dados da entrega
        new_row = pd.DataFrame({'Nome_Cliente': [nome_cliente], 'Km Inicial': [km_inicial], 'data_entrega': [data_viagem]})
        
        # Adicionar a nova linha ao dataframe existente
        inicio_df = pd.concat([inicio_df, new_row], ignore_index=True)
        
        # Escrever os dados atualizados no arquivo CSV
        inicio_df.to_csv(caminho_inicio, index=False)
        st.success("Dados salvos com sucesso!")

def finalizar_entrega():
    km_final = st.number_input('Km Final')
    data_final = st.date_input("Data de finalização:", value=date.today())
    
    # Verificar se o arquivo nomes.csv existe
    if not os.path.isfile(caminho_nomes):
        # Criar o arquivo se ele não existir
        with open(caminho_nomes, 'w') as f:
            f.write('Nome_Cliente\n')
            
    # Ler os dados do arquivo nomes.csv
    nomes_df = pd.read_csv(caminho_nomes)
    
    # Verificar se o arquivo final.csv existe
    if not os.path.isfile(caminho_fim):
        # Criar o arquivo se ele não existir
        with open(caminho_fim, 'w') as f:
            f.write('Nome_Cliente,data_final,Km Final\n')    
            
    # Selecionar o nome do cliente
    nome_cliente = st.selectbox('Nome do Cliente', nomes_df['Nome_Cliente'].unique())
    
    # Ler os dados do arquivo final.csv
    final_df = pd.read_csv(caminho_fim)
    
    # Botão para salvar os dados
    if st.button("Salvar"):
        # Criar uma nova linha com os dados da finalização
        new_row = pd.DataFrame({'Nome_Cliente': [nome_cliente], 'Km Final': [km_final], 'data_final': [data_final]})
        
        # Adicionar a nova linha ao dataframe existente
        final_df = pd.concat([final_df, new_row], ignore_index=True)
        
        # Escrever os dados atualizados no arquivo CSV
        final_df.to_csv(caminho_fim, index=False)
        st.success("Dados de finalização salvos com sucesso!")
        
# Verifica se o arquivo CSV existe
if os.path.isfile(caminho):
    dados_df = pd.read_csv('deliveries.csv')
    print(dados_df)
else:
    pass

# Função km total por viagem
def km_da_viagem():
    nomes = pd.read_csv('nomes.csv')
    config = pd.read_csv('config.csv')
    inicio = pd.read_csv('inicio.csv')
    fim = pd.read_csv('fim.csv')
    
    geral = pd.concat([nomes, inicio, fim], axis=0)
    print(geral)
    
    df_agrupado = geral.groupby('Nome_Cliente').agg({
    'data_entrega': lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan,
    'Km Inicial': lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan,
    'Km Final': lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan}).reset_index()

    geral = df_agrupado
    print(geral)
    
    geral['Km_Total'] = geral['Km Final'] - geral['Km Inicial']
    print(geral)
    
    config = pd.read_csv('config.csv')
    
    geral['Custo_Total'] = (geral['Km_Total'] / config['consumo'].values) * config['preco_litro'].values
    
    geral.to_csv('geral.csv')
    
    st.write(geral)
    
    
# Função grafico
def mostrar_grafico():
    geral = pd.read_csv('geral.csv')
    chart_data = pd.DataFrame(geral)

    st.subheader("Gastos em reais")
    # st.line_chart(geral.groupby('data_entrega')['Custo_Total'].mean())
    # st.line_chart(geral.groupby('data_entrega')['Km_Total'].mean())
    st.bar_chart(chart_data, x="data_entrega", y="Custo_Total", color="Km_Total")


    
# Função Gastos
def mostrar_gastos():
    geral = pd.read_csv('geral.csv')
    config = pd.read_csv('config.csv')
    
    geral['Custo_Total'] = (geral['Km_Total'] / config['consumo'].values) * config['preco_litro'].values
    print(geral)
    
    
    # st.subheader("Custos em reais")
    # st.line_chart(geral.groupby('data_entrega')['Custo_Total'].mean())

# Criar a aplicação web
st.title('Gestão de Entregas')

# Barra lateral para navegação
menu = st.sidebar.selectbox("Menu", ["Configurações", "Iniciar Entrega", "Finalizar Entrega", "Relatórios"])

if menu == "Configurações":
    st.header("Configurações")
    consumo()

if menu == "Iniciar Entrega":
    st.subheader("Preencha os dados a baixo")
    nome_cliente()

if menu == "Iniciar Entrega":
    st.subheader("Iniciar Entrega")
    iniciar_entrega()
    
if menu == "Finalizar Entrega":
    st.header("Finalizar Entrega")
    finalizar_entrega()
    
if menu == "Relatórios":
    st.subheader("Entregas")
    km_da_viagem()
    mostrar_grafico()
    mostrar_gastos()