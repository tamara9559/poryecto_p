Descripción del Proyecto:

Este proyecto consiste en el desarrollo de un Sistema de Gestión de Inventario utilizando tecnologías modernas de backend, una arquitectura modular y un conjunto completo de pruebas automatizadas. 
Su propósito es permitir la administración de categorías y productos, aplicando buenas prácticas de desarrollo, testing y despliegue.
El sistema está construido con FastAPI y utiliza SQLAlchemy como ORM para interactuar con la base de datos. En un entorno real, se conecta a una instancia de Amazon RDS (MySQL), 
mientras que para pruebas automatizadas se emplea SQLite, lo que permite un entorno seguro, reproducible y aislado.
El proyecto está dividido en backend, frontend y pruebas organizadas por niveles (unitarias, integración y E2E), siguiendo principios de arquitectura limpia y mantenible. Adicionalmente, 
se configura un pipeline de GitHub Actions que instala dependencias, ejecuta las pruebas y realiza análisis estático de seguridad con Bandit.

Arquitectura del Proyecto 

El proyecto usa una arquitectura en capas, donde cada parte tiene una responsabilidad clara:

1. API (FastAPI)
Recibe solicitudes HTTP, valida datos y envía respuestas.
No contiene lógica de negocio.

2. Lógica de Negocio (Servicios)
Implementa reglas y procesos del sistema.
Coordina operaciones y gestiona errores.
No depende de HTTP ni de la BD directamente.

3. Acceso a Datos (ORM con SQLAlchemy)
Traduce clases Python a tablas en Amazon RDS.
Ejecuta consultas, maneja transacciones y devuelve objetos a los servicios.

4. Validación (Pydantic)
Valida entradas y salidas.
Garantiza que los datos sean correctos y seguros.

5. Pruebas (unitarias, integración, E2E)
Unitarias: prueban la lógica interna aislada.
Integración: prueba API + servicios + BD juntos.
E2E: prueba flujos completos como un usuario real.

6. Pipeline CI
Automatiza instalación, pruebas y análisis estático (Bandit).
Solo imprime "OK" si todo pasa.




Descripción de la Base de Datos 

El proyecto utiliza una base de datos MySQL alojada en Amazon RDS, a la cual el backend se conecta mediante SQLAlchemy 2.0 usando el driver pymysql. 
La estructura del modelo de datos es simple y está compuesta por dos tablas principales: Category y Product. La tabla Category almacena un identificador y un nombre, 
mientras que Product contiene un id, nombre, precio y una clave foránea (category_id) que referencia a Category. Esto establece una relación uno-a-muchos, donde una categoría puede tener múltiples productos.
Las relaciones están modeladas en SQLAlchemy usando relationship y back_populates, permitiendo que el ORM gestione automáticamente la consulta y navegación entre las entidades.
Antes de que los datos lleguen a la base de datos, son validados mediante Pydantic en los schemas del proyecto, lo que asegura que entradas y salidas cumplan los tipos y restricciones necesarias. 
La lógica que interactúa con la base de datos se encuentra en los services, que ejecutan operaciones como crear, actualizar, listar y eliminar registros, siempre manejando transacciones mediante SQLAlchemy.

Para las pruebas, no se utiliza la base de datos RDS real.
Cada tipo de prueba funciona con una base aislada:

Pruebas unitarias:
Usan una base de datos en memoria SQLite, creada y destruida durante la ejecución.
No interactúan con MySQL, sino con datos mockeados.

Pruebas de integración:
Usan una base SQLite temporal, pero ya conectada al API de FastAPI, lo que simula el comportamiento real del backend incluyendo capas como controladores, servicios y ORM.

Pruebas E2E:
También usan una base SQLite temporal, pero verifican el flujo completo: el cliente (httpx) → API → servicios → ORM → base temporal.
Esto emula el funcionamiento real sin tocar la base de datos productiva en RDS.



Instrucciones de cómo ejecutar el API(de manera local)

1 Clonar repositorio

2 Instala las dependencias con: pip install -r requirements.txt

3 Crea el archivo .env y agrega las variables que te proporcionará el dueño del proyecto.

4 Ejecuta el servidor con: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5 Abre en el navegador http://localhost:8000 para el frontend.

6 Usa http://localhost:8000/docs para ver los endpoints interactivos.

http://localhost:8000/docs con esta URL podrás entrar a la documentación interactiva
Algunos ejemplos de APIS a las que se puede acceder con el metodo http GET
http://localhost:8000/categories/
http://localhost:8000/products/



Instrucciones para ejecutar la interfaz grafica(proyecto en la nube o local)

(nube)

1 Consultar con el dueño del proyecto para que levante el servicio en la nube

2 Entra al siguiente enlace https://poryectop-production.up.railway.app

3 Esto cargará la interfaz gráfica, donde se podrán probar todas las funcionalidades.

