import mysql.connector
import smtplib
from email.mime.text import MIMEText
import secrets
import datetime
from config import DB_CONFIG, EMAIL_CONFIG   # 👈 ahora importamos la config


# ----------------------------
# Conexión con la base de datos
# ----------------------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ----------------------------
# Enviar correo con token
# ----------------------------
def enviar_correo(destinatario, token):
    msg = MIMEText(f"Tu código de recuperación es: {token}")
    msg["Subject"] = "Recuperación de contraseña - AVE Joyas"
    msg["From"] = EMAIL_CONFIG["address"]
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["address"], EMAIL_CONFIG["password"])
            server.sendmail(EMAIL_CONFIG["address"], destinatario, msg.as_string())
        print(f"[INFO] Correo enviado a {destinatario}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar correo: {e}")


# ----------------------------
# Generar y guardar token
# ----------------------------
def generar_token(id_usuario):
    token = secrets.token_hex(4)  # 8 caracteres hexadecimales
    expira = datetime.datetime.now() + datetime.timedelta(minutes=10)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tokens_recuperacion (id_usuario, token, expira)
        VALUES (%s, %s, %s)
    """, (id_usuario, token, expira))
    conn.commit()
    cursor.close()
    conn.close()

    return token
