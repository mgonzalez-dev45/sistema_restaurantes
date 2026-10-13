-- Carga de platos de ejemplo para la tabla `platos` de la base `restaurante`.
-- Uso: phpMyAdmin > base "restaurante" > tabla "platos" > pestaña SQL > pegar > Continuar.
-- (La "Milanesa napolitana" ya la cargaste antes; acá van los demás. Ejecutalo UNA sola vez.)

INSERT INTO platos (nombre, descripcion, precio, imagen) VALUES
('Empanadas criollas', 'Docena de empanadas sobre tabla de madera', 12000, 'empanadas.jpg'),
('Hamburguesa doble', 'Doble carne con papas rústicas', 13500, 'hamburguesa.jpg'),
('Parrillada', 'Carne, pollo y brochettes de langostinos', 28000, 'parrillada.jpg'),
('Pescado a la parrilla', 'Pescado del día con guarnición', 18000, 'pescado.jpg'),
('Pizza de panceta y rúcula', 'Pizza con panceta y rúcula fresca', 11000, 'pizzas.jpg'),
('Pollo asado', 'Con papas fritas y ensalada', 12500, 'pollo.jpg'),
('Ramen', 'Fideos orientales con caldo', 11500, 'ramen.jpg');