O

(local)

1 Ejecuta el servicio backend

2 Entra en el directorio donde se encuentra el archivo index.html desde el explorador de archivos.

3 Ábrelo con el navegador de tu preferencia

4 Esto cargará la interfaz gráfica automáticamente.

Explicacion para ejecutar las pruebas

Las pruebas garantizan que la API funcione correctamente y que cada parte del sistema responda como se espera. Permiten detectar errores antes de subir cambios a producción y asegurar que las 
funcionalidades principales, la lógica de negocio y la comunicación con la base de datos se comporten de forma consistente y estable.
Las pruebas unitarias verifican funciones pequeñas de manera aislada; las pruebas de integración comprueban que módulos como FastAPI, SQLAlchemy y la BD trabajen juntos correctamente; 
y las pruebas E2E evalúan el flujo completo del sistema tal como lo usaría un cliente real. Cada tipo de prueba cubre un nivel diferente del sistema, dando confianza en que tanto las piezas 
individuales como el conjunto completo funcionan sin fallos.

Para ejecutar estas pruebas se usa el comando por terminal "pytest -vv" ya que muestra cada prueba, su nombre completo, el resultado y detalles adicionales
en caso de querer ejecutar un tipo de prueba en especifico se usa para las pruebas unitarias "pytest tests/unit -vv", para las pruebas de integracion "pytest tests/integration -vv",
para las pruebas e2e "pytest tests/e2e -vv" y en caso de querer ejecutar un tipo de prueba en específico se usa "pytest tests/integration/test_categories_integration.py -vv"

Descripcion del pipeline

Este pipeline en GitHub Actions automatiza todo el proceso de validación del proyecto cada vez que se hace un push o pull request a la rama main. 
Primero clona el código y configura Python 3.11; luego instala las dependencias del backend. Después ejecuta de forma separada las pruebas unitarias, pruebas de integración y pruebas E2E, 
usando las credenciales de la base de datos almacenadas como secrets. También realiza un análisis de seguridad con Bandit para detectar vulnerabilidades en el código. 
Si todas las etapas completan correctamente, el pipeline imprime "OK"


Pasos para instalar las dependencias

Para instalar las dependencias del proyecto,  

1 asegúrate de tener Python 3.11 instalado que se puede descargar a través de su pagina web 

2 abre una terminal en la carpeta raíz del proyecto 

3 crea un entorno virtual con el comando python -m venv venv (para windows) source venv/bin/activate (linux\mac)

4 para activar el entorno virtual venv\Scripts\activate (para windows) source venv/bin/activate (linux\mac)

5 ejecuta pip install --upgrade pip para actualizar el gestor de paquetes  

6 instala todas las librerías necesarias con pip install -r requirements.txt

descargará automáticamente todas las dependencias listadas para que la API pueda ejecutarse correctamente.


Decisiones tecnicas tomadas

Framework Backend: FastAPI
Se eligió FastAPI por su alto rendimiento, tipado fuerte, soporte nativo para documentación automática (OpenAPI) y fácil integración con Pydantic.

Validación de datos con Pydantic
Pydantic se usa para validar las entradas y salidas de la API a través de Schemas. Garantiza datos limpios y estructuras estrictas.

ORM elegido: SQLAlchemy
SQLAlchemy se utiliza para manejar la capa de persistencia, permitiendo un mapeo claro entre modelos Python y tablas SQL.

Base de datos: MySQL alojado en Amazon RDS
Se optó por un motor MySQL gestionado para mayor estabilidad, disponibilidad y configuración profesional.

Separación por capas
Controllers → gestionan rutas.
Services → lógica de negocio.
Models → estructura de la BD.
Schemas → validación y serialización.
Esta separación mejora mantenibilidad y escalabilidad.

Pruebas automatizadas con Pytest
Se implementaron pruebas unitarias, integración y E2E, cada una con su propio directorio.
Además, se configuraron fixtures reutilizables con conftest.py.

Pipeline CI en GitHub Actions
Incluye:

instalación de dependencias
ejecución de pruebas unitarias
ejecución de pruebas de integración
pruebas E2E
análisis estático con Bandit
verificación final con “OK”

Seguridad y analisis estatico de codigo con Bandit
Se integró Bandit para detectar vulnerabilidades en el código Python.

CORS habilitado para acceso desde cualquier origen
Se agregó middleware CORS en FastAPI para permitir el acceso del frontend a la API.

Despliegue en Railway
Se eligió Railway por su integración sencilla con FastAPI y su sistema de dominios automáticos para acceso al servicio.


guía para ejecutar el proyecto con o sin Docker

No se utilizó Docker en este proyecto.
Para ejecutar el proyecto consulta la sección "Instrucciones de cómo ejecutar el API (de manera local)" o "Instrucciones para ejecutar la interfaz grafica(proyecto en la nube o local)"
