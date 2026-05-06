-- =============================================================================
-- VecinoSeguro - Datos iniciales de prueba
-- =============================================================================
-- Archivo:      seed.sql
-- Propósito:    Insertar datos de ejemplo para desarrollo y demostración.
-- Importante:   Todos los datos son ficticios. Las contraseñas se muestran
--               como hashes de ejemplo y no deben usarse en ningún entorno
--               real. En producción deben generarse con bcrypt o argon2.
-- =============================================================================

USE vecino_seguro;

-- -----------------------------------------------------------------------------
-- 1. Roles iniciales del sistema
--    Las descripciones se mantienen alineadas con docs/requerimientos.md.
-- -----------------------------------------------------------------------------
INSERT INTO roles (name, description)
VALUES
  ('admin',  'Gestiona reportes, revisa estados y consulta resúmenes.'),
  ('vecino', 'Reporta emergencias y revisa estados.')
ON DUPLICATE KEY UPDATE description = VALUES(description);
-- -----------------------------------------------------------------------------
-- 2. Usuarios de ejemplo
--    RUT con formato chileno válido (algoritmo módulo 11).
--    password_hash es un valor ficticio identificable. NO usar en producción.
-- -----------------------------------------------------------------------------
INSERT INTO users (rut, full_name, email, password_hash, role_id)
VALUES
  ('11111111-1',
   'Administradora Vecinal',
   'admin@vecinoseguro.cl',
   '$2b$12$ficticio.admin.no.usar.en.produccion.AAAAAAAAAAAAAAA',
   1),
  ('22222222-2',
   'Carlos Pérez Soto',
   'carlos.perez@vecinoseguro.cl',
   '$2b$12$ficticio.vecino1.no.usar.en.produccion.BBBBBBBBBBBBB',
   2),
  ('13456789-9',
   'María González Rojas',
   'maria.gonzalez@vecinoseguro.cl',
   '$2b$12$ficticio.vecino2.no.usar.en.produccion.CCCCCCCCCCCCC',
   2)
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name);

-- -----------------------------------------------------------------------------
-- 3. Emergencias de ejemplo
--    Cubren distintos tipos, niveles de urgencia y estados para demostrar
--    el flujo completo del sistema durante las pruebas y la demo.
-- -----------------------------------------------------------------------------
INSERT INTO emergencies (user_id, type, description, location, urgency_level, status)
VALUES
  (2, 'Incendio',
      'Humo visible cerca de una vivienda. Vecinos reportan llamas en el techo.',
      'Pasaje Los Alerces 123, Villa El Bosque',
      'alta',    'pendiente'),
  (2, 'Corte de luz',
      'Sector completo sin suministro eléctrico desde hace dos horas.',
      'Plaza Central, frente a la Junta de Vecinos',
      'media',   'en_revision'),
  (3, 'Robo en proceso',
      'Persona sospechosa ingresando a una vivienda deshabitada.',
      'Avenida Los Robles 456, departamento 3B',
      'critica', 'resuelto'),
  (3, 'Inundación menor',
      'Acumulación de agua en la vereda tras lluvia intensa.',
      'Calle Las Camelias 78, frente al colegio',
      'baja',    'pendiente');

-- -----------------------------------------------------------------------------
-- 4. Historial de cambios de estado
--    Refleja el ciclo de vida de las emergencias. La primera fila de cada
--    emergencia tiene previous_status NULL (estado inicial al ser reportada).
--    La emergencia 3 muestra el flujo completo: pendiente -> en_revision -> resuelto.
-- -----------------------------------------------------------------------------
INSERT INTO emergency_status_history (emergency_id, previous_status, new_status, changed_by, comment)
VALUES
  -- Emergencia 1: solo registro inicial
  (1, NULL,          'pendiente',   2, 'Reporte inicial registrado por el vecino.'),

  -- Emergencia 2: registro inicial y paso a revisión
  (2, NULL,          'pendiente',   2, 'Reporte inicial registrado por el vecino.'),
  (2, 'pendiente',   'en_revision', 1, 'Equipo administrativo tomó contacto con la empresa eléctrica.'),

  -- Emergencia 3: ciclo completo
  (3, NULL,          'pendiente',   3, 'Reporte inicial registrado por el vecino.'),
  (3, 'pendiente',   'en_revision', 1, 'Carabineros notificados, en camino al lugar.'),
  (3, 'en_revision', 'resuelto',    1, 'Situación controlada. Persona detenida y entregada a la autoridad.'),

  -- Emergencia 4: solo registro inicial
  (4, NULL,          'pendiente',   3, 'Reporte inicial registrado por el vecino.');

-- =============================================================================
-- Fin del script seed.sql
-- =============================================================================
