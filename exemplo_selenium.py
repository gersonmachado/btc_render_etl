import psutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def monitorar_memoria_completa():
    """
    Monitora o consumo de memória do processo atual e seus filhos.
    """
    processo_principal = psutil.Process()
    memoria_total = processo_principal.memory_info().rss

    # Inclui memória de processos filhos (ex: ChromeDriver)
    for filho in processo_principal.children(recursive=True):
        memoria_total += filho.memory_info().rss

    return memoria_total / (1024 * 1024)  # Converte para MB

def obter_preco_bitcoin_infomoney():
    """
    Utiliza Selenium para pegar o preço atual do Bitcoin em reais no site InfoMoney usando XPath.
    Monitora o uso de memória durante todo o processo, incluindo processos filhos.
    """
    memoria_inicial = monitorar_memoria_completa()
    print(f"🔍 Memória inicial: {memoria_inicial:.2f} MB")

    # Configuração do WebDriver (Chrome)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Medir memória após abrir o navegador
        memoria_apos_webdriver = monitorar_memoria_completa()
        print(f"📈 Memória após abrir o navegador: {memoria_apos_webdriver:.2f} MB")

        # URL do InfoMoney para cotação do Bitcoin
        url = "https://www.infomoney.com.br/cotacoes/cripto/ativo/bitcoin-btc/"
        print("Abrindo o navegador...")
        driver.get(url)

        # Aguardar o carregamento da página
        time.sleep(5)

        # Medir memória após carregar a página
        memoria_apos_carregamento = monitorar_memoria_completa()
        print(f"📈 Memória após carregar a página: {memoria_apos_carregamento:.2f} MB")

        # Localiza o elemento usando o XPath fornecido
        xpath = "/html/body/div[4]/div/div[1]/div[1]/div/div[3]/div[1]/p"
        elemento_preco = driver.find_element(By.XPATH, xpath)

        # Extrai e imprime o preço
        preco_bitcoin = elemento_preco.text.strip()
        print(f"💰 Preço atual do Bitcoin (InfoMoney): {preco_bitcoin}")

        # Medir memória após captura do preço
        memoria_apos_captura = monitorar_memoria_completa()
        print(f"📈 Memória após captura do preço: {memoria_apos_captura:.2f} MB")

    except Exception as e:
        print(f"❌ Erro ao obter o preço: {e}")
    finally:
        # Fecha o navegador
        driver.quit()

        # Medir memória após fechar o navegador
        memoria_final = monitorar_memoria_completa()
        print(f"🔻 Memória final após fechar o navegador: {memoria_final:.2f} MB")

if __name__ == "__main__":
    obter_preco_bitcoin_infomoney()
