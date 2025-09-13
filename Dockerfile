# Usar imagem oficial Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Comando de inicialização
CMD ["python", "bot_twitter.py"]
