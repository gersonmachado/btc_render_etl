import requests
import tracemalloc

def get_bitcoin_price():
    """Obtém o preço atual do Bitcoin na Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    response = requests.get(url)  # Requisição da API
    data = response.json()
    price = data['data']['amount']
    print(f"Preço atual do Bitcoin: ${price} USD")
    return float(price)

if __name__ == "__main__":
    # Inicia o monitoramento de memória
    tracemalloc.start()

    # Captura o momento inicial
    snapshot_inicio = tracemalloc.take_snapshot()

    # Executa a função para obter o preço do Bitcoin
    get_bitcoin_price()

    # Captura o momento final
    snapshot_fim = tracemalloc.take_snapshot()

    # Pega o pico de memória durante a execução
    memoria_pico = tracemalloc.get_traced_memory()[1] / (1024 * 1024)  # Em MB

    # Exibe o consumo de memória
    print(f"🔍 Pico de memória durante a execução: {memoria_pico:.2f} MB")

    # Para o monitoramento
    tracemalloc.stop()
