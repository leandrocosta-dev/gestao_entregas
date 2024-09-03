import streamlit as st
import pandas as pd
import json
from datetime import datetime
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

# Função para adicionar uma entrega
def add_delivery():
    nome_cliente = st.text_input('Nome do Cliente')
    consumo_medio = st.number_input('Consumo Médio')
    preco_litro = st.number_input('Preço por Litro')
    km_inicial = st.number_input('Km Inicial')
    km_final = st.number_input('Km Final')
    data_viagem = st.date_input("Data de Cadastro:")
    
    deliveries.loc[len(deliveries)] = [ nome_cliente,consumo_medio, preco_litro, km_inicial, km_final, data_viagem]
    
    if st.button("cadastrar viagem"):
        new_row = pd.DataFrame({
            "Nome_Cliente": [nome_cliente],
            "Consumo_medio": [consumo_medio],
            "preco_litro": [preco_litro],
            "km Inicial": [km_inicial],
            "km Final": [km_final],
            "Data de Cadastro": [data_viagem],
        })
        
        # Escrever os dados no arquivo CSV
        if os.path.isfile(caminho):
            new_row.to_csv('deliveries.csv', mode='a', header=False, index=False)
        else:
            new_row.to_csv('deliveries.csv', mode='a', header=True, index=False)
        
        st.success("Entrega adicionada com sucesso!")


# Verifica se o arquivo CSV existe
if os.path.isfile(caminho):
    dados_df = pd.read_csv('deliveries.csv')
    print(dados_df)
else:
    pass

# Função km total por viagem
def km_da_viagem():
    data_inicial = str(st.date_input('Data Inicial'))
    data_final = str(st.date_input('Data Final'))
    km_periodo_df = dados_df.loc[(dados_df['Data de Cadastro'] >= data_inicial) & (dados_df['Data de Cadastro']<= data_final)]
    km_geral = km_periodo_df['km Final'] - km_periodo_df['km Inicial']
    km_total = km_geral.sum()
    st.subheader(km_total)
    print(km_total)

# Função listar entregas
def listar_entregas():
    entregas = dados_df
    custo_entrega = ((dados_df['km Final'] - dados_df['km Inicial']) / dados_df['Consumo_medio']) * dados_df['preco_litro']  
    # st.subheader("R$" + custo_entrega.to_string(index=False, header=False) + "0")
    entrega_completa = dados_df['Custo em reais'] = custo_entrega
    print(entrega_completa)
    st.dataframe(entregas)
    
# Função grafico
def mostrar_grafico():
    st.subheader("Custo por dia")
    st.line_chart(dados_df.groupby('Data de Cadastro')['Custo em reais'].mean())

# Criar a aplicação web
st.title('Gestão de Entregas')

# Barra lateral para navegação
menu = st.sidebar.selectbox("Menu", ["Adicionar Entrega", "Relatórios"])

if menu == "Adicionar Entrega":
    st.header("Adicionar Entrega")
    add_delivery()
    
if menu == "Relatórios":
    st.header("Km Percorrido")
    km_da_viagem()

if menu == "Relatórios":
    st.header("Entregas Realizadas")
    listar_entregas()
    
if menu == "Relatórios":
    st.header("")
    mostrar_grafico()

