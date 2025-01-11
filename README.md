 
# 💰 **Data Pipeline: Extração de Dados Bitcoin com ETL em Python**  
---

Esquema do projeto: [app.excalidraw.com](https://app.excalidraw.com/s/8pvW6zbNUnD/9zZctm3OR9f)

---

## **Introdução**  

Pipelines de dados ETL (Extract, Transform, Load). O objetivo é construir um programa que consome dados de uma **API**, organizar esses dados e armazenar em uma base de dados ao longo do tempo.  


## **Tecnologias Utilizadas**  
- **Python 3.12**  
- **Bibliotecas**:  
   - `requests`: Para consumir APIs.  
   - `pandas`: Para manipulação e organização de dados.  
   - `sqlite3`: Para armazenamento em banco de dados (opcional).  
   - `tinydb`: Para armazenamento em banco de dados NoSQL.
   - `sqlalchemy`: SQLAlchemy é uma biblioteca de mapeamento objeto-relacional para Python.
   - `psycopg2-binary`: Psycopg é uma biblioteca de acesso a dados PostgreSQL para Python.
   - `streamlit`: Para criar dashboards interativos.
   - `time`: Para medir o tempo de execução do programa.
   - `datetime`: Para manipulação de datas e horas.
- **Coinbase API**: Para obter o preço da Bitcoin em tempo real.  

---

## **Exemplo de Dados Coletados**  
| Data/Hora           | Preço (USD) | Moeda   |  
|----------------------|------------|---------|  
| 2024-01-01 12:00:00 | 42,000.50  | Bitcoin |  
| 2024-01-01 13:00:00 | 42,150.75  | Bitcoin |  

---

## **Resultados Esperados**  
Ao final deste projeto, você será capaz de:  
1. Extrair dados em tempo real de APIs públicas.  
2. Transformar e organizar os dados em formato estruturado.  
3. Automatizar o pipeline ETL para coleta recorrente dos dados.  

**Exemplo de Análises Futuras**:  
- Monitorar o preço da Bitcoin ao longo do tempo.  
- Identificar padrões de variação diária, semanal ou mensal.  
- Criar alertas para valores mínimos/máximos.  

---

## **Como Executar o Projeto**  

1. **Clone o Repositório**:  
   ```bash
   git clone https://github.com/seu-usuario/data-pipeline-bitcoin.git
   cd data-pipeline-bitcoin
   ```

2. **Instale as Dependências**:  
   ```bash
   pip install requests pandas
   ```

3. **Execute o Script**:  
   ```bash
   python main.py
   ```

4. **Verifique os Dados**:  
   - O arquivo `bitcoin_prices.csv` será gerado com os preços coletados.  

## **Banco de dados**

Postgres, banco de dados open source.

