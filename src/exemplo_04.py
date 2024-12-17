import requests
import sqlite3
from datetime import datetime
import time

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

    # Estrutura os dados em formato de dicionário
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
    print(f"[{dados['timestamp']}] Dados salvos no SQLite!")

if __name__ == "__main__":
    print("Iniciando ETL com atualização a cada 15 segundos... (CTRL+C para interromper)")
    while True:
        try:
            # Extração e tratamento dos dados
            dados_json = extrair_dados_bitcoin()
            dados_tratados = tratar_dados_bitcoin(dados_json)
            
            # Mostrar os dados tratados no console
            print("Dados Tratados:")
            print(dados_tratados)
            
            # Salvar no SQLite
            salvar_dados_sqlite(dados_tratados)
            
            # Aguarda 15 segundos para a próxima execução
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)  # Aguarda antes de tentar novamente
