import csv
from flask import Response
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from utils import get_db_connection, enviar_correo, generar_token, save_profile_image, hash_password, verify_password
from flask import request, jsonify , current_app
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

    # Obtener filtros
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
    pr.descuento AS descuento_promocion,
    pr.nombre AS nombre_promocion,
    CASE 
        WHEN pr.descuento IS NOT NULL THEN ROUND(p.precio - (p.precio * pr.descuento), 2)
        ELSE p.precio
    END AS precio_final
FROM productos p
LEFT JOIN imagenes i ON p.id_producto = i.id_producto
LEFT JOIN producto_promocion pp ON p.id_producto = pp.id_producto
LEFT JOIN promociones pr 
       ON pp.id_promocion = pr.id_promocion 
       AND pr.estado = 1 
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
    
    # =====================================================
# 🔥 REEMPLAZAR EL STOCK GENERAL CON LA SUMA DE STOCK_TALLAS
# =====================================================
    for p in productos:
        cursor.execute("""
            SELECT COALESCE(SUM(stock), 0) AS total_stock
            FROM stock_tallas
            WHERE id_producto = %s
        """, (p['id_producto'],))
        result = cursor.fetchone()
        p['stock'] = result['total_stock']  # ← Reemplaza el stock original
# =====================================================

    # Normalizar imágenes
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

    # Obtener tipos y materiales para el formulario
    cursor.execute("SELECT * FROM tipos_joya ORDER BY nombre_tipo ASC")
    tipos = cursor.fetchall()
    cursor.execute("SELECT * FROM materiales ORDER BY nombre_material ASC")
    materiales = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'catalogo.html',
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
        GROUP_CONCAT(i.url SEPARATOR '||') AS imagenes_concat
    FROM productos p
    LEFT JOIN imagenes i ON p.id_producto = i.id_producto
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

    # Normalizar imágenes
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
            p.stock,
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
        imagenes = [normalize(s) for s in producto["imagenes_concat"].split("||") if s]

    if producto.get("imagen_local"):
        imagenes.insert(0, normalize(producto["imagen_local"]))

    if not imagenes:
        imagenes = [url_for('static', filename='img/no-image.png')]

    producto["imagenes"] = imagenes

    # ---- Dimensiones ----
    if producto.get("largo") and producto.get("ancho") and producto.get("alto"):
        producto["dimensiones"] = f"{producto['largo']} x {producto['ancho']} x {producto['alto']}"
    else:
        producto["dimensiones"] = "N/A"

   # ---- STOCK POR TALLA ----
    cursor.execute("""
    SELECT talla, stock
    FROM stock_tallas
    WHERE id_producto = %s
    ORDER BY talla ASC
""", (id_producto,))
    producto["tallas"] = cursor.fetchall()

