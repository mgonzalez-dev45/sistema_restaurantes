# AVANCE: navegación entre páginas con Flask + la carta leída desde MySQL.
# Todavía NO se guarda nada desde los formularios (reservas y contacto quedan para la entrega final).
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


# --- RESERVAS (solo muestra el formulario, todavía no guarda) ---
@app.route('/reservas')
def reservas():
    # 'hoy' evita que el calendario deje elegir fechas pasadas
    return render_template('reservas.html', hoy=date.today().isoformat())


# --- CONTACTO (solo muestra el formulario, todavía no guarda) ---
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


# --- GRACIAS ---
@app.route('/gracias')
def gracias():
    return render_template('gracias.html', tipo='consulta')


if __name__ == '__main__':
    # Modo desarrollo para ver los errores en consola
    app.run(debug=True)
