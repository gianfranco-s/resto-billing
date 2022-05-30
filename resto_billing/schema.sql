CREATE DATABASE IF NOT EXISTS `my_resto`;


CREATE TABLE IF NOT EXISTS `my_resto`.`platos` (
    `id_plato` INT(10) NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(255) NOT NULL ,
    `descripcion_plato` VARCHAR(5000) NOT NULL ,
    `precio` FLOAT NOT NULL ,
    `foto` VARCHAR(5000) NOT NULL,
    PRIMARY KEY (`id_plato`) );


CREATE TABLE IF NOT EXISTS `my_resto`.`mesas` (
    `id_mesa` INT(10) NOT NULL AUTO_INCREMENT,
    `pedidos` JSON DEFAULT ('{ }'),
    `hora_abre` DATETIME,
    PRIMARY KEY (`id_mesa`));


CREATE TABLE IF NOT EXISTS `my_resto`.`ventas`(
    `id_venta` INT(20) NOT NULL AUTO_INCREMENT,
    `mesa`INT(10),
    `hora_abre` DATETIME ,
    `hora_cierra` DATETIME,
    `consumo` JSON NOT NULL DEFAULT ('{ }'),
    `total` INT(10),
    PRIMARY KEY (`id_venta`));


CREATE TABLE IF NOT EXISTS `my_resto`.`usuarios`(
    `usuario` VARCHAR(255) NOT NULL,
    `password` VARCHAR(500) NOT NULL,
    `super_usuario` BOOLEAN NULL DEFAULT FALSE,
    PRIMARY KEY (`usuario`))