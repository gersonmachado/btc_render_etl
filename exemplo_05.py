from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def obter_preco_bitcoin_infomoney():
    """
    Utiliza Selenium para pegar o preço atual do Bitcoin em reais no site InfoMoney usando XPath.
    """
    # Configuração do WebDriver (Chrome)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # URL do InfoMoney para cotação do Bitcoin
        url = "https://www.infomoney.com.br/cotacoes/cripto/ativo/bitcoin-btc/"
        print("Abrindo o navegador...")
        driver.get(url)

        # Aguardar o carregamento da página
        time.sleep(5)  # Ajuste o tempo conforme necessário

        # Localiza o elemento usando o XPath fornecido
        xpath = "/html/body/div[4]/div/div[1]/div[1]/div/div[3]/div[1]/p"
        elemento_preco = driver.find_element(By.XPATH, xpath)

        # Extrai e imprime o preço
        preco_bitcoin = elemento_preco.text.strip()
        print(f"💰 Preço atual do Bitcoin (InfoMoney): {preco_bitcoin}")

    except Exception as e:
        print(f"❌ Erro ao obter o preço: {e}")
    finally:
        # Fecha o navegador
        driver.quit()

if __name__ == "__main__":
    obter_preco_bitcoin_infomoney()
