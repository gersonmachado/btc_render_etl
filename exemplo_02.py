import requests
import pandas as pd
from datetime import datetime
import os

# Caminho do arquivo CSV
CAMINHO_ARQUIVO = "preco_bitcoin.csv"

# EXTRAÇÃO
def extrair_preco_bitcoin():
    """
    Extrai o preço atual do Bitcoin usando a API pública da Coinbase.
    Retorna o preço como float.
    """
    url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
    resposta = requests.get(url)
    preco = float(resposta.json()['data']['amount'])
    print(f"Preço atual do Bitcoin: ${preco:.2f} USD")
    return preco

# TRANSFORMAÇÃO
def transformar_dados(preco_atual, preco_anterior=None):
    """
    Transforma os dados extraídos.
    - Adiciona timestamp atual.
    - Calcula a variação percentual em relação ao preço anterior.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    variacao = 0.0
    if preco_anterior:
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

    dados_transformados = {
        "data_hora": timestamp,
        "preco_usd": round(preco_atual, 2),
        "variacao_percentual": round(variacao, 2)
    }
    return dados_transformados

# CARGA
def salvar_dados_csv(dados):
    """
    Salva os dados transformados em um arquivo CSV.
    - Se o arquivo não existir, cria com cabeçalho.
    - Caso exista, adiciona uma nova linha.
    """
    colunas = ["data_hora", "preco_usd", "variacao_percentual"]
    if not os.path.exists(CAMINHO_ARQUIVO):
        df = pd.DataFrame([dados])
        df.to_csv(CAMINHO_ARQUIVO, index=False, sep=';', mode='w', header=True)
    else:
        df = pd.DataFrame([dados])
        df.to_csv(CAMINHO_ARQUIVO, index=False, sep=';', mode='a', header=False)
    print(f"Dados salvos: {dados}")

# PIPELINE
def executar_pipeline():
    """
    Executa o pipeline ETL:
    - Extrai o preço atual do Bitcoin.
    - Transforma os dados, adicionando timestamp e variação.
    - Carrega os dados em um arquivo CSV.
    """
    preco_atual = extrair_preco_bitcoin()
    if preco_atual is not None:
        # Carregar preço anterior, se disponível
        if os.path.exists(CAMINHO_ARQUIVO):
            df = pd.read_csv(CAMINHO_ARQUIVO, sep=';')
            preco_anterior = df.iloc[-1]['preco_usd']
        else:
            preco_anterior = None

        # Transformar os dados
        dados_transformados = transformar_dados(preco_atual, preco_anterior)

        # Salvar os dados no CSV
        salvar_dados_csv(dados_transformados)
    else:
        print("Pipeline interrompido devido a erro na extração.")

# EXECUÇÃO DO PIPELINE
if __name__ == "__main__":
    executar_pipeline()
