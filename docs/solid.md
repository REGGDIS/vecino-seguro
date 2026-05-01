# Principios SOLID en VecinoSeguro

## Single Responsibility Principle

Cada clase o módulo debe tener una responsabilidad clara. Por ejemplo, un `AuthService` valida reglas de autenticación, mientras que un repositorio se encarga del acceso a datos.

## Open/Closed Principle

Los módulos deben permitir extensión sin modificar código estable. Por ejemplo, se podrán agregar nuevos tipos de reportes creando servicios específicos sin reescribir las rutas existentes.

## Liskov Substitution Principle

Las implementaciones futuras de repositorios deberán poder sustituirse sin romper los servicios. Por ejemplo, un repositorio MySQL y un repositorio simulado para pruebas deberían respetar el mismo contrato.

## Interface Segregation Principle

Los clientes no deben depender de métodos que no usan. En VecinoSeguro se evitarán servicios enormes y se preferirán interfaces pequeñas para autenticación, usuarios, emergencias y reportes.

## Dependency Inversion Principle

La lógica de negocio debe depender de abstracciones y no de detalles concretos. Los servicios deberían recibir repositorios o clientes externos desde fuera para facilitar pruebas y cambios de infraestructura.

