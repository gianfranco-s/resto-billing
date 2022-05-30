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
        for i in range(len(ventas)):
            ventas[i] = list(ventas[i])
            ventas[i][4] = (ventas[i][4][1:-1]).split(',')
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