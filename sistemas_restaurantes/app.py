
# CORREGIDO: se agregó url_for (para armar los enlaces) y se importa datetime/date (para validar fechas)
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for

# Importamos la librería para conectar MySQL con Flask que vimos en clase
from flask_mysqldb import MySQL

# Creando la aplicación Flask
app = Flask(__name__)

# Configuramos la conexión a la base de datos local
# La base 'pasogourmet' se crea ejecutando el archivo schema.sql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pasogourmet'

# Inicializamos la conexión
mysql = MySQL(app)


# --- REGLAS DEL RESTAURANTE (NUEVO) ---
# Si cambian los horarios, se modifican solo acá
HORAS_VALIDAS = ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00',
                '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00']
DIAS_ATENCION = (3, 4, 5, 6)          # jueves a domingo (lunes = 0)
MOTIVOS_VALIDOS = ['disponibilidad', 'carta', 'eventos', 'otro']


# --- FILTRO PARA MOSTRAR PRECIOS (NUEVO) ---
# Convierte 14500 en $14.500 para mostrarlo en la carta
@app.template_filter('precio_ar')
def precio_ar(valor):
    return "$" + f"{int(valor):,}".replace(",", ".")


# --- RUTA PRINCIPAL (INICIO) ---
@app.route('/')
def index():
    # Te lleva directo a la pantalla de bienvenida
    return render_template('index.html')


# --- RUTA PARA VER LA CARTA ---
# NUEVO: ahora los platos se leen desde la base de datos (tablas categorias y platos)
@app.route('/carta')
def carta():
    categorias = []
    error = None

    try:
        cursor = mysql.connection.cursor()
        # Traemos solo los platos disponibles, ordenados por categoría
        cursor.execute("""
            SELECT c.id, c.nombre, p.nombre, p.descripcion, p.precio, p.imagen, p.imagen_alt
            FROM platos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            WHERE p.disponible = 1
            ORDER BY c.orden, p.id
        """)
        filas = cursor.fetchall()
        cursor.close()

        # Agrupamos los platos por categoría para mostrarlos en la página
        for cat_id, cat_nombre, nombre, descripcion, precio, imagen, imagen_alt in filas:
            if len(categorias) == 0 or categorias[-1]['id'] != cat_id:
                categorias.append({'id': cat_id, 'nombre': cat_nombre, 'platos': []})
            categorias[-1]['platos'].append({
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'imagen': imagen,
                'imagen_alt': imagen_alt
            })
    except Exception as e:
        # Si la base no responde, la página no se rompe: muestra un aviso
        print("Error al leer la carta:", e)
        error = "No pudimos cargar la carta en este momento. Probá de nuevo en unos minutos."

    return render_template('carta.html', categorias=categorias, error=error)


# --- RUTA PARA VER LA HISTORIA ---
@app.route('/nosotros')
def nosotros():
    # Te muestra la sección de quiénes somos
    return render_template('nosotros.html')


# --- RUTA PARA MOSTRAR EL FORMULARIO DE RESERVAS ---
@app.route('/reservas')
def reservas():
    # 'hoy' se usa para que el calendario no deje elegir fechas pasadas
    return render_template('reservas.html', hoy=date.today().isoformat())


