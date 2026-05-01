-- Datos iniciales de ejemplo para VecinoSeguro.
-- Los password_hash son ficticios y no corresponden a contraseñas reales.

USE vecino_seguro;

INSERT INTO roles (name)
VALUES ('admin'), ('vecino')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO users (rut, full_name, email, password_hash, role_id)
VALUES
  ('11111111-1', 'Administradora Vecinal', 'admin@example.com', 'hash_ficticio_admin_no_usar', 1),
  ('22222222-2', 'Vecino de Ejemplo', 'vecino@example.com', 'hash_ficticio_vecino_no_usar', 2)
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name);

INSERT INTO emergencies (user_id, type, description, location, urgency_level, status)
VALUES
  (2, 'Incendio', 'Humo visible cerca de una vivienda. Ejemplo para pruebas.', 'Pasaje Los Alerces 123', 'alta', 'reportada'),
  (2, 'Corte de luz', 'Sector sin suministro eléctrico. Ejemplo para pruebas.', 'Plaza Central', 'media', 'en_revision');

INSERT INTO emergency_status_history (emergency_id, previous_status, new_status, changed_by)
VALUES
  (1, NULL, 'reportada', 2),
  (2, NULL, 'reportada', 2),
  (2, 'reportada', 'en_revision', 1);

