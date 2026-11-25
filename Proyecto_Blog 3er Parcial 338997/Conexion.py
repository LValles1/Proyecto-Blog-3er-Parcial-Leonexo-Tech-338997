import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# El archivo .env (Informacion de los datos de la conexion)
load_dotenv()

# Datos de la conexion
URI = os.getenv("NEO4J_URI")
USUARIO = os.getenv("NEO4J_USERNAME")
CONTRASENA = os.getenv("NEO4J_PASSWORD")
BASE_DATOS = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(
    URI,
    auth=(USUARIO, CONTRASENA)
)

# Comprobar la conexion
def verificar_conexion():
    try:
        driver.verify_connectivity()

        with driver.session(database=BASE_DATOS) as session:
            resultado = session.run("RETURN 'Conexion exitosa' AS mensaje")
            mensaje = resultado.single()["mensaje"]

        print(mensaje)
        print("Base de datos:", BASE_DATOS)

    except Exception as error:
        print("Error al conectar con Neo4j:")
        print(error)

# Cerrar la conexion
def cerrar_conexion():
    driver.close()
