# Use a imagem base do Python 3.12
FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos (se houver) e instale as dependências
COPY requirements.txt ./
RUN pip install requests tinydb

# Copie o script Python para o contêiner
COPY exemplo_04.py ./

# Comando para executar o script
CMD ["python", "exemplo_04.py"]