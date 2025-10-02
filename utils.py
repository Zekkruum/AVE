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
# Enviar correo Flexible (Token, pedido personalizado)
# ----------------------------
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
import smtplib
from config import EMAIL_CONFIG


def enviar_correo(destinatario, asunto=None, mensaje=None, token=None, archivo_adjunto=None, imagen_inline=None):
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_CONFIG["address"]
    msg["To"] = destinatario

    if token:
        # Caso recuperación de contraseña
        msg["Subject"] = "Recuperación de contraseña - AVE Joyas"
        cuerpo = MIMEText(f"Tu código de recuperación es: {token}", "plain")
        msg.attach(cuerpo)
    else:
        # Caso general (ej. pedidos personalizados)
        msg["Subject"] = asunto or "Notificación AVE Joyas"

        # HTML con placeholder para la imagen inline
        html = f"""
        <html>
          <body>
            <p>{mensaje}</p>
        """

        if imagen_inline:
            html += """
            <p><b>Boceto:</b></p>
            <img src="cid:bocetoimg" style="max-width:400px; border-radius:8px;">
            """

        html += "</body></html>"

        cuerpo = MIMEText(html, "html")
        msg.attach(cuerpo)

    # Adjuntar archivo si existe
    if archivo_adjunto and os.path.exists(archivo_adjunto):
        with open(archivo_adjunto, "rb") as f:
            mime = MIMEBase("application", "octet-stream")
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header("Content-Disposition", f"attachment; filename={os.path.basename(archivo_adjunto)}")
            msg.attach(mime)

    # Adjuntar imagen inline
    if imagen_inline and os.path.exists(imagen_inline):
        with open(imagen_inline, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<bocetoimg>")
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(imagen_inline))
            msg.attach(img)

    # Enviar correo
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
