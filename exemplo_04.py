import requests

def extrair_cotacao_usd_brl(token):
    """
    Extrai a cotação do dólar (USD) para real (BRL) usando a API da Alpha Vantage.
    
    Parâmetros:
        token (str): Token de autenticação fornecido pela Alpha Vantage.

    Retorna:
        dict: Cotação do USD-BRL com preço de compra, data e hora.
    """
    # URL do endpoint com os parâmetros
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "USD",
        "to_currency": "BRL",
        "apikey": token
    }
    
    # Envia a requisição GET
    print("Solicitando cotação USD-BRL da API Alpha Vantage...")
    resposta = requests.get(url, params=params)
    
    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        dados = resposta.json()
        
        # Processa os dados da resposta
        if "Realtime Currency Exchange Rate" in dados:
            cotacao = dados["Realtime Currency Exchange Rate"]
            resultado = {
                "from_currency": cotacao["1. From_Currency Code"],
                "to_currency": cotacao["3. To_Currency Code"],
                "exchange_rate": float(cotacao["5. Exchange Rate"]),
                "last_updated": cotacao["6. Last Refreshed"]
            }
            return resultado
        else:
            print("Erro: Resposta inesperada da API.")
            print(dados)
            return None
    else:
        print(f"Erro na requisição: {resposta.status_code}")
        return None

if __name__ == "__main__":
    # Substitua com seu token da Alpha Vantage
    TOKEN_ALPHA_VANTAGE = "WUUH3MIZHB8ZPH1S"

    # Executa a função e imprime os resultados
    cotacao = extrair_cotacao_usd_brl(TOKEN_ALPHA_VANTAGE)
    if cotacao:
        print("\n--- Cotação USD-BRL ---")
        print(f"Moeda Origem: {cotacao['from_currency']}")
        print(f"Moeda Destino: {cotacao['to_currency']}")
        print(f"Taxa de Câmbio: R${cotacao['exchange_rate']:.2f}")
        print(f"Última Atualização: {cotacao['last_updated']}")
    else:
        print("❌ Não foi possível obter a cotação USD-BRL.")
