from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurante'

mysql = MySQL(app)


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
    # Lee los platos de la tabla 'platos' y se los mandamos al HTML (READ)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos")
    platos = cursor.fetchall()
    cursor.close()
    return render_template('carta.html', platos=platos)

# --- CRUD: MOSTRAR EL FORMULARIO PARA AGREGAR (create) ---
@app.route('/create')
def create():
    # plato=None significa "campos vacíos": es el mismo HTML que usamos para editar
    return render_template('plato_form.html', accion='Agregar', plato=None)

# --- CRUD: GUARDAR UN PLATO NUEVO (store) ---
# Recibe lo que se envió en el formulario /create y lo guarda en la base.
@app.route('/store', methods=['POST'])
def store():
    # 1) LEER del formulario (usamos los mismos nombres de campo que ya tenías)
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    foto = request.files['imagen']

    # 2) NOMBRE ÚNICO para la foto: fecha y hora + nombre original
    # CAMBIO: la guía usa solo %Y%H%M%S; sumamos %m%d (mes y día) para que sea más único
    tiempo = datetime.now().strftime("%Y%m%d%H%M%S")
    nuevoNombreFoto = 'milanesa.jpg'
    if foto.filename != '':
        nuevoNombreFoto = tiempo + foto.filename
        foto.save(app.root_path + "/static/uploads/" + nuevoNombreFoto)

    # 3) SQL + cursor + execute + commit + close
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO platos (nombre, descripcion, precio, imagen)
        VALUES (%s, %s, %s, %s)
    """, (nombre, descripcion, precio, nuevoNombreFoto))
    mysql.connection.commit()
    cursor.close()

    # 4) REDIRECT: volvemos a la carta
    return redirect(url_for('carta'))

# --- CRUD: ELIMINAR UN PLATO (destroy) ---
@app.route('/destroy/<int:id>', methods=['POST'])
def destroy(id):
    cursor = mysql.connection.cursor()
    # CAMBIO: (id,) con coma para que sea una tupla (la guía lo escribe sin coma)
    cursor.execute("DELETE FROM platos WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('carta'))

# --- CRUD: MOSTRAR EL FORMULARIO PARA EDITAR (edit) ---
@app.route('/edit/<int:id>')
def edit(id):
    cursor = mysql.connection.cursor()
    # CAMBIO: (id,) con coma para que sea una tupla (la guía lo escribe sin coma)
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos WHERE id = %s", (id,))
    # fetchone trae UN solo plato (fetchall trae una lista de todos)
    plato = cursor.fetchone()
    cursor.close()
    return render_template('plato_form.html', accion='Editar', plato=plato)


# --- CRUD: GUARDAR LOS CAMBIOS DE UN PLATO (update) ---
@app.route('/update', methods=['POST'])
def update():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')

    # 2) SQL + cursor + execute + commit + close
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE platos
        SET nombre = %s, descripcion = %s, precio = %s
        WHERE id = %s
    """, (nombre, descripcion, precio, id))
    mysql.connection.commit()
    cursor.close()

    # 3) REDIRECT
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
            # Solo se llega acá si todo lo anterior salió bien
            return redirect(url_for('gracias', tipo='reserva'))
        except Exception as e:
            print("Error al guardar reserva:", e)
            mysql.connection.rollback()
            return "No pudimos guardar tu reserva. Por favor, intenta de nuevo más tarde."

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
            return redirect(url_for('gracias', tipo='consulta'))
        except Exception as e:
            print("Error al guardar mensaje:", e)
            mysql.connection.rollback()
            return "No pudimos guardar tu mensaje. Por favor, intenta de nuevo más tarde."

    return render_template('contacto.html')


# --- GRACIAS ---
@app.route('/gracias')
def gracias():
    tipo = request.args.get('tipo', 'consulta')
    return render_template('gracias.html', tipo=tipo)


if __name__ == '__main__':
    # Modo desarrollo para ver los errores en consola
    app.run(debug=True)
