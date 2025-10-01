# ----------------------------
# Configuración de la base de datos
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # cámbialo si usas otro usuario (ej: fluskuser)
    "password": "NuevaClave",          # contraseña de MySQL (si definiste una)
    "database": "ave_joyas"  # nombre de la base de datos
}

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
