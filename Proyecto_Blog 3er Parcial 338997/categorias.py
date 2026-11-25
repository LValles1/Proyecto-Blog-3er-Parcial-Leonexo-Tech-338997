from Conexion import driver, BASE_DATOS

# Registra una categoria
def registrar_categoria(nombre, url):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MERGE (c:Category {name: $nombre})
        ON CREATE SET c.url = $url
        RETURN c
        """
        resultado = session.run(
            consulta,
            nombre=nombre,
            url=url
        )
        return resultado.single() is not None

# Consulta las categorias registradas
def consultar_categorias():
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Category)
        RETURN c.name AS nombre, c.url AS url
        ORDER BY c.name
        """
        resultado = session.run(consulta)
        categorias = []
        # Guarda los datos de cada categoria en una lista
        for registro in resultado:
            categorias.append({
                "nombre": registro["nombre"],
                "url": registro["url"]
            })
        return categorias

# Modifica los datos de una categoria
def modificar_categoria(nombre, nuevo_nombre, nueva_url):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Category {name: $nombre})
        SET c.name = $nuevo_nombre,
            c.url = $url
        RETURN c
        """
        resultado = session.run(
            consulta,
            nombre=nombre,
            nuevo_nombre=nuevo_nombre,
            url=nueva_url
        )
        return resultado.single() is not None

# Elimina una categoria de la base de datos
def eliminar_categoria(nombre):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Category {name: $nombre})
        DETACH DELETE c
        RETURN count(c) AS eliminadas
        """
        resultado = session.run(consulta, nombre=nombre)
        return resultado.single()["eliminadas"] > 0

# Relaciona una categoria con un articulo
def asignar_categoria(nombre_categoria, titulo_articulo):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Category {name: $nombre})
        MATCH (a:Article {title: $titulo})
        MERGE (a)-[:PERTENECE_A]->(c)
        RETURN a, c
        """
        resultado = session.run(
            consulta,
            nombre=nombre_categoria,
            titulo=titulo_articulo
        )
        return resultado.single() is not None