# Usa una imagen base de Python 3.13.9 desde DockerHub
FROM python:3.13.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de tu aplicación (si es necesario)
EXPOSE 5000

# Comando para ejecutar la aplicación (ajusta según tu archivo principal)
CMD ["python", "app.py"]
