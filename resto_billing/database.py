import os

import sqlite3

import cryptocode
import click
from flask import Blueprint, current_app
from flask.cli import with_appcontext
from os import environ

# from flaskext.mysql import MySQL
import psycopg2

bp = Blueprint('database', __name__)


def connect_to_db():
    # mysql = MySQL()
    # mysql.init_app(current_app)
    # return mysql.connect()

    return psycopg2.connect(
                host = 'localhost',
                dbname = environ.get('PGDB','my_resto'),
                user = environ.get('PGUSR','resto_billing'),
                password = environ.get('PGPASS','resto_billing')
                )


def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    # cursor.execute("CREATE DATABASE IF NOT EXISTS `my_resto`;")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS `my_resto`.`categorias` (
    #     `id_categoria` INT(10) NOT NULL AUTO_INCREMENT,
    #     `categoria` VARCHAR(255) NOT NULL,
    #     PRIMARY KEY (`id_categoria`))""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS `my_resto`.`platos` (
    #     `id_plato` INT(10) NOT NULL AUTO_INCREMENT,
    #     `nombre` VARCHAR(255) NOT NULL ,
    #     `descripcion_plato` VARCHAR(5000) NOT NULL ,
    #     `precio` FLOAT NOT NULL ,
    #     `foto` VARCHAR(5000) NOT NULL,
    #     `id_categoria` INT(10) NOT NULL,
    #     PRIMARY KEY (`id_plato`),
    #     FOREIGN KEY (`id_categoria`) REFERENCES `my_resto`.`categorias`(
    #     `id_categoria`));""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS `my_resto`.`mesas` (
    #     `id_mesa` INT(10) NOT NULL AUTO_INCREMENT,
    #     `pedidos` JSON DEFAULT ('{ }'),
    #     `hora_abre` DATETIME,
    #     PRIMARY KEY (`id_mesa`));""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS `my_resto`.`usuarios`(
    #     `usuario` VARCHAR(255) NOT NULL,
    #     `password` VARCHAR(500) NOT NULL,
    #     `super_usuario` BOOLEAN NULL DEFAULT FALSE,
    #     PRIMARY KEY (`usuario`))""")

    # cursor.execute("""CREATE TABLE IF NOT EXISTS `my_resto`.`ventas`(
    #     `id_venta` INT(20) NOT NULL AUTO_INCREMENT,
    #     `mesa`INT(10),
    #     `hora_abre` DATETIME ,
    #     `hora_cierra` DATETIME,
    #     `consumo` JSON NOT NULL DEFAULT ('{ }'),
    #     `total` INT(10),
    #     PRIMARY KEY (`id_venta`));""")

    
    # For PostgreSQL (database must be created before running the project)
    cursor.execute("""CREATE TABLE IF NOT EXISTS categorias (
        id_categoria SERIAL,
        categoria VARCHAR(255) NOT NULL,
        PRIMARY KEY (id_categoria))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS platos (
        id_plato SERIAL,
        nombre VARCHAR(255) NOT NULL ,
        descripcion_plato VARCHAR(5000) NOT NULL ,
        precio FLOAT NOT NULL ,
        foto VARCHAR(5000) NOT NULL,
        id_categoria INT NOT NULL,
        PRIMARY KEY (id_plato),
        FOREIGN KEY (id_categoria) REFERENCES categorias(
        id_categoria));""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS mesas (
        id_mesa SERIAL,
        pedidos JSON DEFAULT ('{ }'),
        hora_abre TIMESTAMP,
        PRIMARY KEY (id_mesa));""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        usuario VARCHAR(255) NOT NULL,
        password VARCHAR(500) NOT NULL,
        super_usuario BOOLEAN NULL DEFAULT FALSE,
        PRIMARY KEY (usuario))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS ventas(
        id_venta SERIAL,
        mesa INT,
        hora_abre TIMESTAMP,
        hora_cierra TIMESTAMP,
        consumo JSON NOT NULL DEFAULT ('{ }'),
        total INT,
        PRIMARY KEY (id_venta));""")

    conn.commit()


def create_admin_user(secret_key):
    conn = connect_to_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT count(*) FROM `my_resto`.`usuarios`")
    # cantidad_de_usuarios = cursor.fetchone()[0]
    # if cantidad_de_usuarios == 0:
    #     clave = cryptocode.encrypt('admin', secret_key)
    #     cursor.execute("""INSERT `my_resto`.`usuarios`(
    #         `usuario`,`password`,`super_usuario`)
    #         VALUES ('admin', %s, 1);""", (clave))

    # For PostgreSQL
    cursor.execute("SELECT count(*) FROM usuarios")
    cantidad_de_usuarios = cursor.fetchone()[0]
    if cantidad_de_usuarios == 0:
        clave = cryptocode.encrypt('admin', secret_key)
        cursor.execute("""INSERT INTO usuarios(
            usuario,password,super_usuario)
            VALUES (%s, %s, %s);""", ('admin', clave, '1'))
    conn.commit()


def define_default_category():
    conn = connect_to_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT count(*) FROM `my_resto`.`categorias`")
    # cantidad_de_categorias = cursor.fetchone()[0]
    # if cantidad_de_categorias == 0:
    #     cursor.execute("""INSERT IGNORE `my_resto`.`categorias` (`categoria`)
    #     VALUES('Sin categoria')""")

    # For PostgreSQL
    cursor.execute("SELECT count(*) FROM categorias")
    cantidad_de_categorias = cursor.fetchone()[0]
    if cantidad_de_categorias == 0:
        cursor.execute("""INSERT INTO categorias(categoria)
        VALUES('Sin categoria')""")
    conn.commit()
