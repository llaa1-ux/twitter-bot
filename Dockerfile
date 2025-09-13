# Usando Python 3.10
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o bot
CMD ["python", "bot_twitter.py"]
