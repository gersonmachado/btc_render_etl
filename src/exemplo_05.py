import requests
from sqlalchemy import create_engine, Column, Float, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

# Configuração do banco de dados PostgreSQL hospedado no Azure
DATABASE_URL = "postgresql://jornadadedados:mudar123@bancodedadospostgres.postgres.database.azure.com:5432/postgres?sslmode=require"

# Configurar SQLAlchemy
Base = declarative_base()

class BitcoinPreco(Base):
    """Define a tabela no banco de dados."""
    __tablename__ = "bitcoin_precos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String, nullable=False)
    moeda = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

# Cria o engine e a sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Função para criar a tabela no banco de dados
def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")

# Função de extração
def extrair_dados_bitcoin():
    """Extrai o JSON completo da API da Coinbase."""
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro na API: {resposta.status_code}")
        return None

# Função de tratamento
def tratar_dados_bitcoin(dados_json):
    """Transforma os dados brutos da API e adiciona timestamp."""
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    timestamp = datetime.now()

    # Estrutura os dados em formato de dicionário
    dados_tratados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_tratados

# Função para salvar no PostgreSQL
def salvar_dados_postgres(dados):
    """Salva os dados no banco PostgreSQL."""
    session = Session()
    novo_registro = BitcoinPreco(
        valor=dados['valor'],
        criptomoeda=dados['criptomoeda'],
        moeda=dados['moeda'],
        timestamp=dados['timestamp']
    )
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")

# Loop principal
if __name__ == "__main__":
    # Cria a tabela no banco
    criar_tabela()
    print("Iniciando ETL com atualização a cada 15 segundos... (CTRL+C para interromper)")

    while True:
        try:
            # Extração e tratamento dos dados
            dados_json = extrair_dados_bitcoin()
            if dados_json:
                dados_tratados = tratar_dados_bitcoin(dados_json)

                # Mostrar os dados tratados no console
                print("Dados Tratados:")
                print(dados_tratados)

                # Salvar no PostgreSQL
                salvar_dados_postgres(dados_tratados)

            # Aguarda 15 segundos para a próxima execução
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)  # Aguarda antes de tentar novamente
