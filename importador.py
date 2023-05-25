import psycopg2

# Parâmetros de conexão com o banco de dados
host = '127.0.0.7'
port = '5432'
database = 'teste'
user = 'postgres'
password = 'postgres'

# Função para obter os dados da tabela
def obter_dados_tabela():
    # Estabelecer conexão com o banco de dados
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    # Criar um cursor para executar comandos SQL
    cur = conn.cursor()

    # Executar a consulta SQL
    cur.execute("SELECT * FROM public.documentos_projetoufg_visuallaws")

    # Obter todos os resultados da consulta
    resultados = cur.fetchall()

    # Fechar o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    # Retornar os resultados
    return resultados

# Chamar a função para obter os dados da tabela
dados_tabela = obter_dados_tabela()

# Imprimir os resultados
for linha in dados_tabela:
    print(linha)
