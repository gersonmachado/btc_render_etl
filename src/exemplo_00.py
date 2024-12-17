import requests

def obter_preco_bitcoin():
    """Obtém o preço atual do Bitcoin na Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    dados = resposta.json()
    return dados

if __name__ == "__main__":
    print(obter_preco_bitcoin())
