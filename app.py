import csv
from flask import Response, send_from_directory
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from utils import generar_codigo_unico, get_db_connection, enviar_correo, generar_token, save_profile_image, hash_password, verify_password
from flask import request, jsonify , current_app
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from openpyxl import Workbook
import io 

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads_productos"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ----------------------------
# Página inicial
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')

# ----------------------------
# Login
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        # print("DEBUG USER:", user)  # 👈 para ver qué datos devuelve
        cursor.close()
        conn.close()

        if user and check_password_hash(user['contrasena'], password):
            session['usuario_id'] = user['id_usuario']   # 👈 este faltaba
            session['usuario'] = user['correo']
            session['rol'] = user['id_rol']

            # 👇 Aquí definimos dónde va cada rol
            if user['id_rol'] == 1:   # admin
                return redirect(url_for('catalogo')) 

            if user['id_rol'] == 2:   # vendedor
                return redirect(url_for('vendedor_panel'))
            elif user['id_rol'] == 3: # cliente
                return redirect(url_for('catalogo'))
            else:
                return redirect(url_for('login'))  # fallback

        return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')


#----------------------------------------------------------------------------------------
# Función auxiliar para obtener datos completos del usuario por correo guardado en sesión
#----------------------------------------------------------------------------------------

def obtener_usuario():
    app.logger.debug(f"Sesión actual: {session}")  # <-- log de sesión

    if 'usuario_id' not in session:
        app.logger.debug("No se encontró 'usuario_id' en la sesión.")
        return None
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (session['usuario_id'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    app.logger.debug(f"Usuario obtenido de BD: {usuario}")  # <-- log del usuario
    return usuario


# ----------------------------
# Perfil de usuario
# ----------------------------
@app.route('/perfil')
def perfil():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    return render_template('perfil.html', usuario=usuario)

# ----------------------------
# Vendedor Panel
# ----------------------------
@app.route('/vendedor')
def vendedor_panel():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    return render_template('vendedor_panel.html', usuario=usuario)


# ----------------------------
# Logout
# ----------------------------
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario', None)
    session.pop('rol', None)
    return redirect(url_for('login'))

# ----------------------------
# Registro
# ----------------------------
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        correo = request.form['correo']

        prefijo = str(request.form['prefijo'])
        telefono_contacto = str(request.form['telefono_contacto'])
        telefono_final = prefijo + telefono_contacto

        contrasena = generate_password_hash(request.form['contrasena'])
        direccion = request.form['direccion']
        estado = 1 # "activo"
        id_rol = None  # aún no tiene rol

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre_completo, correo, telefono_contacto, contrasena, direccion, estado, id_rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre_completo, correo, telefono_final, contrasena, direccion, estado, id_rol))
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        db.close()

        session['pending_user'] = user_id
        return redirect(url_for('elegir_rol'))

    return render_template('signin.html')

# ----------------------------
# Elegir rol
# ----------------------------
@app.route('/elegir_rol', methods=['GET', 'POST'])
def elegir_rol():
    if 'pending_user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        rol = request.form.get('rol')  # 1 = vendedor, 3 = comprador
        user_id = session['pending_user']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE usuarios SET id_rol = %s WHERE id_usuario = %s", (rol, user_id))
        db.commit()
        cursor.close()
        db.close()

        session.pop('pending_user', None)
        return redirect(url_for('login'))

    return render_template('elegir_rol.html')


@app.route('/catalogo')
def catalogo():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    # -----------------------------
    # Obtener filtros
    # -----------------------------
    tipo_selected = request.args.get('tipo', type=int)
    material_selected = request.args.get('material', type=int)
    precio_min_selected = request.args.get('precio_min', type=float)
    precio_max_selected = request.args.get('precio_max', type=float)
    busqueda = request.args.get('busqueda', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ======================================================
    # 🔥 1. PRODUCTOS DESTACADOS (SIN FILTROS)
    # ======================================================
    sql_destacados = """
        SELECT 
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.imagen AS imagen_local,
            GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat,

            pr.descuento AS descuento_promocion,
            pr.titulo AS nombre_promocion,

            CASE 
                WHEN pr.descuento IS NOT NULL AND pr.descuento > 0
                THEN ROUND(p.precio - (p.precio * pr.descuento), 2)
                ELSE p.precio
            END AS precio_final

        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        LEFT JOIN producto_promocion pp ON p.id_producto = pp.id_producto
        LEFT JOIN promociones pr 
            ON pp.id_promocion = pr.id_promocion
            AND pr.estado = 1
            AND pr.activa = 1
            AND pr.fecha_inicio <= NOW()
            AND pr.fecha_fin >= NOW()

        WHERE p.destacado = 1 AND p.activo = 1
        GROUP BY p.id_producto
        ORDER BY p.nombre ASC
    """

    cursor.execute(sql_destacados)
    productos_destacados = cursor.fetchall()

    # ======================================================
    # 🛒 2. PRODUCTOS NORMALES (CON FILTROS)
    # ======================================================
    sql = """
        SELECT 
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.imagen AS imagen_local,
            GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat,

            pr.descuento AS descuento_promocion,
            pr.titulo AS nombre_promocion,

            CASE 
                WHEN pr.descuento IS NOT NULL AND pr.descuento > 0
                THEN ROUND(p.precio - (p.precio * pr.descuento), 2)
                ELSE p.precio
            END AS precio_final

        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        LEFT JOIN producto_promocion pp ON p.id_producto = pp.id_producto
        LEFT JOIN promociones pr 
            ON pp.id_promocion = pr.id_promocion
            AND pr.estado = 1
            AND pr.activa = 1
            AND pr.fecha_inicio <= NOW()
            AND pr.fecha_fin >= NOW()

        WHERE p.activo = 1 AND p.destacado = 0
    """

    params = []

    if tipo_selected:
        sql += " AND p.id_tipo = %s"
        params.append(tipo_selected)

    if material_selected:
        sql += " AND p.id_material = %s"
        params.append(material_selected)

    if precio_min_selected is not None:
        sql += " AND p.precio >= %s"
        params.append(precio_min_selected)

    if precio_max_selected is not None:
        sql += " AND p.precio <= %s"
        params.append(precio_max_selected)

    if busqueda:
        sql += " AND (p.nombre LIKE %s OR p.referencia LIKE %s)"
        like = f"%{busqueda}%"
        params.extend([like, like])

    sql += " GROUP BY p.id_producto ORDER BY p.nombre ASC"

    cursor.execute(sql, params)
    productos = cursor.fetchall()

    # ======================================================
    # 📦 Stock por tallas (AMBOS)
    # ======================================================
    def ajustar_stock(lista):
        for p in lista:
            cursor.execute("""
                SELECT COALESCE(SUM(stock), 0) AS total_stock
                FROM stock_tallas
                WHERE id_producto = %s
            """, (p['id_producto'],))
            p['stock'] = cursor.fetchone()['total_stock']

    ajustar_stock(productos_destacados)
    ajustar_stock(productos)

    # ======================================================
    # 🖼 Normalizar imágenes (AMBOS)
    # ======================================================
    def normalizar_imagenes(lista):
        for p in lista:
            imgs = [s for s in (p.get('imagenes_concat') or '').split('||') if s]
            imagen_src = p['imagen_local'] or (imgs[0] if imgs else None)

            if imagen_src:
                if imagen_src.startswith('static/'):
                    imagen_src = url_for('static', filename=imagen_src.replace('static/', '', 1))
                elif imagen_src.startswith('uploads/'):
                    imagen_src = url_for('static', filename=imagen_src)
            else:
                imagen_src = url_for('static', filename='img/no-image.png')

            p['imagen_src'] = imagen_src

    normalizar_imagenes(productos_destacados)
    normalizar_imagenes(productos)

    # ======================================================
    # 🔍 Filtros
    # ======================================================
    cursor.execute("SELECT * FROM tipos_joya ORDER BY nombre_tipo ASC")
    tipos = cursor.fetchall()

    cursor.execute("SELECT * FROM materiales ORDER BY nombre_material ASC")
    materiales = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'catalogo.html',
        productos_destacados=productos_destacados,
        productos=productos,
        usuario=usuario,
        tipos=tipos,
        materiales=materiales,
        tipo_selected=tipo_selected,
        material_selected=material_selected,
        precio_min_selected=precio_min_selected or '',
        precio_max_selected=precio_max_selected or '',
        busqueda=busqueda
    )

@app.route('/catalogo/filtrar')
def catalogo_filtrar():
    tipo_selected = request.args.get('tipo', type=int)
    material_selected = request.args.get('material', type=int)
    precio_min_selected = request.args.get('precio_min', type=float)
    precio_max_selected = request.args.get('precio_max', type=float)
    busqueda = request.args.get('busqueda', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
SELECT 
    p.id_producto,
    p.nombre,
    p.descripcion,
    p.precio,
    p.stock,
    p.imagen AS imagen_local,
    GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat,

    -- CORRECCIÓN
    pr.descuento AS descuento_promocion,
    pr.nombre AS nombre_promocion,

    CASE 
        WHEN pr.descuento IS NOT NULL AND pr.descuento > 0
        THEN ROUND(p.precio - (p.precio * pr.descuento), 2)
        ELSE p.precio
    END AS precio_final

FROM productos p
LEFT JOIN imagenes i 
    ON p.id_producto = i.id_producto
LEFT JOIN producto_promocion pp 
    ON p.id_producto = pp.id_producto
LEFT JOIN promociones pr 
    ON pp.id_promocion = pr.id_promocion 
    AND pr.estado = 1 
    AND pr.activa = 1
    AND pr.fecha_inicio <= NOW()
    AND pr.fecha_fin >= NOW()

WHERE 1=1
"""



    params = []

    if tipo_selected:
        sql += " AND p.id_tipo = %s"
        params.append(tipo_selected)

    if material_selected:
        sql += " AND p.id_material = %s"
        params.append(material_selected)

    if precio_min_selected is not None:
        sql += " AND p.precio >= %s"
        params.append(precio_min_selected)

    if precio_max_selected is not None:
        sql += " AND p.precio <= %s"
        params.append(precio_max_selected)

    if busqueda:
        sql += " AND (p.nombre LIKE %s OR p.referencia LIKE %s)"
        like_query = f"%{busqueda}%"
        params.extend([like_query, like_query])

    sql += " GROUP BY p.id_producto ORDER BY p.nombre ASC"

    cursor.execute(sql, params)
    productos = cursor.fetchall()

    # NORMALIZAR IMAGENES
    for p in productos:
        imgs = [s for s in (p.get('imagenes_concat') or '').split('||') if s]
        imagen_src = p['imagen_local'] or (imgs[0] if imgs else None)

        if imagen_src:
            if imagen_src.startswith('static/'):
                imagen_src = url_for('static', filename=imagen_src.replace('static/', '', 1))
            elif imagen_src.startswith('uploads/'):
                imagen_src = url_for('static', filename=imagen_src)
        else:
            imagen_src = url_for('static', filename='img/no-image.png')
        p['imagen_src'] = imagen_src

    cursor.close()
    conn.close()

    return render_template('_productos_grid.html', productos=productos)


    
@app.route('/promociones')
def promociones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT nombre, descripcion, descuento AS porcentaje_descuento, fecha_inicio, fecha_fin
        FROM promociones
        WHERE estado = 1
          AND fecha_inicio <= NOW()
          AND fecha_fin >= NOW()
        ORDER BY fecha_fin ASC
    """)
    promos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('promociones.html', promos=promos)


