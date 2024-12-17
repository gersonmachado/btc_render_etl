import requests
import sqlite3
from tinydb import TinyDB
from datetime import datetime

def extrair_dados_bitcoin():
    """Extrai o JSON completo da API da Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    return resposta.json()

def tratar_dados_bitcoin(dados_json):
    """Transforma os dados brutos da API e adiciona timestamp."""
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Estrutura os dados em formato de lista de dicionários
    dados_tratados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_tratados

def salvar_dados_sqlite(dados, db_name="bitcoin_dados.db"):
    """Salva os dados em um banco SQLite."""
    # Conectar ao banco SQLite
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Criar a tabela, se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bitcoin_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL,
            criptomoeda TEXT,
            moeda TEXT,
            timestamp TEXT
        )
    ''')
    
    # Inserir os dados no banco
    cursor.execute('''
        INSERT INTO bitcoin_precos (valor, criptomoeda, moeda, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (dados['valor'], dados['criptomoeda'], dados['moeda'], dados['timestamp']))
    
    conn.commit()
    conn.close()
    print("Dados salvos no SQLite!")

def salvar_dados_tinydb(dados, db_name="bitcoin_dados.json"):
    """Salva os dados em um banco NoSQL usando TinyDB."""
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos no TinyDB!")

if __name__ == "__main__":
    # Extração e tratamento dos dados
    dados_json = extrair_dados_bitcoin()
    dados_tratados = tratar_dados_bitcoin(dados_json)
    
    # Mostrar os dados tratados
    print("Dados Tratados:")
    print(dados_tratados)
    
    # Salvar no SQLite
    salvar_dados_sqlite(dados_tratados)
    
    # Salvar no TinyDB
    salvar_dados_tinydb(dados_tratados)