FROM python:3.11-slim

# Diretório da aplicação
WORKDIR /app

# Copia apenas requirements primeiro (melhor cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app

# Comando padrão ao iniciar o container
CMD ["python", "app/main.py"]
