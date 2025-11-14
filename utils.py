import mysql.connector
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
from datetime import datetime, timedelta
from config import DB_CONFIG, EMAIL_CONFIG
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# ==========================
# GENERAR FACTURA PDF
# ==========================


def generar_factura_pdf(pedido, detalles, ruta_salida):
    """Genera un PDF de factura basado en los datos del pedido y su detalle."""

    # Crear el lienzo
    c = canvas.Canvas(ruta_salida, pagesize=letter)
    width, height = letter

    y = height - 50

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AVE JOYAS - FACTURA DE COMPRA")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Factura Nº: {pedido['id_pedido']}")
    y -= 20
    c.drawString(50, y, f"Fecha de emisión: {str(pedido['fecha'])}")
    y -= 30

    # Datos del cliente
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Datos del Cliente:")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Nombre: {pedido['nombre_cliente']}")
    y -= 20
    c.drawString(50, y, f"Dirección: {pedido['direccion_entrega']}")
    y -= 20
    c.drawString(50, y, f"Correo: {pedido['correo_cliente']}")
    y -= 20
    c.drawString(50, y, f"Teléfono: {pedido['telefono_cliente']}")
    y -= 30

    # Encabezado tabla
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Detalle de Productos:")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Producto")
    c.drawString(250, y, "Cant.")
    c.drawString(300, y, "P.Unit")
    c.drawString(380, y, "Subtotal")
    y -= 15
    c.line(50, y, 500, y)
    y -= 25

    c.setFont("Helvetica", 12)

    # Productos
    for item in detalles:
        c.drawString(50, y, str(item['nombre']))
        c.drawString(260, y, str(item['cantidad']))
        c.drawString(300, y, f"${item['precio_unitario']}")
        c.drawString(380, y, f"${item['subtotal']}")
        y -= 20

    y -= 20
    c.line(50, y, 500, y)
    y -= 30

    # Totales
    c.setFont("Helvetica-Bold", 13)
    c.drawString(300, y, f"Subtotal: ${pedido['subtotal']}")
    y -= 20
    c.drawString(300, y, f"Impuesto (19%): ${pedido['impuesto']}")
    y -= 20
    c.drawString(300, y, f"Total pagado: ${pedido['total']}")
    y -= 40

    # Nota legal
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Este documento es válido como comprobante de pago conforme a la legislación vigente.")

    # Guardar PDF
    c.save()
    return ruta_salida


# ----------------------------
# Conexión con la base de datos
# ----------------------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ----------------------------
# Enviar correo Flexible (Token, pedido personalizado)
# ----------------------------
def enviar_correo(destinatario, asunto=None, mensaje=None, token=None, archivo_adjunto=None, imagen_inline=None):
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_CONFIG["address"]
    msg["To"] = destinatario

    if token:
        msg["Subject"] = "Recuperación de contraseña - AVE Joyas"
        cuerpo = MIMEText(f"Tu código de recuperación es: {token}", "plain")
        msg.attach(cuerpo)
    else:
        msg["Subject"] = asunto or "Notificación AVE Joyas"
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

    if archivo_adjunto and os.path.exists(archivo_adjunto):
        with open(archivo_adjunto, "rb") as f:
            mime = MIMEBase("application", "octet-stream")
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header("Content-Disposition", f"attachment; filename={os.path.basename(archivo_adjunto)}")
            msg.attach(mime)

    if imagen_inline and os.path.exists(imagen_inline):
        with open(imagen_inline, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<bocetoimg>")
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(imagen_inline))
            msg.attach(img)

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
    expira = datetime.now() + timedelta(minutes=10)

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
# Funciones auxiliares para el perfil del usuario
# ----------------------------
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_PROFILE_IMG_SIZE = 2 * 1024 * 1024  # 2 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_image(file_storage, upload_folder_relative='static/uploads/perfiles'):
    if file_storage and file_storage.filename and allowed_file(file_storage.filename):
        filename = secure_filename(file_storage.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        base_dir = current_app.root_path
        upload_folder = os.path.join(base_dir, upload_folder_relative)
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        file_storage.save(save_path)
        return filename
    return None

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hash_value, password):
    return check_password_hash(hash_value, password)