# ---- STOCK TOTAL SUMANDO LAS TALLAS ----
    cursor.execute("""
    SELECT COALESCE(SUM(stock), 0) AS total_stock
    FROM stock_tallas
    WHERE id_producto = %s
""", (id_producto,))
    result = cursor.fetchone()
    producto['stock'] = result['total_stock']


    cursor.close()
    conn.close()

    return render_template("producto_detalle.html", usuario=usuario, producto=producto)


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
        SELECT c.id_producto, c.cantidad, p.nombre, p.precio, 
               COALESCE(i.url, '') AS imagen
        FROM carrito_usuario c
        JOIN productos p ON c.id_producto = p.id_producto
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        WHERE c.id_usuario = %s
    """, (usuario['id_usuario'],))
    carrito = cursor.fetchall()
    cursor.close()
    conn.close()

    total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total, usuario=usuario)

@app.route('/carrito/agregar/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    cantidad = int(request.form.get('cantidad', 1))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ver si el producto ya está en el carrito del usuario
    cursor.execute("""
        SELECT cantidad FROM carrito_usuario
        WHERE id_usuario=%s AND id_producto=%s
    """, (usuario['id_usuario'], id_producto))
    fila = cursor.fetchone()

    if fila:
        # Si existe, sumamos cantidad
        cursor.execute("""
            UPDATE carrito_usuario
            SET cantidad = cantidad + %s
            WHERE id_usuario=%s AND id_producto=%s
        """, (cantidad, usuario['id_usuario'], id_producto))
    else:
        # Si no existe, insertamos nuevo
        cursor.execute("""
            INSERT INTO carrito_usuario (id_usuario, id_producto, cantidad)
            VALUES (%s, %s, %s)
        """, (usuario['id_usuario'], id_producto, cantidad))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('catalogo'))

@app.route('/carrito/eliminar/<int:id_producto>')
def eliminar_carrito(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM carrito_usuario
        WHERE id_usuario=%s AND id_producto=%s
    """, (usuario['id_usuario'], id_producto))
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
    cursor.close(); conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar producto sin talla
        cursor.execute("""
            INSERT INTO productos
                (nombre, descripcion, precio, peso, alto, ancho, largo,
                 id_tipo, id_material, id_color, id_piedra, id_usuario)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nombre, descripcion, precio, peso, alto, ancho, largo,
              id_tipo, id_material, id_color, id_piedra, usuario['id_usuario']))

        id_producto = cursor.lastrowid

        # Stock por talla
        tallas = request.form.getlist('talla[]')
        stocks = request.form.getlist('stock[]')
        for t, s in zip(tallas, stocks):
            cursor.execute("""
                INSERT INTO stock_tallas (id_producto, talla, stock)
                VALUES (%s, %s, %s)
            """, (id_producto, t, int(s)))

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
        cursor.close(); conn.close()
        flash("✅ Producto registrado con éxito", "success")
        return redirect(url_for('mis_productos'))

    return render_template("registrar_producto.html",
                           usuario=usuario,
                           colores=lista_colores,
                           piedras=lista_piedras,
                           tipos=lista_tipos,
                           materiales=lista_materiales)


 


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
    cursor.execute("""
        SELECT nombre, descripcion, precio, stock, umbral_alerta, peso, alto, ancho, largo
        FROM productos WHERE id_usuario=%s
    """, (usuario['id_usuario'],))
    productos = cursor.fetchall()
    cursor.close(); conn.close()

    wb = Workbook()# type: ignore
    ws = wb.active; ws.title = "Inventario"
    ws.append(["Nombre","Descripción","Precio","Stock","Umbral","Peso","Alto","Ancho","Largo"])
    for p in productos:
        ws.append([p['nombre'], p['descripcion'], p['precio'], p['stock'],
                   p['umbral_alerta'], p['peso'], p['alto'], p['ancho'], p['largo']])
    output = io.BytesIO() # type: ignore
    wb.save(output); output.seek(0)
    return send_file(output, as_attachment=True, download_name="reporte_inventario.xlsx", # type: ignore
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

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



# ---------------------------------------------------------
# Gestionar pedidos reales del vendedor (con cambio de estado)
# ---------------------------------------------------------
@app.route('/vendedor/pedidos')
def gestionar_pedidos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    id_vendedor = usuario['id_usuario']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer solo los pedidos que tienen productos de este vendedor
    cursor.execute("""
        SELECT 
            p.id_pedido,
            p.fecha,
            p.estado,
            u.nombre_completo AS cliente,
            GROUP_CONCAT(prod.nombre SEPARATOR ', ') AS productos
        FROM pedidos p
        JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
        JOIN productos prod ON dp.id_producto = prod.id_producto
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        WHERE prod.id_usuario = %s
        GROUP BY p.id_pedido, p.fecha, p.estado, cliente
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

    if request.method == 'POST':

        metodo = request.form['metodo']
        monto = float(request.form['monto'])
        estado = "pagado"

        # Registrar pago
        cursor.execute("""
            INSERT INTO pagos (id_pedido, monto, metodo_pago, estado, fecha)
            VALUES (%s, %s, %s, %s, NOW())
        """, (id_pedido, monto, metodo, estado))
        id_pago = cursor.lastrowid

        # Actualizar estado del pedido
        cursor.execute("""
            UPDATE pedidos 
            SET estado_pago='pagado'
            WHERE id_pedido=%s
        """, (id_pedido,))

        # === Obtener información completa del pedido para factura ===
        cursor.execute("""
            SELECT * FROM pedidos WHERE id_pedido = %s
        """, (id_pedido,))
        pedido = cursor.fetchone()

        cursor.execute("""
            SELECT d.id_producto, d.cantidad, d.precio_unitario,
                   (d.cantidad * d.precio_unitario) AS subtotal,
                   p.nombre
            FROM detalle_pedido d
            JOIN productos p ON p.id_producto = d.id_producto
            WHERE d.id_pedido = %s
        """, (id_pedido,))
        detalles = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        # ====================
        # GENERAR FACTURA PDF
        # ====================
        from utils import generar_factura_pdf
        import os

        carpeta = "static/facturas"
        os.makedirs(carpeta, exist_ok=True)

        ruta_pdf = f"{carpeta}/factura_{id_pedido}.pdf"

        generar_factura_pdf(pedido, detalles, ruta_pdf)

        flash("Pago registrado correctamente. Tu factura está disponible.", "success")
        return redirect(url_for('ver_factura', id_pedido=id_pedido))

    # ====================
    # MÉTODO GET (mostrar formulario)
    # ====================
    cursor.close()
    conn.close()
    return render_template('pago_form.html', usuario=usuario, pedido=pedido)

@app.route('/factura/<int:id_pedido>')
def ver_factura(id_pedido):
    ruta = f"static/facturas/factura_{id_pedido}.pdf"
    return render_template("factura_lista.html", ruta=ruta, id_pedido=id_pedido)



# ----------------------------
# Confirmación de Pago
# ----------------------------
@app.route('/pago/<int:id_pago>/exito')
def pago_exito(id_pago):
    usuario = obtener_usuario()
    # ✅ Ahora permitimos clientes (3) y vendedores (2)
    if not usuario or usuario['id_rol'] not in [1, 2, 3]:
        return redirect(url_for('login'))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pagos WHERE id_pago = %s", (id_pago,))
    pago = cursor.fetchone()
    cursor.close()
    conn.close()


    if not pago:
        return "Pago no encontrado", 404


    return render_template('pago_exito.html', usuario=usuario, pago=pago)




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
        SELECT pa.*, pe.total
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
        SELECT c.id_producto, c.cantidad, p.precio, p.stock
        FROM carrito_usuario c
        JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_usuario = %s
    """, (usuario['id_usuario'],))
    carrito = cursor.fetchall()

    if not carrito:
        cursor.close()
        conn.close()
        return redirect(url_for('carrito'))

    # Calcular totales
    subtotal = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
    impuesto = round(subtotal * 0.19, 2)
    total = subtotal + impuesto

    # Insertar pedido con datos del cliente
    cursor.execute("""
        INSERT INTO pedidos 
        (id_usuario, fecha, estado, subtotal, impuesto, total,
        nombre_cliente, direccion_entrega, telefono_cliente,
        correo_cliente)
        VALUES (%s, NOW(), 'Pendiente', %s, %s, %s,
        %s, %s, %s, %s)
    """, (
        usuario['id_usuario'], subtotal, impuesto, total,
        nombre_cliente, direccion_entrega, telefono_cliente,
        correo_cliente
    ))

    id_pedido = cursor.lastrowid

    # Insertar productos + actualizar stock
    for item in carrito:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_pedido, item['id_producto'], item['cantidad'], item['precio']))

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

    if not producto:
        cursor.close()
        conn.close()
        return "Producto no encontrado", 404

    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        motivo = request.form.get('observacion', '')  # aquí recoges el form

        id_usuario = session.get('usuario_id')  # si no hay sesión, forzar al vendedor con id 2

        if not id_usuario:
            return redirect(url_for('login'))  # seguridad extra

        # 1. Insertar en movimientos_inventario
        cursor.execute("""
            INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, motivo, id_usuario)
            VALUES (%s, 'entrada', %s, %s, %s)
        """, (id_producto, cantidad, motivo, id_usuario))

        # 2. Actualizar stock en la tabla productos
        cursor.execute("""
            UPDATE productos
            SET stock = stock + %s
            WHERE id_producto = %s
        """, (cantidad, id_producto))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template('registrar_entrada_stock.html', producto=producto, usuario=usuario)


#-----------------------------
# Registrar salida stock
#-----------------------------
@app.route('/producto/<int:id_producto>/registrar_salida', methods=['GET', 'POST'])
def registrar_salida_stock(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores/admins
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        motivo = request.form['motivo']

        # Validar stock disponible
        if cantidad <= 0:
            return render_template("registrar_salida_stock.html", producto=producto, error="La cantidad debe ser mayor a 0.")
        if cantidad > producto['stock']:
            return render_template("registrar_salida_stock.html", producto=producto, error="No hay suficiente stock disponible.")

        # Insertar movimiento de salida

        id_usuario = session.get('id_usuario')

        cursor.execute("""
            INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, motivo, id_usuario)
            VALUES (%s, 'salida', %s, %s, %s)
        """, (id_producto, cantidad, motivo, usuario['id_usuario']))

        # Actualizar stock del producto
        cursor.execute("""
            UPDATE productos SET stock = stock - %s WHERE id_producto = %s
        """, (cantidad, id_producto))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('mis_productos'))

    cursor.close()
    conn.close()
    return render_template("registrar_salida_stock.html", producto=producto, usuario=usuario)

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



# ----------------------------
# Reportes de ventas (RF024)
# ----------------------------

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
                u.nombre_completo AS cliente,
                p.estado,
                SUM(dp.cantidad * dp.precio_unitario) AS total,
                GROUP_CONCAT(CONCAT(pr.nombre, ' (x', dp.cantidad, ')') SEPARATOR ', ') AS productos
            FROM pedidos p
            INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN productos pr ON dp.id_producto = pr.id_producto
            WHERE DATE(p.fecha) BETWEEN %s AND %s
              AND pr.id_usuario = %s
            GROUP BY p.id_pedido, p.fecha, u.nombre_completo, p.estado
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
        SELECT id_producto, nombre, descripcion, precio, stock, activo
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
    if not usuario or usuario['id_rol'] != 3:  # solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT DISTINCT 
            dp.id_producto,
            p.nombre,
            p.imagen,
            p.precio,
            ped.estado
        FROM detalle_pedido dp
        JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
        JOIN productos p ON dp.id_producto = p.id_producto
        WHERE ped.id_usuario = %s
          AND ped.estado = 'Entregado'
          AND dp.id_producto NOT IN (
              SELECT id_producto FROM valoraciones WHERE id_usuario = %s
          );
    """
    cursor.execute(query, (usuario['id_usuario'], usuario['id_usuario']))
    productos_para_valorar = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("mis_valoraciones.html",
                           usuario=usuario,
                           productos=productos_para_valorar)
    
# -------------------------------------------------------------------
# Formulario de valoración
# -------------------------------------------------------------------
@app.route('/valorar/<int:id_producto>', methods=['GET'])
def valorar_producto(id_producto):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:
        return redirect(url_for('login'))

    return render_template("valorar_producto.html",
                           usuario=usuario,
                           id_producto=id_producto)

# -------------------------------------------------------------------
# Guardar valoración
# -------------------------------------------------------------------
@app.route('/valorar/<int:id_producto>', methods=['POST'])
def guardar_valoracion(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    calificacion = request.form.get("calificacion")
    comentario = request.form.get("comentario")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO valoraciones (id_usuario, id_producto, calificacion, comentario)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (usuario['id_usuario'], id_producto, calificacion, comentario))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('mis_valoraciones'))

@app.route('/cliente/mis_valoraciones')
def mis_valoraciones_historial():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # 3 = Cliente
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT v.calificacion, v.comentario, v.fecha,
               p.nombre, p.imagen
        FROM valoraciones v
        JOIN productos p ON v.id_producto = p.id_producto
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

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
