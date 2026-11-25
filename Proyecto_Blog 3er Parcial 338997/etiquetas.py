from Conexion import driver, BASE_DATOS

# Registrar una etiqueta
def registrar_etiqueta(nombre, url):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MERGE (t:Tag {name: $nombre})
        ON CREATE SET t.url = $url
        RETURN t
        """
        resultado = session.run(
            consulta,
            nombre=nombre,
            url=url
        )

        return resultado.single() is not None

# Consultar etiquetas
def consultar_etiquetas():
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (t:Tag)
        RETURN t.name AS nombre, t.url AS url
        ORDER BY t.name
        """
        resultado = session.run(consulta)
        etiquetas = []
        for registro in resultado:
            etiquetas.append({
                "nombre": registro["nombre"],
                "url": registro["url"]
            })

        return etiquetas

# Modificar una etiqueta
def modificar_etiqueta(nombre, nuevo_nombre, nueva_url):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (t:Tag {name: $nombre})
        SET t.name = $nuevo_nombre,
            t.url = $url
        RETURN t
        """
        resultado = session.run(
            consulta,
            nombre=nombre,
            nuevo_nombre=nuevo_nombre,
            url=nueva_url
        )
        return resultado.single() is not None

# Eliminar una etiqueta
def eliminar_etiqueta(nombre):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (t:Tag {name: $nombre})
        DETACH DELETE t
        RETURN count(t) AS eliminadas
        """
        resultado = session.run(
            consulta,
            nombre=nombre
        )
        return resultado.single()["eliminadas"] > 0

# Relacion etiqueta - articulo
def asignar_etiqueta(nombre_etiqueta, titulo_articulo):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (t:Tag {name: $nombre})
        MATCH (a:Article {title: $titulo})
        MERGE (a)-[:TIENE_ETIQUETA]->(t)
        RETURN a, t
        """
        resultado = session.run(
            consulta,
            nombre=nombre_etiqueta,
            titulo=titulo_articulo
        )
        return resultado.single() is not None