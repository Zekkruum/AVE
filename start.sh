#!/bin/bash
# Activar el entorno virtual
source venv/bin/activate
# Comando encargado de instalar dependecias y librerias
pip install -r requeriments.txt
# Iniciar la aplicación
python app.py
