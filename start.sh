#!/bin/bash

# Activar el entorno virtual (si es necesario)
source venv/bin/activate

# Instalar las dependencias
pip install -r requeriments.txt

# Iniciar la aplicación
python app.py