# --- RUTA PARA GUARDAR LA RESERVA (PROCESA EL FORMULARIO) ---
# Usamos el método POST igual que en la ruta '/store' del ejemplo de películas
@app.route('/store_reserva', methods=['POST'])
def store_reserva():
    # Capturamos los datos del formulario de 'reservas.html'
    # CORREGIDO: se usa .get() para que no falle con error 400 si falta un campo,
    # y se leen TODOS los campos que tiene el formulario (antes faltaban email, hora, lugar, etc.)
    _nombre = request.form.get('nombre', '').strip()
    _telefono = request.form.get('telefono', '').strip()
    _email = request.form.get('email', '').strip()
    _fecha = request.form.get('fecha', '')
    _hora = request.form.get('hora', '')
    _comensales = request.form.get('personas', '')      # CORREGIDO: el campo del formulario se llama 'personas', no 'comensales'
    _lugar = request.form.get('lugar', 'salon')
    _silla_bebe = 1 if request.form.get('silla-bebe') == 'si' else 0   # el checkbox solo llega si está tildado
    _comentarios = request.form.get('comentarios', '').strip()

    def con_error(mensaje):
        # Vuelve a mostrar el formulario con un cartel de error
        return render_template('reservas.html', hoy=date.today().isoformat(), error=mensaje)

    # NUEVO: validaciones en el servidor (el navegador ya valida, pero esto es la segunda barrera)
    if not _nombre or not _telefono or not _email:
        return con_error("Completá tu nombre, teléfono y correo.")

    if _lugar not in ('salon', 'patio'):
        return con_error("El lugar elegido no es válido.")

    if _hora not in HORAS_VALIDAS:
        return con_error("Elegí un horario de la lista.")

    try:
        _comensales = int(_comensales)
    except ValueError:
        return con_error("Indicá cuántas personas son.")
    if _comensales < 1 or _comensales > 9:
        return con_error("La cantidad de personas debe estar entre 1 y 9.")

    try:
        fecha_reserva = datetime.strptime(_fecha, '%Y-%m-%d').date()
    except ValueError:
        return con_error("La fecha no es válida.")
    if fecha_reserva < date.today():
        return con_error("La fecha no puede ser anterior a hoy.")
    if fecha_reserva.weekday() not in DIAS_ATENCION:
        return con_error("Atendemos de jueves a domingo. Elegí otro día.")

    # Agrupamos los datos en una tupla
    datos = (_nombre, _telefono, _email, _fecha, _hora, _comensales,
            _lugar, _silla_bebe, _comentarios)

    # Preparamos la consulta SQL para insertar en la tabla 'reservas'
    # CORREGIDO: ya no se manda el 'id' (la base lo genera sola con AUTO_INCREMENT)
    # y ahora se guardan todos los campos. El estado queda 'pendiente' por defecto.
    sql = """INSERT INTO reservas
            (nombre, telefono, email, fecha, hora, comensales, lugar, silla_bebe, comentarios)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        # 1. Obtenemos el cursor directamente desde la conexión activa de mysql
        cursor = mysql.connection.cursor()

        # 2. Ejecutamos la sentencia pasando la consulta SQL y la tupla con los datos
        cursor.execute(sql, datos)

        # 3. Confirmamos los cambios en la base de datos local para que impacten
        mysql.connection.commit()

        # 4. Cerramos el cursor para liberar la memoria del servidor
        cursor.close()
    except Exception as e:
        # NUEVO: si la base falla, el usuario ve un mensaje en lugar de una pantalla de error
        print("Error al guardar la reserva:", e)
        return con_error("No pudimos guardar tu reserva. Intentá de nuevo en unos minutos.")

    # CORREGIDO: antes redirigía a '/'; ahora va a la página de agradecimiento
    return redirect(url_for('gracias', tipo='reserva'))


# --- RUTA PARA MOSTRAR EL FORMULARIO DE CONTACTO (NUEVO) ---
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


# --- RUTA PARA GUARDAR LA CONSULTA DEL FORMULARIO DE CONTACTO (NUEVO) ---
@app.route('/store_contacto', methods=['POST'])
def store_contacto():
    _nombre = request.form.get('nombre', '').strip()
    _email = request.form.get('email', '').strip()
    _telefono = request.form.get('telefono', '').strip()
    _motivo = request.form.get('motivo', '')
    _mensaje = request.form.get('mensaje', '').strip()
    _respuesta = request.form.get('respuesta', 'correo')
    _acepto = request.form.get('acepto')

    def con_error(mensaje):
        return render_template('contacto.html', error=mensaje)

    if not _nombre or not _email or not _mensaje:
        return con_error("Completá tu nombre, correo y mensaje.")
    if '@' not in _email:
        return con_error("El correo electrónico no es válido.")
    if _motivo not in MOTIVOS_VALIDOS:
        return con_error("Elegí un motivo de consulta.")
    if _respuesta not in ('correo', 'telefono'):
        return con_error("La forma de respuesta no es válida.")
    if _acepto != 'si':
        return con_error("Tenés que aceptar el uso de tus datos para poder responderte.")

    datos = (_nombre, _email, _telefono, _motivo, _mensaje, _respuesta)
    sql = """INSERT INTO consultas
            (nombre, email, telefono, motivo, mensaje, respuesta_preferida)
            VALUES (%s, %s, %s, %s, %s, %s)"""

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(sql, datos)
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print("Error al guardar la consulta:", e)
        return con_error("No pudimos enviar tu mensaje. Intentá de nuevo en unos minutos.")

    return redirect(url_for('gracias', tipo='consulta'))


# --- PÁGINA DE AGRADECIMIENTO (NUEVO) ---
@app.route('/gracias')
def gracias():
    # 'tipo' puede ser 'reserva' o 'consulta' y cambia el texto que se muestra
    tipo = request.args.get('tipo', 'consulta')
    return render_template('gracias.html', tipo=tipo)


if __name__ == '__main__':
    # Ejecutamos la aplicación en modo desarrollo para ver los errores en consola
    app.run(debug=True)
