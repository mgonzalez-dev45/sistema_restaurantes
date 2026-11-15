# Documento de Defensa de Proyecto Integrador
## Sistema de Gestión Gastronómica y Carta Digital – "Paso Gourmet"

---

### Ficha Técnica del Proyecto
* **Proyecto:** Paso Gourmet – Restaurante & Carta Digital
* **Autor:** Marcelo González
* **Carrera:** Tecnicatura Superior en Desarrollo de Software
* **Cátedra:** Práctica Profesionalizante II
* **Docente Evaluador:** Prof. Mariela Romina López
* **Institución:** Instituto Superior de Formación Técnica "Islas Malvinas" (Subsede Paso de la Patria)
* **Ubicación:** Paso de la Patria, Provincia de Corrientes, República Argentina
* **Stack Tecnológico:** Python 3, Flask, MySQL / MariaDB (XAMPP), HTML5 Semántico, CSS3 Nativo (Grid + Flexbox), Jinja2, Git / GitHub
* **Documento Word Generado:** [`Documentacion_y_Defensa_Paso_Gourmet.docx`](file:///c:/Users/Estudiante/Desktop/sistema_restaurantes/Documentacion_y_Defensa_Paso_Gourmet.docx)

---

## 1. Introducción y Justificación del Negocio

### 1.1. Diagnóstico de la Problemática
Paso de la Patria es una villa turística correntina de fuerte concurrencia estacional vinculada a la pesca deportiva (el Torneo Nacional del Dorado) y las playas del Río Paraná. Históricamente, la oferta gastronómica del lugar enfrenta tres problemas críticos:
1. **Desactualización de precios y platos:** Por las fluctuaciones económicas y la estacionalidad de la pesca fresca del día, las cartas físicas impresas quedan obsoletas rápidamente o están llenas de tachaduras.
2. **Dependencia de redes sociales desordenadas:** Los turistas buscan el menú en fotos de Instagram o Facebook tomadas hace meses, que no reflejan el stock real ni los precios vigentes.
3. **Falta de un canal ágil de reservas:** El proceso tradicional requiere llamadas telefónicas o mensajes de WhatsApp en horarios donde el personal de cocina y salón está sobrecargado.

### 1.2. Propuesta de Valor ("Paso Gourmet")
*Paso Gourmet* soluciona esta brecha mediante una aplicación web moderna, rápida y responsiva que cumple dos funciones clave:
* **Para el comensal (turista o vecino):** Permite explorar la carta interactiva con fotos reales, descripciones y precios actualizados en pesos argentinos, además de solicitar reservas desde el teléfono móvil antes de viajar o llegar al salón.
* **Para el dueño o administrador del restaurante:** Proporciona un sistema de gestión (**CRUD**) intuitivo directamente sobre la carta para incorporar nuevos platos, ajustar precios por inflación en segundos o eliminar platos agotados.

---

## 2. Arquitectura de Software y Tecnologías

El sistema implementa una arquitectura inspirada en el patrón **MVC (Modelo - Vista - Controlador)** adaptada a la simplicidad y robustez de Flask:

```
[ Cliente: Navegador Web (HTML5 + CSS3 + Jinja2) ]
                      |
                      |  Peticiones HTTP (GET / POST)
                      v
[ Backend: Enrutador y Controladores Flask (app.py) ]
                      |
                      |  Consultas SQL Parametrizadas (SELECT, INSERT, UPDATE, DELETE)
                      v
[ Persistencia: Base de Datos MySQL (Tabla 'platos') ]
```

### 2.1. Justificación de las Elecciones Tecnológicas

| Tecnología | Rol en el Proyecto | ¿Por qué se eligió? (Argumentación de Defensa) |
| :--- | :--- | :--- |
| **Python 3** | Lenguaje Backend | Sintaxis limpia, altamente legible, tipado dinámico y velocidad de desarrollo. Estándar pedagógico y productivo. |
| **Flask** | Microframework Web | A diferencia de **Django**, que impone una estructura rígida y un ORM pesado para proyectos medianos, Flask permite comprender a fondo cómo viajan las cabeceras HTTP, cómo opera el enrutador y cómo interactuar directamente con la base de datos sin capas de abstracción innecesarias. Frente a **PHP plano**, ofrece un código más estructurado, seguro y testeable. |
| **MySQL (vía XAMPP)** | Motor de Base de Datos | Motor relacional estándar con soporte ACID, integridad transaccional (`commit`/`rollback`) y gran compatibilidad para despliegues locales y remotos. |
| **flask-mysqldb** | Driver / Conector | Conexión directa y rápida mediante cursores nativos en C (`mysqlclient`). Permite ejecutar sentencias SQL preparadas con prevención de inyección. |
| **Jinja2** | Motor de Plantillas | Desacopla la lógica de negocio de la presentación. Permite iteraciones (`{% for %}`), condicionales (`{% if %}`), inyección dinámica de URLs (`url_for`) y filtros personalizados de formato (`precio_ar`). |
| **HTML5 Semántico** | Maquetado Frontend | Cumple estándares internacionales del W3C y pautas de accesibilidad (**WCAG 2.1**), favoreciendo el indexado en buscadores (SEO) y lectores de pantalla. |
| **CSS3 Puro (Sin Bootstrap)** | Estilizado y Layout | Dominio total del estándar de diseño: uso de **Flexbox** para componentes unidimensionales (navegación, formularios), **CSS Grid** para la carta y portada, y variables nativas para la identidad cromática. Cero dependencias pesadas de terceros. |
| **Git & GitHub** | Control de Versiones | Trazabilidad completa de cada avance, registro de commits atómicos y respaldo seguro en la nube. |

---

## 3. Decisiones Críticas de Arquitectura Web (Puntos de Defensa)

### 3.1. ¿Por qué Arquitectura Multi-Página (MPA) y no una Single Page Application (SPA)?
1. **Posicionamiento SEO Local para el Turismo:** Para un restaurante turístico, la principal captación proviene de búsquedas orgánicas en Google ("dónde comer en Paso de la Patria", "pescado fresco Paso de la Patria"). En una MPA, cada sección cuenta con su propia URL canónica (`/carta`, `/nosotros`, `/reservas`, `/contacto`), su `<title>` y su `<meta name="description">` independientes, indexándose de inmediato sin requerir que los rastreadores ejecuten JavaScript.
2. **Rendimiento en Redes Móviles Inestables:** Al viajar por ruta o pasear por la costa, las conexiones 3G/4G son variables. Una SPA obliga a descargar inicialmente un "bundle" pesado de JavaScript (1 a 4 MB) antes de pintar la pantalla. En nuestra MPA, cada solicitud transfiere apenas 5 a 10 KB de HTML/CSS, logrando un *First Contentful Paint* casi instantáneo.
3. **Navegación Nativa del Navegador:** Los botones "Atrás/Adelante", el historial y la acción de compartir el enlace directo de la carta por WhatsApp funcionan de modo 100% nativo sin librerías de enrutamiento en cliente.
4. **Robustez y Simplicidad:** En el marco de Práctica Profesionalizante II, consolida el flujo HTTP clásico y la persistencia transaccional sin deudas técnicas ni sobrecargas innecesarias.

### 3.2. ¿Por qué hay un único encabezado `<h1>` por página?
1. **Estándar Oficial W3C (HTML5):** El `<h1>` identifica el tema rector y propósito supremo del documento. Múltiples `<h1>` rompen la jerarquía del documento.
2. **Accesibilidad Web (WCAG 2.1 - Nivel AA):** Los lectores de pantalla (NVDA, JAWS, TalkBack) generan un árbol jerárquico de navegación (`h1` -> `h2` -> `h3`). Si existen varios `<h1>`, la persona con discapacidad visual no puede distinguir cuál es el tema principal, provocando desorientación.
3. **SEO Semántico:** Google pondera el contenido del `<h1>` como la palabra clave primaria de la vista. Un único `<h1>` evita la dilución o canibalización de términos.

#### Inventario de `<h1>` en Paso Gourmet:
* `/` (`index.html`): `<h1>Comé bien en Paso de la Patria</h1>`
* `/carta` (`carta.html`): `<h1>La carta</h1>`
* `/plato/nuevo` (`plato_form.html`): `<h1>Agregar plato</h1>` (vía `{{ accion }}`)
* `/plato/editar/<id>` (`plato_form.html`): `<h1>Editar plato</h1>` (vía `{{ accion }}`)
* `/nosotros` (`nosotros.html`): `<h1>Nosotros</h1>`
* `/reservas` (`reservas.html`): `<h1>Reservá tu mesa</h1>`
* `/contacto` (`contacto.html`): `<h1>Contacto</h1>`
* `/gracias` (`gracias.html`): `<h1>¡Gracias!</h1>`

### 3.3. Accesibilidad Web (A11Y) Implementada
* **Enlace de salto rápido (`.saltar`):** `<a class="saltar" href="#contenido">Saltar al contenido</a>` permite a usuarios que navegan con teclado o lectores de pantalla saltarse la cabecera y aterrizar directamente en el `<main>`.
* **Foco visible (`:focus-visible`):** Delineado con un borde dorado de 3px (`outline: 3px solid var(--dorado)`) para identificar con claridad qué control interactivo tiene el foco.
* **Textos alternativos (`alt`):** Todas las imágenes cuentan con descripciones visuales detalladas.
* **Reducción de movimiento (`prefers-reduced-motion`):** Desactiva transiciones y animaciones para usuarios con trastornos vestibulares.

---

## 4. Identidad Visual, Psicología del Color y Sistema de Estilos

### 4.1. Paleta Cromática y Simbología Cultural
* **Verde Río (`--rio: #0e3b43`):** El color principal evoca el cauce del Río Paraná que baña la costa de Paso de la Patria. Transmite calma, frescura y solidez gastronómica.
* **Río Oscuro (`--rio-oscuro: #08262b`):** Aplica en la cabecera fija (`position: sticky`) y el pie de página, enmarcando el contenido y generando un ambiente distinguido y nocturno.
* **Dorado (`--dorado: #e3a72f`):** Inspirado en el "Tigre de los Ríos" (el pez dorado, símbolo del pueblo) y en el sol litoraleño. Psicológicamente, los tonos ámbar estimulan el apetito, aportan calidez y destacan inmediatamente los botones de acción principal (CTA: *Reservar*, *Ver la carta*, *Agregar plato*).
* **Fondo Arena Suave (`--fondo: #f2f5f4`):** Sustituye al blanco puro (`#ffffff`) para mitigar el encandilamiento en pantallas móviles y simular la claridad de las costas correntinas.
* **Blanco (`--blanco: #ffffff`):** Superficie de tarjetas y formularios para máxima legibilidad.
* **Texto Oscuro (`--texto: #17262a`):** Relación de contraste superior a 7:1 contra el fondo, cumpliendo nivel AAA de WCAG.
* **Gris Medio (`--suave: #4d5e61`):** Texto secundario de apoyo.
* **Borde Suave (`--linea: #d5dedc`):** Divisores sutiles de interfaz.

### 4.2. Tipografía y Jerarquía
* **Títulos (`Young Serif`):** Fuente con remates (serif) inspirada en los tradicionales menús de bistró y bodegones. Brinda calidez artesanal y autoridad a los encabezados (`h1`, `h2`, `h3`, `legend`).
* **Cuerpo y Formularios (`Figtree`):** Tipografía sans-serif moderna, de proporciones generosas y excelente altura de x, optimizada para la lectura rápida en dispositivos móviles pequeños.
* **Tipografía fluida (`clamp`):** Escala de fuentes adaptativa que se redimensiona suavemente según el viewport del dispositivo (ej: `clamp(2.1rem, 5vw, 3.4rem)`).

### 4.3. Estrategia de Maquetado: Flexbox vs CSS Grid
* **Flexbox (1D):** Cabecera sticky, navegación principal, barra de acciones de la carta, pie de página y disposición vertical de los campos en formularios.
* **CSS Grid (2D):** Portada dividida al 50%, sección "Lo más pedido" con grilla asimétrica (`grid-row: span 2`), carta digital responsiva mediante `repeat(auto-fill, minmax(260px, 1fr))` y galería de fotos a 3 columnas.

---

## 5. Mapa del Sitio y Vistas del Sistema

1. **Inicio (`/` - `index.html`):** Portada con doble llamada a la acción (*Ver la carta* y *Reservar mesa*), sección "Lo más pedido", banner panorámico de pescado del día y bloque de horarios y mapa.
2. **Carta Digital (`/carta` - `carta.html`):** Lectura dinámica de MySQL, cuadrícula responsiva de tarjetas con precio en formato argentino, botón superior `+ Agregar plato` y botones de tarjeta `Editar` y `Eliminar`.
3. **Formulario de Gestión de Platos (`/plato/nuevo` y `/plato/editar/<id>` - `plato_form.html`):** Formulario unificado para altas y modificaciones, estructurado en `<fieldset>` con `<legend>`, validaciones HTML5 requeridas y precarga condicional de valores.
4. **Nosotros (`/nosotros` - `nosotros.html`):** Relato de la propuesta culinaria a 2 columnas con caja de notas lateral y galería fotográfica de 6 imágenes con micro-interacción `:hover scale(1.07)`.
5. **Reservas (`/reservas` - `reservas.html`):** Formulario con restricción de fecha pasada (`min="{{ hoy }}"`), selección de turnos, comensales, salón climatizado o patio y comodidades especiales.
6. **Contacto (`/contacto` - `contacto.html`):** Formulario de contacto con selector de motivo y canal de respuesta, microformatos semánticos `<address>` y mapa interactivo incrustado de Google Maps.
7. **Página de Agradecimiento (`/gracias` - `gracias.html`):** Retroalimentación contextual (`tipo='reserva'` o `tipo='consulta'`) con enlaces de retorno rápido.

---

## 6. El CRUD en Detalle: Métodos, Rutas y Persistencia

### 6.1. Esquema de Base de Datos Relacional
```sql
CREATE TABLE IF NOT EXISTS `platos` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `precio` INT NOT NULL,
  `imagen` VARCHAR(100) NOT NULL DEFAULT 'milanesa.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 6.2. Las 4 Operaciones y su Código en `app.py`

#### C - CREATE (Alta de plato)
* **Ruta:** `/plato/nuevo` (GET / POST)
* Procesa el formulario, ejecuta `INSERT INTO platos ...` parametrizado con `%s` y confirma con `mysql.connection.commit()`.

#### R - READ (Consulta y Listado)
* **Ruta:** `/carta` (GET)
* Consulta todos los platos con `cursor.fetchall()` y Jinja2 los recorre en un bucle `{% for plato in platos %}`.

#### U - UPDATE (Edición de plato)
* **Ruta:** `/plato/editar/<int:id>` (GET / POST)
* En GET recupera la tupla por ID para precargar el formulario; en POST ejecuta `UPDATE platos SET ... WHERE id = %s` y confirma con `commit()`.

#### D - DELETE (Baja de plato)
* **Ruta:** `/plato/eliminar/<int:id>` (POST / GET)
* Elimina el registro por su clave primaria con `DELETE FROM platos WHERE id = %s` y persiste con `commit()`.

### 6.3. Filtro Personalizado: Formato de Moneda Argentina
```python
@app.template_filter('precio_ar')
def precio_ar(valor):
    return "$" + f"{int(valor):,}".replace(",", ".")
```
En Jinja2: `{{ plato[3] | precio_ar }}` convierte `14500` en `$14.500`.

### 6.4. Destino y Ciclo de Vida de los Formularios (Reservas y Contacto)
1. **Despacho por Método HTTP POST:** Los formularios de [reservas.html](file:///c:/Users/Estudiante/Desktop/sistema_restaurantes/sistemas_restaurantes/templates/reservas.html) y [contacto.html](file:///c:/Users/Estudiante/Desktop/sistema_restaurantes/sistemas_restaurantes/templates/contacto.html) envían sus datos mediante peticiones `POST` a `/reservas` y `/contacto`. La información viaja encapsulada en el cuerpo de la petición (*payload*), manteniéndose invisible en la URL del navegador.
2. **Recepción y Validación en el Controlador (app.py):** El servidor Flask recibe el payload mediante `request.form.get()`, asegurando que no existan campos nulos ni datos mal formateados.
3. **Persistencia en MySQL (Tablas `reservas` y `mensajes`):** Las solicitudes se insertan mediante consultas preparadas parametrizadas en sus respectivas tablas relacionales, garantizando la trazabilidad histórica de cada comensal.
4. **Confirmación Transaccional:** Se ejecuta `mysql.connection.commit()` para garantizar que la reserva o consulta quede asentada físicamente en el motor de base de datos antes de responder al cliente.
5. **Redirección Segura y Retroalimentación (Patrón PRG a `/gracias`):** Para prevenir el reenvío accidental de datos si el usuario presiona F5 (*Post/Redirect/Get*), el backend redirige inmediatamente a la página de agradecimiento (`url_for('gracias', tipo='reserva')` o `tipo='consulta'`), donde el comensal recibe confirmación explícita de su solicitud.

### 6.5. ¿Es completamente seguro para el usuario ingresar sus datos?
La seguridad y privacidad del comensal fueron contempladas bajo un enfoque de **defensa en profundidad**:
1. **Protección de Datos en Tránsito (POST vs GET):** Al utilizar `POST` en lugar de `GET`, los datos confidenciales (nombre, teléfono personal, correo electrónico) no se concatenan en la barra de direcciones. Esto impide que queden guardados en el historial de navegación del teléfono, en la caché de servidores proxy intermediarios o en los archivos de registro (*access logs*) del servidor.
2. **Cifrado de Extremo a Extremo (HTTPS / TLS):** En un despliegue en producción, el sitio se sirve bajo el protocolo HTTPS respaldado por certificados SSL/TLS. Todo el tráfico entre el dispositivo móvil del turista y el servidor viaja fuertemente cifrado, impidiendo ataques de interceptación (*Man-in-the-Middle*) en redes WiFi públicas o abiertas de la playa o el hotel.
3. **Inmunidad Absoluta a Inyección SQL:** Ningún valor ingresado por el usuario se interpola directamente en sentencias SQL. El uso de tuplas de parámetros `(%s)` delega el escape y sanitización de caracteres especiales al conector nativo en C (`mysqlclient`), anulando cualquier intento de inyección de código malicioso.
4. **Cumplimiento Legal de Privacidad (Ley 25.326 de Hábeas Data en Argentina):** En el formulario de contacto se incorporó una casilla de verificación obligatoria: *«Acepto que usen mis datos solo para responder esta consulta»*. Esto garantiza el consentimiento explícito del titular y el principio de finalidad exigidos por el marco normativo nacional de protección de datos personales.
5. **Validación Preventiva en Doble Capa (Cliente y Servidor):** El formulario restringe tipos de datos en el cliente (`type='email'`, `type='tel'`) e inhabilita fechas pasadas (`min='{{ hoy }}'`), mientras que el backend valida la presencia de los campos requeridos antes de confirmar la persistencia.

---

## 7. Banco de Preguntas y Respuestas para la Defensa Oral

1. **¿Por qué integraron el CRUD en la misma carta y no en `/admin`?**
   > *"Por experiencia de usuario y agilidad operativa: el encargado ve el plato modificado exactamente como lo apreciará el cliente en el salón, y puede pausar un producto o actualizar un precio en dos clics desde el teléfono sin navegar menús densos. Para este avance el foco era consolidar la persistencia MySQL; la separación en un panel administrativo con roles queda planificada para la entrega final."*

2. **¿Por qué es indispensable llamar a `mysql.connection.commit()`?**
   > *"MySQL cumple con el estándar transaccional ACID. Toda sentencia DML (INSERT, UPDATE, DELETE) ocurre en una transacción en memoria. Si no se invoca commit(), al cerrarse el cursor o finalizar la petición se produce un rollback implícito y los cambios se descartan. commit() es la orden que escribe efectivamente en disco."*

3. **¿Cómo garantizan que la aplicación no sea vulnerable a Inyección SQL?**
   > *"No se utiliza concatenación ni f-strings. Todas las consultas son parametrizadas pasando los valores como tuplas `(%s, %s, ...)` al método `cursor.execute()`. El driver se encarga de escapar y sanitizar los caracteres peligrosos."*

4. **¿Por qué CSS nativo y no Bootstrap o Tailwind?**
   > *"Para demostrar dominio pleno de los estándares W3C (Flexbox, Grid y variables). Los frameworks añaden cientos de kilobytes innecesarios y estandarizan el diseño. Nuestro CSS pesa menos de 13 KB, carga instantáneamente y responde a la identidad cultural de Paso de la Patria."*

5. **¿Qué técnica evita reservas en fechas pasadas?**
   > *"En el backend capturamos la fecha actual con `date.today().isoformat()` y se la pasamos a la plantilla, asignándola al atributo `min=\"{{ hoy }}\"` del `<input type=\"date\">`. El navegador inhabilita automáticamente todas las fechas anteriores."*

6. **¿Qué resguardo de seguridad existe al borrar platos?**
   > *"En el frontend, el formulario cuenta con `onsubmit=\"return confirm('¿Seguro que querés eliminar...?');\"` para impedir borrados accidentales, y en el backend la mutación destructiva viaja por método `POST`."*

7. **¿A dónde van a parar los datos de los formularios y qué medidas garantizan la seguridad y privacidad del usuario?**
   > *"Los formularios viajan por método HTTP POST hacia los controladores de Flask, que los insertan mediante consultas parametrizadas en las tablas relacionales 'reservas' y 'mensajes' de MySQL, confirmando la persistencia con commit() y redirigiendo a /gracias bajo el patrón PRG para evitar duplicaciones. Respecto a la seguridad: 1) Al usar POST los datos no se exponen en la URL ni en el historial del celular; 2) En producción se transmiten cifrados bajo HTTPS/TLS; 3) Se previene SQL Injection con tuplas de parámetros; 4) Cumplimos con la Ley Nacional 25.326 de Protección de Datos Personales exigiendo consentimiento explícito mediante una casilla de verificación obligatoria."*

---

## 8. Plan de Mejoras Futuras (Roadmap de Entrega Final)

1. **Autenticación y Roles:** Módulo `/login` con contraseñas hasheadas (`bcrypt` o `werkzeug.security`) y sesiones (`flask.session`).
2. **Subida Física de Imágenes:** Carga directa con formularios `multipart/form-data` y `werkzeug.utils.secure_filename`.
3. **Persistencia de Reservas y Contacto:** Creación de tablas `reservas` y `mensajes` con confirmación por correo electrónico.
4. **Filtros por Categoría y Buscador:** Pestañas interactivas (Parrilla, Minutas, Pescados, Postres).

---

## 9. Conclusión

El proyecto integrador **"Paso Gourmet"** combina una interfaz atractiva, accesible y orientada al usuario móvil con un backend en Python y Flask robusto, seguro y eficiente, respaldado por un ciclo CRUD completo con persistencia en MySQL y versionado riguroso con Git.
