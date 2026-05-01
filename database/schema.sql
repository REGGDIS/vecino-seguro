-- Script inicial de esquema para VecinoSeguro.
-- Crea una base de datos MySQL y tablas principales para usuarios, roles y emergencias.

CREATE DATABASE IF NOT EXISTS vecino_seguro
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE vecino_seguro;

-- Roles básicos del sistema, por ejemplo administrador y vecino.
CREATE TABLE IF NOT EXISTS roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

-- Usuarios del sistema. La contraseña se almacena como hash, nunca en texto plano.
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rut VARCHAR(12) NOT NULL UNIQUE,
  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_users_roles
    FOREIGN KEY (role_id) REFERENCES roles(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- Emergencias reportadas por vecinos.
CREATE TABLE IF NOT EXISTS emergencies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  type VARCHAR(80) NOT NULL,
  description TEXT NOT NULL,
  location VARCHAR(255) NOT NULL,
  urgency_level ENUM('baja', 'media', 'alta', 'critica') NOT NULL DEFAULT 'media',
  status ENUM('reportada', 'en_revision', 'en_proceso', 'resuelta', 'cancelada') NOT NULL DEFAULT 'reportada',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_emergencies_users
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- Historial de cambios de estado para auditar el ciclo de vida de una emergencia.
CREATE TABLE IF NOT EXISTS emergency_status_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  emergency_id INT NOT NULL,
  previous_status VARCHAR(50),
  new_status VARCHAR(50) NOT NULL,
  changed_by INT NOT NULL,
  changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_history_emergencies
    FOREIGN KEY (emergency_id) REFERENCES emergencies(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT fk_history_users
    FOREIGN KEY (changed_by) REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_emergencies_user_id ON emergencies(user_id);
CREATE INDEX idx_emergencies_status ON emergencies(status);
CREATE INDEX idx_emergencies_urgency_level ON emergencies(urgency_level);
CREATE INDEX idx_history_emergency_id ON emergency_status_history(emergency_id);

