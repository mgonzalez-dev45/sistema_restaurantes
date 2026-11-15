# AVANCE: navegación entre páginas con Flask + CRUD de platos en MySQL + persistencia de reservas y contacto.
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# Creando la aplicación Flask
app = Flask(__name__)

# Configuramos la conexión a la base de datos (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurante'

mysql = MySQL(app)


# Filtro para mostrar precios: convierte 14500 en $14.500
@app.template_filter('precio_ar')
def precio_ar(valor):
    return "$" + f"{int(valor):,}".replace(",", ".")


# --- INICIO ---
@app.route('/')
def index():
    return render_template('index.html')


# --- CARTA ---
@app.route('/carta')
def carta():
    # Leemos los platos de la tabla 'platos' y se los mandamos al HTML (READ)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos")
    platos = cursor.fetchall()
    cursor.close()
    return render_template('carta.html', platos=platos)


# --- CRUD: AGREGAR PLATO (CREATE) ---
@app.route('/plato/nuevo', methods=['GET', 'POST'])
def nuevo_plato():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        imagen = request.form.get('imagen') or 'milanesa.jpg'

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO platos (nombre, descripcion, precio, imagen)
            VALUES (%s, %s, %s, %s)
        """, (nombre, descripcion, precio, imagen))
        mysql.connection.commit()  # Guardamos los cambios en la base de datos
        cursor.close()

        return redirect(url_for('carta'))

    return render_template('plato_form.html', accion='Agregar', plato=None)


# --- CRUD: EDITAR PLATO (UPDATE) ---
@app.route('/plato/editar/<int:id>', methods=['GET', 'POST'])
def editar_plato(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        imagen = request.form.get('imagen') or 'milanesa.jpg'

        cursor.execute("""
            UPDATE platos
            SET nombre = %s, descripcion = %s, precio = %s, imagen = %s
            WHERE id = %s
        """, (nombre, descripcion, precio, imagen, id))
        mysql.connection.commit()  # Confirmamos la actualización
        cursor.close()

        return redirect(url_for('carta'))

    # Si es GET, consultamos los datos del plato actual para rellenar el formulario
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos WHERE id = %s", (id,))
    plato = cursor.fetchone()
    cursor.close()

    return render_template('plato_form.html', accion='Editar', plato=plato)


# --- CRUD: ELIMINAR PLATO (DELETE) ---
@app.route('/plato/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar_plato(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM platos WHERE id = %s", (id,))
    mysql.connection.commit()  # Confirmamos el borrado
    cursor.close()

    return redirect(url_for('carta'))


# --- NOSOTROS ---
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


# --- RESERVAS (procesa y guarda en MySQL, luego redirige a gracias) ---
@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        personas = request.form.get('personas')
        lugar = request.form.get('lugar') or 'salon'
        silla_bebe = request.form.get('silla-bebe') or 'no'
        comentarios = request.form.get('comentarios') or ''

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    fecha DATE NOT NULL,
                    hora VARCHAR(10) NOT NULL,
                    personas INT NOT NULL,
                    lugar VARCHAR(20) NOT NULL DEFAULT 'salon',
                    silla_bebe VARCHAR(5) NOT NULL DEFAULT 'no',
                    comentarios TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            cursor.execute("""
                INSERT INTO reservas (nombre, telefono, email, fecha, hora, personas, lugar, silla_bebe, comentarios)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, telefono, email, fecha, hora, personas, lugar, silla_bebe, comentarios))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print("Error al guardar reserva:", e)

        return redirect(url_for('gracias', tipo='reserva'))

    # 'hoy' evita que el calendario deje elegir fechas pasadas
    return render_template('reservas.html', hoy=date.today().isoformat())


# --- CONTACTO (procesa y guarda en MySQL, luego redirige a gracias) ---
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono') or ''
        motivo = request.form.get('motivo')
        mensaje = request.form.get('mensaje')
        respuesta = request.form.get('respuesta') or 'correo'

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    telefono VARCHAR(50),
                    motivo VARCHAR(50) NOT NULL,
                    mensaje TEXT NOT NULL,
                    respuesta VARCHAR(20) NOT NULL DEFAULT 'correo',
                    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            cursor.execute("""
                INSERT INTO mensajes (nombre, email, telefono, motivo, mensaje, respuesta)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, email, telefono, motivo, mensaje, respuesta))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print("Error al guardar mensaje:", e)

        return redirect(url_for('gracias', tipo='consulta'))

    return render_template('contacto.html')


# --- GRACIAS ---
@app.route('/gracias')
def gracias():
    tipo = request.args.get('tipo', 'consulta')
    return render_template('gracias.html', tipo=tipo)


if __name__ == '__main__':
    # Modo desarrollo para ver los errores en consola
    app.run(debug=True)