@app.route('/catalogo/buscar')
def buscar_rapido():
    query = request.args.get('query', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
               p.imagen AS imagen_local,
               GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat
        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        WHERE p.nombre LIKE %s OR p.referencia LIKE %s
        GROUP BY p.id_producto
        ORDER BY p.nombre ASC
        LIMIT 50
    """
    like_query = f"%{query}%"
    cursor.execute(sql, (like_query, like_query))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    for p in productos:
        imgs = [s for s in (p.get('imagenes_concat') or '').split('||') if s]
        imagen_src = p['imagen_local'] or (imgs[0] if imgs else None)
        if imagen_src:
            if imagen_src.startswith('static/'):
                imagen_src = url_for('static', filename=imagen_src.replace('static/', '', 1))
            elif imagen_src.startswith('uploads/'):
                imagen_src = url_for('static', filename=imagen_src)
        else:
            imagen_src = url_for('static', filename='img/no-image.png')
        p['imagen_src'] = imagen_src

    return render_template('_productos_grid.html', productos=productos)






@app.route('/producto/<int:id_producto>')
def producto_detalle(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---- Traer datos del producto + relaciones ----
    cursor.execute("""
        SELECT 
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.referencia,
            p.peso,
            p.largo,
            p.ancho,
            p.alto,
            t.nombre_tipo AS tipo_joya,
            m.nombre_material AS material,
            c.nombre AS color,
            pi.nombre AS piedra,
            p.imagen AS imagen_local,
            GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat
        FROM productos p
        LEFT JOIN tipos_joya t ON p.id_tipo = t.id_tipo
        LEFT JOIN materiales m ON p.id_material = m.id_material
        LEFT JOIN colores c ON p.id_color = c.id_color
        LEFT JOIN piedras pi ON p.id_piedra = pi.id_piedra
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        WHERE p.id_producto = %s
        GROUP BY p.id_producto
    """, (id_producto,))

    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        return redirect(url_for('catalogo'))

    # ---- Normalizar imágenes ----
    def normalize(src):
        if not src:
            return None
        if src.startswith('http://') or src.startswith('https://'):
            return src
        if src.startswith('static/'):
            return url_for('static', filename=src.replace('static/', '', 1))
        if src.startswith('uploads/'):
            return url_for('static', filename=src)
        return url_for('static', filename='uploads/' + src)

    imagenes = []
    if producto.get("imagenes_concat"):
        imagenes = [
            normalize(s) for s in producto["imagenes_concat"].split("||") if s
        ]

    if producto.get("imagen_local"):
        imagenes.insert(0, normalize(producto["imagen_local"]))

    if not imagenes:
        imagenes = [url_for('static', filename='img/no-image.png')]

    producto["imagenes"] = imagenes

    # ---- Dimensiones ----
    if producto.get("largo") and producto.get("ancho") and producto.get("alto"):
        producto["dimensiones"] = (
            f"{producto['largo']} x {producto['ancho']} x {producto['alto']} mm"
        )
    else:
        producto["dimensiones"] = "No especificado"

    # ---- STOCK POR TALLA ----
    cursor.execute("""
        SELECT talla, stock
        FROM stock_tallas
        WHERE id_producto = %s
        ORDER BY talla ASC
    """, (id_producto,))
    producto["tallas"] = cursor.fetchall()

    # ---- STOCK TOTAL ----
    cursor.execute("""
        SELECT COALESCE(SUM(stock), 0) AS total_stock
        FROM stock_tallas
        WHERE id_producto = %s
    """, (id_producto,))
    result = cursor.fetchone()
    producto['stock'] = result['total_stock']

    # ---- VALORACIONES ----
    cursor.execute("""
    SELECT 
        v.estrellas,
        v.comentario,
        v.fecha,
        u.nombre_completo AS usuario,
        u.foto_perfil
    FROM valoraciones v
    JOIN usuarios u ON v.id_usuario = u.id_usuario
    WHERE v.id_producto = %s
    ORDER BY v.fecha DESC
""", (id_producto,))
    valoraciones = cursor.fetchall()

    # ---- PROMEDIO ----
    cursor.execute("""
        SELECT 
            COALESCE(AVG(estrellas), 0) AS promedio,
            COUNT(*) AS total
        FROM valoraciones
        WHERE id_producto = %s
    """, (id_producto,))
    stats = cursor.fetchone()
    
    # ---- PRODUCTOS SIMILARES ----
    # ---- PRODUCTOS SIMILARES ----
    cursor.execute("""
        SELECT 
            p.id_producto,
            p.nombre,
            p.precio,
            p.imagen
        FROM productos p
        WHERE p.id_producto != %s
        AND (
            p.id_tipo = (
                SELECT id_tipo FROM productos WHERE id_producto = %s
            )
            OR p.id_material = (
                SELECT id_material FROM productos WHERE id_producto = %s
            )
        )
        LIMIT 6
    """, (id_producto, id_producto, id_producto))

    productos_similares = cursor.fetchall()

    # ---- NORMALIZAR IMÁGENES DE PRODUCTOS SIMILARES ----
    def normalize_producto_image(src):
        if not src:
            return url_for('static', filename='img/no-image.png')

        if src.startswith('http'):
            return src

        if src.startswith('static/'):
            return url_for('static', filename=src.replace('static/', '', 1))

        if src.startswith('uploads/'):
            return url_for('static', filename=src)

        return url_for('static', filename='uploads/' + src)


    for p in productos_similares:
        p["imagen"] = normalize_producto_image(p.get("imagen"))

    cursor.close()
    conn.close()
    
    
    
    def normalize_user_image(src):
        if not src:
            return url_for('static', filename='img/user.png')  # avatar por defecto

    # Si ya viene en una ruta absoluta HTTP
        if src.startswith("http://") or src.startswith("https://"):
            return src

    # Si ya viene con 'uploads/perfiles/...'
        if src.startswith("uploads/perfiles/"):
            return url_for('static', filename=src)

    # Si viene como 'uploads/nombre.jpg' => agregar carpeta perfiles
        if src.startswith("uploads/"):
            return url_for('static', filename='uploads/perfiles/' + src.replace("uploads/", "", 1))

    # Si viene como 'foto.jpg' => asumir perfiles
        return url_for('static', filename='uploads/perfiles/' + src)

    for v in valoraciones:
        v["foto_perfil"] = normalize_user_image(v.get("foto_perfil"))

    return render_template(
        "producto_detalle.html",
        productos_similares=productos_similares,
        usuario=usuario,
        producto=producto,
        valoraciones=valoraciones,
        stats=stats
    )




# ----------------------------
# Carrito de compras
# ----------------------------
@app.route('/carrito')
def carrito():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
        c.id_producto, 
        c.cantidad, 
        c.talla, 
        p.nombre, 
        p.precio,
        p.imagen AS imagen_local,
        (SELECT url FROM imagenes WHERE id_producto = p.id_producto LIMIT 1) AS imagen_extra
    FROM carrito_usuario c
    JOIN productos p ON c.id_producto = p.id_producto
    WHERE c.id_usuario = %s
""", (usuario['id_usuario'],))
    carrito = cursor.fetchall()
    cursor.close() 
    conn.close()

    # 🔥 Normalizar imagen igual que catálogo
    for item in carrito:
        imagen_src = item['imagen_local'] or item['imagen_extra'] 

        if imagen_src:
            if imagen_src.startswith('static/'):
                imagen_src = url_for('static', filename=imagen_src.replace('static/', '', 1))
            elif imagen_src.startswith('uploads/'):
                imagen_src = url_for('static', filename=imagen_src)
        else:
            imagen_src = url_for('static', filename='img/no-image.png')

        item['imagen_src'] = imagen_src

    total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)

    return render_template('carrito.html',
                           carrito=carrito,
                           total=total,
                           usuario=usuario)


@app.route('/carrito/agregar/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer stock actual por talla
    cursor.execute("SELECT talla, stock FROM stock_tallas WHERE id_producto = %s", (id_producto,))
    stock_tallas = {row['talla']: row['stock'] for row in cursor.fetchall()}

    for talla, stock_disponible in stock_tallas.items():
        key = f"cantidad_talla_{talla}"
        cantidad = int(request.form.get(key, 0))
        if cantidad <= 0:
            continue
        if cantidad > stock_disponible:
            flash(f"No hay suficiente stock de la talla {talla}", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('producto_detalle', id_producto=id_producto))

        # Ver si ya está en el carrito
        cursor.execute("""
            SELECT cantidad FROM carrito_usuario
            WHERE id_usuario=%s AND id_producto=%s AND talla=%s
        """, (usuario['id_usuario'], id_producto, talla))
        fila = cursor.fetchone()

        if fila:
            cursor.execute("""
                UPDATE carrito_usuario
                SET cantidad = cantidad + %s
                WHERE id_usuario=%s AND id_producto=%s AND talla=%s
            """, (cantidad, usuario['id_usuario'], id_producto, talla))
        else:
            cursor.execute("""
                INSERT INTO carrito_usuario (id_usuario, id_producto, cantidad, talla)
                VALUES (%s, %s, %s, %s)
            """, (usuario['id_usuario'], id_producto, cantidad, talla))

        # Descontar stock en stock_tallas
        cursor.execute("""
            UPDATE stock_tallas
            SET stock = stock - %s
            WHERE id_producto = %s AND talla = %s
        """, (cantidad, id_producto, talla))

    # Actualizar stock total en productos
    cursor.execute("""
        UPDATE productos
        SET stock = (SELECT COALESCE(SUM(stock),0) FROM stock_tallas WHERE id_producto = %s)
        WHERE id_producto = %s
    """, (id_producto, id_producto))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Producto agregado al carrito correctamente.", "success")
    return redirect(url_for('producto_detalle', id_producto=id_producto))


@app.route('/carrito/eliminar_talla/<int:id_producto>/<talla>', methods=['GET', 'POST'])
def eliminar_talla(id_producto, talla):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Regresar stock
    cursor.execute("""
        SELECT cantidad FROM carrito_usuario
        WHERE id_usuario=%s AND id_producto=%s AND talla=%s
    """, (usuario['id_usuario'], id_producto, talla))
    fila = cursor.fetchone()
    cantidad = fila['cantidad'] if fila else 0

    if cantidad > 0:
        cursor.execute("""
            UPDATE stock_tallas
            SET stock = stock + %s
            WHERE id_producto=%s AND talla=%s
        """, (cantidad, id_producto, talla))

    # Eliminar del carrito
    cursor.execute("""
        DELETE FROM carrito_usuario
        WHERE id_usuario=%s AND id_producto=%s AND talla=%s
    """, (usuario['id_usuario'], id_producto, talla))

    # Actualizar stock total
    cursor.execute("""
        UPDATE productos
        SET stock = (SELECT COALESCE(SUM(stock),0) FROM stock_tallas WHERE id_producto=%s)
        WHERE id_producto = %s
    """, (id_producto, id_producto))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('carrito'))





# ----------------------------
# Recuperar contraseña
# ----------------------------
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form.get('correo')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, correo FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return render_template('recuperar.html', error="Correo no registrado")

        token = generar_token(user['id_usuario'])
        cursor.close()
        conn.close()

        # ✅ Armar asunto y mensaje con HTML
        asunto = "Recuperación de contraseña - AVE Joyas"
        mensaje = f"""
            <p>Hola,</p>
            <p>Tu código de recuperación es:</p>
            <h2>{token}</h2>
            <p>Este código expira en 10 minutos.</p>
        """

        # ✅ Llamada con los parámetros correctos
        enviar_correo(destinatario=correo, asunto=asunto, mensaje=mensaje)

        return redirect(url_for('verificar_token'))

    return render_template('recuperar.html')
