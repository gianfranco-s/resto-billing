import json

from flask import Blueprint, session, request, render_template, redirect, flash
from . import database
from datetime import datetime

bp = Blueprint('historial',__name__)

@bp.route('/ventas/', methods=['GET'])
def ventas():
    """Listado de todas las ventas históricas"""

    if 'super' in session:
        desde = request.args.get('desde')
        hasta = request.args.get('hasta')
        mesa = request.args.get('mesa')
        datos = [desde, hasta]
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")
        ventas = list(cursor.fetchall())
        if len(ventas) > 0:
            fechasMin = (str((ventas[0][2]))).split(' ')[0]
        else:
            fechasMin = datetime.today().strftime('%Y-%m-%d')
        fechasMax = datetime.today().strftime('%Y-%m-%d')
        cursor.execute("SELECT count(*) FROM mesas")
        totalMesas = cursor.fetchone()[0]
        listaMesas = []
        for i in range(1, totalMesas+1):
            listaMesas.append(i)
        if desde and hasta:
            sql = """SELECT * FROM ventas
            WHERE hora_abre BETWEEN %s AND %s"""
            if mesa:
                if mesa != 'Todas':
                    sql += ' AND `mesa` LIKE %s'
                    datos.append(int(mesa))
            else:
                mesa = 'Todas'
            cursor.execute(sql, datos)
            ventas = list(cursor.fetchall())
            fechasMin = desde
            fechasMax = hasta
        else:
            mesa = 'Todas'
        fechasMinMax = (fechasMin, fechasMax)
        total = 0
        print('ventas = ',ventas)
        for i in range(len(ventas)):
            ventas[i] = list(ventas[i]) # ventas[i] era una tupla
            # ventas[i][4] = (ventas[i][4][1:-1]).split(',')  # ventas[i][4] contiene el pedido de la mesa
            total += ventas[i][5]
        conn.commit()
        return render_template('ventas.html',
                               ventas=ventas,
                               total=total,
                               fechasMinMax=fechasMinMax,
                               listaMesas=listaMesas,
                               mesa=mesa)
    flash('Usuario no autorizado a ver el historial')
    return redirect('/mesas')


@bp.route('/cerrar_cuenta/<int:mesa>/')
def cerrarCuenta(mesa):
    """Cerrar la cuenta de la mesa"""

    conn = database.connect()
    cursor = conn.cursor()
    sql = """SELECT pedidos, hora_abre FROM mesas
    WHERE id_mesa = %s"""
    cursor.execute(sql, (mesa, ))
    extracto = cursor.fetchall()[0]
    pedidos, horaAbre = extracto
    # pedidosBorrar = json.loads(pedidos)
    pedidosBorrar = pedidos
    pedidos = json.dumps(pedidos)
    resumen = []
    suma = 0
    if type(pedidosBorrar) == dict:
        for key in pedidosBorrar:
            cant = pedidosBorrar[key]
            sql2 = """SELECT precio FROM platos
                WHERE nombre = %s;"""
            cursor.execute(sql2, (key, ))  # Buscamos el precio unitario del plato
            precio = int(cursor.fetchone()[0])  # Almacenamos el precio
            monto = precio*cant
            suma += monto
            plato = (key, cant, monto)
            resumen.append(plato)
        resumen.append(suma)
        sqlBorrar = """UPDATE mesas
        SET pedidos=NULL, hora_abre=NULL
        WHERE id_mesa=%s;"""
        cursor.execute(sqlBorrar, (mesa, ))
        horaCierra = datetime.now()
        datosVenta = (mesa, horaAbre, horaCierra, pedidos, suma)
        sqlventa = """INSERT INTO ventas
        (mesa, hora_abre, hora_cierra, consumo, total)
        VALUES(%s, %s, %s, %s, %s);"""
        cursor.execute(sqlventa, datosVenta)
        conn.commit()
        return render_template('/resumen.html', resumen=resumen)
    else:
        flash('La mesa no contenia ningun pedido')
        return redirect('/mesas')