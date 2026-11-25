from Conexion import driver, BASE_DATOS

# Registra un comentario
def registrar_comentario(nombre, url, correo_usuario, titulo_articulo):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User {email: $correo})
        MATCH (a:Article {title: $titulo})

        CREATE (c:Comment {
            name: $nombre,
            url: $url
        })

        CREATE (u)-[:ESCRIBE]->(c)
        CREATE (a)-[:TIENE_COMENTARIO]->(c)

        RETURN c
        """
        resultado = session.run(
            consulta,
            nombre=nombre,
            url=url,
            correo=correo_usuario,
            titulo=titulo_articulo
        )

        return resultado.single() is not None

# Consulta comentarios
def consultar_comentarios():
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User)-[:ESCRIBE]->(c:Comment)
              <-[:TIENE_COMENTARIO]-(a:Article)

        RETURN c.name AS comentario,
               c.url AS url,
               u.name AS usuario,
               a.title AS articulo
        ORDER BY a.title
        """
        resultado = session.run(consulta)
        comentarios = []
        for registro in resultado:
            comentarios.append({
                "comentario": registro["comentario"],
                "url": registro["url"],
                "usuario": registro["usuario"],
                "articulo": registro["articulo"]
            })

        return comentarios


# Modifica un comentario
def modificar_comentario(nombre, nuevo_nombre, nueva_url):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Comment {name: $nombre})
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

# Elimina un comentario
def eliminar_comentario(nombre):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (c:Comment {name: $nombre})
        DETACH DELETE c
        RETURN count(c) AS eliminados
        """
        resultado = session.run(
            consulta,
            nombre=nombre
        )
        return resultado.single()["eliminados"] > 0