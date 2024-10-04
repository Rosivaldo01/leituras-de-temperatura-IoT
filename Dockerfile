# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de requisitos para instalar as dependências
COPY requirements.txt .

RUN pip install --upgrade pip

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o contêiner
COPY . .

# Expor a porta 8501
EXPOSE 8501

# Comando para executar a aplicação
# CMD ["streamlit", "run", "dataview.py", "--server.port=8501", "--server.address=0.0.0.0"]