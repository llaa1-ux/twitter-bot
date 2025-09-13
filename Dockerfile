# Usando Python 3.10 slim
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Atualiza repositórios e instala ffmpeg + dependências básicas
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos do projeto
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Define variável de ambiente para o token do Telegram
ENV TOKEN="SEU_TOKEN_DO_BOT"

# Comando para rodar o bot
CMD ["python", "bot_twitter.py"]
