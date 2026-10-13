# Notas de cambios – Sistema Paso Gourmet

Marcelo: acá está todo lo que encontré mal y lo que modifiqué. En `app.py` los cambios
también están marcados con los comentarios **CORREGIDO:** y **NUEVO:**.

Probé todo el sistema funcionando contra un servidor MySQL/MariaDB (rutas, formularios,
guardado en la base y casos de error). Lo que **no** pude probar es tu entorno de Windows/XAMPP.

---

## 1. Qué estaba mal

| # | Dónde | Problema | Qué pasaba | Cómo se corrigió |
|---|-------|----------|-----------|------------------|
| 1 | Nombre del archivo | Se llamaba `apy.py` | `flask run` no lo encuentra (busca `app.py`) | Se renombró a `app.py` |
| 2 | `apy.py`, ruta `/menu` | Buscaba `menu.html`, pero el archivo se llama `carta.html` | Error 500 (`TemplateNotFound`) | Ruta `/carta` que usa `carta.html` |
| 3 | `apy.py` | Faltaban las rutas `/carta`, `/contacto` y `/gracias` | Error 404 al tocar esos botones del menú | Se crearon las tres rutas |
| 4 | `apy.py`, `store_reserva` | Leía `request.form['comensales']`, pero el formulario envía el campo `personas` | Error 400 al enviar cualquier reserva (no se guardaba nada) | Se lee `personas` |
| 5 | `apy.py`, `store_reserva` | Solo leía 4 campos; el formulario tiene 9 (faltaban email, hora, lugar, silla de bebé, comentarios) | Esos datos se perdían | Se leen y se guardan los 9 |
| 6 | `apy.py`, INSERT | Mandaba `id` como `NULL` | Funciona solo si la tabla ya tiene `AUTO_INCREMENT`; era innecesario | Se quitó el `id`; la base lo genera sola |
| 7 | Base de datos | No existía el script: la base `pasogourmet` y la tabla `reservas` no estaban definidas | Error de conexión/tabla inexistente | Se creó `schema.sql` |
| 8 | Templates (`*.html`) | Los enlaces eran archivos (`reservas.html`, `index.html`) | Flask no sirve esos archivos: error 404 | Se cambiaron por `url_for('reservas')`, etc. |
| 9 | Templates | CSS e imágenes apuntaban a `css/estilos.css` e `img/...`; tus archivos están en `static/css/styles.css` y `static/uploads/` | La página se veía sin estilos ni fotos | Se usan rutas `url_for('static', ...)` |
| 10 | Templates | `index.html` pedía `styles.css` y el resto `estilos.css` | Inconsistencia: solo una de las dos existía | Todas usan `styles.css` |
| 11 | Formularios | `action="gracias.html"` con `data-netlify` (eso es para Netlify, no para Flask) | El formulario no enviaba nada a tu servidor | `action` apunta a `/store_reserva` y `/store_contacto` |
| 12 | `reservas.html` | La opción «9 o más» tenía el valor `9+` | No se puede guardar en una columna numérica | Ahora vale `9` (el detalle va en comentarios) |
| 13 | `apy.py` | Después de guardar volvía a `/` sin avisar | La persona no sabe si se guardó | Va a la página «Gracias» |
| 14 | `apy.py` | Sin validaciones ni manejo de errores | Datos inválidos o una base caída mostraban pantalla de error | Validaciones y mensajes claros (ver punto 3) |

---

## 2. Qué agregué

- **`schema.sql`**: crea la base `pasogourmet` con 4 tablas (se puede ejecutar varias veces sin perder datos).
  - `categorias` y `platos`: la carta.
  - `reservas`: con fecha, hora, comensales, lugar, silla de bebé, comentarios y **estado** (`pendiente`, `confirmada`, `rechazada`). Cubre RF04 y RF06.
  - `consultas`: mensajes del formulario de contacto (RF07), con campo `respondida`.
