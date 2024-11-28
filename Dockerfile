#Use a imagem base do Python 
FROM cardinal_wave-python-base-image

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Expor a porta 5000 para o Flask
EXPOSE 5055

# Comando para executar a aplicacao Flask
CMD ["python", "run.py"]