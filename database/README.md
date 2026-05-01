# Base de datos VecinoSeguro

Esta carpeta contiene los scripts iniciales de MySQL para el prototipo.

## Archivos

- `schema.sql`: crea tablas, claves primarias, claves foráneas e índices iniciales.
- `seed.sql`: inserta datos de ejemplo seguros para pruebas locales.

## Ejecución sugerida

```bash
mysql -u root -p < schema.sql
mysql -u root -p vecino_seguro < seed.sql
```

Los datos incluidos son solo ejemplos. Las contraseñas reales deben almacenarse siempre como hash seguro usando un algoritmo apropiado, nunca como texto plano.

