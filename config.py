# ----------------------------
# Configuración de la base de datos
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          
    "password": "",        
    "database": "ave_joyas",
    "charset" :'utf8mb4',
    "use_unicode": True
}

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
