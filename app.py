from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from utils import get_db_connection, enviar_correo, generar_token

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
    if 'usuario_id' not in session:
        return None
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (session['usuario_id'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
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

# ----------------------------
# Catálogo
# ----------------------------
@app.route('/catalogo')
def catalogo():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, 
        p.imagen AS imagen_local, i.url AS imagen_url
        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto;
    """)
    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('catalogo.html', productos=productos, usuario=usuario)

# ----------------------------
# Producto - Detalle (CLIENTE)
# ----------------------------
@app.route('/producto/<int:id_producto>')
def producto_detalle(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, i.url AS imagen
        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        WHERE p.id_producto = %s
    """, (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if not producto:
        return redirect(url_for('catalogo'))

    return render_template('producto_detalle.html', producto=producto, usuario=usuario)

# ----------------------------
# Carrito de compras
# ----------------------------
@app.route('/carrito')
def carrito():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    carrito = session.get('carrito', [])
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
    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.precio, i.url AS imagen
        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
        WHERE p.id_producto = %s
    """, (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if not producto:
        return redirect(url_for('catalogo'))

    if 'carrito' not in session:
        session['carrito'] = []

    carrito = session['carrito']

    for item in carrito:
        if item['id_producto'] == id_producto:
            item['cantidad'] += int(cantidad)
            break
    else:
        carrito.append({
            'id_producto': producto['id_producto'],
            'nombre': producto['nombre'],
            'precio': float(producto['precio']),
            'imagen': producto['imagen'],
            'cantidad': int(cantidad)
        })

    session['carrito'] = carrito
    return redirect(url_for('catalogo'))

@app.route('/carrito/eliminar/<int:id_producto>')
def eliminar_carrito(id_producto):
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))

    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id_producto'] != id_producto]
    session['carrito'] = carrito
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

# ----------------------------
# Registrar producto
# ----------------------------
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    usuario = obtener_usuario()
    if not usuario:
        return redirect(url_for('login'))  # seguridad: solo logueados pueden registrar

    id_usuario = usuario['id_usuario']

    nombre = request.form['nombre']
    precio = request.form['precio']
    stock = request.form['stock']
    categoria = request.form.get('categoria')
    descripcion = request.form.get('descripcion')

    archivo = request.files.get('imagen')
    imagen_nombre = None

    if archivo and archivo.filename != '' and allowed_file(archivo.filename):
        imagen_nombre = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre))

    # Guardar en la BD (incluyendo id_usuario)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, stock, categoria, imagen_nombre, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('mis_productos'))



# ----------------------------
# Ver mis productos
# ----------------------------
@app.route('/vendedor/productos')
def mis_productos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_usuario = %s", (usuario['id_usuario'],))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('mis_productos.html', usuario=usuario, productos=productos)


# ----------------------------
# Estadísticas de ventas (dummy de momento)
# ----------------------------
@app.route('/vendedor/estadisticas')
def estadisticas():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    # TODO: más adelante consultar ventas reales
    data = {
        "total_ventas": 25,
        "ingresos": 1200000,
        "producto_mas_vendido": "Anillo de oro"
    }

    return render_template('estadisticas.html', usuario=usuario, data=data)


# ----------------------------
# Gestionar pedidos (dummy)
# ----------------------------
@app.route('/vendedor/pedidos')
def gestionar_pedidos():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:
        return redirect(url_for('login'))

    # TODO: conectar con tabla de pedidos
    pedidos = [
        {"id": 1, "cliente": "Carlos Pérez", "producto": "Anillo Plata", "estado": "Pendiente"},
        {"id": 2, "cliente": "Ana Torres", "producto": "Collar Oro", "estado": "Enviado"},
    ]

    return render_template('pedidos.html', usuario=usuario, pedidos=pedidos)

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('mis_productos'))

# ----------------------------
# Registrar Pago
# ----------------------------
@app.route('/pedido/<int:id_pedido>/pago', methods=['GET', 'POST'])
def registrar_pago(id_pedido):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:  # Solo clientes
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Traer pedido y total
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s AND id_usuario = %s",
                   (id_pedido, usuario['id_usuario']))
    pedido = cursor.fetchone()

    if not pedido:
        cursor.close()
        conn.close()
        return "Pedido no encontrado o no autorizado", 404

    if request.method == 'POST':
        metodo = request.form['metodo']

        # 2. Usar el total real del pedido, no lo que mande el usuario
        monto = pedido['total']
        estado = "Pagado"

        # 3. Insertar pago
        cursor.execute("""
            INSERT INTO pagos (id_pedido, monto, metodo_pago, estado, fecha)
            VALUES (%s, %s, %s, %s, NOW())
        """, (id_pedido, monto, metodo, estado))
        id_pago = cursor.lastrowid

        # 4. Actualizar estado del pedido
        cursor.execute("""
            UPDATE pedidos SET estado = 'Pagado' WHERE id_pedido = %s
        """, (id_pedido,))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('pago_exito', id_pago=id_pago))

    cursor.close()
    conn.close()
    return render_template('pago_form.html', usuario=usuario, pedido=pedido)


# ----------------------------
# Confirmación de Pago
# ----------------------------
@app.route('/pago/<int:id_pago>/exito')
def pago_exito(id_pago):
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 3:
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
    if not usuario or usuario['id_rol'] != 3:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pa.*, pe.total, pe.fecha AS fecha_pedido
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
    if not usuario or usuario['id_rol'] != 3:  # Solo clientes
        return redirect(url_for('login'))

    carrito = session.get('carrito', [])
    if not carrito:
        return redirect(url_for('carrito'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Calcular total del pedido
    total_pedido = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)

    # 2. Insertamos el pedido con total
    cursor.execute("""
        INSERT INTO pedidos (id_usuario, fecha, estado, total)
        VALUES (%s, NOW(), 'Pendiente', %s)
    """, (usuario['id_usuario'], total_pedido))
    id_pedido = cursor.lastrowid

    # 3. Insertamos cada producto en la tabla detalle_pedido y descontamos stock
    for item in carrito:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_pedido, item['id_producto'], item['cantidad'], item['precio']))

        # Descontar stock del producto
        cursor.execute("""
            UPDATE productos SET stock = stock - %s WHERE id_producto = %s
        """, (item['cantidad'], item['id_producto']))

    conn.commit()
    cursor.close()
    conn.close()

    # Limpiamos el carrito
    session['carrito'] = []

    # Redirigir a la vista de pago
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

    motivo = request.form["motivo"]

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

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
