#!/bin/bash
# Activar el entorno virtual
source venv/bin/activate
# Comando encargado de instalar dependecias y librerias
pip3 install -r requeriments.txt
# Iniciar la aplicación
python3 app.py
