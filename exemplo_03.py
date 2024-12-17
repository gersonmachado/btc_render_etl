import requests
import pandas as pd
from datetime import datetime
import os

# Caminho do arquivo CSV
CAMINHO_ARQUIVO = "preco_bitcoin.csv"

# EXTRAÇÃO
def extrair_preco_bitcoin_usd():
    """
    Extrai o preço atual do Bitcoin em USD usando a API pública da Coinbase.
    """
    url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        preco_usd = float(resposta.json()['data']['amount'])
        print(f"Preço do Bitcoin em USD: ${preco_usd:.2f}")
        return preco_usd
    except Exception as e:
        print(f"Erro ao extrair preço do Bitcoin (USD): {e}")
        return None

def extrair_cotacao_usd_brl(token):
    """
    Extrai a cotação do dólar (USD) para real (BRL) usando a API da Brapi.
    """
    url = f'https://brapi.dev/api/v2/currency?currency=USD-BRL&token={token}'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        cotacao = float(resposta.json()['currency'][0]['bidPrice'])
        print(f"Cotação USD-BRL: R${cotacao:.2f}")
        return cotacao
    except Exception as e:
        print(f"Erro ao extrair cotação USD-BRL: {e}")
        return None

# TRANSFORMAÇÃO
def transformar_dados(preco_usd, cotacao_usd_brl, preco_anterior=None):
    """
    Transforma os dados extraídos:
    - Converte o preço de USD para BRL.
    - Adiciona timestamp atual.
    - Calcula a variação percentual em relação ao preço anterior.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    preco_brl = round(preco_usd * cotacao_usd_brl, 2)
    variacao = 0.0
    if preco_anterior:
        variacao = ((preco_brl - preco_anterior) / preco_anterior) * 100

    dados_transformados = {
        "data_hora": timestamp,
        "preco_usd": round(preco_usd, 2),
        "cotacao_usd_brl": round(cotacao_usd_brl, 2),
        "preco_brl": preco_brl,
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
    colunas = ["data_hora", "preco_usd", "cotacao_usd_brl", "preco_brl", "variacao_percentual"]
    if not os.path.exists(CAMINHO_ARQUIVO):
        df = pd.DataFrame([dados])
        df.to_csv(CAMINHO_ARQUIVO, index=False, sep=';', mode='w', header=True)
    else:
        df = pd.DataFrame([dados])
        df.to_csv(CAMINHO_ARQUIVO, index=False, sep=';', mode='a', header=False)
    print(f"Dados salvos: {dados}")

# PIPELINE
def executar_pipeline(token_brapi):
    """
    Executa o pipeline ETL:
    - Extrai o preço do Bitcoin em USD.
    - Extrai a cotação USD-BRL.
    - Transforma os dados, convertendo para BRL e adicionando variação.
    - Carrega os dados no CSV.
    """
    preco_usd = extrair_preco_bitcoin_usd()
    cotacao_usd_brl = extrair_cotacao_usd_brl(token_brapi)

    if preco_usd is not None and cotacao_usd_brl is not None:
        # Carregar preço anterior, se disponível
        if os.path.exists(CAMINHO_ARQUIVO):
            df = pd.read_csv(CAMINHO_ARQUIVO, sep=';')
            preco_anterior = df.iloc[-1]['preco_brl']
        else:
            preco_anterior = None

        # Transformar os dados
        dados_transformados = transformar_dados(preco_usd, cotacao_usd_brl, preco_anterior)

        # Salvar os dados no CSV
        salvar_dados_csv(dados_transformados)
    else:
        print("Pipeline interrompido devido a erro na extração.")

# EXECUÇÃO DO PIPELINE
if __name__ == "__main__":
    # Substitua 'SEU_TOKEN' pelo token da API Brapi
    TOKEN_BRAPI = "7HTpCQf9z7qUKrwBJftoTh"
    executar_pipeline(TOKEN_BRAPI)