# ----------------------------
# Verificar token
# ----------------------------
@app.route('/verificar_token', methods=['GET', 'POST'])
def verificar_token():
    if request.method == 'POST':
        correo = request.form.get('dato')
        token = request.form.get('token')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return render_template('verificar_token.html', error="El correo no está asociado a ninguna cuenta.")

        cursor.execute("""
            SELECT * FROM tokens_recuperacion
            WHERE id_usuario = %s AND token = %s AND expira > NOW()
        """, (user['id_usuario'], token))
        token_row = cursor.fetchone()

        if token_row:
            session['reset_user'] = user['id_usuario']
            cursor.close()
            conn.close()
            return redirect(url_for('reset_password'))
        else:
            cursor.close()
            conn.close()
            return render_template('verificar_token.html', error="Token inválido o expirado.")

    return render_template('verificar_token.html')

# ----------------------------
# Reset password
# ----------------------------
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_user' not in session:
        return redirect(url_for('recuperar'))

    if request.method == 'POST':
        nueva_pass = request.form.get('nueva_pass')
        confirmar_pass = request.form.get('confirmar_pass')

        if nueva_pass != confirmar_pass:
            return render_template('reset_password.html', error="Las contraseñas no coinciden.")

        hashed_pass = generate_password_hash(nueva_pass)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s",
                       (hashed_pass, session['reset_user']))
        conn.commit()
        cursor.close()
        conn.close()

        session.pop('reset_user', None)

        return redirect(url_for('login'))

    return render_template('reset_password.html')

# --------------------------------------
# 📌 Registrar Producto (con validaciones y atributos extra)
# --------------------------------------
from PIL import Image
import os
from werkzeug.utils import secure_filename
import uuid  # para generar nombres de archivo únicos


# Configuración
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE_MB = 2
MIN_WIDTH, MIN_HEIGHT = 600, 600

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/registrar_producto', methods=['GET', 'POST'])
def registrar_producto():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores
        return redirect(url_for('login'))

    # Generar código único cada vez que se abre el formulario
    codigo_generado = generar_codigo_unico()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Listas para selects
    cursor.execute("SELECT * FROM colores")
    lista_colores = cursor.fetchall()
    cursor.execute("SELECT * FROM piedras")
    lista_piedras = cursor.fetchall()
    cursor.execute("SELECT * FROM tipos_joya")
    lista_tipos = cursor.fetchall()
    cursor.execute("SELECT * FROM materiales")
    lista_materiales = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        peso = float(request.form.get('peso', 0))
        alto = float(request.form.get('alto', 0))
        ancho = float(request.form.get('ancho', 0))
        largo = float(request.form.get('largo', 0))
        id_tipo = request.form.get('id_tipo')
        id_material = request.form.get('id_material')
        id_color = request.form.get('id_color')
        id_piedra = request.form.get('id_piedra')
        codigo_producto = request.form['codigo_producto']  # 🔥 Ya viene del formulario

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validar unicidad por seguridad
        cursor.execute("SELECT id_producto FROM productos WHERE codigo_producto = %s", (codigo_producto,))
        if cursor.fetchone():
            flash("❌ Error: El código del producto ya existe. Intente de nuevo.", "danger")
            return redirect(url_for('registrar_producto'))

        # Insertar producto con código único
        cursor.execute("""
            INSERT INTO productos
                (nombre, descripcion, precio, peso, alto, ancho, largo,
                 id_tipo, id_material, id_color, id_piedra, id_usuario, codigo_producto)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nombre, descripcion, precio, peso, alto, ancho, largo,
              id_tipo, id_material, id_color, id_piedra, usuario['id_usuario'], codigo_producto))

        id_producto = cursor.lastrowid

        # Stock por talla
        tallas = request.form.getlist('talla[]')
        stocks = request.form.getlist('stock[]')

        total_stock = 0
        for t, s in zip(tallas, stocks):
            cantidad = int(s)
            total_stock += cantidad
            cursor.execute("""
                INSERT INTO stock_tallas (id_producto, talla, stock)
                VALUES (%s, %s, %s)
            """, (id_producto, t, cantidad))

        # Actualizar stock total en productos
        cursor.execute("""
            UPDATE productos SET stock = %s WHERE id_producto = %s
        """, (total_stock, id_producto))

        # Imágenes
        if 'imagenes' in request.files:
            files = request.files.getlist('imagenes')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    imagen_src = f"uploads/{filename}"
                    cursor.execute("INSERT INTO imagenes (id_producto, url) VALUES (%s, %s)",
                                   (id_producto, imagen_src))

        conn.commit()
        cursor.close()
        conn.close()
        flash("✅ Producto registrado con éxito", "success")
        return redirect(url_for('mis_productos'))

    return render_template(
        "registrar_producto.html",
        usuario=usuario,
        colores=lista_colores,
        piedras=lista_piedras,
        tipos=lista_tipos,
        materiales=lista_materiales,
        codigo_producto=codigo_generado  # 🔥 Se envía al template
    )




 


# ----------------------------
# Ver mis productos
# ----------------------------
# --------------------------------------
# 📌 Mis Productos (alerta stock bajo)
# --------------------------------------
@app.route('/vendedor/productos')
def mis_productos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *, CASE WHEN stock <= umbral_alerta THEN 1 ELSE 0 END AS alerta
        FROM productos WHERE id_usuario=%s
    """, (usuario['id_usuario'],))
    productos = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template('mis_productos.html', usuario=usuario, productos=productos)


# --------------------------------------
# 📌 Exportar Inventario a Excel
# --------------------------------------



@app.route('/vendedor/reporte_inventario')
def reporte_inventario():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer stock por talla
    cursor.execute("""
        SELECT 
            p.nombre,
            p.descripcion,
            p.precio,
            s.talla,
            s.stock AS stock_talla,
            p.umbral_alerta,
            p.peso,
            p.alto,
            p.ancho,
            p.largo
        FROM productos p
        LEFT JOIN stock_tallas s ON p.id_producto = s.id_producto
        WHERE p.id_usuario = %s
        ORDER BY p.nombre, s.talla
    """, (usuario['id_usuario'],))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    # Generar Excel
    wb = Workbook()  # type: ignore
    ws = wb.active
    ws.title = "Inventario"
    ws.append(["Nombre", "Descripción", "Precio", "Talla", "Stock", "Umbral", "Peso", "Alto", "Ancho", "Largo"])

    for p in productos:
        ws.append([
            p['nombre'],
            p['descripcion'],
            p['precio'],
            p['talla'] or "N/A",
            p['stock_talla'] or 0,
            p['umbral_alerta'],
            p['peso'],
            p['alto'],
            p['ancho'],
            p['largo']
        ])

    output = io.BytesIO()  # type: ignore
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="reporte_inventario.xlsx",  # type: ignore
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ---------------------------------------------------------
# Estadísticas reales del vendedor
# ---------------------------------------------------------
@app.route('/vendedor/estadisticas', methods=["GET"])
def estadisticas():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    id_vendedor = usuario['id_usuario']

    # Filtros GET
    fecha_inicio = request.args.get("inicio")
    fecha_fin = request.args.get("fin")
    modo = request.args.get("modo", "mes")  # por defecto mes

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ------------------------------------------
    # 1) AGRUPACIÓN (día, semana, mes)
    # ------------------------------------------
    if modo == "dia":
        agrupador = "DATE(p.fecha)"
        label = "DATE(p.fecha)"
    elif modo == "semana":
        agrupador = "YEARWEEK(p.fecha)"
        label = "YEARWEEK(p.fecha)"
    else:
        agrupador = "DATE_FORMAT(p.fecha, '%Y-%m')"
        label = "DATE_FORMAT(p.fecha, '%Y-%m')"

    # ------------------------------------------
    # INGRESOS AGRUPADOS
    # ------------------------------------------
    query_ingresos = f"""
        SELECT 
            {label} AS label,
            SUM(dp.cantidad * dp.precio_unitario) AS total
        FROM pedidos p
        JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
        JOIN productos prod ON dp.id_producto = prod.id_producto
        WHERE prod.id_usuario = %s
    """
    valores = [id_vendedor]

    if fecha_inicio and fecha_fin:
        query_ingresos += " AND p.fecha BETWEEN %s AND %s"
        valores.extend([fecha_inicio, fecha_fin])

    query_ingresos += f" GROUP BY {agrupador} ORDER BY {agrupador}"
    cursor.execute(query_ingresos, tuple(valores))
    ingresos_periodo = cursor.fetchall()

    # ------------------------------------------
    # TOP PRODUCTOS
    # ------------------------------------------
    query_top = """
        SELECT 
            prod.nombre,
            SUM(dp.cantidad) AS total_vendidos
        FROM detalle_pedido dp
        JOIN productos prod ON dp.id_producto = prod.id_producto
        WHERE prod.id_usuario = %s
    """
    valores_top = [id_vendedor]

    if fecha_inicio and fecha_fin:
        query_top += " AND dp.id_pedido IN (SELECT id_pedido FROM pedidos WHERE fecha BETWEEN %s AND %s)"
        valores_top.extend([fecha_inicio, fecha_fin])

    query_top += " GROUP BY prod.id_producto ORDER BY total_vendidos DESC LIMIT 5"
    cursor.execute(query_top, tuple(valores_top))
    top_productos = cursor.fetchall()

    # ------------------------------------------
    # RESUMEN GENERAL
    # ------------------------------------------
    query_resumen = """
        SELECT 
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            SUM(dp.cantidad) AS total_unidades,
            SUM(dp.cantidad * dp.precio_unitario) AS total_ingresos
        FROM pedidos p
        JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
        JOIN productos prod ON dp.id_producto = prod.id_producto
        WHERE prod.id_usuario = %s
    """
    valores_resumen = [id_vendedor]

    if fecha_inicio and fecha_fin:
        query_resumen += " AND p.fecha BETWEEN %s AND %s"
        valores_resumen.extend([fecha_inicio, fecha_fin])

    cursor.execute(query_resumen, tuple(valores_resumen))
    resumen = cursor.fetchone() or {}

    cursor.close()
    conn.close()

    return render_template(
        "estadisticas.html",
        usuario=usuario,
        ingresos_periodo=ingresos_periodo,
        top_productos=top_productos,
        total_vendido=resumen.get("total_ingresos", 0),
        total_pedidos=resumen.get("total_pedidos", 0),
        total_items_vendidos=resumen.get("total_unidades", 0),
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        modo=modo
    )



@app.route('/vendedor/pedidos')
def gestionar_pedidos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    id_vendedor = usuario['id_usuario']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer pedidos asociados a los productos del vendedor
    cursor.execute("""
        SELECT 
            p.id_pedido,
            p.fecha,
            p.numero_pedido,
            p.codigo_seguimiento,
            e.nombre_estado,
            u.nombre_completo AS cliente,
            GROUP_CONCAT(prod.nombre SEPARATOR ', ') AS productos
        FROM pedidos p
        LEFT JOIN estados_pedido e ON p.id_estado = e.id_estado
        JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
        JOIN productos prod ON dp.id_producto = prod.id_producto
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE prod.id_usuario = %s
        GROUP BY p.id_pedido, p.fecha, e.nombre_estado, cliente
        ORDER BY p.fecha DESC
    """, (id_vendedor,))

    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pedidos.html', usuario=usuario, pedidos=pedidos)


