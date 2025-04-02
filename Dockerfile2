# Usa una imagen base de Python 3.10
FROM python:3.10-slim

# Instala supervisord
RUN apt-get update && apt-get install -y build-essential libgmp-dev

# Copia los archivos del repositorio al contenedor
COPY . /botTelegram

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /botTelegram

# Instala las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo de configuración de supervisord
CMD ["python3.10", "botTelegram/subscriptions.py"]