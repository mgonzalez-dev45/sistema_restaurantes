-- Base de datos: restaurante
-- Script completo de creación de tablas para "Paso Gourmet"

CREATE DATABASE IF NOT EXISTS `restaurante` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `restaurante`;

-- 1. Tabla de Platos (Carta gastronómica autogestionable)
CREATE TABLE IF NOT EXISTS `platos` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `precio` INT NOT NULL,
  `imagen` VARCHAR(100) NOT NULL DEFAULT 'milanesa.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabla de Reservas (Solicitudes de mesas enviadas desde /reservas)
CREATE TABLE IF NOT EXISTS `reservas` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `telefono` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `fecha` DATE NOT NULL,
  `hora` VARCHAR(10) NOT NULL,
  `personas` INT NOT NULL,
  `lugar` VARCHAR(20) NOT NULL DEFAULT 'salon',
  `silla_bebe` VARCHAR(5) NOT NULL DEFAULT 'no',
  `comentarios` TEXT,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabla de Mensajes (Consultas enviadas desde /contacto)
CREATE TABLE IF NOT EXISTS `mensajes` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `telefono` VARCHAR(50),
  `motivo` VARCHAR(50) NOT NULL,
  `mensaje` TEXT NOT NULL,
  `respuesta` VARCHAR(20) NOT NULL DEFAULT 'correo',
  `fecha_envio` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
