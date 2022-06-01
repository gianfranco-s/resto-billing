
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from . import database
import cryptocode

bp = Blueprint('start', __name__)

@bp.route('/')
def login():
    return render_template('/index.html')


@bp.route('/ingresar', methods=['POST'])
def ingresar():
    nombre = request.form['txtUsuario']
    password = request.form['txtPassword']
    sql = "SELECT * FROM `my_resto`.`usuarios` WHERE `usuario` LIKE %s"
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute(sql, nombre)
    current_app.config['USUARIO'] = cursor.fetchone()
    conn.commit()
    (usuario, clave, superusuario) = current_app.config['USUARIO']
    if usuario != ():
        if password == cryptocode.decrypt(clave, current_app.secret_key):
            session['username'] = usuario
            if superusuario:
                session['super'] = superusuario
            return redirect('/mesas')
        else:
            flash('Usuario o contraseña erroneos')
            return redirect('/')
    else:
        flash('Usuario o contraseña erroneos')
        return redirect('/')


@bp.route('/logout/')
def logout():
    session.pop('username', None)  # Borramos la cookie
    session.pop('super', None)  # Borramos la cookie
    return redirect('/')


@bp.route('/crear_usuario/', methods=['POST'])
def crear_usuario():
    """Creacion de nuevo usuario. Requiere ser super usuario"""

    if 'super' in session:
        nuevoUsuario = request.form['txtUsuario']
        nuevoPassword = request.form['txtPassword']
        super = request.form.get('superUsuario')
        nuevoPassword = cryptocode.encrypt(nuevoPassword, current_app.secret_key)
        usuario1 = nuevoUsuario, nuevoPassword, super
        sql = """INSERT INTO usuarios(
            usuario, password, super_usuario) VALUES (%s, %s,%s)"""
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios;")
        usuarios1 = cursor.fetchall()
        usuarios = []
        for usuarioj in usuarios1:
            usuarios.append(usuarioj[0])
        if nuevoUsuario not in usuarios:
            cursor.execute(sql, usuario1)
        else:
            flash('Nombre de usuario no disponible')
        conn.commit()
        return redirect('/administracion')
    else:
        flash('Usted no tiene los permisos para agregar un nuevo usuario')
        return redirect('/')


@bp.route('/modificar_usuario/', methods=['POST'])
def modificar_usuario():
    """Edicion datos usuario (propios)"""

    if 'username' in session:
        nuevoNombre = request.form['txtUsuario']
        nuevoPassword = request.form['txtPassword']
        nuevoPassword = cryptocode.encrypt(nuevoPassword, current_app.secret_key)
        usuario = current_app.config['USUARIO']
        usuario1 = (nuevoNombre, nuevoPassword, usuario[0][0])
        sql = """UPDATE usuarios
        SET usuario= %s, password= %s WHERE usuario=%s;"""
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios;")
        usuarios = cursor.fetchall()  # Almacenamos los datos en una tupla
        if nuevoNombre not in usuarios or nuevoNombre == usuario[0][0]:
            cursor.execute(sql, usuario1)  # Actualizamos del usuario
        else:
            flash('Nombre de usuario no disponible')
        conn.commit()
        return redirect('/administracion')
