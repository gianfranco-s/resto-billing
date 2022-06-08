from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from os import environ


# These values are found in database.py
pg_connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    environ.get('POSTGRES_USR','resto_billing'),
    environ.get('POSTGRES_PWD','resto_billing'),
    environ.get('POSTGRES_HOST', 'localhost'),
    environ.get('POSTGRES_PORT', '5432'),
    environ.get('POSTGRES_DB','my_resto'),
)

current_app.config['SQLALCHEMY_DATABASE_URI'] = pg_connection_string
db = SQLAlchemy(current_app)


class PlatoPruebaModel(db.Model):
    __tablename__ = 'platos_prueba'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(120), nullable=True)
    precio = db.Column(db.Float(), nullable=False)
    # foto
    # id_categoria

    def __init__(self, nombre, descripcion, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

    def __repr__(self):
        return '<PlatoPruebaModel %r>' % self.nombre
