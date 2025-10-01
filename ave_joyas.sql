-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-09-2025 a las 07:58:18
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

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

--
-- Volcado de datos para la tabla `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`id_detalle`, `id_pedido`, `id_producto`, `id_talla`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 2, 1, 350000.00),
(2, 2, 2, 2, 1, 120000.00),
(3, 3, 3, 4, 1, 95000.00),
(4, 4, 4, 3, 2, 235000.00),
(5, 5, 5, 5, 1, 80000.00),
(6, 6, 3, NULL, 2, 95000.00),
(7, 7, 3, NULL, 1, 95000.00),
(8, 8, 3, NULL, 1, 95000.00),
(9, 9, 2, NULL, 1, 120000.00),
(10, 9, 3, NULL, 1, 95000.00),
(11, 10, 2, NULL, 1, 120000.00),
(12, 10, 3, NULL, 1, 95000.00),
(13, 11, 2, NULL, 1, 120000.00);

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
(2, 2, 'https://nomadajoyas.com/wp-content/uploads/2022/07/collar-corazon-plata.jpg'),
(3, 3, 'https://finagarcia.com/cdn/shop/files/ACPU00593.jpg?v=1729505395'),
(4, 4, 'https://cdn-media.glamira.com/media/product/newgeneration/view/1/sku/G100735/diamond/ruby_AA/alloycolour/white.jpg'),
(5, 5, 'https://taller-cruz.es/wp-content/uploads/broche-hoja-grande-1.jpg'),
(6, 1, 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQXtt5brPXaB6awQSeRp2WLWcpFKznoQ2p3slXxHdIvkbGeuwu5Xe9qmN5DxidjbRb6eM-hQ5XDjEVrnW0l52QlsoIUasnhUITT-Wu6GzJvKKyJ-0Y');

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
  `metodo` varchar(50) NOT NULL,
  `estado` varchar(30) DEFAULT 'Pendiente',
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `referencia_pago` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_pedido`, `metodo_pago`, `monto`, `metodo`, `estado`, `fecha`, `referencia_pago`) VALUES
(1, 7, '', 95000.00, 'tarjeta', 'Pagado', '2025-09-16 00:36:29', NULL);

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
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_cliente`, `fecha`, `estado`, `metodo_envio`, `metodo_pago`, `total`, `estado_pago`, `id_usuario`) VALUES
(1, 1, '2024-06-01', 'Enviado', 'Mensajer?a', 'Tarjeta', 350000.00, 'pendiente', NULL),
(2, 2, '2024-06-02', 'Preparando', 'Contra entrega', 'Efectivo', 120000.00, 'pendiente', NULL),
(3, 3, '2024-06-03', 'Entregado', 'Mensajer?a', 'Nequi', 95000.00, 'pendiente', NULL),
(4, 4, '2024-06-04', 'Enviado', 'Domicilio', 'Tarjeta', 470000.00, 'pendiente', NULL),
(5, 5, '2024-06-05', 'Pendiente', 'Mensajer?a', 'Transferencia', 80000.00, 'pendiente', NULL),
(6, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 11),
(7, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 11),
(8, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23),
(9, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23),
(10, NULL, '2025-09-15', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23),
(11, NULL, '2025-09-16', 'Pendiente', NULL, NULL, NULL, 'pendiente', 23);

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
  `dimensiones` varchar(100) DEFAULT NULL,
  `referencia` varchar(50) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `id_tipo` int(11) DEFAULT NULL,
  `id_material` int(11) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `peso`, `dimensiones`, `referencia`, `stock`, `id_tipo`, `id_material`, `id_usuario`) VALUES
(1, 'Anillo Clásico Oro', 'Anillo elegante de oro 18k', 350000.00, 0.05, '2x2x2cm', 'AOR001', 10, 1, 1, 1),
(2, 'Collar Corazón Plata', 'Collar con dije en forma de corazón', 120000.00, 0.1, '5x5x1cm', 'CPL002', 5, 2, 2, 1),
(3, 'Pulsera Acero Fina', 'Pulsera unisex en acero inoxidable', 95000.00, 0.08, '4x4x2cm', 'PAC003', 20, 3, 3, 1),
(4, 'Aretes Rubí', 'Aretes con incrustaciones de rubí', 470000.00, 0.03, '2x2x1cm', 'ARU004', 7, 4, 4, 1),
(5, 'Broche Hoja', 'Broche de hoja con material ecológico', 80000.00, 0.02, '3x3x1cm', 'BHO005', 12, 5, 5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_promocion`
--

