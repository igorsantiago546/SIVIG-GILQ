import sqlite3
import pyodbc




# 1. Configurações de Conexão
sqlite_db = 'seu_arquivo.db'
sql_server_config = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=100.51.226.160,1433;" # Vírgula 1433 força a porta
    "Database=faculdadeimpacta;"
    "UID=igoradm;"
    "PWD=Impacta123456;"
    "TrustServerCertificate=yes;"# A senha que você definiu na instalação # Use UID e PWD se não for autenticação Windows
)

dados_conexao = (
    
)
tabela_alvo = "aluno"
nome_arquivo_sqlite = "meu_banco_exportado.db"

try:
    conexao = pyodbc.connect(sql_server_config)
    print("Conexão estabelecida!")
    
    # 3. Agora o cursor reconhece a conexao
    cursor = conexao.cursor()
    
    # Exemplo de INSERT
    sql = "INSERT INTO aluno (Nome, Idade) VALUES (?, ?)"
    valores = ('Osvaldo Cruz', 102)
    
    cursor.execute(sql, valores)
    conexao.commit()
    print("Dados inseridos!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    # 4. Sempre feche se a conexao existir
    if 'conexao' in locals():
        conexao.close()

def exportar_sql_para_sqlite():
    try:
        # Conecta no SQL Server
        conn_sql = pyodbc.connect(sql_server_config)
        cursor_sql = conn_sql.cursor()
        
        # Busca os dados e os nomes das colunas
        print(f"Extraindo dados da {tabela_alvo} no SQL Server...")
        cursor_sql.execute(f"SELECT * FROM {tabela_alvo}")
        colunas = [column[0] for column in cursor_sql.description]
        dados = cursor_sql.fetchall()

        # Conecta (ou cria) o arquivo SQLite
        conn_sqlite = sqlite3.connect(nome_arquivo_sqlite)
        cursor_sqlite = conn_sqlite.cursor()

        # Cria a tabela no SQLite com as mesmas colunas
        colunas_str = ", ".join([f"[{c}] TEXT" for c in colunas]) # Criando como TEXT para simplificar
        cursor_sqlite.execute(f"DROP TABLE IF EXISTS {tabela_alvo}")
        cursor_sqlite.execute(f"CREATE TABLE {tabela_alvo} ({colunas_str})")

        # Insere os dados
        placeholders = ", ".join(["?"] * len(colunas))
        cursor_sqlite.executemany(f"INSERT INTO {tabela_alvo} VALUES ({placeholders})", [tuple(row) for row in dados])

        conn_sqlite.commit()
        print(f"Sucesso! O arquivo '{nome_arquivo_sqlite}' foi gerado e já pode ser aberto no SQLite Viewer.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'conn_sql' in locals(): conn_sql.close()
        if 'conn_sqlite' in locals(): conn_sqlite.close()
        
exportar_sql_para_sqlite()