-- =============================================================================
-- VecinoSeguro - Esquema inicial de base de datos
-- =============================================================================
-- Archivo:      schema.sql
-- Propósito:    Crea la base de datos del prototipo y las tablas principales
--               para roles, usuarios, emergencias e historial de estados.
-- Compatible:   MySQL 8.x y MariaDB 10.4+
-- Charset:      utf8mb4 (Unicode completo, soporta acentos y emojis)
-- Cotejamiento: utf8mb4_unicode_ci (case-insensitive, adecuado para español)
-- Autor:        Equipo VecinoSeguro
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Crear y seleccionar la base de datos
-- -----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS vecino_seguro
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE vecino_seguro;

-- -----------------------------------------------------------------------------
-- 2. Tabla `roles`
--    Define los roles del sistema. Por ejemplo: admin, vecino.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50)  NOT NULL UNIQUE COMMENT 'Identificador único del rol',
  description VARCHAR(255) NULL            COMMENT 'Descripción del rol y sus responsabilidades',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 3. Tabla `users`
--    Usuarios del sistema. La contraseña se almacena siempre como hash,
--    nunca en texto plano. RUT y email son únicos.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  rut           VARCHAR(12)  NOT NULL UNIQUE COMMENT 'RUT chileno con dígito verificador (formato 12345678-9)',
  full_name     VARCHAR(150) NOT NULL        COMMENT 'Nombre completo del usuario',
  email         VARCHAR(150) NOT NULL UNIQUE COMMENT 'Correo electrónico único',
  password_hash VARCHAR(255) NOT NULL        COMMENT 'Hash seguro de la contraseña (bcrypt/argon2)',
  role_id       INT          NOT NULL        COMMENT 'Rol asignado al usuario',
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_users_roles
    FOREIGN KEY (role_id) REFERENCES roles(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 4. Tabla `emergencies`
--    Registra las emergencias reportadas por los vecinos. Mantiene el estado
--    actual y el nivel de urgencia mediante ENUM para garantizar valores válidos.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS emergencies (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT          NOT NULL  COMMENT 'Usuario que creó la emergencia',
  type          VARCHAR(80)  NOT NULL  COMMENT 'Tipo de emergencia (ej: incendio, robo, corte de luz)',
  description   TEXT         NOT NULL  COMMENT 'Descripción detallada del evento',
  location      VARCHAR(255) NOT NULL  COMMENT 'Ubicación o sector donde ocurre',
  urgency_level ENUM('baja', 'media', 'alta', 'critica') NOT NULL DEFAULT 'media'
                COMMENT 'Nivel de urgencia: baja, media, alta, critica',
  status        ENUM('pendiente', 'en_revision', 'resuelto') NOT NULL DEFAULT 'pendiente'
                COMMENT 'Estado del ciclo de vida: pendiente, en_revision, resuelto',
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_emergencies_users
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 5. Tabla `emergency_status_history`
--    Audita los cambios de estado de cada emergencia. Permite saber quién
--    cambió qué y cuándo, opcionalmente con un comentario explicativo.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS emergency_status_history (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  emergency_id    INT          NOT NULL  COMMENT 'Emergencia afectada',
  previous_status VARCHAR(50)  NULL      COMMENT 'Estado anterior (NULL en el primer registro)',
  new_status      VARCHAR(50)  NOT NULL  COMMENT 'Estado nuevo aplicado',
  changed_by      INT          NOT NULL  COMMENT 'Usuario que realizó el cambio',
  changed_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment         TEXT         NULL      COMMENT 'Comentario opcional asociado al cambio',
  CONSTRAINT fk_history_emergencies
    FOREIGN KEY (emergency_id) REFERENCES emergencies(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT fk_history_users
    FOREIGN KEY (changed_by) REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 6. Índices secundarios para consultas frecuentes
--    Las claves foráneas crean su propio índice automáticamente, pero estos
--    índices adicionales optimizan filtros comunes como listar por estado,
--    ordenar por fecha de creación o auditar cambios por usuario.
-- -----------------------------------------------------------------------------
CREATE INDEX idx_users_role_id              ON users(role_id);
CREATE INDEX idx_emergencies_user_id        ON emergencies(user_id);
CREATE INDEX idx_emergencies_status         ON emergencies(status);
CREATE INDEX idx_emergencies_urgency_level  ON emergencies(urgency_level);
CREATE INDEX idx_emergencies_created_at     ON emergencies(created_at);
CREATE INDEX idx_history_emergency_id       ON emergency_status_history(emergency_id);
CREATE INDEX idx_history_changed_by         ON emergency_status_history(changed_by);

-- =============================================================================
-- Fin del script schema.sql
-- =============================================================================

