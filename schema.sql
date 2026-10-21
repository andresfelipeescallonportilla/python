-- =====================================================================
--  Pet Manager - estructura de la base de datos MySQL
--  Base de datos: gestormascotasbd
--
--  La estructura es idéntica a la del proyecto Java original
--  (base de datos "administracionmascotasbd"), por lo que puedes usar
--  cualquiera de las dos sin cambiar el código.
--
--  Cómo usarlo en phpMyAdmin (XAMPP):
--    1. Abre http://localhost/phpmyadmin
--    2. Pestaña "Importar" -> "Choose File" -> selecciona este archivo .sql
--    3. Pulsa "Continuar" / "Importar"
--  (o bien: pestaña "SQL" -> pega el contenido -> "Ejecutar")
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `gestormascotasbd`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `gestormascotasbd`;

-- ---------------------------------------------------------------------
-- Tabla general de mascotas (común para perros y gatos)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `tb_pet_hospital`;
DROP TABLE IF EXISTS `tb_hospital`;
DROP TABLE IF EXISTS `tb_doctor`;
DROP TABLE IF EXISTS `tb_dog`;
DROP TABLE IF EXISTS `tb_cat`;
DROP TABLE IF EXISTS `tb_pet`;

CREATE TABLE `tb_pet` (
    `id`            INT         NOT NULL AUTO_INCREMENT,
    `code`          VARCHAR(20) NOT NULL,
    `name`          VARCHAR(50) NOT NULL,
    `born_year`     INT         NOT NULL DEFAULT 0,
    `color`         VARCHAR(20) NOT NULL DEFAULT '',
    `health_status` VARCHAR(30) NOT NULL DEFAULT 'Healthy',
    PRIMARY KEY (`id`),
    KEY `idx_tb_pet_code` (`code`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Tabla específica de perros
--   NOTA: la clave primaria se llama "id" (igual que en la base de datos
--   original del proyecto Java). El programa la detecta sola, por lo que
--   también funciona si en tu base de datos se llama "id_dog".
-- ---------------------------------------------------------------------
CREATE TABLE `tb_dog` (
    `id`       INT         NOT NULL AUTO_INCREMENT,
    `breed`    VARCHAR(30) NOT NULL DEFAULT '',
    `pedigree` TINYINT(1)  NOT NULL DEFAULT 0,
    `id_pet`   INT         NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_tb_dog_pet` (`id_pet`),
    CONSTRAINT `fk_tb_dog_pet` FOREIGN KEY (`id_pet`)
        REFERENCES `tb_pet` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Tabla específica de gatos
-- ---------------------------------------------------------------------
CREATE TABLE `tb_cat` (
    `id`     INT         NOT NULL AUTO_INCREMENT,
    `breed`  VARCHAR(30) NOT NULL DEFAULT '',
    `id_pet` INT         NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_tb_cat_pet` (`id_pet`),
    CONSTRAINT `fk_tb_cat_pet` FOREIGN KEY (`id_pet`)
        REFERENCES `tb_pet` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Tablas del módulo de hospital / veterinario (clases clsDoctor,
-- clsVeterinary y AbstHospital del proyecto Java)
-- ---------------------------------------------------------------------
CREATE TABLE `tb_doctor` (
    `id`      INT          NOT NULL AUTO_INCREMENT,
    `name`    VARCHAR(150) NOT NULL,
    `phone`   VARCHAR(20)  DEFAULT NULL,
    `address` VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

CREATE TABLE `tb_hospital` (
    `id`          INT         NOT NULL AUTO_INCREMENT,
    `name`        VARCHAR(50) NOT NULL,
    `phone`       VARCHAR(50) DEFAULT NULL,
    `address`     VARCHAR(50) DEFAULT NULL,
    `patien_type` INT         DEFAULT NULL,
    `id_doctor`   INT         DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_tb_hospital_doctor` (`id_doctor`),
    CONSTRAINT `fk_tb_hospital_doctor` FOREIGN KEY (`id_doctor`)
        REFERENCES `tb_doctor` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

CREATE TABLE `tb_pet_hospital` (
    `id`          INT NOT NULL AUTO_INCREMENT,
    `id_pet`      INT NOT NULL,
    `id_hospital` INT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_tb_pet_hospital_pet` (`id_pet`),
    KEY `fk_tb_pet_hospital_hospital` (`id_hospital`),
    CONSTRAINT `fk_tb_pet_hospital_pet` FOREIGN KEY (`id_pet`)
        REFERENCES `tb_pet` (`id`),
    CONSTRAINT `fk_tb_pet_hospital_hospital` FOREIGN KEY (`id_hospital`)
        REFERENCES `tb_hospital` (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Datos de ejemplo (opcionales)
-- ---------------------------------------------------------------------
INSERT INTO `tb_pet` (`code`, `name`, `born_year`, `color`, `health_status`) VALUES
    ('001', 'Firulais', 2015, 'gris',   'Sick'),
    ('002', 'Tobby',    2018, 'Negro',  'Healthy'),
    ('003', 'Michi',    2020, 'Negro',  'In Surgery');

INSERT INTO `tb_dog` (`breed`, `pedigree`, `id_pet`) VALUES
    ('Criollo', 0, 1),
    ('Pincher',  1, 2);

INSERT INTO `tb_cat` (`breed`, `id_pet`) VALUES
    ('British', 3);
