#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
# 999 # Clase "catalogo" renombrada a "Usuarios" - SJG
class Usuarios:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # 999 # Esto queda igual
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        # 999 # Cambio de estructura - SJG

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    # 999 # Adaptada a usuarios - SJG
    def alta_corta(self, nombre, apellido, documento, direccion, pais, fono, email, contrasena):
               
        sql = "INSERT INTO usuarios (nombre, apellido, documento, direccion, pais, fono, email, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, documento, direccion, pais, fono, email, contrasena)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuarios = self.cursor.fetchall()
        return usuarios

    #----------------------------------------------------------------
    def modificar_usuario(self, nombre, apellido, documento, direccion, pais, fono, email):
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, direccion = %s, pais = %s, fono = %s, email = %s WHERE documento = %s"
        valores = (nombre, apellido, direccion, pais, fono, email, documento)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def eliminar_usuario(self, documento):
        self.cursor.execute(f"DELETE FROM usuarios WHERE documento = {documento}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    #----------------------------------------------------------------
    def consultar_usuario(self, dni):
        # Consultamos un usuario a partir de su documento
        self.cursor.execute(f"SELECT * FROM usuarios WHERE documento = {dni}")
        return self.cursor.fetchone()  

#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
# 999 # Instanciamos a la clase Usuarios - SJG 
# 999 # Se asume que el usuario "root" de MySQL NO TIENE CLAVE
usuario = Usuarios(host='localhost', user='root', password='', database='gobaires')
#catalogo = Catalogo(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')

#--------------------------------------------------------------------
# Se agrega el Home del sitio
#--------------------------------------------------------------------
@app.route("/")
def home():
    return render_template('index.html')
    
#--------------------------------------------------------------------
# Se agrega el acceso al registro
#--------------------------------------------------------------------
@app.route("/show_reservas")
def show_reservas():
    return render_template('reservas.html')

@app.route("/show_registro")
def show_registro():
    return render_template('registro.html')

@app.route("/show_alta_user")
def show_alta_user():
    return render_template('alta_user.html')

@app.route("/show_list_user")
def show_list_user():
    return render_template('list_user.html')

@app.route("/show_modi_user")
def show_modi_user():
    return render_template('modi_user.html')

@app.route("/show_dele_user")
def show_dele_user():
    return render_template('dele_user.html')

# -------------------------
# Nuevo usuario
#--------------------------------------------------------------------
# 999 # Se modifica la ruta
# 999 # 
@app.route("/do_alta_user", methods=["POST"])
#La ruta Flask `/productos` con el método HTTP POST está diseñada para permitir la adición de un nuevo producto a la base de datos.
#La función agregar_producto se asocia con esta URL y es llamada cuando se hace una solicitud POST a /productos.
def do_alta_user():
    #Recojo los datos del form
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    documento = request.form['documento']
    direccion = request.form['direccion']
    pais = request.form['pais']
    fono = request.form['fono']
    email = request.form['email']
    contrasena = request.form['contrasena']

    id_user = usuario.alta_corta(nombre, apellido, documento, direccion, pais, fono, email, contrasena)
    
    if id_user > 0:    
        #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Usuario agregado correctamente."}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el usuario."}), 500
    

#--------------------------------------------------------------------
# Nuevo usuario
#--------------------------------------------------------------------
# 999 # Se modifica la ruta
# 999 # 
@app.route("/do_list_user", methods=["GET"])
#La ruta Flask `/productos` con el método HTTP POST está diseñada para permitir la adición de un nuevo producto a la base de datos.
#La función agregar_producto se asocia con esta URL y es llamada cuando se hace una solicitud POST a /productos.
def do_list_user():
    usuarios = usuario.listar_usuarios()
    return jsonify(usuarios)

@app.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
    # Obtener el ID de usuario enviado desde el formulario
    documento = request.form['documento']

    # Verificar si el usuario con el ID proporcionado existe en la base de datos
    cur = usuario.conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE documento = %s", (documento,))
    dat_usuario = cur.fetchone()
    cur.close()

    if dat_usuario:
        # Crear un diccionario con los datos del usuario
        datos_usuario = {
            'id_user': dat_usuario[0],
            'nombre': dat_usuario[1],
            'apellido': dat_usuario[2],
            'documento': dat_usuario[3],
            'direccion': dat_usuario[4],
            'pais': dat_usuario[5],
            'fono': dat_usuario[6],
            'email': dat_usuario[7]
        }
        # Devolver los datos del usuario como respuesta JSON
        return jsonify(datos_usuario)
    else:
        return jsonify({"error": "Usuario no encontrado"})

@app.route("/do_updt_user", methods=["POST"])
def do_updt_user():
    #Recojo los datos del form
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    documento = request.form['documento']
    direccion = request.form['direccion']
    pais = request.form['pais']
    fono = request.form['fono']
    email = request.form['email']
     
    updt_user = usuario.modificar_usuario(nombre, apellido, documento, direccion, pais, fono, email)

    if updt_user:    
        #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Usuario agregado correctamente."}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el usuario."}), 500
    
    
@app.route('/do_dele_user/<documento>', methods=["DELETE"])
def do_dele_user(documento):  
    # Verificar si el usuario con el ID proporcionado existe en la base de datos
    cur = usuario.conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE documento = %s", (documento,))
    existe_usuario = cur.fetchone()
    cur.close()

    if existe_usuario:
        cur = usuario.conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE documento = %s", (documento,))
        pudo_eliminar = cur.rowcount > 0 
        cur.close()           

        if pudo_eliminar:   
            #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
            return jsonify({"mensaje": "Usuario eliminado correctamente."}), 201
        else:
            #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
            return jsonify({"mensaje": "Error al agregar el usuario."}), 500
    else:
        return jsonify({"mensaje": "Error al agregar el usuario <documento>."}), 500

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)