-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-11-2025 a las 05:11:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ave_joyas`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_bitacora` (IN `p_id_log` INT, IN `p_accion` VARCHAR(100))   BEGIN
    UPDATE bitacora
    SET accion = p_accion
    WHERE id_log = p_id_log;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_cliente` (IN `p_id_cliente` INT, IN `p_id_usuario` INT)   BEGIN
    UPDATE clientes
    SET id_usuario = p_id_usuario
    WHERE id_cliente = p_id_cliente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_detalle_orden` (IN `p_id_detalle` INT, IN `p_cantidad` INT)   BEGIN
    UPDATE detalle_orden
    SET cantidad = p_cantidad
    WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_detalle_pedido` (IN `p_id_detalle` INT, IN `p_cantidad` INT)   BEGIN
    UPDATE detalle_pedido
    SET cantidad = p_cantidad
    WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_material` (IN `p_id_material` INT, IN `p_nombre_material` VARCHAR(100))   BEGIN
    UPDATE materiales
    SET nombre_material = p_nombre_material
    WHERE id_material = p_id_material;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_orden_compra` (IN `p_id_orden` INT, IN `p_estado` VARCHAR(50))   BEGIN
    UPDATE ordenes_compra
    SET estado = p_estado
    WHERE id_orden = p_id_orden;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_pedido` (IN `p_id_pedido` INT, IN `p_estado` VARCHAR(50))   BEGIN
    UPDATE pedidos
    SET estado = p_estado
    WHERE id_pedido = p_id_pedido;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_producto` (IN `p_id_producto` INT, IN `p_precio` DECIMAL(10,2))   BEGIN
    UPDATE productos
    SET precio = p_precio
    WHERE id_producto = p_id_producto;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_promocion` (IN `p_id_promocion` INT, IN `p_activa` BOOLEAN)   BEGIN
    UPDATE promociones
    SET activa = p_activa
    WHERE id_promocion = p_id_promocion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_proveedor` (IN `p_id_proveedor` INT, IN `p_telefono` VARCHAR(30))   BEGIN
    UPDATE proveedores
    SET telefono = p_telefono
    WHERE id_proveedor = p_id_proveedor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_talla` (IN `p_id_talla` INT, IN `p_nombre_talla` VARCHAR(50))   BEGIN
    UPDATE tallas
    SET nombre_talla = p_nombre_talla
    WHERE id_talla = p_id_talla;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_tipo_joya` (IN `p_id_tipo` INT, IN `p_nombre_tipo` VARCHAR(100))   BEGIN
    UPDATE tipos_joya
    SET nombre_tipo = p_nombre_tipo
    WHERE id_tipo = p_id_tipo;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_usuario` (IN `p_id_usuario` INT, IN `p_nombre_completo` VARCHAR(100))   BEGIN
    UPDATE usuarios
    SET nombre_completo = p_nombre_completo
    WHERE id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `buscar_productos_por_material` (IN `material_nombre` VARCHAR(100))   BEGIN
    SELECT p.id_producto, p.nombre, p.precio, m.nombre_material
    FROM productos p
    JOIN materiales m ON p.id_material = m.id_material
    WHERE m.nombre_material = material_nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `buscar_proveedor` (IN `termino` VARCHAR(100))   BEGIN
    SELECT id_proveedor, nombre, nit, telefono, correo
    FROM proveedores
    WHERE nombre LIKE CONCAT('%', termino, '%') OR nit LIKE CONCAT('%', termino, '%');
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `buscar_usuario_por_correo` (IN `correo_busqueda` VARCHAR(100))   BEGIN
    SELECT id_usuario, nombre_completo, correo, estado
    FROM usuarios
    WHERE correo = correo_busqueda;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_bitacora` (IN `p_id_log` INT)   BEGIN
    DELETE FROM bitacora WHERE id_log = p_id_log;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_cliente` (IN `p_id_cliente` INT)   BEGIN
    DELETE FROM clientes WHERE id_cliente = p_id_cliente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_detalle_orden` (IN `p_id_detalle` INT)   BEGIN
    DELETE FROM detalle_orden WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_detalle_pedido` (IN `p_id_detalle` INT)   BEGIN
    DELETE FROM detalle_pedido WHERE id_detalle = p_id_detalle;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_material` (IN `p_id_material` INT)   BEGIN
    DELETE FROM materiales WHERE id_material = p_id_material;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_orden_compra` (IN `p_id_orden` INT)   BEGIN
    DELETE FROM ordenes_compra WHERE id_orden = p_id_orden;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_pedido` (IN `p_id_pedido` INT)   BEGIN
    DELETE FROM pedidos WHERE id_pedido = p_id_pedido;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_producto` (IN `p_id_producto` INT)   BEGIN
    DELETE FROM productos WHERE id_producto = p_id_producto;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_producto_talla` (IN `p_id_producto` INT, IN `p_id_talla` INT)   BEGIN
    DELETE FROM producto_talla
    WHERE id_producto = p_id_producto AND id_talla = p_id_talla;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_promocion` (IN `p_id_promocion` INT)   BEGIN
    DELETE FROM promociones WHERE id_promocion = p_id_promocion;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_proveedor` (IN `p_id_proveedor` INT)   BEGIN
    DELETE FROM proveedores WHERE id_proveedor = p_id_proveedor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_talla` (IN `p_id_talla` INT)   BEGIN
    DELETE FROM tallas WHERE id_talla = p_id_talla;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_tipo_joya` (IN `p_id_tipo` INT)   BEGIN
    DELETE FROM tipos_joya WHERE id_tipo = p_id_tipo;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_usuario` (IN `p_id_usuario` INT)   BEGIN
    DELETE FROM usuarios WHERE id_usuario = p_id_usuario;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_bitacora` (IN `p_id_usuario` INT, IN `p_accion` VARCHAR(100), IN `p_modulo` VARCHAR(100), IN `p_fecha` DATETIME)   BEGIN
    INSERT INTO bitacora (id_usuario, accion, modulo, fecha)
    VALUES (p_id_usuario, p_accion, p_modulo, p_fecha);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_cliente` (IN `p_id_usuario` INT)   BEGIN
    INSERT INTO clientes (id_usuario)
    VALUES (p_id_usuario);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_detalle_orden` (IN `p_id_orden` INT, IN `p_producto_descripcion` TEXT, IN `p_cantidad` INT, IN `p_precio_unitario` DECIMAL(10,2))   BEGIN
    INSERT INTO detalle_orden (id_orden, producto_descripcion, cantidad, precio_unitario)
    VALUES (p_id_orden, p_producto_descripcion, p_cantidad, p_precio_unitario);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_detalle_pedido` (IN `p_id_pedido` INT, IN `p_id_producto` INT, IN `p_id_talla` INT, IN `p_cantidad` INT, IN `p_precio_unitario` DECIMAL(10,2))   BEGIN
    INSERT INTO detalle_pedido (id_pedido, id_producto, id_talla, cantidad, precio_unitario)
    VALUES (p_id_pedido, p_id_producto, p_id_talla, p_cantidad, p_precio_unitario);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_material` (IN `p_nombre_material` VARCHAR(100))   BEGIN
    INSERT INTO materiales (nombre_material)
    VALUES (p_nombre_material);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_orden_compra` (IN `p_id_proveedor` INT, IN `p_fecha` DATE, IN `p_estado` VARCHAR(50), IN `p_observaciones` TEXT)   BEGIN
    INSERT INTO ordenes_compra (id_proveedor, fecha, estado, observaciones)
    VALUES (p_id_proveedor, p_fecha, p_estado, p_observaciones);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_pedido` (IN `p_id_cliente` INT, IN `p_fecha` DATE, IN `p_estado` VARCHAR(50), IN `p_metodo_envio` VARCHAR(100), IN `p_metodo_pago` VARCHAR(100), IN `p_total` DECIMAL(10,2))   BEGIN
    INSERT INTO pedidos (id_cliente, fecha, estado, metodo_envio, metodo_pago, total)
    VALUES (p_id_cliente, p_fecha, p_estado, p_metodo_envio, p_metodo_pago, p_total);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_producto` (IN `p_nombre` VARCHAR(100), IN `p_descripcion` TEXT, IN `p_precio` DECIMAL(10,2), IN `p_stock` INT, IN `p_referencia` VARCHAR(100), IN `p_id_tipo` INT, IN `p_id_material` INT)   BEGIN
    INSERT INTO productos (nombre, descripcion, precio, stock, referencia, id_tipo, id_material)
    VALUES (p_nombre, p_descripcion, p_precio, p_stock, p_referencia, p_id_tipo, p_id_material);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_producto_talla` (IN `p_id_producto` INT, IN `p_id_talla` INT)   BEGIN
    INSERT INTO producto_talla (id_producto, id_talla)
    VALUES (p_id_producto, p_id_talla);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_promocion` (IN `p_titulo` VARCHAR(100), IN `p_descripcion` TEXT, IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE, IN `p_activa` BOOLEAN)   BEGIN
    INSERT INTO promociones (titulo, descripcion, fecha_inicio, fecha_fin, activa)
    VALUES (p_titulo, p_descripcion, p_fecha_inicio, p_fecha_fin, p_activa);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_proveedor` (IN `p_nombre` VARCHAR(100), IN `p_nit` VARCHAR(50), IN `p_telefono` VARCHAR(30), IN `p_correo` VARCHAR(100), IN `p_direccion` TEXT)   BEGIN
    INSERT INTO proveedores (nombre, nit, telefono, correo, direccion)
    VALUES (p_nombre, p_nit, p_telefono, p_correo, p_direccion);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_talla` (IN `p_nombre_talla` VARCHAR(50))   BEGIN
    INSERT INTO tallas (nombre_talla)
    VALUES (p_nombre_talla);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_tipo_joya` (IN `p_nombre_tipo` VARCHAR(100))   BEGIN
    INSERT INTO tipos_joya (nombre_tipo)
    VALUES (p_nombre_tipo);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_usuario` (IN `p_nombre_completo` VARCHAR(100), IN `p_correo` VARCHAR(100), IN `p_telefono` VARCHAR(30), IN `p_direccion` TEXT, IN `p_contrasena` VARCHAR(100), IN `p_estado` BOOLEAN, IN `p_id_rol` INT)   BEGIN
    INSERT INTO usuarios (nombre_completo, correo, telefono_contacto, direccion, contrasena, estado, id_rol)
    VALUES (p_nombre_completo, p_correo, p_telefono, p_direccion, p_contrasena, p_estado, p_id_rol);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `pedidos_por_cliente` (IN `cliente_id` INT)   BEGIN
    SELECT id_pedido, fecha, estado, total
    FROM pedidos
    WHERE id_cliente = cliente_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `productos_por_rango_precio` (IN `precio_min` DECIMAL(10,2), IN `precio_max` DECIMAL(10,2))   BEGIN
    SELECT id_producto, nombre, precio
    FROM productos
    WHERE precio BETWEEN precio_min AND precio_max;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_bitacora` ()   BEGIN
    SELECT id_log, id_usuario, accion, modulo, fecha
    FROM bitacora;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_pedidos` ()   BEGIN
    SELECT id_pedido, id_cliente, fecha, estado, metodo_envio, metodo_pago, total
    FROM pedidos;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_productos` ()   BEGIN
    SELECT id_producto, nombre, descripcion, precio, stock, referencia
    FROM productos;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_proveedores` ()   BEGIN
    SELECT id_proveedor, nombre, nit, telefono, correo, direccion
    FROM proveedores;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_usuarios` ()   BEGIN
    SELECT id_usuario, nombre_completo, correo, telefono_contacto, direccion, estado, id_rol
    FROM usuarios;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bitacora`
