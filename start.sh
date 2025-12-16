#!/bin/bash

# Mostrar la ruta de python y pip para depurar
echo "Verificando ubicación de Python..."
which python || { echo "Python no está instalado o no está en el PATH. Abortando."; exit 1; }

echo "Verificando ubicación de pip..."
which pip || { echo "pip no está instalado o no está en el PATH. Abortando."; exit 1; }

# Verifica las versiones de Python y pip
echo "Versión de Python:"
python --version

echo "Versión de pip:"
pip --version

# Instala dependencias
echo "Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# Ejecuta la aplicación
echo "Ejecutando la aplicación..."
python app.py
