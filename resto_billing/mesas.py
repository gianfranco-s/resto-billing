
from flask import Blueprint, session, request, current_app, render_template, flash, redirect, make_response
from . import database
import json


bp = Blueprint('mesas', __name__)

@bp.route('/mesas/')
def mesas():
    """Listado de mesas, carga de pedidos por mesa, y cierre de mesa"""

    cookie = request.cookies.get('mesas')
    if cookie:
        current_app.config['CANTIDAD_DE_MESAS'] = int(cookie)

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id_mesa,pedidos FROM mesas")
        mesas_backend = cursor.fetchall()
        mesas = list()
        for mesa in mesas_backend:
            nro_de_mesa = mesa[0]
            pedido = mesa[1]
            suma = 0
            subtotales = list()
            if pedido:
                pedido = json.loads(pedido)  # mesa[1] trae un json
                for plato, cantidad in pedido.items():
                    cursor.execute("""SELECT precio FROM platos
                                   WHERE nombre LIKE %s;""", (plato, ))
                    precio_unitario = cursor.fetchone()[0]
                    subtotal_por_plato = precio_unitario * int(cantidad)
                    subtotales.append((f'{plato}: {cantidad}',
                                       subtotal_por_plato))
                    suma += subtotal_por_plato
            else:
                subtotales.append(['Sin pedidos', 0])
            mesas.append([nro_de_mesa, subtotales, suma])

        # Acotamos la cantidad de mesas al número indicado por el usuario
        mesas = mesas[:current_app.config['CANTIDAD_DE_MESAS']]
        # mesas: (list of lists)
        # mesas[0]: (list)
        #     mesas[0][0]: (int) número de mesa
        #     mesas[0][1]: (tuple) pedido
        #     mesas[0][1][0]: (str) item (agua, fideos, etc)
        #     mesas[0][1][1]: (float) subtotal
        return render_template('/mesas.html', mesas=mesas)
    else:
        flash('Debe registrarse antes')
        return redirect('/')


@bp.route('/cantidad_mesas/', methods=['POST'])
def cantidadMesas():
    """Cantidad de mesas del negocio"""

    current_app.config['CANTIDAD_DE_MESAS'] = int(request.form['cantidad_mesas'])
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM mesas")
    mesas = int(cursor.fetchone()[0])
    while mesas < current_app.config['CANTIDAD_DE_MESAS']:
        cursor.execute("INSERT INTO mesas(pedidos) VALUES(NULL)")
        mesas += 1
    conn.commit()
    respuesta = make_response(redirect('/administracion'))
    respuesta.set_cookie('mesas', str(current_app.config['CANTIDAD_DE_MESAS']))
    return respuesta