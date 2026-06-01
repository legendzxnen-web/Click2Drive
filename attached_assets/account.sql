-- =============================================
-- Click2Drive Database Setup
-- Run this in phpMyAdmin > SQL tab
-- =============================================

CREATE DATABASE IF NOT EXISTS click2drive
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE click2drive;

CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
