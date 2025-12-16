#!/bin/bash

# Verifica si Python está instalado
echo "Verificando instalación de Python..."
python --version || { echo "Python no está instalado. Abortando."; exit 1; }

# Verifica si pip está instalado
echo "Verificando instalación de pip..."
pip --version || { echo "pip no está instalado. Abortando."; exit 1; }

# Instala dependencias
echo "Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# Ejecuta la aplicación
echo "Ejecutando la aplicación..."
python app.py
