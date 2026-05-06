# Principios SOLID en VecinoSeguro

## Single Responsibility Principle

Cada clase o módulo debe tener una responsabilidad clara. Por ejemplo, un `AuthService` valida reglas de autenticación, mientras que un repositorio se encarga del acceso a datos.

En la aplicación desktop con PySide6, una `LoginView` debe encargarse de construir la pantalla de inicio de sesión y emitir eventos de usuario. No debería validar credenciales, decidir permisos ni comunicarse directamente con la API.

## Open/Closed Principle

Los módulos deben permitir extensión sin modificar código estable. Por ejemplo, se podrán agregar nuevos tipos de reportes creando servicios específicos sin reescribir las rutas existentes.

## Liskov Substitution Principle

Las implementaciones futuras de repositorios deberán poder sustituirse sin romper los servicios. Por ejemplo, un repositorio MySQL y un repositorio simulado para pruebas deberían respetar el mismo contrato.

## Interface Segregation Principle

Los clientes no deben depender de métodos que no usan. En VecinoSeguro se evitarán servicios enormes y se preferirán interfaces pequeñas para autenticación, usuarios, emergencias y reportes.

## Dependency Inversion Principle

La lógica de negocio debe depender de abstracciones y no de detalles concretos. Los servicios deberían recibir repositorios o clientes externos desde fuera para facilitar pruebas y cambios de infraestructura.

## Ejemplo aplicado a PySide6

Una pantalla de login puede organizarse con responsabilidades separadas:

- `LoginView`: vista PySide6 que muestra campos, botones y mensajes de estado.
- `AuthController`: coordina el evento de ingreso, toma los datos de la vista y solicita autenticación.
- `AuthService`: contiene la lógica de autenticación de la app desktop y decide cómo interpretar la respuesta del backend.
- `ApiClient`: encapsula las llamadas HTTP hacia la API FastAPI.

Las vistas PySide6 no deben contener lógica de negocio compleja. Su responsabilidad principal es presentar información, capturar interacciones y delegar decisiones a controladores y servicios.
