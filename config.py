# ----------------------------
# Configuración de la base de datos
# ----------------------------

import os
import mysql.connector

mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl_disabled=True
)


#-----------------------------
# Comando para iniciar MariaDB
#-----------------------------

# sudo service mariadb start

# ----------------------------
# Configuración de correo
# ----------------------------
EMAIL_CONFIG = {
    "address": "ave.joyas.juan@gmail.com",
    "password": "rhof yngu bdza ogij"  # app password de Gmail
}

# ----------------------------
# Configuración de Flask
# ----------------------------
SECRET_KEY = "clave_super_secreta"
