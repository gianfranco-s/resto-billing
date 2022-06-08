
from flask import Blueprint, session, request, current_app, render_template, flash, redirect, make_response
from resto_billing import database
import json
from datetime import datetime

bp = Blueprint('mesas', __name__)

@bp.route('/mesas/')
def listar_mesas():
    """Listado de mesas, carga de pedidos por mesa, y cierre de mesa
    mesas =[
        {
            'nro_mesa': int,
            'pedido': {
                        'plato': [...],
                        'cantidad': [...],
                        'subtotales': [...]
                      },
            'total': float
        },
    ]
    """

    cookie = request.cookies.get('mesas')
    if cookie:
        current_app.config['CANTIDAD_DE_MESAS'] = int(cookie)

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id_mesa,pedidos FROM mesas ORDER BY id_mesa ASC")
        mesas_backend = cursor.fetchall()
        mesas = list()
        for mesa in mesas_backend:
            mesa_dict = dict()
            pedido_dict = dict()

            nro_mesa = mesa[0]
            pedido = mesa[1]
            suma = 0
            
            subtotales_list = list()
            plato_list = list()
            cantidad_list = list()
            if pedido:
                for plato, cantidad in pedido.items():
                    cursor.execute("""SELECT precio FROM platos
                                   WHERE nombre LIKE %s;""", (plato,))
                    precio_unitario = cursor.fetchone()[0]
                    subtotal_por_plato = precio_unitario * int(cantidad)
                    suma += subtotal_por_plato
                    
                    plato_list.append(plato)
                    cantidad_list.append(cantidad)
                    subtotales_list.append(subtotal_por_plato)
            else:
                plato_list = ['Sin pedidos']
                cantidad_list = ['']
                subtotales_list = [0]

            pedido_dict['plato'] = plato_list
            pedido_dict['cantidad'] = cantidad_list
            pedido_dict['subtotales'] = subtotales_list

            mesa_dict['nro_mesa'] = nro_mesa
            mesa_dict['pedido'] = pedido_dict
            mesa_dict['total'] = suma
            mesas.append(mesa_dict)

        # Acotamos la cantidad de mesas al número indicado por el usuario en /administracion
        mesas = mesas[:current_app.config['CANTIDAD_DE_MESAS']]

        return render_template('/mesas.html', mesas=mesas)
    else:
        flash('Debe registrarse antes')
        return redirect('/')



@bp.route('/cantidad_mesas/', methods=['POST'])
def establecer_mesas():
    """Establece la cantidad de mesas del negociom según lo indica el usuario"""

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


@bp.route('/platos/<int:id_mesa>/')
def editar_pedido(id_mesa):
    """Listado del menu disponible
    Agregar o quitar platos al pedido
    """

    if 'username' in session:
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM platos;")
        platos = cursor.fetchall()
        conn.commit()
        return render_template('platos.html', platos=platos, mesa=id_mesa)
    else:
        return redirect('/')


@bp.route('/cargarPedido/<int:mesa>', methods=['POST'])
def cargar_pedido(mesa):
    """Cargar pedidos a una mesa"""

    conn = database.connect()
    cursor = conn.cursor()
    sql = "SELECT pedidos FROM mesas WHERE id_mesa=%s;"
    cursor.execute(sql, (mesa, ))
    pedidos = cursor.fetchall()[0][0]
    if bool(pedidos):
        # pedidos = json.loads(str(pedidos))
        pedidos = pedidos
    else:
        hora = datetime.now()
        datos = (hora, mesa)
        sql = "UPDATE mesas SET hora_abre=%s WHERE id_mesa=%s;"
        cursor.execute(sql, datos)
        pedidos = {}
    keys_db = pedidos.keys()
    datos_form = request.form
    keys_form = datos_form.keys()
    for key_form in keys_form:
        if int(datos_form[key_form]) != 0:
            valor = int(datos_form[key_form])
            if key_form in keys_db:  # Pedido previamente
                if (int(pedidos[key_form]) + valor) > 0:
                    pedidos[key_form] = int(pedidos[key_form]) + valor
                else:
                    pedidos.pop(key_form)
            elif valor > 0:
                pedidos.setdefault(key_form, datos_form[key_form])
        for key in pedidos:
            pedidos[key] = int(pedidos[key])
    sql = "UPDATE mesas SET pedidos=%s WHERE id_mesa=%s;"
    valores = (json.dumps(pedidos), (mesa, ))
    cursor.execute(sql, valores)
    conn.commit()
    return redirect('/mesas/')