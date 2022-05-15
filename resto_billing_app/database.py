import sqlite3
import cryptocode
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
from flaskext.mysql import MySQL


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  

    current_app.secret_key = '123Prueba!'
    current_app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    current_app.config['MYSQL_DATABASE_USER'] = 'root'
    current_app.config['MYSQL_DATABASE_PASSWORD'] = ''
    current_app.config['CARPETA'] = os.path.join('fotos')

    mysql = MySQL()
    
    mysql.init_app(current_app)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM `my_resto`.`usuarios`")

    cantidadDeUsuarios = cursor.fetchone()[0]

    if cantidadDeUsuarios == 0:
        clave = cryptocode.encrypt('admin', current_app.secret_key)
        cursor.execute("""INSERT `my_resto`.`usuarios`(
            `usuario`,`password`,`super_usuario`)
            VALUES ('admin', %s, 1);""", (clave))
    conn.commit()





def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

