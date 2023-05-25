import psycopg2

def obter_dados_tabela(processo):
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="teste",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM public.documentos_projetoufg_visuallaws where numero_processo = '"+processo+"'")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

