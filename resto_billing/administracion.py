from flask import Blueprint, session, current_app, render_template, redirect
from . import database

bp = Blueprint('administracion',__name__)

@bp.route('/administracion/')
def mostrar_administracion():
    """Administración
    Alta y edición de usuarios
    Platos
    Configura la cantidad de mesas
    """

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT* FROM platos,
                            categorias WHERE
                            categorias.id_categoria=
                            platos.id_categoria
                            ORDER BY categoria;""")
        platos = cursor.fetchall()
        cursor.execute("SELECT * FROM categorias;")
        categorias = cursor.fetchall()
        conn.commit()
        
        return render_template(
                'administracion.html',
                platos=platos,
                cantidad=current_app.config['CANTIDAD_DE_MESAS'],
                categorias=categorias)
    else:
        return redirect('/')