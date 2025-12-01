# Use imagem oficial do Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app/ ./app

# Variável de ambiente para não precisar passar FLASK_APP manualmente
ENV FLASK_APP=app/api.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "-u", "app/consumer.py"]
