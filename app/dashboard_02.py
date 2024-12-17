import streamlit as st
import sqlite3
import pandas as pd
import time

# Função para ler os dados do SQLite
def ler_dados_sqlite(db_name="/app/db/bitcoin_dados.db"):
    """Lê os dados do banco SQLite e retorna como DataFrame."""
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM bitcoin_precos ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Configuração do Dashboard Streamlit
def main():
    st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")
    st.title("📊 Dashboard de Preços do Bitcoin")
    st.write("Este dashboard exibe os dados do preço do Bitcoin coletados periodicamente.")

    # Definir o tempo de atualização em segundos
    intervalo_atualizacao = 15  # Altere aqui para ajustar o intervalo de atualização

    # Criar um espaço para o contador regressivo
    placeholder_contador = st.empty()

    # Carregar os dados do SQLite
    df = ler_dados_sqlite()

    if not df.empty:
        # Exibir os dados como tabela
        st.subheader("📋 Dados Recentes")
        st.dataframe(df)

        # Gráfico de linha: evolução do preço ao longo do tempo
        st.subheader("📈 Evolução do Preço do Bitcoin")
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Converter para datetime
        df = df.sort_values(by='timestamp')  # Garantir a ordenação por tempo
        st.line_chart(data=df, x='timestamp', y='valor', use_container_width=True)

        # Mostrar estatísticas
        st.subheader("🔢 Estatísticas Gerais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"${df['valor'].iloc[-1]:,.2f}")
        col2.metric("Preço Máximo", f"${df['valor'].max():,.2f}")
        col3.metric("Preço Mínimo", f"${df['valor'].min():,.2f}")
    else:
        st.warning("Nenhum dado encontrado no banco de dados SQLite.")

    # Contador regressivo para auto-reload
    for i in range(intervalo_atualizacao, 0, -1):
        placeholder_contador.text(f"🔄 Atualizando em {i} segundos...")
        time.sleep(1)
    st.rerun()  # Força o recarregamento da página

if __name__ == "__main__":
    main()
