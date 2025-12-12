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
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch

    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading1Center', parent=styles['Heading1'], alignment=1))
    styles.add(ParagraphStyle(name='BoldLeft', parent=styles['Normal'], fontName='Helvetica-Bold'))

    story = []

    # ---------------------
    # LOGO
    # ---------------------
    logo_path = "static/img/logoave.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=140, height=60))
        story.append(Spacer(1, 12))

    # ---------------------
    # TÍTULO DE FACTURA
    # ---------------------
    story.append(Paragraph("<b>FACTURA DE COMPRA</b>", styles["Heading1Center"]))
    story.append(Spacer(1, 20))

    # ---------------------
    # DATOS GENERALES
    # ---------------------
    info_pedido = [
        ["Factura Nº:", str(pedido["id_pedido"])],
        ["Número de Pedido:", pedido.get("numero_pedido", "N/A")],
        ["Fecha de Compra:", str(pedido["fecha"])],
        ["Código de Seguimiento:", pedido.get("codigo_seguimiento", pedido.get("numero_pedido"))],
    ]

    table_info = Table(info_pedido, colWidths=[150, 350])
    table_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dcd6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    story.append(table_info)
    story.append(Spacer(1, 20))

    # ---------------------
    # DATOS DEL CLIENTE
    # ---------------------
    story.append(Paragraph("<b>Datos del Cliente:</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    datos_cliente = [
        ["Nombre:", pedido["nombre_cliente"]],
        ["Dirección:", pedido["direccion_entrega"]],
        ["Correo:", pedido["correo_cliente"]],
        ["Teléfono:", pedido["telefono_cliente"]],
    ]

    tabla_cliente = Table(datos_cliente, colWidths=[120, 380])
    tabla_cliente.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.gray),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f7f7f7")),
    ]))

    story.append(tabla_cliente)
    story.append(Spacer(1, 20))

    # ---------------------
    # DETALLE DE PRODUCTOS
    # ---------------------
    story.append(Paragraph("<b>Detalle de Productos:</b>", styles["Heading2"]))
    story.append(Spacer(1, 12))

    encabezado = ["Producto", "Cantidad", "Talla", "Precio Unit.", "Subtotal"]

    filas = [encabezado]
    for item in detalles:
        filas.append([
            item["nombre"],
            str(item["cantidad"]),
            item["talla"],
            f"${item['precio_unitario']}",
            f"${item['subtotal']}"
        ])

    tabla_productos = Table(filas, colWidths=[180, 70, 60, 100, 100])
    tabla_productos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dcd6ff")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    story.append(tabla_productos)
    story.append(Spacer(1, 20))

    # ---------------------
    # TOTAL A PAGAR
    # ---------------------
    totales = [
        ["Subtotal:", f"${pedido['subtotal']}"],
        ["Impuesto (19%):", f"${pedido['impuesto']}"],
        ["Total Pagado:", f"<b>${pedido['total']}</b>"],
    ]

    tabla_totales = Table(totales, colWidths=[200, 140])
    tabla_totales.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f9f9ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.gray),
    ]))

    story.append(tabla_totales)
    story.append(Spacer(1, 40))

    # ---------------------
    # NOTA LEGAL
    # ---------------------
    story.append(Paragraph(
        "Gracias por tu compra. Este documento es válido como comprobante fiscal.",
        styles["Italic"]
    ))

    doc.build(story)



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






# ----------------------------
# Generar número único de pedido
# ----------------------------
def generar_numero_pedido():
    from datetime import datetime
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fecha en formato AAAAMMDD
    fecha = datetime.now().strftime("%Y%m%d")

    # Contar pedidos creados hoy para generar correlativo
    cursor.execute("""
        SELECT COUNT(*) 
        FROM pedidos 
        WHERE numero_pedido LIKE %s
    """, (f"PED-{fecha}-%",))

    count = cursor.fetchone()[0] + 1  # correlativo incremental

    # Construcción del número de pedido
    numero_pedido = f"PED-{fecha}-{count:06d}"

    cursor.close()
    conn.close()
    
    return numero_pedido

import random
import string

def generar_codigo_unico():
    prefijo = "PRD"
    aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefijo}-{aleatorio}"