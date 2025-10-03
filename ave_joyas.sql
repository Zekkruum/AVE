/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ave_joyas
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bitacora`
--

DROP TABLE IF EXISTS `bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bitacora` (
  `id_log` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `accion` varchar(100) DEFAULT NULL,
  `modulo` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id_log`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `bitacora_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora`
--

LOCK TABLES `bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora` DISABLE KEYS */;
INSERT INTO `bitacora` VALUES
(1,1,'Cre? nuevo usuario','usuarios','2024-05-01 09:00:00'),
(2,2,'Edit? producto','productos','2024-05-02 10:15:00'),
(3,3,'Registr? venta','pedidos','2024-05-03 11:30:00'),
(4,4,'Gener? reporte de ventas','reportes','2024-05-04 12:45:00'),
(5,5,'Aprob? devoluci?n','devoluciones','2024-05-05 14:00:00');
/*!40000 ALTER TABLE `bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES
(5,1),
(4,2),
(1,3),
(2,4),
(3,5);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colores`
--

DROP TABLE IF EXISTS `colores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `colores` (
  `id_color` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_color`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colores`
--

LOCK TABLES `colores` WRITE;
/*!40000 ALTER TABLE `colores` DISABLE KEYS */;
/*!40000 ALTER TABLE `colores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_orden`
--

DROP TABLE IF EXISTS `detalle_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_orden` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `id_orden` int(11) DEFAULT NULL,
  `producto_descripcion` text DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_orden` (`id_orden`),
  CONSTRAINT `detalle_orden_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `ordenes_compra` (`id_orden`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_orden`
--

LOCK TABLES `detalle_orden` WRITE;
/*!40000 ALTER TABLE `detalle_orden` DISABLE KEYS */;
INSERT INTO `detalle_orden` VALUES
(1,1,'Lote de oro 18k - 50 piezas',50,500000.00),
(2,1,'Lote de plata ley 925 - 100 piezas',100,250000.00),
(3,2,'Bobinas de acero inoxidable - 200m',200,10000.00),
(4,3,'Cuentas de piedra natural - 500 unidades',500,2000.00),
(5,5,'Material ecol?gico en rollos - 300m',300,1500.00);
/*!40000 ALTER TABLE `detalle_orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `id_talla` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  KEY `id_talla` (`id_talla`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `detalle_pedido_ibfk_3` FOREIGN KEY (`id_talla`) REFERENCES `tallas` (`id_talla`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES
(1,1,1,2,1,350000.00),
(2,2,2,2,1,120000.00),
(3,3,3,4,1,95000.00),
(4,4,4,3,2,235000.00),
(5,5,5,5,1,80000.00),
(6,6,3,NULL,2,95000.00),
(7,7,3,NULL,1,95000.00),
(8,8,3,NULL,1,95000.00),
(9,9,2,NULL,1,120000.00),
(10,9,3,NULL,1,95000.00),
(11,10,2,NULL,1,120000.00),
(12,10,3,NULL,1,95000.00),
(13,11,2,NULL,1,120000.00),
(14,12,6,NULL,1,98000.00),
(15,13,6,NULL,1,98000.00),
(16,14,6,NULL,1,98000.00),
(17,15,6,NULL,1,98000.00),
(18,16,4,NULL,1,470000.00),
(19,17,5,NULL,1,80000.00),
(20,18,2,NULL,1,120000.00),
(21,19,4,NULL,1,470000.00),
(22,20,3,NULL,1,95000.00),
(23,21,10,NULL,1,90000.00),
(24,22,3,NULL,1,95000.00),
(25,23,2,NULL,1,120000.00),
(26,23,7,NULL,5,120000.00),
(27,24,6,NULL,1,98000.00),
(28,25,6,NULL,1,98000.00),
(29,26,2,NULL,1,120000.00),
(30,27,2,NULL,1,120000.00),
(31,27,10,NULL,1,90000.00),
(32,28,3,NULL,1,95000.00),
(33,28,4,NULL,1,470000.00),
(34,28,7,NULL,1,120000.00);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devoluciones`
--

DROP TABLE IF EXISTS `devoluciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `devoluciones` (
  `id_devolucion` int(11) NOT NULL AUTO_INCREMENT,
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `motivo` text DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'Pendiente',
  PRIMARY KEY (`id_devolucion`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `devoluciones_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devoluciones`
--

LOCK TABLES `devoluciones` WRITE;
/*!40000 ALTER TABLE `devoluciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `devoluciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagenes`
--

DROP TABLE IF EXISTS `imagenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes` (
  `id_imagen` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_imagen`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `imagenes_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes`
--

LOCK TABLES `imagenes` WRITE;
/*!40000 ALTER TABLE `imagenes` DISABLE KEYS */;
INSERT INTO `imagenes` VALUES
(2,2,'https://nomadajoyas.com/wp-content/uploads/2022/07/collar-corazon-plata.jpg'),
(3,3,'https://finagarcia.com/cdn/shop/files/ACPU00593.jpg?v=1729505395'),
(4,4,'https://cdn-media.glamira.com/media/product/newgeneration/view/1/sku/G100735/diamond/ruby_AA/alloycolour/white.jpg'),
(5,5,'https://taller-cruz.es/wp-content/uploads/broche-hoja-grande-1.jpg'),
(6,1,'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQXtt5brPXaB6awQSeRp2WLWcpFKznoQ2p3slXxHdIvkbGeuwu5Xe9qmN5DxidjbRb6eM-hQ5XDjEVrnW0l52QlsoIUasnhUITT-Wu6GzJvKKyJ-0Y');
/*!40000 ALTER TABLE `imagenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materiales`
--

DROP TABLE IF EXISTS `materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiales` (
  `id_material` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_material` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_material`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiales`
--

LOCK TABLES `materiales` WRITE;
/*!40000 ALTER TABLE `materiales` DISABLE KEYS */;
INSERT INTO `materiales` VALUES
(1,'Oro'),
(2,'Plata'),
(3,'Acero inoxidable'),
(4,'Piedra preciosa'),
(5,'Material sostenible');
/*!40000 ALTER TABLE `materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_inventario`
--

DROP TABLE IF EXISTS `movimientos_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_inventario` (
  `id_movimiento` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto` int(11) NOT NULL,
  `tipo` enum('entrada','salida') NOT NULL,
  `cantidad` int(11) NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_movimiento`),
  KEY `id_producto` (`id_producto`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `movimientos_inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `movimientos_inventario_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_inventario`
--

LOCK TABLES `movimientos_inventario` WRITE;
/*!40000 ALTER TABLE `movimientos_inventario` DISABLE KEYS */;
INSERT INTO `movimientos_inventario` VALUES
(1,6,'salida',20,'Vencido',24,'2025-10-01 20:14:43'),
(2,6,'entrada',7,'Fueron un regalo de la empresa por ser compradores frecuentes',2,'2025-10-01 20:22:30'),
(3,6,'entrada',7,'Fueron un regalo de la empresa por ser compradores frecuentes',2,'2025-10-01 20:22:47'),
(4,6,'salida',10,'Venta en tienda',24,'2025-10-01 20:23:56'),
(5,6,'entrada',3,'Se hizo un mal conteo al momento de hacer inventario ',2,'2025-10-01 20:24:55'),
(6,6,'entrada',5,'Se compraron 5 más',24,'2025-10-01 20:38:05');
/*!40000 ALTER TABLE `movimientos_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenes_compra`
--

DROP TABLE IF EXISTS `ordenes_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_compra` (
  `id_orden` int(11) NOT NULL AUTO_INCREMENT,
  `id_proveedor` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `estado` varchar(30) DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  PRIMARY KEY (`id_orden`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `ordenes_compra_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_compra`
--

LOCK TABLES `ordenes_compra` WRITE;
/*!40000 ALTER TABLE `ordenes_compra` DISABLE KEYS */;
INSERT INTO `ordenes_compra` VALUES
(1,1,'2024-05-01','Completado','Compra inicial de oro y plata'),
(2,2,'2024-05-03','Pendiente','Orden de acero inoxidable'),
(3,3,'2024-05-05','Completado','Materiales para pulseras'),
(4,4,'2024-05-07','Cancelado','Retraso en entrega de piedras'),
(5,5,'2024-05-09','Pendiente','Pedido de materiales sostenibles');
/*!40000 ALTER TABLE `ordenes_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL AUTO_INCREMENT,
  `id_pedido` int(11) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `estado` varchar(30) DEFAULT 'Pendiente',
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `referencia_pago` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
INSERT INTO `pagos` VALUES
(1,7,'',95000.00,'Pagado','2025-09-16 00:36:29',NULL),
(2,13,'Efectivo',98000.00,'Pagado','2025-10-01 22:48:24',NULL),
(3,14,'Transferencia',98000.00,'Pagado','2025-10-01 22:48:52',NULL),
(4,15,'Tarjeta',98000.00,'Pagado','2025-10-01 22:54:56',NULL),
(5,16,'efectivo',470000.00,'Pagado','2025-10-01 23:07:51',NULL),
(6,19,'efectivo',470000.00,'Pagado','2025-10-01 23:27:15',NULL),
(7,20,'transferencia',95000.00,'Pagado','2025-10-02 02:15:22',NULL),
(8,21,'tarjeta',90000.00,'Pagado','2025-10-02 03:54:36',NULL),
(9,22,'tarjeta',95000.00,'Pagado','2025-10-02 03:54:51',NULL),
(10,23,'tarjeta',720000.00,'Pagado','2025-10-02 13:20:36',NULL),
(11,24,'transferencia',116620.00,'Pagado','2025-10-02 15:56:34',NULL),
(12,25,'contraentrega',116620.00,'Pagado','2025-10-02 16:01:01',NULL),
(13,26,'tarjeta',142800.00,'Pagado','2025-10-02 16:16:09',NULL),
(14,27,'tarjeta',249900.00,'Pagado','2025-10-02 16:31:39',NULL),
(15,28,'tarjeta',815150.00,'Pagado','2025-10-02 16:32:20',NULL);
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  KEY `fk_pedido_usuario` (`id_usuario`),
  CONSTRAINT `fk_pedido_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES
(1,1,'2024-06-01','Enviado','Mensajer?a','Tarjeta',350000.00,'pendiente',NULL,0.00,0.00),
(2,2,'2024-06-02','Preparando','Contra entrega','Efectivo',120000.00,'pendiente',NULL,0.00,0.00),
(3,3,'2024-06-03','Entregado','Mensajer?a','Nequi',95000.00,'pendiente',NULL,0.00,0.00),
(4,4,'2024-06-04','Enviado','Domicilio','Tarjeta',470000.00,'pendiente',NULL,0.00,0.00),
(5,5,'2024-06-05','Pendiente','Mensajer?a','Transferencia',80000.00,'pendiente',NULL,0.00,0.00),
(6,NULL,'2025-09-15','Pendiente',NULL,NULL,NULL,'pendiente',11,0.00,0.00),
(7,NULL,'2025-09-15','Pendiente',NULL,NULL,NULL,'pendiente',11,0.00,0.00),
(8,NULL,'2025-09-15','Pendiente',NULL,NULL,NULL,'pendiente',23,0.00,0.00),
(9,NULL,'2025-09-15','Pendiente',NULL,NULL,NULL,'pendiente',23,0.00,0.00),
(10,NULL,'2025-09-15','Pendiente',NULL,NULL,NULL,'pendiente',23,0.00,0.00),
(11,NULL,'2025-09-16','Pendiente',NULL,NULL,NULL,'pendiente',23,0.00,0.00),
(12,NULL,'2025-10-01','Pendiente',NULL,NULL,NULL,'pendiente',25,0.00,0.00),
(13,NULL,'2025-10-01','Pagado',NULL,NULL,98000.00,'pendiente',25,0.00,0.00),
(14,NULL,'2025-10-01','Pagado',NULL,NULL,98000.00,'pendiente',25,0.00,0.00),
(15,NULL,'2025-10-01','Pagado',NULL,NULL,98000.00,'pendiente',25,0.00,0.00),
(16,NULL,'2025-10-01','Pagado',NULL,NULL,470000.00,'pendiente',25,0.00,0.00),
(17,NULL,'2025-10-01','Pendiente',NULL,NULL,80000.00,'pendiente',25,0.00,0.00),
(18,NULL,'2025-10-01','Pendiente',NULL,NULL,120000.00,'pendiente',25,0.00,0.00),
(19,NULL,'2025-10-01','Pagado',NULL,NULL,470000.00,'pendiente',25,0.00,0.00),
(20,NULL,'2025-10-02','Pagado',NULL,NULL,95000.00,'pendiente',25,0.00,0.00),
(21,NULL,'2025-10-02','Pagado',NULL,NULL,90000.00,'pendiente',25,0.00,0.00),
(22,NULL,'2025-10-02','Pagado',NULL,NULL,95000.00,'pendiente',25,0.00,0.00),
(23,NULL,'2025-10-02','Pagado',NULL,NULL,720000.00,'pendiente',25,0.00,0.00),
(24,NULL,'2025-10-02','Pendiente',NULL,NULL,116620.00,'pendiente',25,98000.00,18620.00),
(25,NULL,'2025-10-02','Pendiente',NULL,NULL,116620.00,'pendiente',25,98000.00,18620.00),
(26,NULL,'2025-10-02','Pendiente',NULL,NULL,142800.00,'pendiente',24,120000.00,22800.00),
(27,NULL,'2025-10-02','Pendiente',NULL,NULL,249900.00,'pendiente',25,210000.00,39900.00),
(28,NULL,'2025-10-02','Pendiente',NULL,NULL,815150.00,'pendiente',25,685000.00,130150.00);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos_personalizados`
--

DROP TABLE IF EXISTS `pedidos_personalizados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_personalizados` (
  `id_pedido_personalizado` int(11) NOT NULL AUTO_INCREMENT,
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
  `fecha_entrega_estimada` date DEFAULT NULL,
  PRIMARY KEY (`id_pedido_personalizado`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_vendedor` (`id_vendedor`),
  CONSTRAINT `pedidos_personalizados_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `pedidos_personalizados_ibfk_2` FOREIGN KEY (`id_vendedor`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_personalizados`
--

LOCK TABLES `pedidos_personalizados` WRITE;
/*!40000 ALTER TABLE `pedidos_personalizados` DISABLE KEYS */;
INSERT INTO `pedidos_personalizados` VALUES
(1,25,24,'Manilla','Oro','Quiero que la manilla tenga un colgante con el personaje de Hornet del videojuego titulado Hollow Knight Silksong',120000.00,'Hornet_Idle.jpg','Rechazado','NMMS WE MUY DIFICIL WE','2025-10-02 00:51:44',NULL),
(2,25,24,'Manilla','Oro','Quiero que esta manilla tenga un adorno con la figura de Hornet del videojuego titulado Hollow Knight Silksong',120000.00,'Hornet_Idle.jpg','Aceptado',NULL,'2025-10-02 01:11:34',NULL),
(3,25,24,'Manilla','Oro','Quiero que esta manilla tenga un adorno con la figura de Hornet del videojuego titulado Hollow Knight Silksong',120000.00,'Hornet_Idle.jpg','Aceptado',NULL,'2025-10-02 01:21:05','2025-10-17'),
(4,25,24,'Collar','Plata y un dije','Quiero que este collar sea algo unico pero sin ser algo tan llamativo, lo quiero algo delgado y que el dije sea un nombre algo similar a la imagen adjunta',90000.00,'DNP-06.jpg','Rechazado','eso no fue muy so so 🗣️','2025-10-02 01:44:49',NULL),
(5,25,24,'Manilla','plata','Quiero que esta manilla sea sencilla pero con un nombre en el centro de ella, el nombre tiene que ser niyireth',80000.00,'ejemplo.jpg','Rechazado','Bro, no tengo manos XD','2025-10-02 01:59:52',NULL),
(6,25,24,'Cadena','Acero','Quiero que esta cadena tenga un estilo vikingo/nordico',100000.00,'71kXKyBRLlL._UF8941000_QL80_.jpg','Aceptado',NULL,'2025-10-02 02:03:51','2025-10-09'),
(7,25,23,'Seas Mamon','Mineral Palido 🗣️','Para entender la historia de Five Nights at Freddy\'s hay que olvidarse que estos son juegos y quiero que tomen realmente a esta saga como lo que es. ¿Terror? Sí, pero sobre todo, ciencia ficción. Antes de comenzar, quiero decir que esta cronología la realizamos entre 3 youtubers conocidos de Five Nights at Freddy\'s y yo. Por lo tanto, agradecería que si les gusta el contenido de este juego vayan a visitar sus canales. Ahora sí, empecemos. ¿Qué pasaría si dos amigos se abren una pizzería? Esa es la primera pregunta que hay que plantearnos. Lo normal sería que todo vaya medianamente bien con algún tipo de problemas, pero nada saldría más allá de eso. La pregunta cambia completamente si nos preguntamos ¿Qué pasaría si Henry y William abren una pizzería? ¿Quienes son estos personajes? En un principio, grandes amigos. Henry, por un lado, era un ferviente y talentoso mecánico que cuidaba a su única hija, Charlie. No sabemos nada de su esposa, ni siquiera si tiene a alguien más en su familia. Y por el otro lado, William Afton. La familia de Afton estaba compuesta por 5 miembros. William, una persona con mucho dinero y con buena capacidad para la mecánica. Su hija menor, Elizabeth. Este pendejo que no sabemos el nombre, pero llora todo el tiempo, así que vamos a ponerle Crying Child. Michael Afton, su hijo mayor y su esposa, de quien no se sabe nada. Estos dos personajes unieron sus capacidades de mecánicos y con el buen capital que tenía William ahorrado, entre los dos abrieron un restaurante. Así fue como entre los años 1980 a 1982, supuestamente, Fredbear Family Dinner abrió sus puertas. La principal atracción de este lugar eran los animatrónicos. ¿Que Son? Bueno, básicamente eran robots que podrían ser controlados tanto por ellos mismos como por personas o por almas. Estos animatrónicos habían sido desarrollados por los dueños del restaurante, pero Henry destacó un poco más debido a que hizo un complejo sistema de recursos que permitía a la persona usar estos trajes. Solamente que tenía que ser extremadamente cuidadosa, ya que de lo contrario el mecanismo del mismo se activaría y la persona que esté dentro seguramente quedaría lastimada. Estos trajes híbridos darían a luz en un principio a su principal éxito, Fredbear y Spring Bonnie. Dos animatrónicos que durante esos años 80 habían hecho furor y tan bien les estaba yendo a estos dos amigos que la competencia empezó a llegar. Y es por eso que a unos pocos meses de la salida de Fredbear Family Dinner llegaría su competencia, Fazbear Entertainment, pero que esta no sería relevante hasta en un futuro. En paralelo a estos hechos, empezaban a haber roces entre la dupla principal, ya que William no solamente había abierto el restaurante para comer, sino que detrás de sus intenciones de matar había algo mucho más oscuro, gente. Es por eso que en una fecha que desconocemos, William creó un nuevo local, Circus Baby Pizza World, y es en este donde presentaría sus nuevos animatrónicos, los Funtime. Estos animatrónicos estarían hechos bajo la empresa Afton Robotics, que como podrán imaginar, esta empresa era de William. Aunque los Funtime no eran animatrónicos normales, si tenían buenas características muy innovadoras con respecto a los primeros trajes híbridos, estos Funtime estarían creados específicamente para matar. Una inteligencia artificial muy avanzada, poder abrir diferentes partes de su cuerpo y la posibilidad de hablar. Claramente no tenían una buena intención, pero a William se le volvería todo en contra cuando el mismo día de la inauguración de su local, a pesar de sus advertencias a Elizabeth, esta entró igual al cuarto donde estaban los animatrónicos para ver si estaba su robot. favorito, bebé. Y luego de que este animatrónico le ofrece un helado para hacer que se acercara a ella, la mata. O bueno, no tanto. Mientras a todo esto, recordamos que William pensaba que ya todos los niños estaban capturados dentro de los animatrónicos, debido a que la apertura de su local había sido completamente exitosa. Entonces alerta a toda la gente de una fuga de gas para que así tengan que evacuar el local y él poder ir a ver su recompensa. Cuando William va a ver si sus animatrónicos habían capturado niños, sí, así es, habían capturado niños. Que eso lo sabemos debido a que en los planos de los animatrónicos aparecen cuerpos dentro de estos robots. Pero también William se daría cuenta de que su animatrónico principal había matado a Elizabeth. O en realidad, su hija estaba tomando el control de Baby debido a que los ojos del animatrónico pasarían de ser azules a como los tenía su hijita, verdes. Por supuesto que William al enterarse de todo esto no sabe qué hacer y es por eso que decide encerrarla en Circus Baby Entertainment, un lugar ubicado debajo de Circus Baby. Tras el cierre de Circus Baby y la incertidumbre de lo ocurrido con su hija menor, estas cosas empezarían a afectar a William Afton, dando comienzo a su declive. Por eso, luego del fracaso de Circus Baby, éste vuelve a pedirle ayuda y trabajo a Henry, que a pesar de todos los problemas que había tenido con su anterior socio, le da trabajo de administrador o mecánico, por eso se lo puede ver colocándole. la cabeza de Fredbear a uno de los empleados de Fredbear Family Dinner. Durante estos meses, de un año que suponemos que es 1883, Henry creó y anunció otros animatrónicos por la televisión, que serían Freddy, Foxy, Chica y Bonnie. Por supuesto que William, al ver que había creado más animatrónicos, crecería la tensión con su nuevo jefe, pero lo que realmente llevaría a William a ponerse de un tono violeta sería la muerte de su hijo menor, el pendejo que llora, Crying Child. . ¿Se acuerdan de Mike, el hijo mayor de William? Bueno, este personaje asustaba de manera sobre medida a Crying Child y mientras ésta atormentaba a su único hermano chico, William protegía de sobre manera a su hijo menor, poniendo cámaras por toda la casa y dándole un peluche creado por él mismo para que pueda hablarle y sentirse cómodo. Todo esto, a pesar del comportamiento psicópata de William, serviría para vigilar a su hijo menor y así que no se escapara a ver a los animatrónicos debido a que a Crying Child le fascinaban. Pero William, al haber creado con Henry los dos primeros trajes sabían lo que podían hacer y lo danino que eran, por eso las medidas de sobreprotección. Pero ahora vamos a remontarnos a una teoría entre Five Nights at Freddy\'s 4 y The Twisted Ones, el primer libro. Supuestamente, Five Nights at Freddy\'s 4 ocurriría en las pesadillas de Crying Child, pero la verdad es que no, las pesadillas esas que ve son reales y no un mal sueño de este niño, ya que son parte de un plan muy macabro de su padre. . Verán, en la novela de The Twisted Ones, William crea un disco que hace tener alucinaciones con animatrónicos, exagerando su forma, su tamaño, etc. Algo así como la película de Batman donde el espantapájaros tiene un spray que te hace sobredimensionar tus miedos. ¿Y cómo se relaciona esto con el juego? El tema de las alucinaciones, no Batman, no tiene nada que ver Batman acá. Bueno, tenemos que remontarnos a Five Nights at Freddy\'s Ultimate Custom Night, en donde los animatrónicos Nightmares aparecen en este juego, pero en este juego controlamos a William, entonces es imposible que William logre saber con exactitud cómo son estos animatrónicos si es que en realidad son las pesadillas de su hijo menor. En otras palabras, ¿cómo sabes exactamente las pesadillas de otras personas? Con lo cual, si volvemos al primer libro, nos presentamos que William creó discos ilusorios para hacer creer a la gente cosas que realmente no hay, y esto lo utilizaría con Crying Child para hacer que se aleje definitivamente de los animatrónicos. Por eso es que tampoco nunca lo vemos regañar a su hijo mayor por maltratar a su hermanito, debido a que este le estaba generando un trauma con los animatrónicos, cosa que a William le sirvió, aunque el error de William fue confiar demasiado en Michael, porque este no sabía dónde estaba el límite de la broma, ya que Mike asustaba a su hermano solamente por diversión, y el problema se desataría en ese año 83, en el lugar donde había comenzado y terminado todo, Fredbear Family Dinner. Mike y sus amigos llevan a Crying Child por la fuerza al restaurante para seguir molestándolos con los animatrónicos en el día de su cumpleaños, y siguiendo con la broma, lo ponen en la boca de Fredbear simulando que se lo iba a comer, y desgraciadamente no. solo simulo eso. Como había dicho en un principio, el sistema de recurso de Henry era sensato, por lo que al introducir un niño dentro de la boca, el traje se cerró en la cabeza de Crying Child, que luego de eso, el mini Afton entra en un estado de coma donde están todos los animatrónicos que él conoció y el peluche que le había regalado William, donde en esta pantalla se da a entender como que su padre le está dedicando las últimas palabras a su hijo, pidiéndole que lo perdone, y diciendo dos frases que quedarían para muchísimas teorías. Vos estás roto, yo te reconstruiré. Por supuesto que esto lo dice debido a que a partir de la muerte de Elizabeth, él sabía que de alguna forma los animatrónicos lograban tomar el alma de la persona y adaptarla a su cuerpo, o por lo menos ahí alma y animatrónico convivían en un solo. cuerpo. Una curiosidad de esta parte de la historia es que como estamos en 1983, si recorremos la casa de los Afton, nos vamos a encontrar con un cuarto que da a entender que es de una niña, y quién era la única niña que tenía la familia. Afton, Elizabeth Afton. Por lo tanto, antes de ese 1983, la hija de William ya estaba dentro del cuerpo de Baby.',1.00,'Troleador_cara.jpg','Pendiente',NULL,'2025-10-02 02:08:27',NULL),
(8,25,15,'Seas Mamon','Mineral Palido 🗣️','Para entender la historia de Five Nights at Freddy\'s hay que olvidarse que estos son juegos y quiero que tomen realmente a esta saga como lo que es. ¿Terror? Sí, pero sobre todo, ciencia ficción. Antes de comenzar, quiero decir que esta cronología la realizamos entre 3 youtubers conocidos de Five Nights at Freddy\'s y yo. Por lo tanto, agradecería que si les gusta el contenido de este juego vayan a visitar sus canales. Ahora sí, empecemos. ¿Qué pasaría si dos amigos se abren una pizzería? Esa es la primera pregunta que hay que plantearnos. Lo normal sería que todo vaya medianamente bien con algún tipo de problemas, pero nada saldría más allá de eso. La pregunta cambia completamente si nos preguntamos ¿Qué pasaría si Henry y William abren una pizzería? ¿Quienes son estos personajes? En un principio, grandes amigos. Henry, por un lado, era un ferviente y talentoso mecánico que cuidaba a su única hija, Charlie. No sabemos nada de su esposa, ni siquiera si tiene a alguien más en su familia. Y por el otro lado, William Afton. La familia de Afton estaba compuesta por 5 miembros. William, una persona con mucho dinero y con buena capacidad para la mecánica. Su hija menor, Elizabeth. Este pendejo que no sabemos el nombre, pero llora todo el tiempo, así que vamos a ponerle Crying Child. Michael Afton, su hijo mayor y su esposa, de quien no se sabe nada. Estos dos personajes unieron sus capacidades de mecánicos y con el buen capital que tenía William ahorrado, entre los dos abrieron un restaurante. Así fue como entre los años 1980 a 1982, supuestamente, Fredbear Family Dinner abrió sus puertas. La principal atracción de este lugar eran los animatrónicos. ¿Que Son? Bueno, básicamente eran robots que podrían ser controlados tanto por ellos mismos como por personas o por almas. Estos animatrónicos habían sido desarrollados por los dueños del restaurante, pero Henry destacó un poco más debido a que hizo un complejo sistema de recursos que permitía a la persona usar estos trajes. Solamente que tenía que ser extremadamente cuidadosa, ya que de lo contrario el mecanismo del mismo se activaría y la persona que esté dentro seguramente quedaría lastimada. Estos trajes híbridos darían a luz en un principio a su principal éxito, Fredbear y Spring Bonnie. Dos animatrónicos que durante esos años 80 habían hecho furor y tan bien les estaba yendo a estos dos amigos que la competencia empezó a llegar. Y es por eso que a unos pocos meses de la salida de Fredbear Family Dinner llegaría su competencia, Fazbear Entertainment, pero que esta no sería relevante hasta en un futuro. En paralelo a estos hechos, empezaban a haber roces entre la dupla principal, ya que William no solamente había abierto el restaurante para comer, sino que detrás de sus intenciones de matar había algo mucho más oscuro, gente. Es por eso que en una fecha que desconocemos, William creó un nuevo local, Circus Baby Pizza World, y es en este donde presentaría sus nuevos animatrónicos, los Funtime. Estos animatrónicos estarían hechos bajo la empresa Afton Robotics, que como podrán imaginar, esta empresa era de William. Aunque los Funtime no eran animatrónicos normales, si tenían buenas características muy innovadoras con respecto a los primeros trajes híbridos, estos Funtime estarían creados específicamente para matar. Una inteligencia artificial muy avanzada, poder abrir diferentes partes de su cuerpo y la posibilidad de hablar. Claramente no tenían una buena intención, pero a William se le volvería todo en contra cuando el mismo día de la inauguración de su local, a pesar de sus advertencias a Elizabeth, esta entró igual al cuarto donde estaban los animatrónicos para ver si estaba su robot. favorito, bebé. Y luego de que este animatrónico le ofrece un helado para hacer que se acercara a ella, la mata. O bueno, no tanto. Mientras a todo esto, recordamos que William pensaba que ya todos los niños estaban capturados dentro de los animatrónicos, debido a que la apertura de su local había sido completamente exitosa. Entonces alerta a toda la gente de una fuga de gas para que así tengan que evacuar el local y él poder ir a ver su recompensa. Cuando William va a ver si sus animatrónicos habían capturado niños, sí, así es, habían capturado niños. Que eso lo sabemos debido a que en los planos de los animatrónicos aparecen cuerpos dentro de estos robots. Pero también William se daría cuenta de que su animatrónico principal había matado a Elizabeth. O en realidad, su hija estaba tomando el control de Baby debido a que los ojos del animatrónico pasarían de ser azules a como los tenía su hijita, verdes. Por supuesto que William al enterarse de todo esto no sabe qué hacer y es por eso que decide encerrarla en Circus Baby Entertainment, un lugar ubicado debajo de Circus Baby. Tras el cierre de Circus Baby y la incertidumbre de lo ocurrido con su hija menor, estas cosas empezarían a afectar a William Afton, dando comienzo a su declive. Por eso, luego del fracaso de Circus Baby, éste vuelve a pedirle ayuda y trabajo a Henry, que a pesar de todos los problemas que había tenido con su anterior socio, le da trabajo de administrador o mecánico, por eso se lo puede ver colocándole. la cabeza de Fredbear a uno de los empleados de Fredbear Family Dinner. Durante estos meses, de un año que suponemos que es 1883, Henry creó y anunció otros animatrónicos por la televisión, que serían Freddy, Foxy, Chica y Bonnie. Por supuesto que William, al ver que había creado más animatrónicos, crecería la tensión con su nuevo jefe, pero lo que realmente llevaría a William a ponerse de un tono violeta sería la muerte de su hijo menor, el pendejo que llora, Crying Child. . ¿Se acuerdan de Mike, el hijo mayor de William? Bueno, este personaje asustaba de manera sobre medida a Crying Child y mientras ésta atormentaba a su único hermano chico, William protegía de sobre manera a su hijo menor, poniendo cámaras por toda la casa y dándole un peluche creado por él mismo para que pueda hablarle y sentirse cómodo. Todo esto, a pesar del comportamiento psicópata de William, serviría para vigilar a su hijo menor y así que no se escapara a ver a los animatrónicos debido a que a Crying Child le fascinaban. Pero William, al haber creado con Henry los dos primeros trajes sabían lo que podían hacer y lo danino que eran, por eso las medidas de sobreprotección. Pero ahora vamos a remontarnos a una teoría entre Five Nights at Freddy\'s 4 y The Twisted Ones, el primer libro. Supuestamente, Five Nights at Freddy\'s 4 ocurriría en las pesadillas de Crying Child, pero la verdad es que no, las pesadillas esas que ve son reales y no un mal sueño de este niño, ya que son parte de un plan muy macabro de su padre. . Verán, en la novela de The Twisted Ones, William crea un disco que hace tener alucinaciones con animatrónicos, exagerando su forma, su tamaño, etc. Algo así como la película de Batman donde el espantapájaros tiene un spray que te hace sobredimensionar tus miedos. ¿Y cómo se relaciona esto con el juego? El tema de las alucinaciones, no Batman, no tiene nada que ver Batman acá. Bueno, tenemos que remontarnos a Five Nights at Freddy\'s Ultimate Custom Night, en donde los animatrónicos Nightmares aparecen en este juego, pero en este juego controlamos a William, entonces es imposible que William logre saber con exactitud cómo son estos animatrónicos si es que en realidad son las pesadillas de su hijo menor. En otras palabras, ¿cómo sabes exactamente las pesadillas de otras personas? Con lo cual, si volvemos al primer libro, nos presentamos que William creó discos ilusorios para hacer creer a la gente cosas que realmente no hay, y esto lo utilizaría con Crying Child para hacer que se aleje definitivamente de los animatrónicos. Por eso es que tampoco nunca lo vemos regañar a su hijo mayor por maltratar a su hermanito, debido a que este le estaba generando un trauma con los animatrónicos, cosa que a William le sirvió, aunque el error de William fue confiar demasiado en Michael, porque este no sabía dónde estaba el límite de la broma, ya que Mike asustaba a su hermano solamente por diversión, y el problema se desataría en ese año 83, en el lugar donde había comenzado y terminado todo, Fredbear Family Dinner. Mike y sus amigos llevan a Crying Child por la fuerza al restaurante para seguir molestándolos con los animatrónicos en el día de su cumpleaños, y siguiendo con la broma, lo ponen en la boca de Fredbear simulando que se lo iba a comer, y desgraciadamente no. solo simulo eso. Como había dicho en un principio, el sistema de recurso de Henry era sensato, por lo que al introducir un niño dentro de la boca, el traje se cerró en la cabeza de Crying Child, que luego de eso, el mini Afton entra en un estado de coma donde están todos los animatrónicos que él conoció y el peluche que le había regalado William, donde en esta pantalla se da a entender como que su padre le está dedicando las últimas palabras a su hijo, pidiéndole que lo perdone, y diciendo dos frases que quedarían para muchísimas teorías. Vos estás roto, yo te reconstruiré. Por supuesto que esto lo dice debido a que a partir de la muerte de Elizabeth, él sabía que de alguna forma los animatrónicos lograban tomar el alma de la persona y adaptarla a su cuerpo, o por lo menos ahí alma y animatrónico convivían en un solo. cuerpo. Una curiosidad de esta parte de la historia es que como estamos en 1983, si recorremos la casa de los Afton, nos vamos a encontrar con un cuarto que da a entender que es de una niña, y quién era la única niña que tenía la familia. Afton, Elizabeth Afton. Por lo tanto, antes de ese 1983, la hija de William ya estaba dentro del cuerpo de Baby.',1.00,'Troleador_cara.jpg','Pendiente',NULL,'2025-10-02 04:10:25',NULL),
(9,25,22,'Cadena','Oro','Quiero que esta cadena cuente con eslabones ',3000000.00,'images.png','Pendiente',NULL,'2025-10-02 16:34:35',NULL);
/*!40000 ALTER TABLE `pedidos_personalizados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `piedras`
--

DROP TABLE IF EXISTS `piedras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `piedras` (
  `id_piedra` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_piedra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `piedras`
--

LOCK TABLES `piedras` WRITE;
/*!40000 ALTER TABLE `piedras` DISABLE KEYS */;
/*!40000 ALTER TABLE `piedras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_colores`
--

DROP TABLE IF EXISTS `producto_colores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_colores` (
  `id_producto` int(11) NOT NULL,
  `id_color` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`,`id_color`),
  KEY `id_color` (`id_color`),
  CONSTRAINT `producto_colores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `producto_colores_ibfk_2` FOREIGN KEY (`id_color`) REFERENCES `colores` (`id_color`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_colores`
--

LOCK TABLES `producto_colores` WRITE;
/*!40000 ALTER TABLE `producto_colores` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto_colores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_piedras`
--

DROP TABLE IF EXISTS `producto_piedras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_piedras` (
  `id_producto` int(11) NOT NULL,
  `id_piedra` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`,`id_piedra`),
  KEY `id_piedra` (`id_piedra`),
  CONSTRAINT `producto_piedras_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `producto_piedras_ibfk_2` FOREIGN KEY (`id_piedra`) REFERENCES `piedras` (`id_piedra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_piedras`
--

LOCK TABLES `producto_piedras` WRITE;
/*!40000 ALTER TABLE `producto_piedras` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto_piedras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_promocion`
--

DROP TABLE IF EXISTS `producto_promocion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_promocion` (
  `id_producto` int(11) NOT NULL,
  `id_promocion` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`,`id_promocion`),
  KEY `id_promocion` (`id_promocion`),
  CONSTRAINT `producto_promocion_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `producto_promocion_ibfk_2` FOREIGN KEY (`id_promocion`) REFERENCES `promociones` (`id_promocion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_promocion`
--

LOCK TABLES `producto_promocion` WRITE;
/*!40000 ALTER TABLE `producto_promocion` DISABLE KEYS */;
INSERT INTO `producto_promocion` VALUES
(1,1),
(1,2),
(2,1),
(2,4),
(3,2),
(3,5),
(4,3),
(5,3);
/*!40000 ALTER TABLE `producto_promocion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_talla`
--

DROP TABLE IF EXISTS `producto_talla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_talla` (
  `id_producto` int(11) NOT NULL,
  `id_talla` int(11) NOT NULL,
  PRIMARY KEY (`id_producto`,`id_talla`),
  KEY `id_talla` (`id_talla`),
  CONSTRAINT `producto_talla_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `producto_talla_ibfk_2` FOREIGN KEY (`id_talla`) REFERENCES `tallas` (`id_talla`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_talla`
--

LOCK TABLES `producto_talla` WRITE;
/*!40000 ALTER TABLE `producto_talla` DISABLE KEYS */;
INSERT INTO `producto_talla` VALUES
(1,2),
(1,3),
(2,2),
(3,4),
(4,1),
(4,3),
(5,5);
/*!40000 ALTER TABLE `producto_talla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
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
  `id_usuario` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `id_tipo` (`id_tipo`),
  KEY `id_material` (`id_material`),
  KEY `fk_producto_usuario` (`id_usuario`),
  CONSTRAINT `fk_producto_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipos_joya` (`id_tipo`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_material`) REFERENCES `materiales` (`id_material`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES
(1,'Anillo Clásico Oro','Anillo elegante de oro 18k',350000.00,0.05,0.00,0.00,0.00,'2x2x2cm','AOR001',10,5,1,1,1,NULL,NULL),
(2,'Collar Corazón Plata','Collar con dije en forma de corazón',120000.00,0.1,0.00,0.00,0.00,'5x5x1cm','CPL002',3,5,2,2,1,NULL,NULL),
(3,'Pulsera Acero Fina','Pulsera unisex en acero inoxidable',95000.00,0.08,0.00,0.00,0.00,'4x4x2cm','PAC003',18,5,3,3,1,NULL,NULL),
(4,'Aretes Rubí','Aretes con incrustaciones de rubí',470000.00,0.03,0.00,0.00,0.00,'2x2x1cm','ARU004',5,5,4,4,1,NULL,NULL),
(5,'Broche Hoja','Broche de hoja con material ecológico',80000.00,0.02,0.00,0.00,0.00,'3x3x1cm','BHO005',11,5,5,5,1,NULL,NULL),
(6,'Cadenita','SHAW',98000.00,NULL,0.00,0.00,0.00,NULL,NULL,32,5,NULL,NULL,24,NULL,NULL),
(7,'Cadena ','Cadena nordica asi bien aqui asi bien chavalona',120000.00,NULL,0.00,0.00,0.00,NULL,NULL,7,5,NULL,NULL,24,'71kXKyBRLlL._UF8941000_QL80_.jpg',NULL),
(10,'Cadena ','Una cadena de la SHAW',90000.00,NULL,0.00,0.00,0.00,NULL,NULL,20,5,NULL,NULL,24,'Hornet_Idle.jpg','Cadenas');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promociones`
--

DROP TABLE IF EXISTS `promociones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `promociones` (
  `id_promocion` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `activa` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_promocion`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promociones`
--

LOCK TABLES `promociones` WRITE;
/*!40000 ALTER TABLE `promociones` DISABLE KEYS */;
INSERT INTO `promociones` VALUES
(1,'D?a de la Madre','10% de descuento en anillos y collares','2024-05-01','2024-05-10',1),
(2,'Semana del Oro','15% descuento en todos los productos de oro','2024-06-01','2024-06-07',1),
(3,'Black Friday','Hasta 50% en joyas seleccionadas','2024-11-25','2024-11-30',1),
(4,'Navidad Especial','20% en colecciones de invierno','2024-12-15','2024-12-31',1),
(5,'A?o Nuevo','5% de descuento adicional','2025-01-01','2025-01-05',1);
/*!40000 ALTER TABLE `promociones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `nit` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES
(1,'Joyas Medell?n Ltda.','800123456','6044448899','contacto@joyamedellin.com','Calle 30 #70-15'),
(2,'Insumos Joya S.A.S.','900876543','6019998899','ventas@insujoyas.com','Carrera 40 #10-20'),
(3,'Metales del Norte','830112233','6051112233','info@metalesnorte.com','Av. Norte #10-10'),
(4,'Piedras Preciosas Co.','820332211','6023332211','pedidos@piedrasco.com','Calle de las Piedras #5'),
(5,'EcoMateriales S.A.','840998877','6069988776','hola@ecomateriales.com','Vereda El Bosque');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES
(1,'Administrador'),
(2,'Vendedor'),
(3,'Cliente'),
(4,'Soporte'),
(5,'Invitado');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tallas`
--

DROP TABLE IF EXISTS `tallas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tallas` (
  `id_talla` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_talla` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_talla`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tallas`
--

LOCK TABLES `tallas` WRITE;
/*!40000 ALTER TABLE `tallas` DISABLE KEYS */;
INSERT INTO `tallas` VALUES
(1,'XS'),
(2,'S'),
(3,'M'),
(4,'L'),
(5,'XL');
/*!40000 ALTER TABLE `tallas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_joya`
--

DROP TABLE IF EXISTS `tipos_joya`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_joya` (
  `id_tipo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_tipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_joya`
--

LOCK TABLES `tipos_joya` WRITE;
/*!40000 ALTER TABLE `tipos_joya` DISABLE KEYS */;
INSERT INTO `tipos_joya` VALUES
(1,'Anillo'),
(2,'Collar'),
(3,'Pulsera'),
(4,'Arete'),
(5,'Broche');
/*!40000 ALTER TABLE `tipos_joya` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokens_recuperacion`
--

DROP TABLE IF EXISTS `tokens_recuperacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokens_recuperacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `token` varchar(20) NOT NULL,
  `expira` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `tokens_recuperacion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens_recuperacion`
--

LOCK TABLES `tokens_recuperacion` WRITE;
/*!40000 ALTER TABLE `tokens_recuperacion` DISABLE KEYS */;
INSERT INTO `tokens_recuperacion` VALUES
(5,13,'6fdcaa33','2025-09-07 21:54:58'),
(9,15,'148fa6cb','2025-09-08 06:56:38'),
(10,16,'e2ca1dc7','2025-09-08 07:01:33'),
(12,18,'e17e96e1','2025-09-09 16:32:44'),
(17,24,'ccde3c88','2025-10-02 01:14:18'),
(18,24,'c2eef339','2025-10-02 01:19:04');
/*!40000 ALTER TABLE `tokens_recuperacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES
(1,'Juan P?rez','juan@ave.com','3001112233','clave123','Calle 123',1,1),
(2,'Ana G?mez','ana@ave.com','3000000000','clave123','Carrera 45',0,2),
(3,'Luis Rojas','luis@ave.com','3003334455','clave123','Av. Norte 9',0,3),
(4,'Luc?a D?az','lucia@ave.com','3004445566','clave123','Nueva Direcci?n 456',1,3),
(5,'Soporte AVE','soporte@ave.com','3005556677','clave123','Oficina 5',1,4),
(9,'Keinner Santiago','keinner@ave.com','1234567890','scrypt:32768:8:1$RSHF9SWKA5uBgcju$399aeb09899861ac8d72917a892afac9373455001f1449e9d345520410a3c60b0305adcad23e411fb332a8da4c58d09a6b36652bd3943c5324d81417d8246a13','su casa ',0,3),
(10,'Esteban Espitia','esteban@ave.com','0987654321','scrypt:32768:8:1$HUuf65it9zjSZUUB$d8fee9e6d6ea1b27f9f634005a31cf2f8b063ae14c7f62e06043e1e79351c3178b609f7b1c44fc9e95e8d2b97a9938fe20018dfd465bce476c0e0397551c9d4d','Suba (Es un Cerro)',0,1),
(11,'Uldarico Andrade','uldarico@gmail.com','7890123456','scrypt:32768:8:1$UVX3mRSPAJ0qlwpq$8ed58f7e3f51eebb0a0bae844f9f90017a05969e8deea64a33c823ab4810a43b7ea914985d3e9a6a71a6704a9b008fbeaa024c3eec0ced58299c1c8c6894318d','carrera del amorch',0,3),
(12,'Danna Gabriela','dannagb@gmail.com','1234567890','scrypt:32768:8:1$Zkl79IRpzx4UV2q2$65b9399dbda0e5d9ff880f88b14c8c0509d14c3be7d66b7bfcdcb17f474c168fc7bd5621f4bac88fb9104c9edcb627e3358f64d392790233b8982bd0700cabb6','Cerru',0,2),
(13,'Maria Teresa','juancamilogarciabonilla54@gmail.com','+573194988478','scrypt:32768:8:1$Jx3ubUv7XhrfxUgh$cb4dffe8b7ad00a5901f1c1ac54f006eb5698e5bfe09872582b9546a3eddbbfe3537f5f8dd3d2a6be2aa5372ea10534aa1a1e7e0575146e8c4cc1f0423a2b5aa','Suba (En la falda del Cerro)',0,1),
(15,'Keinner Perez','keinnerrodriguez0916@gmail.com','+573245019909','scrypt:32768:8:1$sykbyu6lLeIf8Ip8$27a7fd82e4bdb70bce32d64c58a0365bc5ff2a98d46b78f61ea38100ec9ccbe51e2963b5206e94f3d909d666c54a600518862380eb62bd8e3a6683ed6942f209','Portal 80',0,2),
(16,'Samuel Mari?o','samuel.e.marino@hotmail.com','+573212136560','scrypt:32768:8:1$zCFvMCLKDsOKc6j3$a22b2dac2a4757647bb6ee408082ac9f373253b4ed9d094bf9e9ccdb55b9eefe9b40e35098f478265f3ddc94669a0aa636969f39098f85042b02ac211bcfdf8e','Bosa',0,1),
(17,'Luis Garcia','luis.garcia@gmail.com','+5712340987654','scrypt:32768:8:1$9m3QskmkdBnF2v16$ed669e720f10627a9ecb6ad25a770167c2ee812efccdb37e99250e4bedc14ac21b560657784c3c9cbf0e36102d7ca56f70859429505b7218e9c56ad70387e425','Casa',0,1),
(18,'Maria Bonilla','matebojejuda123@gmail.com','+57097327647','scrypt:32768:8:1$wd1GIWxJNcZAXUy7$64ae89d9d7a160750c02296b4edbc64d72a7387c1a6961edc20b5a27e4d411ec67d19d1f58a1a45328ebdb2fcd5c926f23a180864773ae9a108b1837e84c6245','Casa',0,1),
(20,'jhon','jhon@ave.com','+573506257556','scrypt:32768:8:1$ORAZ1tBwMtgF8UP8$7e95fe4eae0acdab5d34d19fc33996bfc0c1265aedb59ef76b7291aa498d8e5b8ad769d9d4c5ed3af2066cd52cf4b3ed752f3f3e17dd8641ed7e92443963cca8','xd',0,2),
(21,'Nicole Quiroga','paolakimoficial@gmail.com','+573007151138','scrypt:32768:8:1$a8N2mO0IJVSvMlhU$22521088b02de3e4516418e69c8066b7e9bb2513fd08e40de70329f0d1a63f5cbcac94a7336fda2712fab1774f62c7b96fa35e0b536eadc32dc8432f8b878779','casa xd',0,3),
(22,'Juan Garcia','juancgb2007@gmail.com','+573194988478','scrypt:32768:8:1$QCFlm3rymKtIJdGf$08ebc944ddea26d65b106266d7bbaac04a81bc62bc638a29bbb15afe85bc6b98edc7c44ce8e64d9ad5c7908451d1f5f9643f1f0636c463f7dcde72ceb414eea6','Cerru Premium',0,2),
(23,'esteban espitia ','estebanof2005@gmail.com','+573506257556','scrypt:32768:8:1$SQM6CMvBpHOeHEpq$70f7b559b8abc1ad805816b59b53a7b6e9748798986845f63ec181c23043538464f61e24757d7824c4dc08137f79d46e14d6c77b7038b10732fc52086189a409','suba (cerro)',0,2),
(24,'Juan Garcia','juanpgr768@gmail.com','+57091234782','scrypt:32768:8:1$47dkFKyVYWgqEuTg$c9200e415aa47cb7ee2568c957fe98ac4d4011fb262e286cdcd0b4efc3e133e63884f51801fd2579691519375a4e8643f206927cdce120d9e94856dff464e22d','Cerru Premium',1,2),
(25,'Juan Bonilla','juancgb.drive@gmail.com','+57984208924','scrypt:32768:8:1$UGkjjjVuIq1JfxFa$2b7572d5a3ab4cf801b3b27a63b70063b0eaab97c1398040451113f0423da161795894ca8608e6650c102bf82d25e74e80dce47c4cc87e8d663061bb32a74a34','Mi casita ',1,3);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `vista_bitacora_usuarios`
--

DROP TABLE IF EXISTS `vista_bitacora_usuarios`;
/*!50001 DROP VIEW IF EXISTS `vista_bitacora_usuarios`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_bitacora_usuarios` AS SELECT
 1 AS `id_log`,
  1 AS `nombre_completo`,
  1 AS `accion`,
  1 AS `modulo`,
  1 AS `fecha` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_clientes_contacto`
--

DROP TABLE IF EXISTS `vista_clientes_contacto`;
/*!50001 DROP VIEW IF EXISTS `vista_clientes_contacto`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_clientes_contacto` AS SELECT
 1 AS `nombre_completo`,
  1 AS `correo`,
  1 AS `telefono_contacto` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_detalle_pedido_extendido`
--

DROP TABLE IF EXISTS `vista_detalle_pedido_extendido`;
/*!50001 DROP VIEW IF EXISTS `vista_detalle_pedido_extendido`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_detalle_pedido_extendido` AS SELECT
 1 AS `id_pedido`,
  1 AS `producto`,
  1 AS `cantidad`,
  1 AS `precio_unitario`,
  1 AS `id_talla` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_ordenes_proveedor`
--

DROP TABLE IF EXISTS `vista_ordenes_proveedor`;
/*!50001 DROP VIEW IF EXISTS `vista_ordenes_proveedor`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_ordenes_proveedor` AS SELECT
 1 AS `id_orden`,
  1 AS `proveedor`,
  1 AS `fecha`,
  1 AS `estado` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_pedidos_clientes`
--

DROP TABLE IF EXISTS `vista_pedidos_clientes`;
/*!50001 DROP VIEW IF EXISTS `vista_pedidos_clientes`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_pedidos_clientes` AS SELECT
 1 AS `id_pedido`,
  1 AS `cliente`,
  1 AS `fecha`,
  1 AS `estado`,
  1 AS `total` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_productos_completos`
--

DROP TABLE IF EXISTS `vista_productos_completos`;
/*!50001 DROP VIEW IF EXISTS `vista_productos_completos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_productos_completos` AS SELECT
 1 AS `id_producto`,
  1 AS `nombre`,
  1 AS `descripcion`,
  1 AS `precio`,
  1 AS `stock`,
  1 AS `tipo_joya`,
  1 AS `material` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_productos_mas_vendidos`
--

DROP TABLE IF EXISTS `vista_productos_mas_vendidos`;
/*!50001 DROP VIEW IF EXISTS `vista_productos_mas_vendidos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_productos_mas_vendidos` AS SELECT
 1 AS `nombre`,
  1 AS `total_vendido` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_productos_promocion`
--

DROP TABLE IF EXISTS `vista_productos_promocion`;
/*!50001 DROP VIEW IF EXISTS `vista_productos_promocion`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_productos_promocion` AS SELECT
 1 AS `producto`,
  1 AS `promocion`,
  1 AS `fecha_inicio`,
  1 AS `fecha_fin` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_promociones_activas`
--

DROP TABLE IF EXISTS `vista_promociones_activas`;
/*!50001 DROP VIEW IF EXISTS `vista_promociones_activas`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_promociones_activas` AS SELECT
 1 AS `titulo`,
  1 AS `descripcion`,
  1 AS `fecha_inicio`,
  1 AS `fecha_fin` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_stock_bajo`
--

DROP TABLE IF EXISTS `vista_stock_bajo`;
/*!50001 DROP VIEW IF EXISTS `vista_stock_bajo`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_stock_bajo` AS SELECT
 1 AS `id_producto`,
  1 AS `nombre`,
  1 AS `stock` */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vista_bitacora_usuarios`
--

/*!50001 DROP VIEW IF EXISTS `vista_bitacora_usuarios`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_bitacora_usuarios` AS select `b`.`id_log` AS `id_log`,`u`.`nombre_completo` AS `nombre_completo`,`b`.`accion` AS `accion`,`b`.`modulo` AS `modulo`,`b`.`fecha` AS `fecha` from (`bitacora` `b` join `usuarios` `u` on(`b`.`id_usuario` = `u`.`id_usuario`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_clientes_contacto`
--

/*!50001 DROP VIEW IF EXISTS `vista_clientes_contacto`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_clientes_contacto` AS select `u`.`nombre_completo` AS `nombre_completo`,`u`.`correo` AS `correo`,`u`.`telefono_contacto` AS `telefono_contacto` from (`clientes` `c` join `usuarios` `u` on(`c`.`id_usuario` = `u`.`id_usuario`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_detalle_pedido_extendido`
--

/*!50001 DROP VIEW IF EXISTS `vista_detalle_pedido_extendido`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_detalle_pedido_extendido` AS select `dp`.`id_pedido` AS `id_pedido`,`pr`.`nombre` AS `producto`,`dp`.`cantidad` AS `cantidad`,`dp`.`precio_unitario` AS `precio_unitario`,`dp`.`id_talla` AS `id_talla` from (`detalle_pedido` `dp` join `productos` `pr` on(`dp`.`id_producto` = `pr`.`id_producto`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_ordenes_proveedor`
--

/*!50001 DROP VIEW IF EXISTS `vista_ordenes_proveedor`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_ordenes_proveedor` AS select `o`.`id_orden` AS `id_orden`,`pr`.`nombre` AS `proveedor`,`o`.`fecha` AS `fecha`,`o`.`estado` AS `estado` from (`ordenes_compra` `o` join `proveedores` `pr` on(`o`.`id_proveedor` = `pr`.`id_proveedor`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_pedidos_clientes`
--

/*!50001 DROP VIEW IF EXISTS `vista_pedidos_clientes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_pedidos_clientes` AS select `pe`.`id_pedido` AS `id_pedido`,`u`.`nombre_completo` AS `cliente`,`pe`.`fecha` AS `fecha`,`pe`.`estado` AS `estado`,`pe`.`total` AS `total` from ((`pedidos` `pe` join `clientes` `c` on(`pe`.`id_cliente` = `c`.`id_cliente`)) join `usuarios` `u` on(`c`.`id_usuario` = `u`.`id_usuario`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_productos_completos`
--

/*!50001 DROP VIEW IF EXISTS `vista_productos_completos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_productos_completos` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre`,`p`.`descripcion` AS `descripcion`,`p`.`precio` AS `precio`,`p`.`stock` AS `stock`,`t`.`nombre_tipo` AS `tipo_joya`,`m`.`nombre_material` AS `material` from ((`productos` `p` join `tipos_joya` `t` on(`p`.`id_tipo` = `t`.`id_tipo`)) join `materiales` `m` on(`p`.`id_material` = `m`.`id_material`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_productos_mas_vendidos`
--

/*!50001 DROP VIEW IF EXISTS `vista_productos_mas_vendidos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_productos_mas_vendidos` AS select `p`.`nombre` AS `nombre`,sum(`dp`.`cantidad`) AS `total_vendido` from (`detalle_pedido` `dp` join `productos` `p` on(`dp`.`id_producto` = `p`.`id_producto`)) group by `dp`.`id_producto` order by sum(`dp`.`cantidad`) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_productos_promocion`
--

/*!50001 DROP VIEW IF EXISTS `vista_productos_promocion`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_productos_promocion` AS select `p`.`nombre` AS `producto`,`pr`.`titulo` AS `promocion`,`pr`.`fecha_inicio` AS `fecha_inicio`,`pr`.`fecha_fin` AS `fecha_fin` from ((`productos` `p` join `producto_promocion` `pp` on(`p`.`id_producto` = `pp`.`id_producto`)) join `promociones` `pr` on(`pp`.`id_promocion` = `pr`.`id_promocion`)) where `pr`.`activa` = 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_promociones_activas`
--

/*!50001 DROP VIEW IF EXISTS `vista_promociones_activas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_promociones_activas` AS select `promociones`.`titulo` AS `titulo`,`promociones`.`descripcion` AS `descripcion`,`promociones`.`fecha_inicio` AS `fecha_inicio`,`promociones`.`fecha_fin` AS `fecha_fin` from `promociones` where `promociones`.`activa` = 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_stock_bajo`
--

/*!50001 DROP VIEW IF EXISTS `vista_stock_bajo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_stock_bajo` AS select `productos`.`id_producto` AS `id_producto`,`productos`.`nombre` AS `nombre`,`productos`.`stock` AS `stock` from `productos` where `productos`.`stock` < 10 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-03  1:38:16
