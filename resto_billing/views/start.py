
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from resto_billing.models import database
import cryptocode

bp = Blueprint('start', __name__)

@bp.route('/')
def login():
    return render_template('/index.html')


@bp.route('/ingresar', methods=['POST'])
def ingresar():
    usuario_backend = ()

    nombre = request.form['txtUsuario']
    password = request.form['txtPassword']
    sql = "SELECT * FROM usuarios WHERE usuario = %s"
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (nombre, ))
    usuario_backend = cursor.fetchone()
    conn.commit()
    
    if usuario_backend:
        usuario, clave, superusuario = usuario_backend
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
        nuevo_usuario = request.form['txtUsuario']
        nuevo_password = cryptocode.encrypt(request.form['txtPassword'], 
                                            current_app.secret_key)
        super = request.form.get('superUsuario')
        datos_usuario = nuevo_usuario, nuevo_password, super
        sql = """INSERT INTO usuarios(
            usuario, password, super_usuario) VALUES (%s, %s,%s)"""
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios ;")
        usuarios_backend = cursor.fetchall()
        usuarios_registrados = set(i[0] for i in usuarios_backend)
        if nuevo_usuario not in usuarios_registrados:
            cursor.execute(sql, datos_usuario)
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
        nuevo_nombre = request.form['txtUsuario']
        nuevo_password = request.form['txtPassword']
        nuevo_password = cryptocode.encrypt(nuevo_password, current_app.secret_key)
        usuario_modificado = nuevo_nombre, nuevo_password, session['username']
        sql = """UPDATE usuarios
        SET usuario= %s, password= %s WHERE usuario=%s;"""
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario FROM usuarios;")
        usuarios_backend = cursor.fetchall()
        usuarios_registrados = set(i[0] for i in usuarios_backend)
        if (nuevo_nombre not in usuarios_registrados 
            or nuevo_nombre == session['username']):
            cursor.execute(sql, usuario_modificado)
            session['username'] = nuevo_nombre
        else:
            flash('Nombre de usuario no disponible')
        conn.commit()
        return redirect('/administracion')
