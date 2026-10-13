# AVANCE: navegación entre páginas con Flask + la carta leída desde MySQL.
# Todavía NO se guarda nada desde los formularios (reservas y contacto quedan para la entrega final).
from datetime import date
from flask import Flask, render_template
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
    # Leemos los platos de la tabla 'platos' y se los mandamos al HTML
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos")
    platos = cursor.fetchall()
    cursor.close()
    return render_template('carta.html', platos=platos)


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
