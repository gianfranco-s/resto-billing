
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
    conn = database.connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql, nombre)
    global usuario
    usuario = cursor.fetchall()
    conn.commit()
    if usuario != ():
        clave2 = cryptocode.decrypt(usuario[0][1], current_app.secret_key)
        if password == clave2:
            session['username'] = usuario[0][0]
            if usuario[0][2]:
                session['super'] = usuario[0][2]
            return redirect('/mesas')
        else:
            flash('Usuario o contraseña erroneos')
            return redirect('/')
    else:
        flash('Usuario o contraseña erroneos')
        return redirect('/')