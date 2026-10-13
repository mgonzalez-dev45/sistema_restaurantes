-- =================================================================
-- PASO GOURMET - Base de datos 'pasogourmet'
-- Se ejecuta una sola vez (en phpMyAdmin > Importar, o con
-- mysql -u root < schema.sql). Se puede volver a ejecutar sin romper
-- los datos que ya existan.
-- =================================================================

CREATE DATABASE IF NOT EXISTS pasogourmet
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pasogourmet;

-- ---------- CATEGORÍAS DE LA CARTA ----------
CREATE TABLE IF NOT EXISTS categorias (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  orden  TINYINT NOT NULL DEFAULT 0          -- orden en que se muestran en la carta
);

-- ---------- PLATOS (RF03 / RF05) ----------
CREATE TABLE IF NOT EXISTS platos (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  categoria_id INT NOT NULL,
  nombre       VARCHAR(80)  NOT NULL,
  descripcion  VARCHAR(255) NOT NULL,
  precio       DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  imagen       VARCHAR(100) NOT NULL,        -- nombre del archivo dentro de static/uploads
  imagen_alt   VARCHAR(160) NOT NULL,        -- texto alternativo (accesibilidad)
  disponible   TINYINT(1) NOT NULL DEFAULT 1,  -- 0 = no se muestra en la carta
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- ---------- RESERVAS (RF04 / RF06) ----------
CREATE TABLE IF NOT EXISTS reservas (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  telefono    VARCHAR(30)  NOT NULL,
  email       VARCHAR(120) NOT NULL,
  fecha       DATE NOT NULL,
  hora        TIME NOT NULL,
  comensales  TINYINT UNSIGNED NOT NULL CHECK (comensales BETWEEN 1 AND 20),
  lugar       ENUM('salon','patio') NOT NULL DEFAULT 'salon',
  silla_bebe  TINYINT(1) NOT NULL DEFAULT 0,
  comentarios TEXT NULL,
  estado      ENUM('pendiente','confirmada','rechazada') NOT NULL DEFAULT 'pendiente',
  creada_en   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_fecha_hora (fecha, hora)         -- para buscar rápido las reservas de un día
);

-- ---------- CONSULTAS DE CONTACTO (RF07) ----------
CREATE TABLE IF NOT EXISTS consultas (
  id                  INT AUTO_INCREMENT PRIMARY KEY,
  nombre              VARCHAR(100) NOT NULL,
  email               VARCHAR(120) NOT NULL,
  telefono            VARCHAR(30)  NULL,
  motivo              ENUM('disponibilidad','carta','eventos','otro') NOT NULL,
  mensaje             TEXT NOT NULL,
  respuesta_preferida ENUM('correo','telefono') NOT NULL DEFAULT 'correo',
  enviada_en          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  respondida          TINYINT(1) NOT NULL DEFAULT 0
);

-- ---------- DATOS INICIALES DE LA CARTA ----------
INSERT IGNORE INTO categorias (id, nombre, orden) VALUES
  (1, 'Para empezar', 1),
  (2, 'Minutas', 2),
  (3, 'Parrilla', 3),
  (4, 'Pizzas y fideos', 4);

INSERT IGNORE INTO platos (id, categoria_id, nombre, descripcion, precio, imagen, imagen_alt) VALUES
  (1, 1, 'Empanadas criollas', 'Media docena de empanadas de carne, horneadas en masa casera.', 9000, 'empanadas.jpg', 'Empanadas criollas sobre una tabla de madera'),
  (2, 2, 'Milanesa con ensalada', 'Milanesa crocante con ensalada de lechuga, tomate, palta y pepino, y dos salsas de la casa.', 14500, 'milanesa.jpg', 'Milanesa con ensalada y dos salsas'),
  (3, 2, 'Milanesa a la napolitana', 'Milanesa con jamón, queso, salsa de tomate y cebollín.', 16800, 'napolitana.jpg', 'Milanesa a la napolitana con queso y salsa de tomate'),
  (4, 2, 'Hamburguesa doble', 'Dos medallones, queso, cebolla caramelizada y tomate, con papas rústicas.', 13900, 'hamburguesa.jpg', 'Hamburguesa doble con papas rústicas y tomates cherry'),
  (5, 3, 'Parrillada mixta', 'Cortes de carne y pollo a las brasas, con brochettes de langostinos.', 28000, 'parrillada.jpg', 'Parrillada con carne, pollo y brochettes de langostinos'),
  (6, 3, 'Pollo asado con papas', 'Pollo asado con papas fritas, ensalada fresca y salsas.', 15500, 'pollo.jpg', 'Pollo asado con papas fritas, ensalada y salsas'),
  (7, 3, 'Pescado del día a la parrilla', 'Pescado fresco a la parrilla. Consultá cuál tenemos hoy.', 17500, 'pescado.jpg', 'Pescado a la parrilla con humo y pinzas'),
  (8, 4, 'Pizzas al horno', 'Masa de borde aireado, muzzarella y distintos gustos. Preguntá los del día.', 12500, 'pizzas.jpg', 'Pizza con muzzarella, panceta y rúcula sobre una tabla de madera'),
  (9, 4, 'Ramen de langostinos', 'Fideos en caldo picante con huevo, langostinos y cebollita de verdeo.', 15900, 'ramen.jpg', 'Bowl de fideos orientales levantados con palillos');