- **Carta desde la base de datos**: los platos y precios ya no están escritos en el HTML. Si cambiás un precio en la tabla `platos`, cambia en la web (RF03 y RF05).
- **Contacto guardado**: rutas `/contacto` y `/store_contacto`.
- **Página «Gracias»** que cambia el texto según sea reserva o consulta.
- **`requirements.txt`** con las librerías necesarias.
- **Estilo para los carteles de error** (al final de `static/css/styles.css`).

## 3. Validaciones que hace el servidor

Aunque el navegador ya valida, el servidor vuelve a controlar:

- Nombre, teléfono y correo no vacíos.
- Hora dentro de la lista de horarios permitidos.
- Personas: número entre 1 y 9.
- Fecha válida, **no anterior a hoy** y **solo de jueves a domingo**.
- Lugar: solo `salon` o `patio`.
- Contacto: correo con `@`, motivo válido y casilla de aceptación tildada.
- Si la base de datos no responde, se muestra un mensaje en vez de un error feo.

> Los horarios y los días de atención están en las constantes `HORAS_VALIDAS` y
> `DIAS_ATENCION` al principio de `app.py`. Son los de ejemplo del sitio: si los reales
> son otros, cambialos ahí.

---

## 4. Cómo ponerlo en marcha

1. Encendé **MySQL** (por ejemplo, desde el panel de XAMPP).
2. Creá la base: en phpMyAdmin, pestaña **Importar** → elegí `schema.sql` → Continuar.
   (O por consola: `mysql -u root < schema.sql`).
3. Instalá las librerías: `pip install -r requirements.txt`
4. Ejecutá: `python app.py`
5. Abrí **http://127.0.0.1:5000** en el navegador.

Si tu MySQL tiene contraseña para `root`, ponela en `MYSQL_PASSWORD` dentro de `app.py`.

## 5. Consultas útiles para ver lo que se guarda

```sql
USE pasogourmet;

-- Todas las reservas, las más próximas primero
SELECT * FROM reservas ORDER BY fecha, hora;

-- Reservas pendientes de confirmar
SELECT id, nombre, telefono, fecha, hora, comensales FROM reservas WHERE estado = 'pendiente';

-- Confirmar una reserva (cambiá el 1 por el id que quieras)
UPDATE reservas SET estado = 'confirmada' WHERE id = 1;

-- Consultas sin responder
SELECT * FROM consultas WHERE respondida = 0;

-- Cambiar un precio o sacar un plato de la carta
UPDATE platos SET precio = 15000 WHERE id = 3;
UPDATE platos SET disponible = 0 WHERE id = 7;
```

---

## 6. Lo que todavía falta (próximas iteraciones)

- **Login y panel de administración** (RF01, RF05, RF06): hoy el encargado confirma reservas
  directamente en la base. Importante: **no hay que publicar un panel de administración sin
  contraseña**, por eso todavía no lo agregué.
- **Control de cupos**: hoy se pueden aceptar más reservas que lugares en el salón.
- **Contraseñas y seguridad** (RNF01): cuando haya usuarios, guardar las contraseñas cifradas
  (nunca en texto plano) y no dejar la contraseña de la base escrita en el código.
- **Publicación**: este sistema necesita un servidor que ejecute Python. **Netlify solo publica
  sitios estáticos**, así que la versión con base de datos no se puede subir ahí (la versión
  anterior en HTML puro sí). Para publicarla habría que usar un hosting con Python.

## 7. Estructura de carpetas

```
sistema_restaurante/
├── app.py                  ← aplicación Flask (antes apy.py)
├── schema.sql              ← crea la base de datos
├── requirements.txt
├── NOTAS_DE_CAMBIOS.md     ← este archivo
├── templates/              ← páginas HTML
└── static/
    ├── css/styles.css
    └── uploads/            ← imágenes y favicon
```
(El zip original tenía la carpeta `sistema_restaurante` dentro de otra igual; la dejé en un solo nivel.)
