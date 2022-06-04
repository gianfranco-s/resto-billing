import os
from flask import Blueprint, session, request, redirect, send_from_directory, current_app, render_template
from . import database
from datetime import datetime

bp = Blueprint('platos',__name__)

@bp.route('/update', methods=['POST'])
@bp.route('/update/<int:id_plato>', methods=['POST'])
def update_plato(id_plato=None):
    """Platos
    Alta y modificaciones
    """

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        nombre = request.form['txtNombre'].capitalize().replace(' ', '_')
        descripcion_plato = request.form['txtDescripcionPlato'].capitalize()
        precio = float(request.form['txtPrecio'])
        foto = request.files['txtFoto']
        categoria = request.form['txtCategoria']
        now = datetime.now()
        tiempo = now.strftime('%Y%H%M%S_')
        extension = foto.filename.split('.')
        if foto.filename != '':
            nuevo_nombre_foto = tiempo+nombre+'.'+extension[1]
            foto.save('App_restaurant/fotos/'+nuevo_nombre_foto)
            if id_plato:
                sql = 'SELECT foto FROM platos WHERE id_plato=%s'
                cursor.execute(sql, id_plato)
                foto_vieja = cursor.fetchall()[0][0]
                borrar_foto(foto_vieja)
        else:
            nuevo_nombre_foto = request.form['viejoNombreFoto']
            if nuevo_nombre_foto == '':
                nuevo_nombre_foto = 'Sin foto'
        dato = [nombre, descripcion_plato, precio, nuevo_nombre_foto, categoria]
        if id_plato:
            dato.append(id_plato)
            sql = """UPDATE platos
            SET nombre=%s,
            descripcion_plato=%s,
            precio=%s,
            foto=%s,
            id_categoria=%s
            WHERE id_plato=%s"""
        else:
            sql = """INSERT INTO platos
            (nombre,descripcion_plato,precio,foto,id_categoria)
            VALUES(%s,%s,%s,%s,%s)"""
        cursor.execute(sql, dato)
        conn.commit()
        return redirect('/administracion')
    else:
        return redirect('/')


def borrar_foto(nombre):
    """Borra la foto de 'App_restaurant/fotos' pasada por parametro"""
    try:
        os.remove('App_restaurant/fotos/' + nombre)
    except FileNotFoundError:
        print('Archivo no encontrado')


@bp.route('/updateCategoria', methods=['POST'])
@bp.route('/updateCategoria/<int:id_categoria>', methods=['POST'])
def update_categoria(id_categoria=None):
    """Categorias
    Alta y modificaciones
    """

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cat = request.form['txtCategoria'].capitalize().replace(' ', '_')
        datos = [cat]
        if id_categoria:
            datos.append(id_categoria)
            sql = """UPDATE categorias
            SET categoria=%s
            WHERE id_categoria=%s"""
        else:
            sql = """INSERT INTO categorias
            (categoria)
            VALUES(%s)"""
        cursor.execute(sql, datos)
        conn.commit()
        return redirect('/administracion')
    else:
        return redirect('/')


@bp.route('/fotos/<nombreFoto>')
def uploads(nombreFoto):
    """Guardado de las fotos en la carpeta correspondiente"""
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)


@bp.route('/edit/<int:id>')
def show_plato_edit_form(id):
    """Formulario para editar el plato"""

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        sql = """SELECT * FROM platos,
                categorias WHERE
                categorias.id_categoria=platos.id_categoria AND
                id_plato=%s"""
        cursor.execute(sql, (id, ))
        plato = list(cursor.fetchone())
        cursor.execute("SELECT * FROM categorias;")
        categorias = cursor.fetchall()
        conn.commit()
        return render_template('edit.html', plato=plato,
                               categorias=categorias)
    else:
        return redirect('/')


@bp.route('/destroy/<int:id>')  # Recibe como parámetro el id del producto
def destroy_plato(id):
    """Borrado de plato por ID"""

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT foto FROM platos
        WHERE id_plato=%s""", (id, ))
        fila = cursor.fetchone()[0]
        borrar_foto(fila)
        sql = "DELETE FROM platos WHERE id_plato=%s"
        cursor.execute(sql, (id, ))
        conn.commit()
        return redirect('/administracion')
    else:
        return redirect('/')


@bp.route('/destroyCategoria/<int:id>')
def destroy_categoria(id):
    """Borrado de categoria por ID"""

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        sql1 = """SELECT id_plato FROM platos
            WHERE id_categoria=%s"""
        cursor.execute(sql1, (id, ))
        platos = cursor.fetchall()
        sql2 = """UPDATE platos SET id_categoria=1
            WHERE id_plato=%s"""
        for plato in platos:
            cursor.execute(sql2, plato[0])
        sql3 = "DELETE FROM categorias WHERE id_categoria=%s"
        cursor.execute(sql3, (id, ))
        conn.commit()
        return redirect('/administracion')
    else:
        return redirect('/')
