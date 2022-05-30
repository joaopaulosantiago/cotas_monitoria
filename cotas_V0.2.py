#!/usr/bin/env python
# coding: utf-8

# In[1]:
from datetime import datetime
from PIL import Image
import pandas as pd
import streamlit as st
import psycopg2
import time
###########################################################################################################
df_docente = pd.read_excel("Oferta_2022-1.xlsx", sheet_name = "Docente")
lista_docente = list(pd.read_excel("Oferta_2022-1.xlsx", sheet_name = "Docente")['Docente'])
lista_docente.append("")
lista_docente = sorted(lista_docente)
lista_disciplina = list(pd.read_excel("Oferta_2022-1.xlsx", sheet_name = "Disciplina")['Disciplina'])
lista_disciplina.append("")
lista_disciplina = sorted(lista_disciplina)
lista_qtdeMonitores = [i+1 for i in range(10)]
image = Image.open('UnB_ENM.png')
add_selectbox = st.sidebar.selectbox("Menu",("Inserir", "Consultar"))




###########################################################################################################

###########################################################################################################
###########################################################################################################
if add_selectbox == "Inserir":
    
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    }
    </style>    '''

    st.image(image)
    st.header("Formulário de Solicitação de Monitores")
    with st.form("CotasMonitoria", clear_on_submit = True):
        docente = st.selectbox(
             'Docente',lista_docente)
        
        disciplina = st.selectbox(
             'Disciplina',lista_disciplina)
        
        quantidade = st.number_input("Quantidade de Monitores", min_value = 1, max_value = 10, step = 1)
        
        enviar = st.form_submit_button("Enviar")


        if enviar:
            if docente == '':
                st.write('*Favor informar nome')
            if disciplina == '':
                st.write('*Favor informar uma disciplina')
            else:
                data_atual = datetime.now()
                data_hora = data_atual.strftime('%d/%m/%Y - %H:%M:%S')
                
                
                # Conectando a uma base de dados
                conexao = psycopg2.connect(host = st.secrets["db_host"], 
                                           database = st.secrets["db_database"],
                                           user = st.secrets["db_user"], 
                                           password = st.secrets["db_password"])        


                cursor = conexao.cursor()

                # cursor.execute("CREATE TABLE cotas_monitoria (id_cotas serial PRIMARY KEY, data_hora varchar, docente varchar, disciplina varchar, qtde_monitores integer);")

                # Executando um comando
                cursor.execute("INSERT INTO cotas_monitoria (data_hora, docente, disciplina, qtde_monitores) VALUES (%s, %s, %s, %s)",(data_hora, docente, disciplina, quantidade))
                # Fazendo mudanças no banco de dados de modo permanente
                conexao.commit()
                # Encerrando comunicação com o banco de dados
                cursor.close()
                conexao.close()
                
                # Exibindo o sucesso da operação
                st.success("Solicitação Enviada com Sucesso")

###########################################################################################################
if add_selectbox == "Consultar":
    st.image(image)
    
    st.header("Registro de Solicitações de Monitores")
    conexao = psycopg2.connect(host = st.secrets["db_host"], 
                               database = st.secrets["db_database"],
                               user = st.secrets["db_user"], 
                               password = st.secrets["db_password"])     
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cotas_monitoria;")
    df_solicitacoes = cursor.fetchall()
    df_solicitacoes = pd.DataFrame(df_solicitacoes, columns=['ID','Data-Hora', 'Docente','Disciplina' ,'Qtde Monitores'])
    df_solicitacoes.set_index('ID', inplace = True)
    st.table(df_solicitacoes)
#     st.dataframe(data=df_consolidado, width=700, height=1000)
