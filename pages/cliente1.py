import streamlit as st
import sqlite3
import pandas as pd

# Função para criar a tabela no banco de dados se não existir
def criar_tabela():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            telefone TEXT
        )
    """)
    conn.commit()
    conn.close()

# Função para adicionar um cliente ao banco de dados
def adicionar_cliente(nome, email, telefone):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (UPPER(?), ?, LOWER(?))", (nome, email, telefone))
    conn.commit()
    conn.close()

# Função para recuperar os dados dos clientes do banco de dados
def obter_clientes():
    conn = sqlite3.connect("clientes.db")
    query = "SELECT * FROM clientes"
    clientes_df = pd.read_sql_query(query, conn)
    conn.close()
    return clientes_df

def limpar_form(nome,email,telefone):
    st.text_input("Nome:")
    email = st.text_input("E-mail:")
    telefone = st.text_input("Telefone:")

# Função principal
def main():
    st.title("Cadastro de Clientes")

    # Criar a tabela no banco de dados se não existir
    criar_tabela()

    # Formulário para adicionar um novo cliente
    st.header("Adicionar Novo Cliente")
    nome = st.text_input("Nome:")
    email = st.text_input("E-mail:")
    telefone = st.text_input("Telefone:")

    if st.button("Adicionar Cliente"):
        if nome and email and telefone:
            adicionar_cliente(nome, email, telefone)
            st.success("Cliente adicionado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos.")

    # Exibir a lista de clientes em uma tabela customizada
    st.header("Lista de Clientes")
    clientes_df = obter_clientes()

    if not clientes_df.empty:
        # Exibir tabela customizada usando o streamlit
        st.dataframe(clientes_df)
    else:
        st.info("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()