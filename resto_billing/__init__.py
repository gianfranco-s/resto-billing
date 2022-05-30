import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(SECRET_KEY='dev')
    app.config['CANTIDAD_DE_MESAS'] = int()
    app.config['CARPETA'] = os.path.join('fotos')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import database
    app.register_blueprint(database.bp)
    
    # For MySQL connections:
    app.secret_key = '123Prueba!'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''

    # For PostgreSQL connections
    
    database.create_tables()
    database.create_admin_user(app.secret_key)
    database.define_default_category()
    
    if os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true'):
        database.load_test_data()

    from . import start
    app.register_blueprint(start.bp)


    from . import mesas
    app.register_blueprint(mesas.bp)


    from . import administracion
    app.register_blueprint(administracion.bp)


    from . import platos
    app.register_blueprint(platos.bp)


    from . import historial
    app.register_blueprint(historial.bp)

    return app