# Imagem base
FROM python:3.10-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para iniciar o bot
CMD ["python", "bot_twitter.py"]
