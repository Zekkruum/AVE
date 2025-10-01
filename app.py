from flask import Flask, request, redirect, url_for, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from utils import get_db_connection, enviar_correo, generar_token

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

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
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, i.url AS imagen
        FROM productos p
        LEFT JOIN imagenes i ON p.id_producto = i.id_producto
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
    return redirect(url_for('carrito'))

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

        enviar_correo(correo, token)
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
@app.route('/vendedor/producto/nuevo', methods=['GET', 'POST'])
def registrar_producto():
    usuario = obtener_usuario()
    if not usuario or usuario['id_rol'] != 2:  # Solo vendedores
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precio, stock, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, stock, usuario['id_usuario']))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('mis_productos'))

    return render_template('registrar_producto.html', usuario=usuario)



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
    if not usuario or usuario['id_rol'] != 3:  # Solo clientes pueden pagar
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🚨 IMPORTANTE: aquí supongo que tienes tabla pedidos con total
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id_pedido,))
    pedido = cursor.fetchone()

    if not pedido:
        cursor.close()
        conn.close()
        return "Pedido no encontrado", 404

    if request.method == 'POST':
        metodo = request.form['metodo']
        monto = float(request.form['monto'])
        estado = "Pagado"

        cursor.execute("""
            INSERT INTO pagos (id_pedido, monto, metodo, estado, fecha)
            VALUES (%s, %s, %s, %s, NOW())
        """, (id_pedido, monto, metodo, estado))
        conn.commit()
        id_pago = cursor.lastrowid

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

    # 🚨 IMPORTANTE: asumo que la tabla pedidos tiene id_usuario
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

    carrito = session.get('carrito', [])
    if not carrito:
        return redirect(url_for('carrito'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Insertamos el pedido
    cursor.execute("""
        INSERT INTO pedidos (id_usuario, fecha, estado)
        VALUES (%s, NOW(), 'Pendiente')
    """, (usuario['id_usuario'],))
    id_pedido = cursor.lastrowid

    # 2. Insertamos cada producto en la tabla detalle_pedido
    for item in carrito:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_pedido, item['id_producto'], item['cantidad'], item['precio']))

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
    if not usuario or usuario['id_rol'] != 1:
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
        observacion = request.form.get('observacion', '')

        # 1. Insertar en movimientos_inventario
        cursor.execute("""
            INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, observacion)
            VALUES (%s, 'entrada', %s, %s)
        """, (id_producto, cantidad, observacion))

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




# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
