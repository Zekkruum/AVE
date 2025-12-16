# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto (ajústalo a lo que use tu proyecto)
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