# ---------------------------------------------------------
# Cambiar estado a "Enviado"
# ---------------------------------------------------------
@app.route('/vendedor/pedido/<int:id_pedido>/enviar')
def marcar_enviado(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pedidos
        SET estado = 'Enviado'
        WHERE id_pedido = %s
    """, (id_pedido,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('gestionar_pedidos'))


# ---------------------------------------------------------
# Cambiar estado a "Entregado"
# ---------------------------------------------------------
@app.route('/vendedor/pedido/<int:id_pedido>/entregar')
def marcar_entregado(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pedidos
        SET estado = 'Entregado'
        WHERE id_pedido = %s
    """, (id_pedido,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('gestionar_pedidos'))


@app.route("/incidencia/<int:id_pedido>", methods=["GET"])
def registrar_incidencia_form(id_pedido):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Validar que el pedido exista y pertenezca al usuario
    cursor.execute("""
    SELECT 
        p.id_pedido,
        p.numero_pedido,
        p.fecha,
        pa.id_pago,
        pa.monto
    FROM pedidos p
    INNER JOIN pagos pa ON pa.id_pedido = p.id_pedido
    WHERE p.id_pedido = %s
""", (id_pedido,))

    pedido = cursor.fetchone()

    cursor.close()
    conn.close()

    if not pedido:
        return "Pedido no encontrado o no pertenece al usuario", 404

    return render_template(
        "registrar_incidencia.html",
        pedido=pedido,
        usuario=usuario
    )

@app.route("/mis-incidencias")
def incidencias_historial():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            i.*,
            pe.fecha AS fecha_pedido,
            pa.monto AS monto_pago
        FROM incidencias i
        JOIN pedidos pe ON i.id_pedido = pe.id_pedido
        LEFT JOIN pagos pa ON pa.id_pedido = pe.id_pedido
        WHERE i.id_usuario = %s
        ORDER BY i.fecha_registro DESC
    """, (usuario['id_usuario'],))

    incidencias = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "incidencias_historial.html",
        incidencias=incidencias,
        usuario=usuario
    )

@app.route("/incidencia/<int:id_pedido>/guardar", methods=["POST"])
def registrar_incidencia_guardar(id_pedido):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for("login"))

    # 🔹 Datos del formulario
    tipo = request.form["tipo"]
    comentario = request.form["comentario"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidencias (id_pedido, id_usuario, tipo, comentario, fecha_registro)
        VALUES (%s, %s, %s, %s, NOW())
    """, (
        id_pedido,
        usuario["id_usuario"],
        tipo,
        comentario
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("incidencias_historial"))


@app.route("/vendedor/incidencias")
def incidencias_vendedor():
    usuario = obtener_usuario()
    if not usuario or usuario["id_rol"] != 2:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT DISTINCT
        i.id_incidencia,
        i.tipo,
        i.comentario,
        i.estado,
        i.fecha_registro,
        p.id_pedido AS numero_pedido,
        u.nombre_completo AS cliente
    FROM incidencias i
    JOIN pedidos p ON i.id_pedido = p.id_pedido
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    JOIN usuarios u ON i.id_usuario = u.id_usuario
    WHERE pr.id_usuario = %s
    ORDER BY i.fecha_registro DESC
""", (usuario["id_usuario"],))


    incidencias = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "incidencias_vendedor.html",
        incidencias=incidencias,
        usuario=usuario
    )

@app.route("/vendedor/incidencias/<int:id>/estado", methods=["POST"])
def actualizar_estado_incidencia(id):
    usuario = obtener_usuario()
    if not usuario or usuario["id_rol"] != 2:
        return redirect(url_for("login"))

    estado = request.form["estado"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE incidencias
        SET estado = %s
        WHERE id_incidencia = %s
    """, (estado, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("incidencias_vendedor"))


# ----------------------------
# Producto - Detalle (VENDEDOR)
# ----------------------------
@app.route('/vendedor/producto/<int:id_producto>')
def producto_detalle_vendedor(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s AND id_usuario = %s",
                   (id_producto, usuario['id_usuario']))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if not producto:
        return "Producto no encontrado o no autorizado", 404

    return render_template('producto_detalle_vendedor.html', producto=producto, usuario=usuario)


# ----------------------------
# Producto - Editar
# ----------------------------
@app.route('/producto/<int:id_producto>/editar', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        cursor.execute("""
            UPDATE productos 
            SET nombre=%s, descripcion=%s, precio=%s, stock=%s
            WHERE id_producto=%s
        """, (nombre, descripcion, precio, stock, id_producto))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template('editar_producto.html', producto=producto)


# ----------------------------
# Producto - Eliminar
# ----------------------------
@app.route('/producto/<int:id_producto>/eliminar', methods=['POST'])
def eliminar_producto(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:  # Solo admin (1) o vendedor (2)
        flash("No tienes permisos para eliminar productos.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc('eliminar_producto', [id_producto])
        conn.commit()
        flash(" Producto eliminado correctamente.", "success")

    except Exception as e:
        conn.rollback()
        flash(f" Error al eliminar el producto: {e}", "error")

    finally:
        cursor.close()
        conn.close()

    # Redirige según el tipo de usuario
    if usuario['id_rol'] == 1:
        return redirect(url_for('admin_ver_productos'))
    else:
        return redirect(url_for('mis_productos'))


# ===========================================
# REGISTRAR PAGO + GENERAR FACTURA (RF060)
# ===========================================
@app.route('/pedido/<int:id_pedido>/pago', methods=['GET', 'POST'])
def registrar_pago(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2, 3]:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener el pedido
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id_pedido,))
    pedido = cursor.fetchone()

    if not pedido:
        cursor.close()
        conn.close()
        return "Pedido no encontrado", 404

    # ======================
    # MÉTODO POST (REGISTRAR PAGO)
    # ======================
    if request.method == 'POST':

        metodo = request.form['metodo']
        monto = float(request.form['monto'])
        estado = "pagado"  # tu columna estado_pago

        # -------------------------------
        # OBTENER DATOS DE TARJETA SI APLICA
        # -------------------------------
        if metodo == "tarjeta":
            numero_tarjeta = request.form.get("numero_tarjeta", "").replace(" ", "")
            vencimiento = request.form.get("vencimiento")
            cvc = request.form.get("cvc")
        else:
            numero_tarjeta = None
            vencimiento = None
            cvc = None

        # Registrar el pago en base de datos
        cursor.execute("""
            INSERT INTO pagos 
                (id_pedido, monto, metodo_pago, estado, fecha,
                 numero_tarjeta, vencimiento, cvc)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s)
        """, (id_pedido, monto, metodo, estado,
              numero_tarjeta, vencimiento, cvc))

        id_pago = cursor.lastrowid

        # ------------------------------------------
        # ACTUALIZAR ESTADO DEL PEDIDO (SISTEMA ANTIGUO)
        # ------------------------------------------
        cursor.execute("""
            UPDATE pedidos 
            SET estado_pago = 'pagado'
            WHERE id_pedido = %s
        """, (id_pedido,))

        # ------------------------------------------
        # NUEVO SISTEMA DE ESTADOS (id_estado)
        # ------------------------------------------
        # Buscar id del estado 'Pagado'
        cursor.execute("""
            SELECT id_estado 
            FROM estados_pedido 
            WHERE nombre_estado = 'Pagado'
            LIMIT 1
        """)
        estado_row = cursor.fetchone()

        if estado_row:
            id_estado = estado_row['id_estado']

            # Actualizar pedido
            cursor.execute("""
                UPDATE pedidos
                SET id_estado = %s
                WHERE id_pedido = %s
            """, (id_estado, id_pedido))

            # Registrar historial
            cursor.execute("""
                INSERT INTO historial_pedido (id_pedido, id_estado, id_usuario, comentario)
                VALUES (%s, %s, %s, %s)
            """, (id_pedido, id_estado, usuario['id_usuario'], "Pago registrado"))

        # -------------------------------
        # Información para generar factura
        # -------------------------------
        cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        pedido = cursor.fetchone()

        cursor.execute("""
            SELECT d.id_producto, d.cantidad, d.precio_unitario,
                   (d.cantidad * d.precio_unitario) AS subtotal,
                   p.nombre, d.talla
            FROM detalle_pedido d
            JOIN productos p ON p.id_producto = d.id_producto
            WHERE d.id_pedido = %s
        """, (id_pedido,))
        detalles = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        # ======================
        # GENERAR FACTURA PDF
        # ======================
        from utils import generar_factura_pdf
        import os

        carpeta = "static/facturas"
        os.makedirs(carpeta, exist_ok=True)

        ruta_pdf = f"{carpeta}/factura_{id_pedido}.pdf"

        generar_factura_pdf(pedido, detalles, ruta_pdf)

        flash("Pago registrado correctamente. Tu factura está disponible.", "success")
        return redirect(url_for('ver_factura', id_pedido=id_pedido))

    # ======================
    # MÉTODO GET (FORMULARIO)
    # ======================
    cursor.close()
    conn.close()
    return render_template('pago_form.html', usuario=usuario, pedido=pedido)


@app.route('/factura/<int:id_pedido>')
def ver_factura(id_pedido):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))
    
    ruta = f"static/facturas/factura_{id_pedido}.pdf"
    return render_template("factura_lista.html",
                           ruta=ruta,
                           id_pedido=id_pedido,
                           usuario=usuario)


# ----------------------------
# Historial de Pagos
# ----------------------------
@app.route('/mis_pagos')
def mis_pagos():
    usuario = obtener_usuario()
    # ✅ Ahora permitimos tanto clientes (3) como vendedores (2)
    if not usuario or usuario['id_rol'] not in [1, 2, 3]:
        return redirect(url_for('login'))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    # 🚨 asumo que pedidos.id_usuario guarda al dueño del pedido
    cursor.execute("""
        SELECT pa.*, pe.total, pe.numero_pedido
        FROM pagos pa
        INNER JOIN pedidos pe ON pa.id_pedido = pe.id_pedido
        WHERE pe.id_usuario = %s
        ORDER BY pa.fecha DESC
        """, (usuario['id_usuario'],))
    pagos = cursor.fetchall()




    cursor.close()
    conn.close()


    return render_template('mis_pagos.html', usuario=usuario, pagos=pagos)

# ----------------------------
# Crear pedido (desde el carrito)
# ----------------------------
@app.route('/crear_pedido', methods=['POST'])
def crear_pedido():
    from utils import generar_numero_pedido  # Tu función original
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    # Datos del formulario
    nombre_cliente = request.form.get('nombre_cliente')
    direccion_entrega = request.form.get('direccion_entrega')
    telefono_cliente = request.form.get('telefono_cliente')
    correo_cliente = request.form.get('correo_cliente')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener carrito
    cursor.execute("""
    SELECT c.id_producto, c.cantidad, c.talla, p.precio, p.stock
    FROM carrito_usuario c
    JOIN productos p ON c.id_producto = p.id_producto
    WHERE c.id_usuario = %s
    """, (usuario['id_usuario'],))
    carrito = cursor.fetchall()

    if not carrito:
        cursor.close()
        conn.close()
        return redirect(url_for('carrito'))

    # Validar stock
    for item in carrito:
        stock = item['stock']
        if stock is None:
            cursor.close()
            conn.close()
            return f"Producto {item['id_producto']} no tiene stock definido.", 400

        if item['cantidad'] > stock:
            cursor.close()
            conn.close()
            return f"Stock insuficiente para el producto {item['id_producto']}.", 400

    # Calcular totales
    subtotal = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
    impuesto = round(subtotal * 0.19, 2)
    total = subtotal + impuesto

    # ------------------------------------
    # GENERAR CÓDIGO ÚNICO DEL PEDIDO
    # ------------------------------------
    numero_pedido = generar_numero_pedido()  # 🔥 tu sistema actual
    codigo_seguimiento = numero_pedido       # 🔥 mismo valor (como me dijiste)

    # ------------------------------------
    # Insertar el pedido
    # ------------------------------------
    cursor.execute("""
    INSERT INTO pedidos (
        id_usuario, 
        nombre_cliente,
        direccion_entrega,
        telefono_cliente,
        correo_cliente,
        fecha,
        id_estado,
        subtotal,
        impuesto,
        total,
        numero_pedido,
        codigo_seguimiento
    )
    VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)
""", (
    usuario['id_usuario'],
    nombre_cliente,
    direccion_entrega,
    telefono_cliente,
    correo_cliente,
    1,  # Estado inicial
    subtotal,
    impuesto,
    total,
    numero_pedido,
    numero_pedido  # 🔥 Son iguales según tu sistema
))

    id_pedido = cursor.lastrowid

    # ------------------------------------
    # Estado inicial según la nueva tabla estados_pedido
    # ------------------------------------
    cursor.execute("SELECT id_estado FROM estados_pedido WHERE nombre_estado = 'Pendiente' LIMIT 1")
    estado_row = cursor.fetchone()

    if estado_row:
        id_estado = estado_row['id_estado']

        cursor.execute("""
            UPDATE pedidos
            SET id_estado = %s
            WHERE id_pedido = %s
        """, (id_estado, id_pedido))

        # Registrar en historial
        cursor.execute("""
            INSERT INTO historial_pedido (id_pedido, id_estado, id_usuario, comentario)
            VALUES (%s, %s, %s, %s)
        """, (id_pedido, id_estado, usuario['id_usuario'], "Pedido creado"))

    # ------------------------------------
    # Insertar detalles y descontar stock
    # ------------------------------------
    for item in carrito:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario, talla)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_pedido, item['id_producto'], item['cantidad'], item['precio'], item['talla']))

        cursor.execute("""
            UPDATE productos SET stock = stock - %s
            WHERE id_producto = %s
        """, (item['cantidad'], item['id_producto']))

    # Vaciar carrito
    cursor.execute("DELETE FROM carrito_usuario WHERE id_usuario = %s", (usuario['id_usuario'],))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('registrar_pago', id_pedido=id_pedido))






