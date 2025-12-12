AVE Joyas – Sistema de Gestión Integral para Inventario, Ventas y Seguimiento de Pedidos

AVE Joyas es una aplicación web desarrollada con Flask y MySQL que ofrece una solución completa para la gestión de productos, control de inventario, procesamiento de pedidos, administración de usuarios, pagos y trazabilidad logística. El sistema está diseñado para joyerías o comercios que requieren una plataforma sólida que integre el flujo operativo completo: desde el registro del producto hasta la entrega final al cliente.

Este proyecto se centra en proporcionar eficiencia operativa, trazabilidad del proceso de venta, herramientas administrativas para el personal interno y una experiencia clara para los clientes en el proceso de compra y seguimiento de sus pedidos.

Descripción General del Sistema

El sistema abarca módulos esenciales para la administración de una tienda online de joyería:

Catálogo administrable de productos con atributos específicos.

Control de inventario con manejo por tallas.

Carrito de compras por usuario.

Generación automática de pedidos con número único y código de seguimiento.

Gestión de estados del pedido a lo largo de su ciclo de vida.

Registro de pagos y generación de facturas en PDF.

Panel de usuarios para clientes, vendedores y administradores.

Funcionalidades de rastreo accesibles únicamente para clientes con sesión activa.

La arquitectura organiza de forma clara las plantillas, los recursos estáticos y las utilidades del sistema. También incluye herramientas automatizadas para generar documentos como facturas y fichas técnicas mediante ReportLab.

Características Principales

2.1 Gestión de Productos
El sistema permite crear, editar y administrar productos con múltiples atributos:

Código único generado automáticamente.

Nombre, descripción, precio, peso y dimensiones.

Atributos configurables: tipo de joya, material, color y tipo de piedra.

Soporte para múltiples imágenes.

Control de stock general y stock por talla.

El módulo de registro de productos incluye validaciones, vista previa de imágenes y organización de archivos.

2.2 Proceso de Venta y Generación de Pedidos
El cliente puede añadir productos al carrito y confirmar la compra. Al crear un pedido:

Se genera un número de pedido único.

Se asigna el estado inicial correspondiente.

Se registran los detalles del pedido.

Se descuenta el stock disponible.

Se vacía el carrito del usuario.

Este proceso garantiza consistencia en el inventario y trazabilidad del pedido.

2.3 Gestión de Estados del Pedido
Los estados se administran mediante una tabla dedicada y permiten categorizar los pedidos según su progreso. Los estados incluyen: Pendiente de preparación, En preparación, Enviado, Entregado, Cancelado y Devuelto.

Cada pedido tiene un estado actual y un historial detallado de cambios para auditoría.

2.4 Registro de Pagos y Facturación
El sistema permite registrar pagos asociados a un pedido mediante distintos métodos, tales como efectivo, transferencia y tarjeta. Cuando el pago se registra:

Se actualiza el estado del pedido.

Se genera una factura en PDF que incluye logo, datos del cliente, detalle de productos, totales, impuestos y número de pedido.

La generación del documento se realiza mediante ReportLab.

2.5 Rastreo de Pedidos
Los clientes autenticados pueden consultar el estado actual de su pedido mediante su número de pedido o código de seguimiento. El sistema muestra:

Estado actual del pedido.

Detalles del pedido.

Historial completo de cambios.

Esto facilita la transparencia y reduce la necesidad de soporte.

Tecnologías Utilizadas

Backend:

Python 3.x

Flask

MySQL / MariaDB

ReportLab

Frontend:

HTML5

CSS3

Bootstrap

Jinja2

Otros:

Manejo de sesiones por roles

Subida y validación de imágenes

Módulo utilitario centralizado en utils.py

Estructura del Proyecto

/AVE
│── app.py (aplicación Flask)
│── utils.py (funciones auxiliares)
│── ave_joyas.sql (base de datos)
│── /templates (vistas HTML)
│── /static (css, imágenes, facturas, uploads)
└── README.md

Instalación y Configuración

Clonar el repositorio:
git clone https://github.com/USUARIO/AVE-Joyas.git

cd AVE-Joyas

Crear entorno virtual:
python -m venv venv
source venv/Scripts/activate

Instalar dependencias:
pip install -r requirements.txt

Importar base de datos:
mysql -u root -p < ave_joyas.sql

Configurar credenciales en app.py:
host, usuario, contraseña y nombre de base de datos.

Ejecutar la aplicación:
python app.py

Roles del Sistema y Acceso

Administrador: acceso completo a productos, usuarios y pedidos.
Vendedor: gestión de productos, estados y pagos.
Cliente: compras, pagos, facturas y seguimiento de pedidos.