CREATE TABLE `producto_promocion` (
  `id_producto` int(11) NOT NULL,
  `id_promocion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto_promocion`
--

INSERT INTO `producto_promocion` (`id_producto`, `id_promocion`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 4),
(3, 2),
(3, 5),
(4, 3),
(5, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_talla`
--

CREATE TABLE `producto_talla` (
  `id_producto` int(11) NOT NULL,
  `id_talla` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto_talla`
--

INSERT INTO `producto_talla` (`id_producto`, `id_talla`) VALUES
(1, 2),
(1, 3),
(2, 2),
(3, 4),
(4, 1),
(4, 3),
(5, 5);

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
  `activa` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `promociones`
--

INSERT INTO `promociones` (`id_promocion`, `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `activa`) VALUES
(1, 'D?a de la Madre', '10% de descuento en anillos y collares', '2024-05-01', '2024-05-10', 1),
(2, 'Semana del Oro', '15% descuento en todos los productos de oro', '2024-06-01', '2024-06-07', 1),
(3, 'Black Friday', 'Hasta 50% en joyas seleccionadas', '2024-11-25', '2024-11-30', 1),
(4, 'Navidad Especial', '20% en colecciones de invierno', '2024-12-15', '2024-12-31', 1),
(5, 'A?o Nuevo', '5% de descuento adicional', '2025-01-01', '2025-01-05', 1);

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
(5, 'Broche');

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
(12, 18, 'e17e96e1', '2025-09-09 16:32:44');

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
  `estado` tinyint(1) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_completo`, `correo`, `telefono_contacto`, `contrasena`, `direccion`, `estado`, `id_rol`) VALUES
(1, 'Juan P?rez', 'juan@ave.com', '3001112233', 'clave123', 'Calle 123', 1, 1),
(2, 'Ana G?mez', 'ana@ave.com', '3000000000', 'clave123', 'Carrera 45', 0, 2),
(3, 'Luis Rojas', 'luis@ave.com', '3003334455', 'clave123', 'Av. Norte 9', 0, 3),
(4, 'Luc?a D?az', 'lucia@ave.com', '3004445566', 'clave123', 'Nueva Direcci?n 456', 1, 3),
(5, 'Soporte AVE', 'soporte@ave.com', '3005556677', 'clave123', 'Oficina 5', 1, 4),
(9, 'Keinner Santiago', 'keinner@ave.com', '1234567890', 'scrypt:32768:8:1$RSHF9SWKA5uBgcju$399aeb09899861ac8d72917a892afac9373455001f1449e9d345520410a3c60b0305adcad23e411fb332a8da4c58d09a6b36652bd3943c5324d81417d8246a13', 'su casa ', 0, 2),
(10, 'Esteban Espitia', 'esteban@ave.com', '0987654321', 'scrypt:32768:8:1$HUuf65it9zjSZUUB$d8fee9e6d6ea1b27f9f634005a31cf2f8b063ae14c7f62e06043e1e79351c3178b609f7b1c44fc9e95e8d2b97a9938fe20018dfd465bce476c0e0397551c9d4d', 'Suba (Es un Cerro)', 0, 1),
(11, 'Uldarico Andrade', 'uldarico@gmail.com', '7890123456', 'scrypt:32768:8:1$UVX3mRSPAJ0qlwpq$8ed58f7e3f51eebb0a0bae844f9f90017a05969e8deea64a33c823ab4810a43b7ea914985d3e9a6a71a6704a9b008fbeaa024c3eec0ced58299c1c8c6894318d', 'carrera del amorch', 0, 3),
(12, 'Danna Gabriela', 'dannagb@gmail.com', '1234567890', 'scrypt:32768:8:1$Zkl79IRpzx4UV2q2$65b9399dbda0e5d9ff880f88b14c8c0509d14c3be7d66b7bfcdcb17f474c168fc7bd5621f4bac88fb9104c9edcb627e3358f64d392790233b8982bd0700cabb6', 'Cerru', 0, 2),
(13, 'Maria Teresa', 'juancamilogarciabonilla54@gmail.com', '+573194988478', 'scrypt:32768:8:1$Jx3ubUv7XhrfxUgh$cb4dffe8b7ad00a5901f1c1ac54f006eb5698e5bfe09872582b9546a3eddbbfe3537f5f8dd3d2a6be2aa5372ea10534aa1a1e7e0575146e8c4cc1f0423a2b5aa', 'Suba (En la falda del Cerro)', 0, 1),
(15, 'Keinner Perez', 'keinnerrodriguez0916@gmail.com', '+573245019909', 'scrypt:32768:8:1$sykbyu6lLeIf8Ip8$27a7fd82e4bdb70bce32d64c58a0365bc5ff2a98d46b78f61ea38100ec9ccbe51e2963b5206e94f3d909d666c54a600518862380eb62bd8e3a6683ed6942f209', 'Portal 80', 0, 2),
(16, 'Samuel Mari?o', 'samuel.e.marino@hotmail.com', '+573212136560', 'scrypt:32768:8:1$zCFvMCLKDsOKc6j3$a22b2dac2a4757647bb6ee408082ac9f373253b4ed9d094bf9e9ccdb55b9eefe9b40e35098f478265f3ddc94669a0aa636969f39098f85042b02ac211bcfdf8e', 'Bosa', 0, 1),
(17, 'Luis Garcia', 'luis.garcia@gmail.com', '+5712340987654', 'scrypt:32768:8:1$9m3QskmkdBnF2v16$ed669e720f10627a9ecb6ad25a770167c2ee812efccdb37e99250e4bedc14ac21b560657784c3c9cbf0e36102d7ca56f70859429505b7218e9c56ad70387e425', 'Casa', 0, 1),
(18, 'Maria Bonilla', 'matebojejuda123@gmail.com', '+57097327647', 'scrypt:32768:8:1$wd1GIWxJNcZAXUy7$64ae89d9d7a160750c02296b4edbc64d72a7387c1a6961edc20b5a27e4d411ec67d19d1f58a1a45328ebdb2fcd5c926f23a180864773ae9a108b1837e84c6245', 'Casa', 0, 1),
(20, 'jhon', 'jhon@ave.com', '+573506257556', 'scrypt:32768:8:1$ORAZ1tBwMtgF8UP8$7e95fe4eae0acdab5d34d19fc33996bfc0c1265aedb59ef76b7291aa498d8e5b8ad769d9d4c5ed3af2066cd52cf4b3ed752f3f3e17dd8641ed7e92443963cca8', 'xd', 0, 2),
(21, 'Nicole Quiroga', 'paolakimoficial@gmail.com', '+573007151138', 'scrypt:32768:8:1$a8N2mO0IJVSvMlhU$22521088b02de3e4516418e69c8066b7e9bb2513fd08e40de70329f0d1a63f5cbcac94a7336fda2712fab1774f62c7b96fa35e0b536eadc32dc8432f8b878779', 'casa xd', 0, 1),
(22, 'Juan Garcia', 'juancgb2007@gmail.com', '+573194988478', 'scrypt:32768:8:1$QCFlm3rymKtIJdGf$08ebc944ddea26d65b106266d7bbaac04a81bc62bc638a29bbb15afe85bc6b98edc7c44ce8e64d9ad5c7908451d1f5f9643f1f0636c463f7dcde72ceb414eea6', 'Cerru Premium', 0, 2),
(23, 'esteban espitia ', 'estebanof2005@gmail.com', '+573506257556', 'scrypt:32768:8:1$SQM6CMvBpHOeHEpq$70f7b559b8abc1ad805816b59b53a7b6e9748798986845f63ec181c23043538464f61e24757d7824c4dc08137f79d46e14d6c77b7038b10732fc52086189a409', 'suba (cerro)', 0, 2);

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
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

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
-- Indices de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD PRIMARY KEY (`id_imagen`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `materiales`
--
ALTER TABLE `materiales`
  ADD PRIMARY KEY (`id_material`);

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
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_tipo` (`id_tipo`),
  ADD KEY `id_material` (`id_material`),
  ADD KEY `fk_producto_usuario` (`id_usuario`);

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
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  MODIFY `id_imagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `materiales`
--
ALTER TABLE `materiales`
  MODIFY `id_material` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ordenes_compra`
--
ALTER TABLE `ordenes_compra`
  MODIFY `id_orden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `promociones`
--
ALTER TABLE `promociones`
  MODIFY `id_promocion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
-- AUTO_INCREMENT de la tabla `tallas`
--
ALTER TABLE `tallas`
  MODIFY `id_talla` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tipos_joya`
--
ALTER TABLE `tipos_joya`
  MODIFY `id_tipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tokens_recuperacion`
--
ALTER TABLE `tokens_recuperacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD CONSTRAINT `bitacora_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

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
-- Filtros para la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD CONSTRAINT `imagenes_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

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
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_producto_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipos_joya` (`id_tipo`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_material`) REFERENCES `materiales` (`id_material`);

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
-- Filtros para la tabla `tokens_recuperacion`
--
ALTER TABLE `tokens_recuperacion`
  ADD CONSTRAINT `tokens_recuperacion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
