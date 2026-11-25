# Leonexo Tech
Leonexo Tech es una aplicación de escritorio desarrollada en Python que permite administrar un blog tecnológico mediante una base de datos orientada a grafos utilizando Neo4j.
El sistema permite gestionar usuarios, artículos, comentarios, etiquetas y categorías, así como establecer relaciones entre los diferentes elementos del blog.

## Tecnologías utilizadas
- Python
- Tkinter
- Neo4j
- Cypher
- Neo4j Python Driver
- python-dotenv

## Estructura del proyecto
- `app.py`: ventana principal e interfaz de la aplicación.
- `Conexion.py`: conexión con la base de datos Neo4j.
- `usuarios.py`: administración de usuarios.
- `articulos.py`: administración de artículos.
- `comentarios.py`: administración de comentarios.
- `etiquetas.py`: administración de etiquetas.
- `categorias.py`: administración de categorías.
- `Leonexo_Tech.cypher`: creación de nodos, relaciones y restricciones de la base de datos.
- `requirements.txt`: bibliotecas necesarias para ejecutar la aplicación.
- `.env.ejemplo`: ejemplo de configuración de la conexión.
- `Proyecto final Blog 338997.pdf`: reporte del proyecto.

## Requisitos
- Python instalado.
- Neo4j instalado y en ejecución.
- Una base de datos llamada `blog`.

## Instalación y configuración
1. Descargar o clonar este repositorio.
2. Instalar las dependencias:
   `pip install -r requirements.txt`
3. Crear un archivo `.env` a partir de `.env.ejemplo`.
4. Configurar los datos de conexión a Neo4j en el archivo `.env`.
5. Preparar la base de datos `blog` y ejecutar los archivos Cypher correspondientes.

##IMPORTANTE: revisar el contenido del script Cypher antes de ejecutarlo, ya que incluye una instrucción que elimina los nodos y relaciones existentes en la base de datos seleccionada.

## Ejecución
Una vez configurada la conexión con Neo4j, ejecutar:
`python app.py`

Leonel Valles Chavez 338997 | Proyecto Final Blog | Bases de datos avanzadas