--

CREATE TABLE `bitacora` (
  `id_log` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `accion` varchar(100) DEFAULT NULL,
  `modulo` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bitacora`
--

INSERT INTO `bitacora` (`id_log`, `id_usuario`, `accion`, `modulo`, `fecha`) VALUES
(1, 1, 'Cre? nuevo usuario', 'usuarios', '2024-05-01 09:00:00'),
(2, 2, 'Edit? producto', 'productos', '2024-05-02 10:15:00'),
(3, 3, 'Registr? venta', 'pedidos', '2024-05-03 11:30:00'),
(4, 4, 'Gener? reporte de ventas', 'reportes', '2024-05-04 12:45:00'),
(5, 5, 'Aprob? devoluci?n', 'devoluciones', '2024-05-05 14:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_usuario`
--

CREATE TABLE `carrito_usuario` (
  `id_carrito` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carrito_usuario`
--

INSERT INTO `carrito_usuario` (`id_carrito`, `id_usuario`, `id_producto`, `cantidad`, `fecha`) VALUES
(27, 28, 61, 1, '2025-11-14 03:58:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `id_usuario`) VALUES
(5, 1),
(4, 2),
(1, 3),
(2, 4),
(3, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colores`
--

CREATE TABLE `colores` (
  `id_color` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `colores`
--

INSERT INTO `colores` (`id_color`, `nombre`) VALUES
(1, 'Oro Amarillo'),
(2, 'Oro Blanco'),
(3, 'Oro Rosa'),
(4, 'Plata'),
(5, 'Negro Mate'),
(6, 'Bronce'),
(7, 'Azul Marino'),
(8, 'Verde Esmeralda'),
(9, 'Rojo Rubí'),
(10, 'Rosa Pastel'),
(11, 'Transparente'),
(12, 'Blanco Perlado'),
(13, 'Gris Titanio'),
(14, 'Champaña'),
(15, 'Cobre Pulido');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `costos_envio`
--

CREATE TABLE `costos_envio` (
  `id_costo` int(11) NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `costo_base` decimal(10,2) DEFAULT NULL,
  `costo_por_kg` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_orden`
--

CREATE TABLE `detalle_orden` (
  `id_detalle` int(11) NOT NULL,
  `id_orden` int(11) DEFAULT NULL,
  `producto_descripcion` text DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_orden`
--

INSERT INTO `detalle_orden` (`id_detalle`, `id_orden`, `producto_descripcion`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 'Lote de oro 18k - 50 piezas', 50, 500000.00),
(2, 1, 'Lote de plata ley 925 - 100 piezas', 100, 250000.00),
(3, 2, 'Bobinas de acero inoxidable - 200m', 200, 10000.00),
(4, 3, 'Cuentas de piedra natural - 500 unidades', 500, 2000.00),
(5, 5, 'Material ecol?gico en rollos - 300m', 300, 1500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id_detalle` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `id_talla` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones`
--

CREATE TABLE `devoluciones` (
  `id_devolucion` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `motivo` text DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'Pendiente',
  `estado_fisico` varchar(20) NOT NULL DEFAULT 'bueno'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `faq`
--

CREATE TABLE `faq` (
  `id_faq` int(11) NOT NULL,
  `pregunta` varchar(255) DEFAULT NULL,
  `respuesta` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `faq`
--

INSERT INTO `faq` (`id_faq`, `pregunta`, `respuesta`, `fecha_creacion`) VALUES
(1, '¿Cuánto tarda el envío?', 'El envío tarda entre 3 y 5 días hábiles.', '2025-11-11 02:25:14'),
(2, '¿Puedo devolver un producto?', 'Sí, tienes 15 días para devolver productos no personalizados.', '2025-11-11 02:25:14'),
(3, '¿Aceptan pagos con tarjeta?', 'Sí, aceptamos todas las tarjetas principales y PayPal.', '2025-11-11 02:25:14');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes`
--

CREATE TABLE `imagenes` (
  `id_imagen` int(11) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imagenes`
--

INSERT INTO `imagenes` (`id_imagen`, `id_producto`, `url`) VALUES
(7, 72, 'uploads/eff2c23522fb46b88f218dbae9a23265_7a56dffb03c74ffe92a4a85f2ec16e83_sg-11134201-7qvg4-liijuezgbfnx54.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidencias_entrega`
--

CREATE TABLE `incidencias_entrega` (
  `id_incidencia` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiales`
--

CREATE TABLE `materiales` (
  `id_material` int(11) NOT NULL,
  `nombre_material` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materiales`
--

INSERT INTO `materiales` (`id_material`, `nombre_material`) VALUES
(1, 'Oro'),
(2, 'Plata'),
(3, 'Acero inoxidable'),
(4, 'Piedra preciosa'),
(5, 'Material sostenible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_inventario`
--

CREATE TABLE `movimientos_inventario` (
  `id_movimiento` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `tipo` enum('entrada','salida') NOT NULL,
  `cantidad` int(11) NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes_compra`
--

CREATE TABLE `ordenes_compra` (
  `id_orden` int(11) NOT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `estado` varchar(30) DEFAULT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ordenes_compra`
--

INSERT INTO `ordenes_compra` (`id_orden`, `id_proveedor`, `fecha`, `estado`, `observaciones`) VALUES
(1, 1, '2024-05-01', 'Completado', 'Compra inicial de oro y plata'),
(2, 2, '2024-05-03', 'Pendiente', 'Orden de acero inoxidable'),
(3, 3, '2024-05-05', 'Completado', 'Materiales para pulseras'),
(4, 4, '2024-05-07', 'Cancelado', 'Retraso en entrega de piedras'),
(5, 5, '2024-05-09', 'Pendiente', 'Pedido de materiales sostenibles');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `estado` varchar(30) DEFAULT 'Pendiente',
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `referencia_pago` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_pedido`, `metodo_pago`, `monto`, `estado`, `fecha`, `referencia_pago`) VALUES
(1, 7, '', 95000.00, 'Pagado', '2025-09-16 00:36:29', NULL),
(2, 13, 'Efectivo', 98000.00, 'Pagado', '2025-10-01 22:48:24', NULL),
(3, 14, 'Transferencia', 98000.00, 'Pagado', '2025-10-01 22:48:52', NULL),
(4, 15, 'Tarjeta', 98000.00, 'Pagado', '2025-10-01 22:54:56', NULL),
(5, 16, 'efectivo', 470000.00, 'Pagado', '2025-10-01 23:07:51', NULL),
(6, 19, 'efectivo', 470000.00, 'Pagado', '2025-10-01 23:27:15', NULL),
(7, 20, 'transferencia', 95000.00, 'Pagado', '2025-10-02 02:15:22', NULL),
(8, 21, 'tarjeta', 90000.00, 'Pagado', '2025-10-02 03:54:36', NULL),
(9, 22, 'tarjeta', 95000.00, 'Pagado', '2025-10-02 03:54:51', NULL),
(10, 23, 'tarjeta', 720000.00, 'Pagado', '2025-10-02 13:20:36', NULL),
(11, 24, 'transferencia', 116620.00, 'Pagado', '2025-10-02 15:56:34', NULL),
(12, 25, 'contraentrega', 116620.00, 'Pagado', '2025-10-02 16:01:01', NULL),
(13, 26, 'tarjeta', 142800.00, 'Pagado', '2025-10-02 16:16:09', NULL),
(14, 27, 'tarjeta', 249900.00, 'Pagado', '2025-10-02 16:31:39', NULL),
(15, 28, 'tarjeta', 815150.00, 'Pagado', '2025-10-02 16:32:20', NULL),
(16, 32, 'tarjeta', 559300.00, 'Pagado', '2025-10-03 17:34:15', NULL),
(17, 32, 'tarjeta', 559300.00, 'Pagado', '2025-10-03 17:34:35', NULL),
(18, 33, 'tarjeta', 559300.00, 'Pagado', '2025-10-03 17:50:08', NULL),
(19, 39, 'tarjeta', 416500.00, 'Pagado', '2025-11-11 07:08:00', NULL),
(20, 40, 'tarjeta', 95200.00, 'Pagado', '2025-11-11 07:17:22', NULL),
(21, 41, 'tarjeta', 95200.00, 'Pagado', '2025-11-11 07:35:52', NULL);

--
-- Disparadores `pagos`
--
DELIMITER $$
CREATE TRIGGER `actualizar_estado_pedido` AFTER INSERT ON `pagos` FOR EACH ROW BEGIN
    UPDATE pedidos SET estado = 'Pagado'
    WHERE id_pedido = NEW.id_pedido;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `estado` varchar(30) DEFAULT NULL,
  `metodo_envio` varchar(50) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `estado_pago` enum('pendiente','pagado','cancelado') DEFAULT 'pendiente',
  `id_usuario` int(11) DEFAULT NULL,
  `subtotal` decimal(10,2) NOT NULL DEFAULT 0.00,
  `impuesto` decimal(10,2) NOT NULL DEFAULT 0.00,
  `codigo_seguimiento` varchar(50) DEFAULT NULL,
  `nombre_cliente` varchar(120) NOT NULL,
  `direccion_entrega` varchar(255) NOT NULL,
  `telefono_cliente` varchar(30) NOT NULL,
  `correo_cliente` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_cliente`, `fecha`, `estado`, `metodo_envio`, `metodo_pago`, `total`, `estado_pago`, `id_usuario`, `subtotal`, `impuesto`, `codigo_seguimiento`, `nombre_cliente`, `direccion_entrega`, `telefono_cliente`, `correo_cliente`) VALUES
(1, 1, '2024-06-01', 'Enviado', 'Mensajer?a', 'Tarjeta', 350000.00, 'pendiente', NULL, 0.00, 0.00, NULL, '', '', '', ''),
(2, 2, '2024-06-02', 'Preparando', 'Contra entrega', 'Efectivo', 120000.00, 'pendiente', NULL, 0.00, 0.00, NULL, '', '', '', ''),
(3, 3, '2024-06-03', 'Entregado', 'Mensajer?a', 'Nequi', 95000.00, 'pendiente', NULL, 0.00, 0.00, NULL, '', '', '', ''),
(4, 4, '2024-06-04', 'Enviado', 'Domicilio', 'Tarjeta', 470000.00, 'pendiente', NULL, 0.00, 0.00, NULL, '', '', '', ''),
(5, 5, '2024-06-05', 'Pendiente', 'Mensajer?a', 'Transferencia', 80000.00, 'pendiente', NULL, 0.00, 0.00, NULL, '', '', '', ''),
(6, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 11, 0.00, 0.00, NULL, '', '', '', ''),
(7, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 11, 0.00, 0.00, NULL, '', '', '', ''),
(8, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23, 0.00, 0.00, NULL, '', '', '', ''),
(9, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23, 0.00, 0.00, NULL, '', '', '', ''),
(10, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23, 0.00, 0.00, NULL, '', '', '', ''),
(11, NULL, '2025-09-16', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23, 0.00, 0.00, NULL, '', '', '', ''),
(12, NULL, '2025-10-01', 'Pendiente', NULL, NULL, NULL, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(13, NULL, '2025-10-01', 'Pagado', NULL, NULL, 98000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(14, NULL, '2025-10-01', 'Pagado', NULL, NULL, 98000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(15, NULL, '2025-10-01', 'Pagado', NULL, NULL, 98000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(16, NULL, '2025-10-01', 'Pagado', NULL, NULL, 470000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(17, NULL, '2025-10-01', 'Pendiente', NULL, NULL, 80000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(18, NULL, '2025-10-01', 'Pendiente', NULL, NULL, 120000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(19, NULL, '2025-10-01', 'Pagado', NULL, NULL, 470000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(20, NULL, '2025-10-02', 'Pagado', NULL, NULL, 95000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(21, NULL, '2025-10-02', 'Pagado', NULL, NULL, 90000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(22, NULL, '2025-10-02', 'Pagado', NULL, NULL, 95000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(23, NULL, '2025-10-02', 'Pagado', NULL, NULL, 720000.00, 'pendiente', 25, 0.00, 0.00, NULL, '', '', '', ''),
(24, NULL, '2025-10-02', 'Pendiente', NULL, NULL, 116620.00, 'pendiente', 25, 98000.00, 18620.00, NULL, '', '', '', ''),
(25, NULL, '2025-10-02', 'Pendiente', NULL, NULL, 116620.00, 'pendiente', 25, 98000.00, 18620.00, NULL, '', '', '', ''),
(26, NULL, '2025-10-02', 'Pendiente', NULL, NULL, 142800.00, 'pendiente', 24, 120000.00, 22800.00, NULL, '', '', '', ''),
(27, NULL, '2025-10-02', 'Pendiente', NULL, NULL, 249900.00, 'pendiente', 25, 210000.00, 39900.00, NULL, '', '', '', ''),
(28, NULL, '2025-10-02', 'Pendiente', NULL, NULL, 815150.00, 'pendiente', 25, 685000.00, 130150.00, NULL, '', '', '', ''),
(29, NULL, '2025-10-03', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 16, 470000.00, 89300.00, NULL, '', '', '', ''),
(30, NULL, '2025-10-03', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 16, 470000.00, 89300.00, NULL, '', '', '', ''),
(31, NULL, '2025-10-03', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 16, 470000.00, 89300.00, NULL, '', '', '', ''),
(32, NULL, '2025-10-03', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 16, 470000.00, 89300.00, NULL, '', '', '', ''),
(33, NULL, '2025-10-03', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 16, 470000.00, 89300.00, NULL, '', '', '', ''),
(34, NULL, '2025-11-11', 'Pendiente', NULL, NULL, 559300.00, 'pendiente', 29, 470000.00, 89300.00, NULL, '', '', '', ''),
(35, NULL, '2025-11-11', 'Pendiente', NULL, NULL, 142800.00, 'pendiente', 29, 120000.00, 22800.00, NULL, '', '', '', ''),
(36, NULL, '2025-11-11', 'Pendiente', NULL, NULL, 1886150.00, 'pendiente', 29, 1585000.00, 301150.00, NULL, '', '', '', ''),
(37, NULL, '2025-11-11', 'Pendiente', NULL, NULL, 95200.00, 'pendiente', 29, 80000.00, 15200.00, NULL, '', '', '', ''),
(38, NULL, '2025-11-11', 'Pendiente', NULL, NULL, 142800.00, 'pendiente', 29, 120000.00, 22800.00, NULL, '', '', '', ''),
(39, NULL, '2025-11-11', 'Pagado', NULL, NULL, 416500.00, 'pendiente', 29, 350000.00, 66500.00, NULL, '', '', '', ''),
(40, NULL, '2025-11-11', 'Pagado', NULL, NULL, 95200.00, 'pendiente', 29, 80000.00, 15200.00, NULL, '', '', '', ''),
(41, NULL, '2025-11-11', 'Pagado', NULL, NULL, 95200.00, 'pendiente', 29, 80000.00, 15200.00, NULL, '', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos_personalizados`
--

CREATE TABLE `pedidos_personalizados` (
  `id_pedido_personalizado` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_vendedor` int(11) NOT NULL,
  `tipo_producto` varchar(100) NOT NULL,
  `materiales` text NOT NULL,
  `diseno` text NOT NULL,
  `presupuesto` decimal(10,2) NOT NULL,
  `archivo` varchar(255) DEFAULT NULL,
  `estado` varchar(30) DEFAULT 'Pendiente',
  `motivo_rechazo` text DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  `fecha_entrega_estimada` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos_personalizados`
--

INSERT INTO `pedidos_personalizados` (`id_pedido_personalizado`, `id_usuario`, `id_vendedor`, `tipo_producto`, `materiales`, `diseno`, `presupuesto`, `archivo`, `estado`, `motivo_rechazo`, `fecha`, `fecha_entrega_estimada`) VALUES
(1, 25, 24, 'Manilla', 'Oro', 'Quiero que la manilla tenga un colgante con el personaje de Hornet del videojuego titulado Hollow Knight Silksong', 120000.00, 'Hornet_Idle.jpg', 'Rechazado', 'NMMS WE MUY DIFICIL WE', '2025-10-02 00:51:44', NULL),
(2, 25, 24, 'Manilla', 'Oro', 'Quiero que esta manilla tenga un adorno con la figura de Hornet del videojuego titulado Hollow Knight Silksong', 120000.00, 'Hornet_Idle.jpg', 'Aceptado', NULL, '2025-10-02 01:11:34', NULL),
(3, 25, 24, 'Manilla', 'Oro', 'Quiero que esta manilla tenga un adorno con la figura de Hornet del videojuego titulado Hollow Knight Silksong', 120000.00, 'Hornet_Idle.jpg', 'Aceptado', NULL, '2025-10-02 01:21:05', '2025-10-17'),
(4, 25, 24, 'Collar', 'Plata y un dije', 'Quiero que este collar sea algo unico pero sin ser algo tan llamativo, lo quiero algo delgado y que el dije sea un nombre algo similar a la imagen adjunta', 90000.00, 'DNP-06.jpg', 'Rechazado', 'eso no fue muy so so 🗣️', '2025-10-02 01:44:49', NULL),
(5, 25, 24, 'Manilla', 'plata', 'Quiero que esta manilla sea sencilla pero con un nombre en el centro de ella, el nombre tiene que ser niyireth', 80000.00, 'ejemplo.jpg', 'Rechazado', 'Bro, no tengo manos XD', '2025-10-02 01:59:52', NULL),
(6, 25, 24, 'Cadena', 'Acero', 'Quiero que esta cadena tenga un estilo vikingo/nordico', 100000.00, '71kXKyBRLlL._UF8941000_QL80_.jpg', 'Aceptado', NULL, '2025-10-02 02:03:51', '2025-10-09'),
(7, 25, 23, 'Seas Mamon', 'Mineral Palido 🗣️', 'Para entender la historia de Five Nights at Freddy\'s hay que olvidarse que estos son juegos y quiero que tomen realmente a esta saga como lo que es. ¿Terror? Sí, pero sobre todo, ciencia ficción. Antes de comenzar, quiero decir que esta cronología la realizamos entre 3 youtubers conocidos de Five Nights at Freddy\'s y yo. Por lo tanto, agradecería que si les gusta el contenido de este juego vayan a visitar sus canales. Ahora sí, empecemos. ¿Qué pasaría si dos amigos se abren una pizzería? Esa es la primera pregunta que hay que plantearnos. Lo normal sería que todo vaya medianamente bien con algún tipo de problemas, pero nada saldría más allá de eso. La pregunta cambia completamente si nos preguntamos ¿Qué pasaría si Henry y William abren una pizzería? ¿Quienes son estos personajes? En un principio, grandes amigos. Henry, por un lado, era un ferviente y talentoso mecánico que cuidaba a su única hija, Charlie. No sabemos nada de su esposa, ni siquiera si tiene a alguien más en su familia. Y por el otro lado, William Afton. La familia de Afton estaba compuesta por 5 miembros. William, una persona con mucho dinero y con buena capacidad para la mecánica. Su hija menor, Elizabeth. Este pendejo que no sabemos el nombre, pero llora todo el tiempo, así que vamos a ponerle Crying Child. Michael Afton, su hijo mayor y su esposa, de quien no se sabe nada. Estos dos personajes unieron sus capacidades de mecánicos y con el buen capital que tenía William ahorrado, entre los dos abrieron un restaurante. Así fue como entre los años 1980 a 1982, supuestamente, Fredbear Family Dinner abrió sus puertas. La principal atracción de este lugar eran los animatrónicos. ¿Que Son? Bueno, básicamente eran robots que podrían ser controlados tanto por ellos mismos como por personas o por almas. Estos animatrónicos habían sido desarrollados por los dueños del restaurante, pero Henry destacó un poco más debido a que hizo un complejo sistema de recursos que permitía a la persona usar estos trajes. Solamente que tenía que ser extremadamente cuidadosa, ya que de lo contrario el mecanismo del mismo se activaría y la persona que esté dentro seguramente quedaría lastimada. Estos trajes híbridos darían a luz en un principio a su principal éxito, Fredbear y Spring Bonnie. Dos animatrónicos que durante esos años 80 habían hecho furor y tan bien les estaba yendo a estos dos amigos que la competencia empezó a llegar. Y es por eso que a unos pocos meses de la salida de Fredbear Family Dinner llegaría su competencia, Fazbear Entertainment, pero que esta no sería relevante hasta en un futuro. En paralelo a estos hechos, empezaban a haber roces entre la dupla principal, ya que William no solamente había abierto el restaurante para comer, sino que detrás de sus intenciones de matar había algo mucho más oscuro, gente. Es por eso que en una fecha que desconocemos, William creó un nuevo local, Circus Baby Pizza World, y es en este donde presentaría sus nuevos animatrónicos, los Funtime. Estos animatrónicos estarían hechos bajo la empresa Afton Robotics, que como podrán imaginar, esta empresa era de William. Aunque los Funtime no eran animatrónicos normales, si tenían buenas características muy innovadoras con respecto a los primeros trajes híbridos, estos Funtime estarían creados específicamente para matar. Una inteligencia artificial muy avanzada, poder abrir diferentes partes de su cuerpo y la posibilidad de hablar. Claramente no tenían una buena intención, pero a William se le volvería todo en contra cuando el mismo día de la inauguración de su local, a pesar de sus advertencias a Elizabeth, esta entró igual al cuarto donde estaban los animatrónicos para ver si estaba su robot. favorito, bebé. Y luego de que este animatrónico le ofrece un helado para hacer que se acercara a ella, la mata. O bueno, no tanto. Mientras a todo esto, recordamos que William pensaba que ya todos los niños estaban capturados dentro de los animatrónicos, debido a que la apertura de su local había sido completamente exitosa. Entonces alerta a toda la gente de una fuga de gas para que así tengan que evacuar el local y él poder ir a ver su recompensa. Cuando William va a ver si sus animatrónicos habían capturado niños, sí, así es, habían capturado niños. Que eso lo sabemos debido a que en los planos de los animatrónicos aparecen cuerpos dentro de estos robots. Pero también William se daría cuenta de que su animatrónico principal había matado a Elizabeth. O en realidad, su hija estaba tomando el control de Baby debido a que los ojos del animatrónico pasarían de ser azules a como los tenía su hijita, verdes. Por supuesto que William al enterarse de todo esto no sabe qué hacer y es por eso que decide encerrarla en Circus Baby Entertainment, un lugar ubicado debajo de Circus Baby. Tras el cierre de Circus Baby y la incertidumbre de lo ocurrido con su hija menor, estas cosas empezarían a afectar a William Afton, dando comienzo a su declive. Por eso, luego del fracaso de Circus Baby, éste vuelve a pedirle ayuda y trabajo a Henry, que a pesar de todos los problemas que había tenido con su anterior socio, le da trabajo de administrador o mecánico, por eso se lo puede ver colocándole. la cabeza de Fredbear a uno de los empleados de Fredbear Family Dinner. Durante estos meses, de un año que suponemos que es 1883, Henry creó y anunció otros animatrónicos por la televisión, que serían Freddy, Foxy, Chica y Bonnie. Por supuesto que William, al ver que había creado más animatrónicos, crecería la tensión con su nuevo jefe, pero lo que realmente llevaría a William a ponerse de un tono violeta sería la muerte de su hijo menor, el pendejo que llora, Crying Child. . ¿Se acuerdan de Mike, el hijo mayor de William? Bueno, este personaje asustaba de manera sobre medida a Crying Child y mientras ésta atormentaba a su único hermano chico, William protegía de sobre manera a su hijo menor, poniendo cámaras por toda la casa y dándole un peluche creado por él mismo para que pueda hablarle y sentirse cómodo. Todo esto, a pesar del comportamiento psicópata de William, serviría para vigilar a su hijo menor y así que no se escapara a ver a los animatrónicos debido a que a Crying Child le fascinaban. Pero William, al haber creado con Henry los dos primeros trajes sabían lo que podían hacer y lo danino que eran, por eso las medidas de sobreprotección. Pero ahora vamos a remontarnos a una teoría entre Five Nights at Freddy\'s 4 y The Twisted Ones, el primer libro. Supuestamente, Five Nights at Freddy\'s 4 ocurriría en las pesadillas de Crying Child, pero la verdad es que no, las pesadillas esas que ve son reales y no un mal sueño de este niño, ya que son parte de un plan muy macabro de su padre. . Verán, en la novela de The Twisted Ones, William crea un disco que hace tener alucinaciones con animatrónicos, exagerando su forma, su tamaño, etc. Algo así como la película de Batman donde el espantapájaros tiene un spray que te hace sobredimensionar tus miedos. ¿Y cómo se relaciona esto con el juego? El tema de las alucinaciones, no Batman, no tiene nada que ver Batman acá. Bueno, tenemos que remontarnos a Five Nights at Freddy\'s Ultimate Custom Night, en donde los animatrónicos Nightmares aparecen en este juego, pero en este juego controlamos a William, entonces es imposible que William logre saber con exactitud cómo son estos animatrónicos si es que en realidad son las pesadillas de su hijo menor. En otras palabras, ¿cómo sabes exactamente las pesadillas de otras personas? Con lo cual, si volvemos al primer libro, nos presentamos que William creó discos ilusorios para hacer creer a la gente cosas que realmente no hay, y esto lo utilizaría con Crying Child para hacer que se aleje definitivamente de los animatrónicos. Por eso es que tampoco nunca lo vemos regañar a su hijo mayor por maltratar a su hermanito, debido a que este le estaba generando un trauma con los animatrónicos, cosa que a William le sirvió, aunque el error de William fue confiar demasiado en Michael, porque este no sabía dónde estaba el límite de la broma, ya que Mike asustaba a su hermano solamente por diversión, y el problema se desataría en ese año 83, en el lugar donde había comenzado y terminado todo, Fredbear Family Dinner. Mike y sus amigos llevan a Crying Child por la fuerza al restaurante para seguir molestándolos con los animatrónicos en el día de su cumpleaños, y siguiendo con la broma, lo ponen en la boca de Fredbear simulando que se lo iba a comer, y desgraciadamente no. solo simulo eso. Como había dicho en un principio, el sistema de recurso de Henry era sensato, por lo que al introducir un niño dentro de la boca, el traje se cerró en la cabeza de Crying Child, que luego de eso, el mini Afton entra en un estado de coma donde están todos los animatrónicos que él conoció y el peluche que le había regalado William, donde en esta pantalla se da a entender como que su padre le está dedicando las últimas palabras a su hijo, pidiéndole que lo perdone, y diciendo dos frases que quedarían para muchísimas teorías. Vos estás roto, yo te reconstruiré. Por supuesto que esto lo dice debido a que a partir de la muerte de Elizabeth, él sabía que de alguna forma los animatrónicos lograban tomar el alma de la persona y adaptarla a su cuerpo, o por lo menos ahí alma y animatrónico convivían en un solo. cuerpo. Una curiosidad de esta parte de la historia es que como estamos en 1983, si recorremos la casa de los Afton, nos vamos a encontrar con un cuarto que da a entender que es de una niña, y quién era la única niña que tenía la familia. Afton, Elizabeth Afton. Por lo tanto, antes de ese 1983, la hija de William ya estaba dentro del cuerpo de Baby.', 1.00, 'Troleador_cara.jpg', 'Pendiente', NULL, '2025-10-02 02:08:27', NULL),
(8, 25, 15, 'Seas Mamon', 'Mineral Palido 🗣️', 'Para entender la historia de Five Nights at Freddy\'s hay que olvidarse que estos son juegos y quiero que tomen realmente a esta saga como lo que es. ¿Terror? Sí, pero sobre todo, ciencia ficción. Antes de comenzar, quiero decir que esta cronología la realizamos entre 3 youtubers conocidos de Five Nights at Freddy\'s y yo. Por lo tanto, agradecería que si les gusta el contenido de este juego vayan a visitar sus canales. Ahora sí, empecemos. ¿Qué pasaría si dos amigos se abren una pizzería? Esa es la primera pregunta que hay que plantearnos. Lo normal sería que todo vaya medianamente bien con algún tipo de problemas, pero nada saldría más allá de eso. La pregunta cambia completamente si nos preguntamos ¿Qué pasaría si Henry y William abren una pizzería? ¿Quienes son estos personajes? En un principio, grandes amigos. Henry, por un lado, era un ferviente y talentoso mecánico que cuidaba a su única hija, Charlie. No sabemos nada de su esposa, ni siquiera si tiene a alguien más en su familia. Y por el otro lado, William Afton. La familia de Afton estaba compuesta por 5 miembros. William, una persona con mucho dinero y con buena capacidad para la mecánica. Su hija menor, Elizabeth. Este pendejo que no sabemos el nombre, pero llora todo el tiempo, así que vamos a ponerle Crying Child. Michael Afton, su hijo mayor y su esposa, de quien no se sabe nada. Estos dos personajes unieron sus capacidades de mecánicos y con el buen capital que tenía William ahorrado, entre los dos abrieron un restaurante. Así fue como entre los años 1980 a 1982, supuestamente, Fredbear Family Dinner abrió sus puertas. La principal atracción de este lugar eran los animatrónicos. ¿Que Son? Bueno, básicamente eran robots que podrían ser controlados tanto por ellos mismos como por personas o por almas. Estos animatrónicos habían sido desarrollados por los dueños del restaurante, pero Henry destacó un poco más debido a que hizo un complejo sistema de recursos que permitía a la persona usar estos trajes. Solamente que tenía que ser extremadamente cuidadosa, ya que de lo contrario el mecanismo del mismo se activaría y la persona que esté dentro seguramente quedaría lastimada. Estos trajes híbridos darían a luz en un principio a su principal éxito, Fredbear y Spring Bonnie. Dos animatrónicos que durante esos años 80 habían hecho furor y tan bien les estaba yendo a estos dos amigos que la competencia empezó a llegar. Y es por eso que a unos pocos meses de la salida de Fredbear Family Dinner llegaría su competencia, Fazbear Entertainment, pero que esta no sería relevante hasta en un futuro. En paralelo a estos hechos, empezaban a haber roces entre la dupla principal, ya que William no solamente había abierto el restaurante para comer, sino que detrás de sus intenciones de matar había algo mucho más oscuro, gente. Es por eso que en una fecha que desconocemos, William creó un nuevo local, Circus Baby Pizza World, y es en este donde presentaría sus nuevos animatrónicos, los Funtime. Estos animatrónicos estarían hechos bajo la empresa Afton Robotics, que como podrán imaginar, esta empresa era de William. Aunque los Funtime no eran animatrónicos normales, si tenían buenas características muy innovadoras con respecto a los primeros trajes híbridos, estos Funtime estarían creados específicamente para matar. Una inteligencia artificial muy avanzada, poder abrir diferentes partes de su cuerpo y la posibilidad de hablar. Claramente no tenían una buena intención, pero a William se le volvería todo en contra cuando el mismo día de la inauguración de su local, a pesar de sus advertencias a Elizabeth, esta entró igual al cuarto donde estaban los animatrónicos para ver si estaba su robot. favorito, bebé. Y luego de que este animatrónico le ofrece un helado para hacer que se acercara a ella, la mata. O bueno, no tanto. Mientras a todo esto, recordamos que William pensaba que ya todos los niños estaban capturados dentro de los animatrónicos, debido a que la apertura de su local había sido completamente exitosa. Entonces alerta a toda la gente de una fuga de gas para que así tengan que evacuar el local y él poder ir a ver su recompensa. Cuando William va a ver si sus animatrónicos habían capturado niños, sí, así es, habían capturado niños. Que eso lo sabemos debido a que en los planos de los animatrónicos aparecen cuerpos dentro de estos robots. Pero también William se daría cuenta de que su animatrónico principal había matado a Elizabeth. O en realidad, su hija estaba tomando el control de Baby debido a que los ojos del animatrónico pasarían de ser azules a como los tenía su hijita, verdes. Por supuesto que William al enterarse de todo esto no sabe qué hacer y es por eso que decide encerrarla en Circus Baby Entertainment, un lugar ubicado debajo de Circus Baby. Tras el cierre de Circus Baby y la incertidumbre de lo ocurrido con su hija menor, estas cosas empezarían a afectar a William Afton, dando comienzo a su declive. Por eso, luego del fracaso de Circus Baby, éste vuelve a pedirle ayuda y trabajo a Henry, que a pesar de todos los problemas que había tenido con su anterior socio, le da trabajo de administrador o mecánico, por eso se lo puede ver colocándole. la cabeza de Fredbear a uno de los empleados de Fredbear Family Dinner. Durante estos meses, de un año que suponemos que es 1883, Henry creó y anunció otros animatrónicos por la televisión, que serían Freddy, Foxy, Chica y Bonnie. Por supuesto que William, al ver que había creado más animatrónicos, crecería la tensión con su nuevo jefe, pero lo que realmente llevaría a William a ponerse de un tono violeta sería la muerte de su hijo menor, el pendejo que llora, Crying Child. . ¿Se acuerdan de Mike, el hijo mayor de William? Bueno, este personaje asustaba de manera sobre medida a Crying Child y mientras ésta atormentaba a su único hermano chico, William protegía de sobre manera a su hijo menor, poniendo cámaras por toda la casa y dándole un peluche creado por él mismo para que pueda hablarle y sentirse cómodo. Todo esto, a pesar del comportamiento psicópata de William, serviría para vigilar a su hijo menor y así que no se escapara a ver a los animatrónicos debido a que a Crying Child le fascinaban. Pero William, al haber creado con Henry los dos primeros trajes sabían lo que podían hacer y lo danino que eran, por eso las medidas de sobreprotección. Pero ahora vamos a remontarnos a una teoría entre Five Nights at Freddy\'s 4 y The Twisted Ones, el primer libro. Supuestamente, Five Nights at Freddy\'s 4 ocurriría en las pesadillas de Crying Child, pero la verdad es que no, las pesadillas esas que ve son reales y no un mal sueño de este niño, ya que son parte de un plan muy macabro de su padre. . Verán, en la novela de The Twisted Ones, William crea un disco que hace tener alucinaciones con animatrónicos, exagerando su forma, su tamaño, etc. Algo así como la película de Batman donde el espantapájaros tiene un spray que te hace sobredimensionar tus miedos. ¿Y cómo se relaciona esto con el juego? El tema de las alucinaciones, no Batman, no tiene nada que ver Batman acá. Bueno, tenemos que remontarnos a Five Nights at Freddy\'s Ultimate Custom Night, en donde los animatrónicos Nightmares aparecen en este juego, pero en este juego controlamos a William, entonces es imposible que William logre saber con exactitud cómo son estos animatrónicos si es que en realidad son las pesadillas de su hijo menor. En otras palabras, ¿cómo sabes exactamente las pesadillas de otras personas? Con lo cual, si volvemos al primer libro, nos presentamos que William creó discos ilusorios para hacer creer a la gente cosas que realmente no hay, y esto lo utilizaría con Crying Child para hacer que se aleje definitivamente de los animatrónicos. Por eso es que tampoco nunca lo vemos regañar a su hijo mayor por maltratar a su hermanito, debido a que este le estaba generando un trauma con los animatrónicos, cosa que a William le sirvió, aunque el error de William fue confiar demasiado en Michael, porque este no sabía dónde estaba el límite de la broma, ya que Mike asustaba a su hermano solamente por diversión, y el problema se desataría en ese año 83, en el lugar donde había comenzado y terminado todo, Fredbear Family Dinner. Mike y sus amigos llevan a Crying Child por la fuerza al restaurante para seguir molestándolos con los animatrónicos en el día de su cumpleaños, y siguiendo con la broma, lo ponen en la boca de Fredbear simulando que se lo iba a comer, y desgraciadamente no. solo simulo eso. Como había dicho en un principio, el sistema de recurso de Henry era sensato, por lo que al introducir un niño dentro de la boca, el traje se cerró en la cabeza de Crying Child, que luego de eso, el mini Afton entra en un estado de coma donde están todos los animatrónicos que él conoció y el peluche que le había regalado William, donde en esta pantalla se da a entender como que su padre le está dedicando las últimas palabras a su hijo, pidiéndole que lo perdone, y diciendo dos frases que quedarían para muchísimas teorías. Vos estás roto, yo te reconstruiré. Por supuesto que esto lo dice debido a que a partir de la muerte de Elizabeth, él sabía que de alguna forma los animatrónicos lograban tomar el alma de la persona y adaptarla a su cuerpo, o por lo menos ahí alma y animatrónico convivían en un solo. cuerpo. Una curiosidad de esta parte de la historia es que como estamos en 1983, si recorremos la casa de los Afton, nos vamos a encontrar con un cuarto que da a entender que es de una niña, y quién era la única niña que tenía la familia. Afton, Elizabeth Afton. Por lo tanto, antes de ese 1983, la hija de William ya estaba dentro del cuerpo de Baby.', 1.00, 'Troleador_cara.jpg', 'Pendiente', NULL, '2025-10-02 04:10:25', NULL),
(9, 25, 22, 'Cadena', 'Oro', 'Quiero que esta cadena cuente con eslabones ', 3000000.00, 'images.png', 'Pendiente', NULL, '2025-10-02 16:34:35', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `piedras`
--

CREATE TABLE `piedras` (
  `id_piedra` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `piedras`
--

INSERT INTO `piedras` (`id_piedra`, `nombre`) VALUES
(1, 'Diamante'),
(2, 'Zafiro Azul'),
(3, 'Esmeralda'),
(4, 'Rubí'),
(5, 'Amatista'),
(6, 'Topacio'),
(7, 'Ópalo'),
(8, 'Turquesa'),
(9, 'Cuarzo Rosa'),
(10, 'Perla'),
(11, 'Granate'),
(12, 'Onix Negro'),
(13, 'Jade Verde'),
(14, 'Citrino'),
(15, 'Aguamarina');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `alto` decimal(10,2) DEFAULT 0.00,
  `ancho` decimal(10,2) DEFAULT 0.00,
  `largo` decimal(10,2) DEFAULT 0.00,
  `dimensiones` varchar(100) DEFAULT NULL,
  `referencia` varchar(50) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `umbral_alerta` int(11) DEFAULT 5,
  `id_tipo` int(11) DEFAULT NULL,
  `id_material` int(11) DEFAULT NULL,
  `id_color` int(11) DEFAULT NULL,
  `id_piedra` int(11) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `destacado` tinyint(1) DEFAULT 0,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `peso`, `alto`, `ancho`, `largo`, `dimensiones`, `referencia`, `stock`, `umbral_alerta`, `id_tipo`, `id_material`, `id_color`, `id_piedra`, `id_usuario`, `imagen`, `categoria`, `destacado`, `activo`) VALUES
(58, 'Anillo Solitario \"Aurora\"', 'Anillo de oro amarillo con diamante central talla brillante, sofisticado.', 5500000.00, 5, 0.50, 2.00, 2.00, NULL, NULL, NULL, 5, 1, 1, 1, 1, 28, 'uploads/anillo_aurora.jpg', NULL, 0, 1),
(59, 'Collar \"Verde Imperial\"', 'Collar de plata con colgante de esmeralda en corte ovalado, elegante.', 3900000.00, 20, 0.50, 1.00, 45.00, NULL, NULL, NULL, 5, 2, 2, 2, 3, 28, 'uploads/collar_verde_imperial.jpg', NULL, 0, 1),
(60, 'Pulsera \"Cielo Azul\"', 'Pulsera de acero inoxidable con topacios azules engarzados finamente.', 1850000.00, 15, 0.50, 0.50, 18.00, NULL, NULL, NULL, 5, 3, 3, 3, 6, 28, 'uploads/pulsera_cielo_azul.jpg', NULL, 0, 1),
(61, 'Aretes \"Rubí Encanto\"', 'Aretes de oro con rubíes rojos en forma de gota, clásico y refinado.', 2750000.00, 4, 0.50, 0.50, 1.00, NULL, NULL, NULL, 5, 4, 1, 4, 4, 28, 'uploads/aretes_rubi_encanto.jpg', NULL, 0, 1),
(62, 'Broche \"Perla Majestuosa\"', 'Broche de plata con perla natural central, ideal para ocasiones especiales.', 1370000.00, 10, 0.50, 3.00, 4.00, NULL, NULL, NULL, 5, 5, 2, 5, 10, 28, 'uploads/broche_perla_majestuosa.jpg', NULL, 0, 1),
(63, 'Pendientes \"Ágata Serenidad\"', 'Pendientes largos de acero con ágata verde, estilo bohemio elegante.', 1000000.00, 6, 1.00, 1.00, 7.00, NULL, NULL, NULL, 5, 6, 3, 6, 12, 28, 'uploads/pendientes_agata_serenidad.jpg', NULL, 0, 1),
(64, 'Tobillera \"Turquesa Brillante\"', 'Tobillera ajustable en plata con piedras turquesa pequeñas, delicada.', 820000.00, 12, 0.50, 0.50, 25.00, NULL, NULL, NULL, 5, 7, 2, 7, 8, 28, 'uploads/tobillera_turquesa_brillante.jpg', NULL, 0, 1),
(65, 'Dije \"Citrino Radiante\"', 'Dije de oro con citrino tallado en forma de corazón, elegante y refinado.', 1600000.00, 3, 0.50, 1.50, 2.00, NULL, NULL, NULL, 5, 8, 1, 8, 14, 28, 'uploads/dije_citrino_radiante.jpg', NULL, 0, 1),
(66, 'Gemelos \"Onix Noche\"', 'Gemelos de acero inoxidable con ónix negro pulido, sofisticados.', 550000.00, 8, 0.50, 2.00, 2.00, NULL, NULL, NULL, 5, 9, 3, 9, 12, 28, 'uploads/gemelos_onix_noche.jpg', NULL, 0, 1),
(67, 'Tiara \"Diamante Celestial\"', 'Tiara de plata con diamantes incrustados, perfecta para eventos de gala.', 9900000.00, 50, 5.00, 5.00, 30.00, NULL, NULL, NULL, 5, 10, 2, 1, 1, 28, 'uploads/tiara_diamante_celestial.jpg', NULL, 0, 1),
(72, 'Collar de hollow knight', 'Amuleto de bocasusia', 49990.00, 20, 42.00, 2.00, 4.00, NULL, NULL, NULL, 5, 2, 5, 5, NULL, 28, NULL, NULL, 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos_relacionados`
--

CREATE TABLE `productos_relacionados` (
  `id` int(11) NOT NULL,
  `id_producto_principal` int(11) NOT NULL,
  `id_producto_relacionado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_colores`
--

CREATE TABLE `producto_colores` (
  `id_producto` int(11) NOT NULL,
  `id_color` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_piedras`
--

CREATE TABLE `producto_piedras` (
  `id_producto` int(11) NOT NULL,
  `id_piedra` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_promocion`
--

CREATE TABLE `producto_promocion` (
  `id_producto` int(11) NOT NULL,
  `id_promocion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_talla`
--

CREATE TABLE `producto_talla` (
  `id_producto` int(11) NOT NULL,
  `id_talla` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promociones`
--

CREATE TABLE `promociones` (
  `id_promocion` int(11) NOT NULL,
  `titulo` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `activa` tinyint(1) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `descuento` decimal(5,2) DEFAULT 0.00,
  `estado` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `promociones`
--

INSERT INTO `promociones` (`id_promocion`, `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `activa`, `nombre`, `descuento`, `estado`) VALUES
(1, 'D?a de la Madre', '10% de descuento en anillos y collares', '2024-05-01', '2024-05-10', 1, NULL, 0.00, 1),
(2, 'Semana del Oro', '15% descuento en todos los productos de oro', '2024-06-01', '2024-06-07', 1, NULL, 0.00, 1),
(3, 'Black Friday', 'Hasta 50% en joyas seleccionadas', '2024-11-25', '2024-11-30', 1, NULL, 0.00, 1),
(4, 'Navidad Especial', '20% en colecciones de invierno', '2024-12-15', '2024-12-31', 1, NULL, 0.00, 1),
(5, 'A?o Nuevo', '5% de descuento adicional', '2025-01-01', '2025-01-05', 1, NULL, 0.00, 1),
(6, 'Promocion de prueba', 'Promoción válida por tiempo limitado', '2025-11-01', '2025-12-31', 1, 'Descuento de Verano', 0.15, 1),
(7, NULL, 'Descuentos navideños', '2025-11-11', '2025-11-21', NULL, 'Navidad 2025', 0.20, 1);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `promociones_activas_tienda`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `promociones_activas_tienda` (
`id_promocion` int(11)
,`titulo` varchar(100)
,`descripcion` text
,`fecha_inicio` date
,`fecha_fin` date
,`activa` tinyint(1)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `nit` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `nombre`, `nit`, `telefono`, `correo`, `direccion`) VALUES
(1, 'Joyas Medell?n Ltda.', '800123456', '6044448899', 'contacto@joyamedellin.com', 'Calle 30 #70-15'),
(2, 'Insumos Joya S.A.S.', '900876543', '6019998899', 'ventas@insujoyas.com', 'Carrera 40 #10-20'),
(3, 'Metales del Norte', '830112233', '6051112233', 'info@metalesnorte.com', 'Av. Norte #10-10'),
(4, 'Piedras Preciosas Co.', '820332211', '6023332211', 'pedidos@piedrasco.com', 'Calle de las Piedras #5'),
(5, 'EcoMateriales S.A.', '840998877', '6069988776', 'hola@ecomateriales.com', 'Vereda El Bosque');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `resumen_carrito`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `resumen_carrito` (
`id_usuario` int(11)
,`nombre_completo` varchar(100)
,`producto` varchar(100)
,`cantidad` int(11)
,`precio` decimal(10,2)
,`subtotal` decimal(20,2)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre_rol`) VALUES
(1, 'Administrador'),
(2, 'Vendedor'),
(3, 'Cliente'),
(4, 'Soporte'),
(5, 'Invitado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stock_tallas`
--

CREATE TABLE `stock_tallas` (
  `id_stock` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `talla` varchar(50) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `stock_tallas`
--

INSERT INTO `stock_tallas` (`id_stock`, `id_producto`, `talla`, `stock`) VALUES
(10, 58, '8', 5),
(11, 58, '9', 3),
(12, 58, '10', 2),
(13, 59, '45 cm', 4),
(14, 59, '50 cm', 2),
(15, 60, '18 cm', 6),
(16, 60, '20 cm', 3),
(17, 61, 'Única', 10),
(18, 62, 'Única', 7),
(19, 63, '7', 4),
(20, 63, '8', 5),
(21, 63, '9', 3),
(22, 64, '40 cm', 3),
(23, 64, '45 cm', 2),
(24, 65, '17 cm', 6),
(25, 65, '19 cm', 4),
(26, 66, 'Única', 8),
(27, 67, 'Única', 5),
(32, 72, '45cm', 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tallas`
--

CREATE TABLE `tallas` (
  `id_talla` int(11) NOT NULL,
  `nombre_talla` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tallas`
--

INSERT INTO `tallas` (`id_talla`, `nombre_talla`) VALUES
(1, 'XS'),
(2, 'S'),
(3, 'M'),
(4, 'L'),
(5, 'XL');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `tallas_disponibles_producto`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `tallas_disponibles_producto` (
`id_producto` int(11)
,`nombre` varchar(100)
,`nombre_talla` varchar(20)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_joya`
--

CREATE TABLE `tipos_joya` (
  `id_tipo` int(11) NOT NULL,
  `nombre_tipo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_joya`
--

INSERT INTO `tipos_joya` (`id_tipo`, `nombre_tipo`) VALUES
(1, 'Anillo'),
(2, 'Collar'),
(3, 'Pulsera'),
(4, 'Arete'),
(5, 'Broche'),
(6, 'Cadena'),
(7, 'Argolla'),
(8, 'Choker'),
(9, 'Gargantilla'),
(10, 'Colgante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tokens_recuperacion`
--

CREATE TABLE `tokens_recuperacion` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `token` varchar(20) NOT NULL,
  `expira` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tokens_recuperacion`
--

INSERT INTO `tokens_recuperacion` (`id`, `id_usuario`, `token`, `expira`) VALUES
(5, 13, '6fdcaa33', '2025-09-07 21:54:58'),
(9, 15, '148fa6cb', '2025-09-08 06:56:38'),
(10, 16, 'e2ca1dc7', '2025-09-08 07:01:33'),
(12, 18, 'e17e96e1', '2025-09-09 16:32:44'),
(17, 24, 'ccde3c88', '2025-10-02 01:14:18'),
(18, 24, 'c2eef339', '2025-10-02 01:19:04'),
(19, 16, 'f2e87090', '2025-10-03 09:27:09'),
(20, 16, '18c0a92e', '2025-10-03 09:27:12'),
(21, 15, '0e589337', '2025-11-12 14:38:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `fecha_modificacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_completo`, `correo`, `telefono_contacto`, `contrasena`, `direccion`, `foto_perfil`, `estado`, `id_rol`, `fecha_nacimiento`, `fecha_modificacion`) VALUES
(1, 'Juan Pérez', 'juan@ave.com', '3001112233', 'clave123', 'Calle 123', NULL, 1, 1, NULL, NULL),
(2, 'Ana Gómez', 'ana@ave.com', '3000000000', 'clave123', 'Carrera 45', NULL, 0, 2, NULL, NULL),
(3, 'Luis Rojas', 'luis@ave.com', '3003334455', 'clave123', 'Av. Norte 9', NULL, 0, 3, NULL, NULL),
(4, 'Lucía Díaz', 'lucia@ave.com', '3004445566', 'clave123', 'Nueva Direcci?n 456', NULL, 1, 3, NULL, NULL),
(5, 'Soporte AVE', 'soporte@ave.com', '3005556677', 'clave123', 'Oficina 5', NULL, 1, 4, NULL, NULL),
(9, 'Keinner Santiago', 'keinner@ave.com', '1234567890', 'scrypt:32768:8:1$RSHF9SWKA5uBgcju$399aeb09899861ac8d72917a892afac9373455001f1449e9d345520410a3c60b0305adcad23e411fb332a8da4c58d09a6b36652bd3943c5324d81417d8246a13', 'su casa ', NULL, 0, 3, NULL, NULL),
(10, 'Esteban Espitia', 'esteban@ave.com', '0987654321', 'scrypt:32768:8:1$HUuf65it9zjSZUUB$d8fee9e6d6ea1b27f9f634005a31cf2f8b063ae14c7f62e06043e1e79351c3178b609f7b1c44fc9e95e8d2b97a9938fe20018dfd465bce476c0e0397551c9d4d', 'Suba (Es un Cerro)', NULL, 0, 1, NULL, NULL),
(11, 'Uldarico Andrade', 'uldarico@gmail.com', '7890123456', 'scrypt:32768:8:1$UVX3mRSPAJ0qlwpq$8ed58f7e3f51eebb0a0bae844f9f90017a05969e8deea64a33c823ab4810a43b7ea914985d3e9a6a71a6704a9b008fbeaa024c3eec0ced58299c1c8c6894318d', 'carrera del amorch', NULL, 0, 3, NULL, NULL),
(12, 'Danna Gabriela', 'dannagb@gmail.com', '1234567890', 'scrypt:32768:8:1$Zkl79IRpzx4UV2q2$65b9399dbda0e5d9ff880f88b14c8c0509d14c3be7d66b7bfcdcb17f474c168fc7bd5621f4bac88fb9104c9edcb627e3358f64d392790233b8982bd0700cabb6', 'Cerru', NULL, 0, 2, NULL, NULL),
(13, 'Maria Teresa', 'juancamilogarciabonilla54@gmail.com', '+573194988478', 'scrypt:32768:8:1$Jx3ubUv7XhrfxUgh$cb4dffe8b7ad00a5901f1c1ac54f006eb5698e5bfe09872582b9546a3eddbbfe3537f5f8dd3d2a6be2aa5372ea10534aa1a1e7e0575146e8c4cc1f0423a2b5aa', 'Suba (En la falda del Cerro)', NULL, 0, 1, NULL, NULL),
(15, 'Keinner Perez', 'keinnerrodriguez0916@gmail.com', '+573245019909', 'scrypt:32768:8:1$vvKkyy12LOi0Q2aq$7904b878b6977efa5a7e7b57bd3643122e7327300a16b27d04236b2f3f4286c3dc80542ed81637cb7da68af3faf9c0c746b24d21471f8ed76c5ca039dbe4470b', 'Portal 80', 'Troleador_cara_20251113134424846477.jpg', 0, 2, '2011-11-11', '2025-11-13 13:44:24'),
(16, 'Samuel Mariño', 'samuel.e.marino@hotmail.com', '+573212136560', 'scrypt:32768:8:1$lVGYMtunbBF5oZM2$06acb0dbc8f87963de0e3d88ea6d3227ed6760ca0bbc61e370143b9a85214918a2ee86510aca0cae0168934b5afaa69df23fde2e762396c39837a92082e34a8f', 'Por ahí', 'homer-uchiha-v0-zh5brm4usx2e1_20251112214627793491_20251113133143262241.jpg', 0, 1, '2008-08-21', '2025-11-13 13:31:43'),
(17, 'Luis Garcia', 'luis.garcia@gmail.com', '+5712340987654', 'scrypt:32768:8:1$9m3QskmkdBnF2v16$ed669e720f10627a9ecb6ad25a770167c2ee812efccdb37e99250e4bedc14ac21b560657784c3c9cbf0e36102d7ca56f70859429505b7218e9c56ad70387e425', 'Casa', NULL, 0, 1, NULL, NULL),
(18, 'Maria Bonilla', 'matebojejuda123@gmail.com', '+57097327647', 'scrypt:32768:8:1$wd1GIWxJNcZAXUy7$64ae89d9d7a160750c02296b4edbc64d72a7387c1a6961edc20b5a27e4d411ec67d19d1f58a1a45328ebdb2fcd5c926f23a180864773ae9a108b1837e84c6245', 'Casa', NULL, 0, 1, NULL, NULL),
(20, 'jhon', 'jhon@ave.com', '+573506257556', 'scrypt:32768:8:1$ORAZ1tBwMtgF8UP8$7e95fe4eae0acdab5d34d19fc33996bfc0c1265aedb59ef76b7291aa498d8e5b8ad769d9d4c5ed3af2066cd52cf4b3ed752f3f3e17dd8641ed7e92443963cca8', 'xd', NULL, 0, 2, NULL, NULL),
(21, 'Nicole Quiroga', 'paolakimoficial@gmail.com', '+573007151138', 'scrypt:32768:8:1$a8N2mO0IJVSvMlhU$22521088b02de3e4516418e69c8066b7e9bb2513fd08e40de70329f0d1a63f5cbcac94a7336fda2712fab1774f62c7b96fa35e0b536eadc32dc8432f8b878779', 'casa xd', NULL, 0, 3, NULL, NULL),
(22, 'Juan Garcia', 'juancgb2007@gmail.com', '+573194988478', 'scrypt:32768:8:1$QCFlm3rymKtIJdGf$08ebc944ddea26d65b106266d7bbaac04a81bc62bc638a29bbb15afe85bc6b98edc7c44ce8e64d9ad5c7908451d1f5f9643f1f0636c463f7dcde72ceb414eea6', 'Cerru Premium', NULL, 0, 2, NULL, NULL),
(23, 'esteban espitia ', 'estebanof2005@gmail.com', '+573506257556', 'scrypt:32768:8:1$SQM6CMvBpHOeHEpq$70f7b559b8abc1ad805816b59b53a7b6e9748798986845f63ec181c23043538464f61e24757d7824c4dc08137f79d46e14d6c77b7038b10732fc52086189a409', 'suba (cerro)', NULL, 0, 2, NULL, NULL),
(24, 'Juan Garcia', 'juanpgr768@gmail.com', '+57091234782', 'scrypt:32768:8:1$47dkFKyVYWgqEuTg$c9200e415aa47cb7ee2568c957fe98ac4d4011fb262e286cdcd0b4efc3e133e63884f51801fd2579691519375a4e8643f206927cdce120d9e94856dff464e22d', 'Cerru Premium', NULL, 1, 2, NULL, NULL),
(25, 'Juan Bonilla', 'juancgb.drive@gmail.com', '+57984208924', 'scrypt:32768:8:1$UGkjjjVuIq1JfxFa$2b7572d5a3ab4cf801b3b27a63b70063b0eaab97c1398040451113f0423da161795894ca8608e6650c102bf82d25e74e80dce47c4cc87e8d663061bb32a74a34', 'Mi casita ', NULL, 1, 3, NULL, NULL),
(28, 'José Muñoz', 'jose@test.com', '+573005006005', 'scrypt:32768:8:1$qKYD6cYrfcVfDI1n$466d8feca983bda4ba580d8c22919c18c270f82592b83a18b6ada3a508093a8183bff5a841b9351bc5893d288cf834f44e323ed816fe1ac011c2258a69e22461', 'Calle 1 #81 - 29', 'anime-koe-no-katachi-shouya-ishida-hd-wallpaper-thumb_20251113031914714479.jpg', 1, 2, '2008-08-21', '2025-11-13 03:29:16'),
(29, 'Alan David Perez Guerra', 'alandavidperezguerra@gmail.com', '+57 3209551825', 'scrypt:32768:8:1$jzelyapmyAZmPSK0$82e7f1cf08cd081745dc547766b130e71f1dc5321ce9c388b29c183a8c2ae4bdb73ab439652a4726c052c42007e60cddaa60a2a9605f47c45f80fbd023ad4d82', 'calle 65bis#89-30', NULL, 1, 3, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `valoraciones`
--

CREATE TABLE `valoraciones` (
  `id_valoracion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `estrellas` int(11) NOT NULL CHECK (`estrellas` between 1 and 5),
  `comentario` text NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_bitacora_usuarios`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_bitacora_usuarios` (
`id_log` int(11)
,`nombre_completo` varchar(100)
,`accion` varchar(100)
,`modulo` varchar(50)
,`fecha` datetime
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_clientes_contacto`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_clientes_contacto` (
`nombre_completo` varchar(100)
,`correo` varchar(100)
,`telefono_contacto` varchar(20)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_detalle_pedido_extendido`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_detalle_pedido_extendido` (
`id_pedido` int(11)
,`producto` varchar(100)
,`cantidad` int(11)
,`precio_unitario` decimal(10,2)
,`id_talla` int(11)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_ordenes_proveedor`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_ordenes_proveedor` (
`id_orden` int(11)
,`proveedor` varchar(100)
,`fecha` date
,`estado` varchar(30)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_pedidos_clientes`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_pedidos_clientes` (
`id_pedido` int(11)
,`cliente` varchar(100)
,`fecha` date
,`estado` varchar(30)
,`total` decimal(10,2)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_productos_completos`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_productos_completos` (
`id_producto` int(11)
,`nombre` varchar(100)
,`descripcion` text
,`precio` decimal(10,2)
,`stock` int(11)
,`tipo_joya` varchar(50)
,`material` varchar(50)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_productos_mas_vendidos`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_productos_mas_vendidos` (
`nombre` varchar(100)
,`total_vendido` decimal(32,0)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_productos_promocion`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_productos_promocion` (
`producto` varchar(100)
,`promocion` varchar(100)
,`fecha_inicio` date
,`fecha_fin` date
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_promociones_activas`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_promociones_activas` (
`titulo` varchar(100)
,`descripcion` text
,`fecha_inicio` date
,`fecha_fin` date
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_stock_bajo`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_stock_bajo` (
`id_producto` int(11)
,`nombre` varchar(100)
,`stock` int(11)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `promociones_activas_tienda`
--
DROP TABLE IF EXISTS `promociones_activas_tienda`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `promociones_activas_tienda`  AS SELECT `promociones`.`id_promocion` AS `id_promocion`, `promociones`.`titulo` AS `titulo`, `promociones`.`descripcion` AS `descripcion`, `promociones`.`fecha_inicio` AS `fecha_inicio`, `promociones`.`fecha_fin` AS `fecha_fin`, `promociones`.`activa` AS `activa` FROM `promociones` WHERE `promociones`.`activa` = 1 AND curdate() between `promociones`.`fecha_inicio` and `promociones`.`fecha_fin` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `resumen_carrito`
--
DROP TABLE IF EXISTS `resumen_carrito`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `resumen_carrito`  AS SELECT `cu`.`id_usuario` AS `id_usuario`, `u`.`nombre_completo` AS `nombre_completo`, `p`.`nombre` AS `producto`, `cu`.`cantidad` AS `cantidad`, `p`.`precio` AS `precio`, `cu`.`cantidad`* `p`.`precio` AS `subtotal` FROM ((`carrito_usuario` `cu` join `usuarios` `u` on(`cu`.`id_usuario` = `u`.`id_usuario`)) join `productos` `p` on(`cu`.`id_producto` = `p`.`id_producto`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `tallas_disponibles_producto`
--
DROP TABLE IF EXISTS `tallas_disponibles_producto`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `tallas_disponibles_producto`  AS SELECT `p`.`id_producto` AS `id_producto`, `p`.`nombre` AS `nombre`, `t`.`nombre_talla` AS `nombre_talla` FROM ((`productos` `p` join `producto_talla` `pt` on(`p`.`id_producto` = `pt`.`id_producto`)) join `tallas` `t` on(`pt`.`id_talla` = `t`.`id_talla`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_bitacora_usuarios`
--
DROP TABLE IF EXISTS `vista_bitacora_usuarios`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_bitacora_usuarios`  AS SELECT `b`.`id_log` AS `id_log`, `u`.`nombre_completo` AS `nombre_completo`, `b`.`accion` AS `accion`, `b`.`modulo` AS `modulo`, `b`.`fecha` AS `fecha` FROM (`bitacora` `b` join `usuarios` `u` on(`b`.`id_usuario` = `u`.`id_usuario`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_clientes_contacto`
--
DROP TABLE IF EXISTS `vista_clientes_contacto`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_clientes_contacto`  AS SELECT `u`.`nombre_completo` AS `nombre_completo`, `u`.`correo` AS `correo`, `u`.`telefono_contacto` AS `telefono_contacto` FROM (`clientes` `c` join `usuarios` `u` on(`c`.`id_usuario` = `u`.`id_usuario`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_detalle_pedido_extendido`
--
DROP TABLE IF EXISTS `vista_detalle_pedido_extendido`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_detalle_pedido_extendido`  AS SELECT `dp`.`id_pedido` AS `id_pedido`, `pr`.`nombre` AS `producto`, `dp`.`cantidad` AS `cantidad`, `dp`.`precio_unitario` AS `precio_unitario`, `dp`.`id_talla` AS `id_talla` FROM (`detalle_pedido` `dp` join `productos` `pr` on(`dp`.`id_producto` = `pr`.`id_producto`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_ordenes_proveedor`
--
DROP TABLE IF EXISTS `vista_ordenes_proveedor`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_ordenes_proveedor`  AS SELECT `o`.`id_orden` AS `id_orden`, `pr`.`nombre` AS `proveedor`, `o`.`fecha` AS `fecha`, `o`.`estado` AS `estado` FROM (`ordenes_compra` `o` join `proveedores` `pr` on(`o`.`id_proveedor` = `pr`.`id_proveedor`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_pedidos_clientes`
--
DROP TABLE IF EXISTS `vista_pedidos_clientes`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_pedidos_clientes`  AS SELECT `pe`.`id_pedido` AS `id_pedido`, `u`.`nombre_completo` AS `cliente`, `pe`.`fecha` AS `fecha`, `pe`.`estado` AS `estado`, `pe`.`total` AS `total` FROM ((`pedidos` `pe` join `clientes` `c` on(`pe`.`id_cliente` = `c`.`id_cliente`)) join `usuarios` `u` on(`c`.`id_usuario` = `u`.`id_usuario`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_productos_completos`
--
DROP TABLE IF EXISTS `vista_productos_completos`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_productos_completos`  AS SELECT `p`.`id_producto` AS `id_producto`, `p`.`nombre` AS `nombre`, `p`.`descripcion` AS `descripcion`, `p`.`precio` AS `precio`, `p`.`stock` AS `stock`, `t`.`nombre_tipo` AS `tipo_joya`, `m`.`nombre_material` AS `material` FROM ((`productos` `p` join `tipos_joya` `t` on(`p`.`id_tipo` = `t`.`id_tipo`)) join `materiales` `m` on(`p`.`id_material` = `m`.`id_material`)) ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_productos_mas_vendidos`
--
DROP TABLE IF EXISTS `vista_productos_mas_vendidos`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_productos_mas_vendidos`  AS SELECT `p`.`nombre` AS `nombre`, sum(`dp`.`cantidad`) AS `total_vendido` FROM (`detalle_pedido` `dp` join `productos` `p` on(`dp`.`id_producto` = `p`.`id_producto`)) GROUP BY `dp`.`id_producto` ORDER BY sum(`dp`.`cantidad`) DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_productos_promocion`
--
DROP TABLE IF EXISTS `vista_productos_promocion`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_productos_promocion`  AS SELECT `p`.`nombre` AS `producto`, `pr`.`titulo` AS `promocion`, `pr`.`fecha_inicio` AS `fecha_inicio`, `pr`.`fecha_fin` AS `fecha_fin` FROM ((`productos` `p` join `producto_promocion` `pp` on(`p`.`id_producto` = `pp`.`id_producto`)) join `promociones` `pr` on(`pp`.`id_promocion` = `pr`.`id_promocion`)) WHERE `pr`.`activa` = 1 ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_promociones_activas`
--
DROP TABLE IF EXISTS `vista_promociones_activas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_promociones_activas`  AS SELECT `promociones`.`titulo` AS `titulo`, `promociones`.`descripcion` AS `descripcion`, `promociones`.`fecha_inicio` AS `fecha_inicio`, `promociones`.`fecha_fin` AS `fecha_fin` FROM `promociones` WHERE `promociones`.`activa` = 1 ;

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_stock_bajo`
--
DROP TABLE IF EXISTS `vista_stock_bajo`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_stock_bajo`  AS SELECT `productos`.`id_producto` AS `id_producto`, `productos`.`nombre` AS `nombre`, `productos`.`stock` AS `stock` FROM `productos` WHERE `productos`.`stock` < 10 ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `carrito_usuario`
--
ALTER TABLE `carrito_usuario`
  ADD PRIMARY KEY (`id_carrito`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `colores`
--
ALTER TABLE `colores`
  ADD PRIMARY KEY (`id_color`);

--
-- Indices de la tabla `costos_envio`
--
ALTER TABLE `costos_envio`
  ADD PRIMARY KEY (`id_costo`);

--
-- Indices de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_orden` (`id_orden`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_talla` (`id_talla`);

--
-- Indices de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD PRIMARY KEY (`id_devolucion`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `faq`
--
ALTER TABLE `faq`
  ADD PRIMARY KEY (`id_faq`);

--
-- Indices de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD PRIMARY KEY (`id_imagen`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `incidencias_entrega`
--
ALTER TABLE `incidencias_entrega`
  ADD PRIMARY KEY (`id_incidencia`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indices de la tabla `materiales`
--
ALTER TABLE `materiales`
  ADD PRIMARY KEY (`id_material`);

--
-- Indices de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD PRIMARY KEY (`id_movimiento`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `ordenes_compra`
--
ALTER TABLE `ordenes_compra`
  ADD PRIMARY KEY (`id_orden`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `fk_pedido_usuario` (`id_usuario`);

--
-- Indices de la tabla `pedidos_personalizados`
--
ALTER TABLE `pedidos_personalizados`
  ADD PRIMARY KEY (`id_pedido_personalizado`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_vendedor` (`id_vendedor`);

--
-- Indices de la tabla `piedras`
--
ALTER TABLE `piedras`
  ADD PRIMARY KEY (`id_piedra`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_tipo` (`id_tipo`),
  ADD KEY `id_material` (`id_material`),
  ADD KEY `fk_producto_usuario` (`id_usuario`),
  ADD KEY `fk_productos_colores` (`id_color`),
  ADD KEY `fk_productos_piedras` (`id_piedra`);

--
-- Indices de la tabla `productos_relacionados`
--
ALTER TABLE `productos_relacionados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_producto_principal` (`id_producto_principal`),
  ADD KEY `id_producto_relacionado` (`id_producto_relacionado`);

--
-- Indices de la tabla `producto_colores`
--
ALTER TABLE `producto_colores`
  ADD PRIMARY KEY (`id_producto`,`id_color`),
  ADD KEY `id_color` (`id_color`);

--
-- Indices de la tabla `producto_piedras`
--
ALTER TABLE `producto_piedras`
  ADD PRIMARY KEY (`id_producto`,`id_piedra`),
  ADD KEY `id_piedra` (`id_piedra`);

--
-- Indices de la tabla `producto_promocion`
--
ALTER TABLE `producto_promocion`
  ADD PRIMARY KEY (`id_producto`,`id_promocion`),
  ADD KEY `id_promocion` (`id_promocion`);

--
-- Indices de la tabla `producto_talla`
--
ALTER TABLE `producto_talla`
  ADD PRIMARY KEY (`id_producto`,`id_talla`),
  ADD KEY `id_talla` (`id_talla`);

--
-- Indices de la tabla `promociones`
--
ALTER TABLE `promociones`
  ADD PRIMARY KEY (`id_promocion`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `stock_tallas`
--
ALTER TABLE `stock_tallas`
  ADD PRIMARY KEY (`id_stock`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `tallas`
--
ALTER TABLE `tallas`
  ADD PRIMARY KEY (`id_talla`);

--
-- Indices de la tabla `tipos_joya`
--
ALTER TABLE `tipos_joya`
  ADD PRIMARY KEY (`id_tipo`);

--
-- Indices de la tabla `tokens_recuperacion`
--
ALTER TABLE `tokens_recuperacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_rol` (`id_rol`);

--
-- Indices de la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  ADD PRIMARY KEY (`id_valoracion`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`,`id_producto`),
  ADD KEY `id_producto` (`id_producto`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `carrito_usuario`
--
ALTER TABLE `carrito_usuario`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `colores`
--
ALTER TABLE `colores`
  MODIFY `id_color` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `costos_envio`
--
ALTER TABLE `costos_envio`
  MODIFY `id_costo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  MODIFY `id_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `faq`
--
ALTER TABLE `faq`
  MODIFY `id_faq` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  MODIFY `id_imagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `incidencias_entrega`
--
ALTER TABLE `incidencias_entrega`
  MODIFY `id_incidencia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materiales`
--
ALTER TABLE `materiales`
  MODIFY `id_material` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  MODIFY `id_movimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ordenes_compra`
--
ALTER TABLE `ordenes_compra`
  MODIFY `id_orden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `pedidos_personalizados`
--
ALTER TABLE `pedidos_personalizados`
  MODIFY `id_pedido_personalizado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `piedras`
--
ALTER TABLE `piedras`
  MODIFY `id_piedra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `productos_relacionados`
--
ALTER TABLE `productos_relacionados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `promociones`
--
ALTER TABLE `promociones`
  MODIFY `id_promocion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `stock_tallas`
--
ALTER TABLE `stock_tallas`
  MODIFY `id_stock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `tallas`
--
ALTER TABLE `tallas`
  MODIFY `id_talla` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tipos_joya`
--
ALTER TABLE `tipos_joya`
  MODIFY `id_tipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tokens_recuperacion`
--
ALTER TABLE `tokens_recuperacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  MODIFY `id_valoracion` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD CONSTRAINT `bitacora_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `carrito_usuario`
--
ALTER TABLE `carrito_usuario`
  ADD CONSTRAINT `carrito_usuario_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `carrito_usuario_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD CONSTRAINT `detalle_orden_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `ordenes_compra` (`id_orden`);

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  ADD CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `detalle_pedido_ibfk_3` FOREIGN KEY (`id_talla`) REFERENCES `tallas` (`id_talla`);

--
-- Filtros para la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  ADD CONSTRAINT `devoluciones_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD CONSTRAINT `imagenes_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `incidencias_entrega`
--
ALTER TABLE `incidencias_entrega`
  ADD CONSTRAINT `incidencias_entrega_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`);

--
-- Filtros para la tabla `movimientos_inventario`
--
ALTER TABLE `movimientos_inventario`
  ADD CONSTRAINT `movimientos_inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `movimientos_inventario_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `ordenes_compra`
--
ALTER TABLE `ordenes_compra`
  ADD CONSTRAINT `ordenes_compra_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `fk_pedido_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`);

--
-- Filtros para la tabla `pedidos_personalizados`
--
ALTER TABLE `pedidos_personalizados`
  ADD CONSTRAINT `pedidos_personalizados_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `pedidos_personalizados_ibfk_2` FOREIGN KEY (`id_vendedor`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_producto_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_productos_colores` FOREIGN KEY (`id_color`) REFERENCES `colores` (`id_color`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_productos_piedras` FOREIGN KEY (`id_piedra`) REFERENCES `piedras` (`id_piedra`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipos_joya` (`id_tipo`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_material`) REFERENCES `materiales` (`id_material`);

--
-- Filtros para la tabla `productos_relacionados`
--
ALTER TABLE `productos_relacionados`
  ADD CONSTRAINT `productos_relacionados_ibfk_1` FOREIGN KEY (`id_producto_principal`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `productos_relacionados_ibfk_2` FOREIGN KEY (`id_producto_relacionado`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `producto_colores`
--
ALTER TABLE `producto_colores`
  ADD CONSTRAINT `producto_colores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `producto_colores_ibfk_2` FOREIGN KEY (`id_color`) REFERENCES `colores` (`id_color`);

--
-- Filtros para la tabla `producto_piedras`
--
ALTER TABLE `producto_piedras`
  ADD CONSTRAINT `producto_piedras_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `producto_piedras_ibfk_2` FOREIGN KEY (`id_piedra`) REFERENCES `piedras` (`id_piedra`);

--
-- Filtros para la tabla `producto_promocion`
--
ALTER TABLE `producto_promocion`
  ADD CONSTRAINT `producto_promocion_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `producto_promocion_ibfk_2` FOREIGN KEY (`id_promocion`) REFERENCES `promociones` (`id_promocion`);

--
-- Filtros para la tabla `producto_talla`
--
ALTER TABLE `producto_talla`
  ADD CONSTRAINT `producto_talla_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `producto_talla_ibfk_2` FOREIGN KEY (`id_talla`) REFERENCES `tallas` (`id_talla`);

--
-- Filtros para la tabla `stock_tallas`
--
ALTER TABLE `stock_tallas`
  ADD CONSTRAINT `stock_tallas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tokens_recuperacion`
--
ALTER TABLE `tokens_recuperacion`
  ADD CONSTRAINT `tokens_recuperacion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);

--
-- Filtros para la tabla `valoraciones`
--
ALTER TABLE `valoraciones`
  ADD CONSTRAINT `valoraciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `valoraciones_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