# ----------------------------
# Registrar entrada de stock
# ----------------------------
@app.route('/vendedor/stock/entrada/<int:id_producto>', methods=['GET', 'POST'])
def registrar_entrada_stock(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    # Traer tallas disponibles
    cursor.execute("SELECT talla, stock FROM stock_tallas WHERE id_producto = %s", (id_producto,))
    tallas = cursor.fetchall()

    if not producto:
        cursor.close()
        conn.close()
        return "Producto no encontrado", 404

    if request.method == 'POST':
        talla = request.form['talla']  # seleccionada por el vendedor
        cantidad = int(request.form['cantidad'])
        motivo = request.form.get('observacion', '')

        if cantidad <= 0:
            return render_template('registrar_entrada_stock.html', producto=producto, tallas=tallas, error="Cantidad debe ser mayor a 0.")

        # 1. Insertar en movimientos_inventario con talla
        cursor.execute("""
            INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, motivo, id_usuario, talla)
            VALUES (%s, 'entrada', %s, %s, %s, %s)
        """, (id_producto, cantidad, motivo, usuario['id_usuario'], talla))

        # 2. Actualizar stock de esa talla
        cursor.execute("""
            UPDATE stock_tallas
            SET stock = stock + %s
            WHERE id_producto = %s AND talla = %s
        """, (cantidad, id_producto, talla))

        # 3. Actualizar stock total en productos
        cursor.execute("""
            UPDATE productos
            SET stock = (SELECT COALESCE(SUM(stock),0) FROM stock_tallas WHERE id_producto = %s)
            WHERE id_producto = %s
        """, (id_producto, id_producto))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template('registrar_entrada_stock.html', producto=producto, tallas=tallas, usuario=usuario)



#-----------------------------
# Registrar salida stock
#-----------------------------
@app.route('/producto/<int:id_producto>/registrar_salida', methods=['GET', 'POST'])
def registrar_salida_stock(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    # Traer tallas disponibles
    cursor.execute("SELECT talla, stock FROM stock_tallas WHERE id_producto = %s", (id_producto,))
    tallas = cursor.fetchall()

    if request.method == 'POST':
        talla = request.form['talla']
        cantidad = int(request.form['cantidad'])
        motivo = request.form.get('motivo', '')

        # Validar stock
        cursor.execute("SELECT stock FROM stock_tallas WHERE id_producto = %s AND talla = %s", (id_producto, talla))
        fila = cursor.fetchone()
        stock_talla = fila['stock'] if fila else 0

        if cantidad <= 0:
            return render_template('registrar_salida_stock.html', producto=producto, tallas=tallas, error="Cantidad debe ser mayor a 0.")
        if cantidad > stock_talla:
            return render_template('registrar_salida_stock.html', producto=producto, tallas=tallas, error=f"No hay suficiente stock de la talla {talla}.")

        # Registrar movimiento
        cursor.execute("""
            INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, motivo, id_usuario, talla)
            VALUES (%s, 'salida', %s, %s, %s, %s)
        """, (id_producto, cantidad, motivo, usuario['id_usuario'], talla))

        # Actualizar stock de esa talla
        cursor.execute("""
            UPDATE stock_tallas
            SET stock = stock - %s
            WHERE id_producto = %s AND talla = %s
        """, (cantidad, id_producto, talla))

        # Actualizar stock total en productos
        cursor.execute("""
            UPDATE productos
            SET stock = (SELECT COALESCE(SUM(stock),0) FROM stock_tallas WHERE id_producto = %s)
            WHERE id_producto = %s
        """, (id_producto, id_producto))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template('registrar_salida_stock.html', producto=producto, tallas=tallas, usuario=usuario)


# ----------------------------
# generador de devoluciones 2.0
# ----------------------------

@app.route('/vendedor/devolucion/<int:id_producto>', methods=['GET', 'POST'])
def registrar_devolucion(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario.get('id_rol') != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener datos del producto
    cursor.execute("""
        SELECT id_producto, nombre, stock 
        FROM productos 
        WHERE id_producto = %s AND id_usuario = %s
    """, (id_producto, usuario['id_usuario']))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        flash("Producto no encontrado o no autorizado.", "error")
        return redirect(url_for('mis_productos'))

    # -----------------------------------
    #  generador de devoluciones, lectura del formulario
    # -----------------------------------
    if request.method == 'POST':

        # Cantidad devuelta
        try:
            cantidad = int(request.form['cantidad'])
        except:
            flash("Cantidad inválida.", "error")
            return redirect(url_for('registrar_devolucion', id_producto=id_producto))

        motivo = request.form.get('motivo', '').strip()
        estado_fisico = request.form.get('estado_fisico')   

        # Pedido opcional
        id_pedido_form = request.form.get('id_pedido')
        id_pedido = int(id_pedido_form) if id_pedido_form else None

        cursor_write = conn.cursor()

        # Guardamos la devolución
        cursor_write.execute("""
            INSERT INTO devoluciones (id_pedido, id_producto, cantidad, motivo, estado, estado_fisico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_pedido, id_producto, cantidad, motivo, 'Registrada', estado_fisico))

        # Si el producto está en buen estado → vuelve al inventario
        if estado_fisico == "bueno":
            cursor_write.execute("""
                UPDATE productos SET stock = stock + %s WHERE id_producto = %s
            """, (cantidad, id_producto))
            mensaje = "El producto fue devuelto al inventario."
        else:
            mensaje = "Producto defectuoso: no se añadió al inventario."

        conn.commit()
        cursor_write.close()
        cursor.close()
        conn.close()

        flash(mensaje, "success")
        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template('registrar_devolucion.html', usuario=usuario, producto=producto)


@app.route('/vendedor/reportes', methods=['GET', 'POST'])
def reportes_ventas():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores
        return redirect(url_for('login'))

    reportes = []
    fecha_inicio = fecha_fin = None

    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                p.id_pedido,
                p.fecha,
                p.nombre_cliente AS cliente,
                ep.nombre_estado AS estado,
                SUM(dp.cantidad * dp.precio_unitario) AS total,
                GROUP_CONCAT(CONCAT(pr.nombre, ' (x', dp.cantidad, ')') SEPARATOR ', ') AS productos
            FROM pedidos p
            INNER JOIN estados_pedido ep ON ep.id_estado = p.id_estado
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN productos pr ON dp.id_producto = pr.id_producto
            WHERE DATE(p.fecha) BETWEEN %s AND %s
              AND p.id_vendedor = %s  -- 🔥 Solo ventas de este vendedor
            GROUP BY p.id_pedido
            ORDER BY p.fecha ASC
        """, (fecha_inicio, fecha_fin, usuario['id_usuario']))

        reportes = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template("reportes_ventas.html",
                           usuario=usuario,
                           reportes=reportes,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)


# ----------------------------
# Estadísticas visuales (RF025)
# ----------------------------
@app.route('/vendedor/estadisticas_visual')
def estadisticas_visual():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Ventas agrupadas por mes
    cursor.execute("""
        SELECT DATE_FORMAT(p.fecha, '%Y-%m') AS mes,
               SUM(dp.cantidad * dp.precio_unitario) AS total
        FROM pedidos p
        INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
        INNER JOIN productos pr ON dp.id_producto = pr.id_producto
        WHERE pr.id_usuario = %s
        GROUP BY mes
        ORDER BY mes ASC
    """, (usuario['id_usuario'],))
    ventas_mensuales = cursor.fetchall()

    # 2. Productos más vendidos
    cursor.execute("""
        SELECT pr.nombre, SUM(dp.cantidad) AS total_vendidos
        FROM detalle_pedido dp
        INNER JOIN productos pr ON dp.id_producto = pr.id_producto
        WHERE pr.id_usuario = %s
        GROUP BY pr.nombre
        ORDER BY total_vendidos DESC
        LIMIT 5
    """, (usuario['id_usuario'],))
    productos_vendidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("estadisticas_visual.html",
                           usuario=usuario,
                           ventas_mensuales=ventas_mensuales,
                           productos_vendidos=productos_vendidos)

# ----------------------------
# RF062 – Gestionar preguntas frecuentes (FAQ)
# ----------------------------
@app.route('/faq')
def faq():
    usuario = obtener_usuario()  # Mantener la sesión si es necesaria
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faq ORDER BY id_faq ASC")
    preguntas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('faq.html', usuario=usuario, preguntas=preguntas)
# ----------------------------
# PANEL DE FAQ (ADMIN / VENDEDOR)
# ----------------------------

@app.route('/admin/faq')
def admin_faq():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faq ORDER BY fecha_creacion DESC")
    faqs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_faq.html', usuario=usuario, faqs=faqs)


@app.route('/admin/faq/nuevo', methods=['GET', 'POST'])
def faq_nuevo():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:
        return redirect(url_for('login'))

    if request.method == 'POST':
        pregunta = request.form['pregunta']
        respuesta = request.form['respuesta']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faq (pregunta, respuesta, fecha_creacion) VALUES (%s, %s, NOW())",
            (pregunta, respuesta)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin_faq'))

    return render_template('faq_form.html', usuario=usuario, modo="nuevo")


@app.route('/admin/faq/editar/<int:id_faq>', methods=['GET', 'POST'])
def faq_editar(id_faq):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        pregunta = request.form['pregunta']
        respuesta = request.form['respuesta']

        cursor.execute(
            "UPDATE faq SET pregunta=%s, respuesta=%s WHERE id_faq=%s",
            (pregunta, respuesta, id_faq)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_faq'))

    cursor.execute("SELECT * FROM faq WHERE id_faq = %s", (id_faq,))
    faq = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('faq_form.html', usuario=usuario, faq=faq, modo="editar")


@app.route('/admin/faq/eliminar/<int:id_faq>', methods=['POST'])
def faq_eliminar(id_faq):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faq WHERE id_faq = %s", (id_faq,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_faq'))

# ----------------------------
# RF026 - Productos más vendidos
# ----------------------------
@app.route('/vendedor/productos_mas_vendidos', methods=['GET', 'POST'])
def productos_mas_vendidos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # solo vendedores
        return redirect(url_for('login'))

    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Si no se define rango, usamos el último mes
    if not fecha_inicio or not fecha_fin:
        cursor.execute("""
            SELECT MIN(DATE(p.fecha)) AS inicio, MAX(DATE(p.fecha)) AS fin
            FROM pedidos p
        """)
        rango = cursor.fetchone()
        fecha_inicio = rango['inicio']
        fecha_fin = rango['fin']

    # Consulta: productos más vendidos del vendedor
    cursor.execute("""
        SELECT 
            pr.nombre AS producto,
            SUM(dp.cantidad) AS cantidad_vendida,
            SUM(dp.cantidad * dp.precio_unitario) AS total_facturado
        FROM detalle_pedido dp
        INNER JOIN productos pr ON dp.id_producto = pr.id_producto
        INNER JOIN pedidos p ON dp.id_pedido = p.id_pedido
        WHERE pr.id_usuario = %s
          AND DATE(p.fecha) BETWEEN %s AND %s
        GROUP BY pr.id_producto, pr.nombre
        ORDER BY cantidad_vendida DESC
        LIMIT 10
    """, (usuario['id_usuario'], fecha_inicio, fecha_fin))

    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("productos_mas_vendidos.html",
                           usuario=usuario,
                           productos=productos,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)

# --------------------------------------
# RF027 - Seleccionar a un vendedor para los pedidos personalizados
# --------------------------------------

@app.route('/pedido_personalizado')
def seleccionar_vendedor():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre_completo, correo FROM usuarios WHERE id_rol = 2")
    vendedores = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("seleccionar_vendedor.html", usuario=usuario, vendedores=vendedores)

# --------------------------------------
#  Realizar el pedido personalizado 
# --------------------------------------

@app.route('/pedido_personalizado/<int:id_vendedor>', methods=['GET', 'POST'])
def pedido_personalizado(id_vendedor):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        tipo_producto = request.form['tipo_producto']
        materiales = request.form['materiales']
        diseno = request.form['diseno']
        presupuesto = request.form['presupuesto']
        archivo = request.files.get('archivo')

        archivo_nombre = None
        if archivo and archivo.filename != "":
            archivo_nombre = secure_filename(archivo.filename)
            upload_path = os.path.join("static", "uploads")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            archivo.save(os.path.join(upload_path, archivo_nombre))

        # Guardar en BD
        cursor.execute("""
            INSERT INTO pedidos_personalizados 
            (id_usuario, id_vendedor, tipo_producto, materiales, diseno, presupuesto, archivo, estado, fecha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pendiente', NOW())
        """, (usuario['id_usuario'], id_vendedor, tipo_producto, materiales, diseno, presupuesto, archivo_nombre))
        conn.commit()

        # Obtener correo del vendedor
        cursor.execute("SELECT nombre_completo, correo FROM usuarios WHERE id_usuario = %s", (id_vendedor,))
        vendedor = cursor.fetchone()

        if vendedor:
            asunto = "📩 Nuevo Pedido Personalizado"
            mensaje = f"""
                <p>Hola <b>{vendedor['nombre_completo']}</b>,</p>
                <p>Has recibido un nuevo pedido personalizado de <b>{usuario['nombre_completo']}</b>.</p>

                <ul>
                    <li>🛠 <b>Tipo de producto:</b> {tipo_producto}</li>
                    <li>💎 <b>Materiales:</b> {materiales}</li>
                    <li>🎨 <b>Diseño:</b> {diseno}</li>
                    <li>💰 <b>Presupuesto:</b> ${presupuesto}</li>
                </ul>
            """

            ruta_archivo = os.path.join("static", "uploads", archivo_nombre) if archivo_nombre else None

            if archivo_nombre and archivo_nombre.lower().endswith(('.png', '.jpg', '.jpeg')):
                enviar_correo(vendedor['correo'], asunto, mensaje, imagen_inline=ruta_archivo)
            elif archivo_nombre and archivo_nombre.lower().endswith('.pdf'):
                enviar_correo(vendedor['correo'], asunto, mensaje, archivo_adjunto=ruta_archivo)
            else:
                enviar_correo(vendedor['correo'], asunto, mensaje)

        cursor.close()
        conn.close()
        return redirect(url_for('mis_pedidos_personalizados'))

    cursor.close()
    conn.close()
    return render_template("pedido_personalizado.html", usuario=usuario, id_vendedor=id_vendedor)


# --------------------------------------
# Ver mis pedidos personalizados
# --------------------------------------
@app.route('/mis_pedidos_personalizados')
def mis_pedidos_personalizados():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # Solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Solo pedidos del usuario en sesión
    cursor.execute("""
    SELECT 
        id_pedido_personalizado AS id_pedido, 
        tipo_producto, materiales, diseno, presupuesto, archivo, estado, fecha
    FROM pedidos_personalizados
    WHERE id_usuario = %s
    ORDER BY fecha DESC""", 
    (usuario['id_usuario'],))
    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("mis_pedidos_personalizados.html", usuario=usuario, pedidos=pedidos)

# --------------------------------------
# Ver detalle de pedido personalizado
# --------------------------------------
@app.route('/detalle_pedido_personalizado/<int:id_pedido>')
def detalle_pedido_personalizado(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pp.id_pedido_personalizado,
               pp.tipo_producto,
               pp.materiales,
               pp.diseno,
               pp.presupuesto,
               pp.archivo,
               pp.estado,
               pp.fecha,
               u.nombre_completo AS vendedor
        FROM pedidos_personalizados pp
        INNER JOIN usuarios u ON pp.id_vendedor = u.id_usuario
        WHERE pp.id_pedido_personalizado = %s AND pp.id_usuario = %s
    """, (id_pedido, usuario['id_usuario']))
    pedido = cursor.fetchone()

    cursor.close()
    conn.close()

    if not pedido:
        return "Pedido no encontrado o no autorizado", 404

    return render_template("detalle_pedido_personalizado.html", usuario=usuario, pedido=pedido)

@app.route('/mis_pedidos')
def mis_pedidos():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_pedido, fecha, estado, total, estado_pago, codigo_seguimiento
        FROM pedidos
        WHERE id_usuario = %s
        ORDER BY fecha DESC
    """, (usuario['id_usuario'],))
    pedidos = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template('mis_pedidos.html', usuario=usuario, pedidos=pedidos)
# ----------------------------
# Pedidos recibidos por vendedor
# ----------------------------
from datetime import date

@app.route('/pedidos_recibidos')
def pedidos_recibidos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id_pedido_personalizado, p.tipo_producto, p.materiales, p.diseno, 
               p.presupuesto, p.archivo, p.estado, u.nombre_completo AS nombre_cliente
        FROM pedidos_personalizados p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE p.id_vendedor = %s
    """, (usuario['id_usuario'],))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("pedidos_recibidos.html", usuario=usuario, pedidos=pedidos, fecha_hoy=date.today().isoformat())
#-----------------------------
# validar talla 
#-----------------------------
@app.route('/validar_talla', methods=['POST'])
def validar_talla():
    usuario = obtener_usuario()
    if not usuario:
        return {"error": "No autorizado"}, 401

    id_producto = request.form.get('id_producto', type=int)
    id_talla = request.form.get('id_talla', type=int)
    cantidad = request.form.get('cantidad', type=int, default=1)

    if not id_producto or not id_talla:
        return {"error": "Faltan datos"}, 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Consultar stock específico de la talla
    cursor.execute("""
        SELECT stock 
        FROM detalle_pedido dp
        JOIN producto_talla pt ON dp.id_producto = pt.id_producto
        WHERE pt.id_producto = %s AND pt.id_talla = %s
        LIMIT 1
    """, (id_producto, id_talla))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()

    if fila and fila['stock'] >= cantidad:
        return {"ok": True, "stock": fila['stock']}
    else:
        return {"ok": False, "stock": fila['stock'] if fila else 0}


# RF059 – Calcular costo de envío
@app.route('/calcular_envio', methods=['POST'])
def calcular_envio():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    # Obtener datos del formulario
    peso_total = float(request.form.get('peso_total', 0))
    ciudad = request.form.get('ciudad', '').strip()

    # Ejemplo simple de cálculo
    # Puedes usar tabla de tarifas o API de envío real
    costo_envio = 0
    if ciudad.lower() == "bogota":
        costo_envio = 5000 + peso_total * 2000
    elif ciudad.lower() == "medellin":
        costo_envio = 6000 + peso_total * 2000
    else:
        costo_envio = 10000 + peso_total * 2500

    return render_template('calculo_envio.html', usuario=usuario, ciudad=ciudad, peso_total=peso_total, costo_envio=costo_envio)


#-----------------------------
# Cambiar estado de pedido
#-----------------------------
@app.route("/pedido_personalizado/<int:id_pedido>/estado", methods=["POST"])
def cambiar_estado_pedido(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario["id_rol"] != 2:
        return redirect(url_for("login"))

    estado = request.form["estado"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE pedidos_personalizados
        SET estado=%s
        WHERE id_pedido_personalizado=%s
    """, (estado, id_pedido))
    conn.commit()

    cursor.execute("""
        SELECT u.correo, u.nombre_completo
        FROM pedidos_personalizados p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE p.id_pedido_personalizado = %s
    """, (id_pedido,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        enviar_correo(
            destinatario=cliente["correo"],
            asunto="✅ Tu pedido personalizado fue aceptado",
            mensaje=f"""
                <p>Hola <b>{cliente['nombre_completo']}</b>,</p>
                <p>Nos alegra informarte que tu pedido personalizado fue <b>aceptado</b>.</p>
                <p>Pronto el vendedor se pondrá en contacto contigo para coordinar detalles.</p>
                <p>Saludos,<br><b>AVE Joyas</b></p>
            """
        )

    return redirect(url_for("pedidos_recibidos"))

@app.route("/pedido_personalizado/<int:id_pedido>/rechazar", methods=["POST"])
def rechazar_pedido(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario["id_rol"] != 2:
        return redirect(url_for("login"))

    motivo = request.form.get("motivo", "").strip()  # 👈 evita error si falta

    if not motivo:
        flash("Debes ingresar un motivo de rechazo.", "error")
        return redirect(url_for("pedidos_recibidos"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE pedidos_personalizados
        SET estado=%s, motivo_rechazo=%s
        WHERE id_pedido_personalizado=%s
    """, ("Rechazado", motivo, id_pedido))
    conn.commit()

    cursor.execute("""
        SELECT u.correo, u.nombre_completo
        FROM pedidos_personalizados p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE p.id_pedido_personalizado = %s
    """, (id_pedido,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        enviar_correo(
            destinatario=cliente["correo"],
            asunto="❌ Tu pedido personalizado fue rechazado",
            mensaje=f"""
                <p>Hola <b>{cliente['nombre_completo']}</b>,</p>
                <p>Lamentamos informarte que tu pedido personalizado fue <b>rechazado</b>.</p>
                <p><b>Motivo:</b> {motivo}</p>
                <p>Te invitamos a realizar otro pedido con diferentes condiciones.</p>
                <p>Saludos,<br><b>AVE Joyas</b></p>
            """
        )

    return redirect(url_for("pedidos_recibidos"))


#-----------------------------
#
#------------------------------

from datetime import date

@app.route('/pedido_personalizado/<int:id_pedido>/actualizar', methods=['POST'])
def actualizar_pedido_personalizado(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # solo vendedores
        return redirect(url_for('login'))

    estado = request.form['estado']
    comentario_rechazo = request.form.get('comentario_rechazo')
    fecha_entrega = request.form.get('fecha_entrega')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Validar fecha si se envía
    if fecha_entrega:
        fecha_entrega = date.fromisoformat(fecha_entrega)
        if fecha_entrega <= date.today():
            flash("La fecha estimada de entrega debe ser posterior al día de hoy.", "error")
            return redirect(url_for('pedidos_recibidos'))

    # Actualizar pedido
    cursor.execute("""
        UPDATE pedidos_personalizados
        SET estado = %s, fecha_entrega_estimada = %s
        WHERE id_pedido_personalizado = %s
    """, (estado, fecha_entrega, id_pedido))

    conn.commit()

    # 🔹 Obtener datos del cliente
    cursor.execute("""
        SELECT u.correo, u.nombre_completo, p.tipo_producto
        FROM pedidos_personalizados p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE p.id_pedido_personalizado = %s
    """, (id_pedido,))
    pedido = cursor.fetchone()

    cursor.close()
    conn.close()

    # 🔹 Enviar correo según estado
    if pedido:
        if estado == "Aceptado":
            asunto = "✅ Tu pedido personalizado fue aceptado"
            mensaje = f"""
            <p>Hola <b>{pedido['nombre_completo']}</b>,</p>
            <p>Tu pedido de <b>{pedido['tipo_producto']}</b> fue <b>aceptado</b>.</p>
            <p>📅 Fecha estimada de entrega: <b>{fecha_entrega.strftime("%d/%m/%Y")}</b></p>
            <p>Gracias por confiar en AVE Joyas ✨</p>
            """
            enviar_correo(destinatario=pedido['correo'], asunto=asunto, mensaje=mensaje)

        elif estado == "Rechazado":
            asunto = "❌ Tu pedido personalizado fue rechazado"
            mensaje = f"""
            <p>Hola <b>{pedido['nombre_completo']}</b>,</p>
            <p>Lamentamos informarte que tu pedido fue rechazado.</p>
            <p>Motivo: <i>{comentario_rechazo}</i></p>
            <p>Si lo deseas, puedes intentarlo de nuevo con otra solicitud.</p>
            """
            enviar_correo(destinatario=pedido['correo'], asunto=asunto, mensaje=mensaje)

    return redirect(url_for('pedidos_recibidos'))


# =============================
# RF060 – Resumen de compra antes de pagar
# =============================
@app.route('/resumen_compra')
def resumen_compra():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener productos en el carrito
    cursor.execute("""
        SELECT p.nombre, p.precio, c.cantidad, (p.precio * c.cantidad) AS subtotal
        FROM carrito_usuario c
        JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_usuario = %s
    """, (usuario['id_usuario'],))
    carrito = cursor.fetchall()

    if not carrito:
        cursor.close()
        conn.close()
        return redirect(url_for('catalogo'))

    subtotal = sum(item['subtotal'] for item in carrito)
    impuesto = round(subtotal * 0.19, 2)

    # --- Cálculo de envío (misma lógica de RF059) ---
    costo_envio = 5000
    if subtotal >= 200000:
        costo_envio = 0

    cursor.execute("SELECT direccion FROM usuarios WHERE id_usuario=%s", (usuario['id_usuario'],))
    data_user = cursor.fetchone()
    direccion_usuario = data_user['direccion'].lower()

    if "bogotá" not in direccion_usuario and "bogota" not in direccion_usuario:
        costo_envio += 8000

    total = subtotal + impuesto + costo_envio

    cursor.close()
    conn.close()

    return render_template(
        'resumen_compra.html',
        carrito=carrito,
        subtotal=subtotal,
        impuesto=impuesto,
        costo_envio=costo_envio,
        total=total,
        usuario=usuario
    )


# ----------------------------
# Configuración subida imágenes
# ----------------------------
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE_MB = 2  # máximo 2MB por imagen
MIN_WIDTH, MIN_HEIGHT = 600, 600  # resolución mínima

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/usuarios/<int:id_usuario>/editar', methods=['POST'])
def editar_rol_usuario(id_usuario):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores/admin
        return redirect(url_for('login'))


    nuevo_rol = request.form.get('rol')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET id_rol = %s WHERE id_usuario = %s", (nuevo_rol, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()


    return redirect(url_for('listar_usuarios'))

@app.route('/exportar_pedidos')
def exportar_pedidos():
    usuario = obtener_usuario()
    # Solo vendedores pueden exportar
    if not usuario or usuario['id_rol'] not in [1, 2]:  # Solo admin o vendedor

        return redirect(url_for('login'))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_pedido, fecha, estado, total,
               (SELECT nombre_completo FROM usuarios WHERE usuarios.id_usuario = pedidos.id_usuario) AS cliente
        FROM pedidos
        WHERE id_usuario = %s
        ORDER BY fecha DESC
    """, (usuario['id_usuario'],))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()


    # Crear CSV en memoria
    def generate():
        data = csv.StringIO()
        writer = csv.writer(data)


        # Cabecera
        writer.writerow(["ID Pedido", "Fecha", "Cliente", "Estado", "Total"])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)


        # Filas
        for pedido in pedidos:
            writer.writerow([
                pedido['id_pedido'],
                pedido['fecha'],
                pedido['cliente'],
                pedido['estado'],
                pedido['total']
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)


    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=pedidos.csv"})

@app.route('/usuarios')
def listar_usuarios():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] not in [1, 2]:  # Solo admin o vendedor
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre_completo, correo, id_rol, estado FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios, usuario=usuario)

# ============================================================
# RUTAS DE PERFIL DEL CLIENTE  (RF054 - adaptado a tu BD)
# ============================================================

from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from utils import get_db_connection, save_profile_image

def _usuario_logueado():
    """Obtiene el ID del usuario actual desde la sesión."""
    return session.get('user_id') or session.get('usuario_id')

@app.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    user_id = _usuario_logueado()
    if not user_id:
        flash('Debe iniciar sesión para editar su perfil.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form.get('nombre_completo', '').strip()
        telefono = request.form.get('telefono_contacto', '').strip()
        direccion = request.form.get('direccion', '').strip()
        fecha_nacimiento = request.form.get('fecha_nacimiento') or None

        # Procesar imagen de perfil (JPG, PNG, GIF)
        foto_nombre = None
        if 'foto_perfil' in request.files:
            archivo = request.files['foto_perfil']
            if archivo and archivo.filename != '':
                foto_nombre = save_profile_image(archivo)

        # Si no se sube nueva imagen, conservar la anterior
        if not foto_nombre:
            cursor.execute("SELECT foto_perfil FROM usuarios WHERE id_usuario=%s", (user_id,))
            fila = cursor.fetchone()
            foto_nombre = fila.get('foto_perfil') if fila else None

        # Validación básica
        if not nombre:
            flash('El nombre completo es obligatorio.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('editar_perfil'))

        # Actualizar datos en la base de datos
        cursor.execute("""
            UPDATE usuarios
            SET nombre_completo=%s,
                telefono_contacto=%s,
                direccion=%s,
                fecha_nacimiento=%s,
                foto_perfil=%s,
                fecha_modificacion=%s
            WHERE id_usuario=%s
        """, (nombre, telefono, direccion, fecha_nacimiento, foto_nombre, datetime.utcnow(), user_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('perfil'))

    # GET → Mostrar formulario con datos actuales
    cursor.execute("""
        SELECT id_usuario, nombre_completo, correo, telefono_contacto, direccion, 
               foto_perfil, fecha_nacimiento
        FROM usuarios WHERE id_usuario = %s
    """, (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('editar_perfil.html', usuario=usuario)



@app.route('/perfil/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    user_id = _usuario_logueado()
    if not user_id:
        flash('Debe iniciar sesión.', 'warning')
        return redirect(url_for('login'))

    actual = request.form.get('contrasena_actual', '')
    nueva = request.form.get('nueva_contrasena', '')
    repetir = request.form.get('repetir_contrasena', '')

    if not nueva or nueva != repetir:
        flash('Las contraseñas no coinciden o están vacías.', 'danger')
        return redirect(url_for('perfil'))

    if len(nueva) < 8:
        flash('La nueva contraseña debe tener al menos 8 caracteres.', 'danger')
        return redirect(url_for('perfil'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT contrasena FROM usuarios WHERE id_usuario=%s", (user_id,))
    fila = cursor.fetchone()
    if not fila:
        flash('Usuario no encontrado.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('perfil'))

    hash_actual = fila.get('contrasena')
    if not verify_password(hash_actual, actual):
        flash('La contraseña actual no es correcta.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('perfil'))

    nueva_hash = hash_password(nueva)
    cursor.execute("""
        UPDATE usuarios
        SET contrasena=%s, fecha_modificacion=%s
        WHERE id_usuario=%s
    """, (nueva_hash, datetime.utcnow(), user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Contraseña actualizada correctamente.', 'success')
    return redirect(url_for('perfil'))

@app.route('/admin/productos')
def admin_ver_productos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 1:
        flash("❌ Solo los administradores pueden acceder a esta sección.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT id_producto, nombre, descripcion, precio, stock, activo, destacado
    FROM productos
    ORDER BY id_producto ASC
""")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_productos.html', usuario=usuario, productos=productos)

#-----------------------------------------------------------------
# Funcion para mostrar la informacion del usuario en el checkout
#-----------------------------------------------------------------

@app.route('/checkout', methods=['GET'])
def checkout():
    if not session.get('usuario_id'):
        flash("Debe iniciar sesión para procesar un pedido.", "warning")
        return redirect(url_for('login'))

    id_usuario = session['usuario_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener carrito del usuario
    cursor.execute("""
        SELECT c.id_producto, c.cantidad, p.nombre, p.precio, p.stock, p.imagen
        FROM carrito c
        INNER JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_usuario = %s
    """, (id_usuario,))
    carrito = cursor.fetchall()

    if len(carrito) == 0:
        flash("El carrito está vacío.", "danger")
        return redirect(url_for('catalogo'))

    # Datos del usuario (para prellenar)
    cursor.execute("""
        SELECT nombre_completo, direccion, telefono_contacto, correo
        FROM usuarios
        WHERE id_usuario = %s
    """, (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("checkout.html", usuario=usuario, carrito=carrito)

@app.route('/datos_envio', methods=['GET'])
def datos_envio():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))
    
    return render_template('datos_envio.html', usuario=usuario)

# -------------------------------------------------------------------
# Productos que el cliente puede valorar
# -------------------------------------------------------------------
@app.route('/mis_valoraciones')
def mis_valoraciones():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
       SELECT DISTINCT 
    dp.id_producto,
    p.nombre,
    COALESCE(img.url, '') AS imagen,
    p.precio,
    ep.nombre_estado
FROM detalle_pedido dp
JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
JOIN productos p ON dp.id_producto = p.id_producto
JOIN estados_pedido ep ON ep.id_estado = ped.id_estado
LEFT JOIN imagenes img ON img.id_producto = p.id_producto
WHERE ped.id_usuario = %s
  AND ped.id_estado = 4   -- ENTREGADO
  AND dp.id_producto NOT IN (
      SELECT id_producto FROM valoraciones WHERE id_usuario = %s
  )
GROUP BY dp.id_producto;
    """
    cursor.execute(query, (usuario['id_usuario'], usuario['id_usuario']))
    productos = cursor.fetchall()

    conn.close()

    return render_template(
        "mis_valoraciones.html",
        usuario=usuario,
        productos=productos
    )

    
# -------------------------------------------------------------------
# Formulario de valoración
# -------------------------------------------------------------------
@app.route('/valorar/<int:id_producto>', methods=['GET'])
def valorar_producto(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:
        return redirect(url_for('login'))

    return render_template(
        "valorar_producto.html",
        id_producto=id_producto,
        usuario=usuario
    )


# -------------------------------------------------------------------
# Guardar valoración
# -------------------------------------------------------------------
@app.route('/valorar/<int:id_producto>', methods=['POST'])
def guardar_valoracion(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    estrellas = int(request.form.get("calificacion"))
    comentario = request.form.get("comentario")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO valoraciones (id_usuario, id_producto, estrellas, comentario)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        usuario['id_usuario'],
        id_producto,
        estrellas,
        comentario
    ))

    conn.commit()
    conn.close()

    flash("Valoración registrada correctamente", "success")
    return redirect(url_for('mis_valoraciones'))


@app.route('/cliente/mis_valoraciones')
def mis_valoraciones_historial():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # 3 = Cliente
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT v.estrellas AS calificacion, v.comentario, v.fecha,
       p.nombre, img.url AS imagen
FROM valoraciones v
JOIN productos p ON v.id_producto = p.id_producto
LEFT JOIN imagenes img ON img.id_producto = p.id_producto
WHERE v.id_usuario = %s
ORDER BY v.fecha DESC
    """
    cursor.execute(query, (usuario['id_usuario'],))
    valoraciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("mis_valoraciones_historial.html",
                           valoraciones=valoraciones,
                           usuario=usuario)

@app.route('/descargar_ficha/<int:id_producto>')
def descargar_ficha(id_producto):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    import os

    carpeta_pdf = "static/pdf"
    if not os.path.exists(carpeta_pdf):
        os.makedirs(carpeta_pdf)

    nombre_pdf = f"ficha_{id_producto}.pdf"
    ruta_pdf = os.path.join(carpeta_pdf, nombre_pdf)

    # Si ya existe, devolver directamente
    if os.path.exists(ruta_pdf):
        return send_from_directory(carpeta_pdf, nombre_pdf, as_attachment=True)

    # ----------------------------------------
    # OBTENER DATOS DEL PRODUCTO
    # ----------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id_producto,
            p.codigo_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.peso,
            p.alto,
            p.ancho,
            p.largo,
            t.nombre_tipo AS tipo_joya,
            m.nombre_material AS material,
            c.nombre AS color,
            pi.nombre AS piedra
        FROM productos p
        LEFT JOIN tipos_joya t ON p.id_tipo = t.id_tipo
        LEFT JOIN materiales m ON p.id_material = m.id_material
        LEFT JOIN colores c ON p.id_color = c.id_color
        LEFT JOIN piedras pi ON p.id_piedra = pi.id_piedra
        WHERE p.id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    # Obtener tallas
    cursor.execute("""
        SELECT talla, stock 
        FROM stock_tallas 
        WHERE id_producto = %s
        ORDER BY talla ASC
    """, (id_producto,))
    tallas = cursor.fetchall()

    # Obtener UNA imagen desde tabla imagenes
    cursor.execute("""
        SELECT url FROM imagenes
        WHERE id_producto = %s
        ORDER BY id_imagen ASC
        LIMIT 1
    """, (id_producto,))
    imagen_extra = cursor.fetchone()

    cursor.close()
    conn.close()

    if not producto:
        return "Producto no encontrado", 404

    # ----------------------------------------
    # PROCESAR IMÁGENES
    # ----------------------------------------
    imagen_producto = None

    # 1) Si la tabla productos tuviera columna imagen (no la tienes pero no dará error)
    imagen_principal = producto.get("imagen")

    if imagen_principal:
        posible = os.path.join("static", imagen_principal)
        if os.path.exists(posible):
            imagen_producto = posible

    # 2) Imagen desde tabla imagenes
    if not imagen_producto and imagen_extra:
        posible = os.path.join("static", imagen_extra["url"])
        if os.path.exists(posible):
            imagen_producto = posible

    # ----------------------------------------
    # CREAR EL PDF
    # ----------------------------------------
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Logo
    logo_path = "static/img/logoave.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=140, height=60))
        story.append(Spacer(1, 12))

    # Título
    story.append(Paragraph("<b>Ficha Técnica del Producto</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # Imagen del producto
    if imagen_producto and os.path.exists(imagen_producto):
        story.append(Image(imagen_producto, width=250, height=250))
        story.append(Spacer(1, 20))

    # TABLA DE INFORMACIÓN
    info = [
        ["Nombre", producto["nombre"]],
        ["Código", producto["codigo_producto"]],
        ["Tipo de joya", producto["tipo_joya"]],
        ["Material", producto["material"]],
        ["Color", producto["color"]],
        ["Piedra", producto["piedra"]],
        ["Peso", f"{producto['peso']} g"],
        ["Dimensiones", f"{producto['largo']} x {producto['ancho']} x {producto['alto']} mm"],
        ["Precio", f"${producto['precio']}"],
    ]

    tabla_info = Table(info, colWidths=[130, 350])
    tabla_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d9c7ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    story.append(tabla_info)
    story.append(Spacer(1, 20))

    # Descripción
    story.append(Paragraph("<b>Descripción del Producto:</b>", styles["Heading3"]))
    story.append(Paragraph(producto["descripcion"], styles["BodyText"]))
    story.append(Spacer(1, 20))

    # TABLA DE TALLAS
    if tallas:
        story.append(Paragraph("<b>Tallas Disponibles</b>", styles["Heading3"]))
        datos_tallas = [["Talla", "Stock"]] + [[t["talla"], t["stock"]] for t in tallas]
        tabla_tallas = Table(datos_tallas, colWidths=[100, 120])
        tabla_tallas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d9c7ff")),
            ('GRID', (0, 0), (-1, -1), 1, colors.gray),
            ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ]))
        story.append(tabla_tallas)

    story.append(Spacer(1, 40))
    story.append(Paragraph("Documento generado automáticamente por <b>AVE Joyas</b>.", styles["Italic"]))

    doc.build(story)

    return send_from_directory(carpeta_pdf, nombre_pdf, as_attachment=True)

from datetime import datetime

def obtener_id_estado(cursor, nombre_estado):
    cursor.execute("SELECT id_estado FROM estados_pedido WHERE nombre_estado = %s LIMIT 1", (nombre_estado,))
    row = cursor.fetchone()
    return row['id_estado'] if row else None

def registrar_historial(cursor, id_pedido, id_estado, id_usuario=None, comentario=None):
    cursor.execute("""
        INSERT INTO historial_pedido (id_pedido, id_estado, id_usuario, comentario)
        VALUES (%s, %s, %s, %s)
    """, (id_pedido, id_estado, id_usuario, comentario))
    

def actualizar_estado_pedido(id_pedido, nuevo_estado, id_usuario=None, comentario=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener id del estado nuevo
    cursor.execute("""
        SELECT id_estado 
        FROM estados_pedido 
        WHERE nombre_estado = %s
        LIMIT 1
    """, (nuevo_estado,))
    
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        raise ValueError(f"Estado '{nuevo_estado}' no existe en la tabla estados_pedido")

    id_estado = row['id_estado']

    # Actualizar pedido
    cursor.execute("""
        UPDATE pedidos
        SET id_estado = %s
        WHERE id_pedido = %s
    """, (id_estado, id_pedido))

    # Registrar en historial
    cursor.execute("""
        INSERT INTO historial_pedido (id_pedido, id_estado, id_usuario, comentario)
        VALUES (%s, %s, %s, %s)
    """, (id_pedido, id_estado, id_usuario, comentario))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/pedido/<int:id_pedido>/estado/<string:nuevo_estado>', methods=['POST'])
def ruta_actualizar_estado_pedido(id_pedido, nuevo_estado):
    usuario = obtener_usuario()

    # Solo admin (1) y vendedor (2)
    if not usuario or usuario['id_rol'] not in [1, 2]:
        return redirect(url_for('login'))

    try:
        actualizar_estado_pedido(
            id_pedido=id_pedido,
            nuevo_estado=nuevo_estado,
            id_usuario=usuario['id_usuario'],
            comentario=f"Estado cambiado a {nuevo_estado}"
        )

        flash(f"El pedido ahora está en estado: {nuevo_estado}", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('gestionar_pedidos'))

@app.route('/rastreo/<codigo>')
def rastreo_publico(codigo):
    usuario = obtener_usuario()  # puede ser None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, e.nombre_estado
        FROM pedidos p
        LEFT JOIN estados_pedido e ON p.id_estado = e.id_estado
        WHERE p.numero_pedido = %s OR p.codigo_seguimiento = %s
        LIMIT 1
    """, (codigo, codigo))

    pedido = cursor.fetchone()

    if not pedido:
        cursor.close()
        conn.close()
        return render_template("rastreo_error.html", usuario=usuario)

    cursor.execute("""
        SELECT d.*, pr.nombre
        FROM detalle_pedido d
        LEFT JOIN productos pr ON pr.id_producto = d.id_producto
        WHERE d.id_pedido = %s
    """, (pedido["id_pedido"],))
    detalles = cursor.fetchall()

    cursor.execute("""
        SELECT h.*, e.nombre_estado, u.nombre_completo AS usuario
        FROM historial_pedido h
        LEFT JOIN estados_pedido e ON e.id_estado = h.id_estado
        LEFT JOIN usuarios u ON u.id_usuario = h.id_usuario
        WHERE h.id_pedido = %s
        GROUP BY h.id_estado
        ORDER BY MIN(h.fecha) ASC
    """, (pedido["id_pedido"],))
    historial = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "rastreo_publico.html",
        usuario=usuario,  # puede ser None
        pedido=pedido,
        detalles=detalles,
        historial=historial
    )


    
@app.route('/mi-pedido/<codigo>')
def mi_pedido(codigo):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar pedido por código, pero SOLO si pertenece al usuario logueado
    cursor.execute("""
        SELECT p.*, e.nombre_estado
        FROM pedidos p
        LEFT JOIN estados_pedido e ON p.id_estado = e.id_estado
        WHERE (p.numero_pedido = %s OR p.codigo_seguimiento = %s)
          AND p.id_usuario = %s
        LIMIT 1
    """, (codigo, codigo, usuario['id_usuario']))

    pedido = cursor.fetchone()

    # Si el pedido no pertenece al usuario o no existe
    if not pedido:
        cursor.close()
        conn.close()
        flash("No puedes ver este pedido o no existe.", "danger")
        return redirect(url_for('mis_pedidos'))

    # Obtener los productos del pedido
    cursor.execute("""
        SELECT d.*, pr.nombre
        FROM detalle_pedido d
        LEFT JOIN productos pr ON pr.id_producto = d.id_producto
        WHERE d.id_pedido = %s
    """, (pedido['id_pedido'],))

    detalles = cursor.fetchall()

    # Obtener historial completo
    cursor.execute("""
        SELECT h.*, e.nombre_estado, u.nombre_completo AS usuario
        FROM historial_pedido h
        LEFT JOIN estados_pedido e ON e.id_estado = h.id_estado
        LEFT JOIN usuarios u ON u.id_usuario = h.id_usuario
        WHERE h.id_pedido = %s
        ORDER BY h.fecha ASC
    """, (pedido['id_pedido'],))

    historial = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'mi_pedido.html',
        usuario=usuario,
        pedido=pedido,
        detalles=detalles,
        historial=historial
    )

@app.route('/rastreo', methods=['GET', 'POST'])
def buscar_rastreo():
    usuario = obtener_usuario()

    if request.method == 'POST':
        codigo = request.form.get("codigo")
        return redirect(url_for('rastreo_publico', codigo=codigo))

    return render_template("rastreo_buscar.html", usuario=usuario)

@app.route('/producto/<int:id_producto>/destacar')
def destacar_producto(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 1:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener estado actual
    cursor.execute(
        "SELECT destacado FROM productos WHERE id_producto = %s",
        (id_producto,)
    )
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        return redirect(url_for('admin_ver_productos'))

    nuevo_estado = 0 if producto['destacado'] == 1 else 1

    # Actualizar estado
    cursor.execute(
        "UPDATE productos SET destacado = %s WHERE id_producto = %s",
        (nuevo_estado, id_producto)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_ver_productos'))

@app.route('/producto/<int:id_producto>/quitar-destacado')
def quitar_destacado(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 1:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE productos SET destacado = 0 WHERE id_producto = %s",
        (id_producto,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_ver_productos'))

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
