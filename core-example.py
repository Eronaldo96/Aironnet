from urllib.parse import quote_plus

import pyodbc
from sqlalchemy import create_engine

parametros = (
    # Driver que será utilizado na conexão
    'DRIVER={ODBC Driver 17 for SQL Server};'
    # IP ou nome do servidor.
    'SERVER=ip;'
    # Porta
    'PORT=1433;'
    # Banco que será utilizado.
    'DATABASE=banco;'
    # Nome de usuário.
    'UID=user;'
    # Senha/Token.
    'PWD=password')

url_db = quote_plus(parametros)

db = create_engine("mssql+pyodbc:///?odbc_connect=%s" % url_db)

conexao = db.connect()

resultado = conexao.execute("SELECT * FROM PARCEIRO")

for row in resultado:
     print(row)
