import mysql.connector
import smtplib
from email.mime.text import MIMEText
import secrets
import datetime

# ----------------------------
# Configuración SMTP (correo Gmail)
# ----------------------------
EMAIL_ADDRESS = "ave.joyas.juan@gmail.com"
EMAIL_PASSWORD = "rhof yngu bdza ogij"



# ----------------------------
# Conexión con la base de datos
# ----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="",         
        database="ave_joyas"
    )

# ----------------------------
# Enviar correo con token
# ----------------------------
def enviar_correo(destinatario, token):
    msg = MIMEText(f"Tu código de recuperación es: {token}")
    msg["Subject"] = "Recuperación de contraseña - AVE Joyas"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, destinatario, msg.as_string())
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
