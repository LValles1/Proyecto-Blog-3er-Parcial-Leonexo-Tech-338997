from Conexion import driver, BASE_DATOS

# Registra un articulo
def registrar_articulo(titulo, fecha, texto, correo_usuario):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User {email: $correo})
        CREATE (a:Article {
            title: $titulo,
            date: $fecha,
            text: $texto
        })
        CREATE (u)-[:PUBLICA]->(a)
        RETURN a
        """

        resultado = session.run(
            consulta,
            titulo=titulo,
            fecha=fecha,
            texto=texto,
            correo=correo_usuario
        )

        return resultado.single() is not None


# Consulta todos los articulos
def consultar_articulos():
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User)-[:PUBLICA]->(a:Article)
        RETURN a.title AS titulo, a.date AS fecha, a.text AS texto, u.name AS autor
        ORDER BY a.title
        """

        resultado = session.run(consulta)

        articulos = []

        for registro in resultado:
            articulos.append({
                "titulo": registro["titulo"],
                "fecha": registro["fecha"],
                "texto": registro["texto"],
                "autor": registro["autor"]
            })

        return articulos


# Modifica un articulo
def modificar_articulo(titulo, nueva_fecha, nuevo_texto):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (a:Article {title: $titulo})
        SET a.date = $fecha,
            a.text = $texto
        RETURN a
        """

        resultado = session.run(
            consulta,
            titulo=titulo,
            fecha=nueva_fecha,
            texto=nuevo_texto
        )

        return resultado.single() is not None


# Elimina un articulo
def eliminar_articulo(titulo):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (a:Article {title: $titulo})
        DETACH DELETE a
        RETURN count(a) AS eliminados
        """

        resultado = session.run(
            consulta,
            titulo=titulo
        )

        return resultado.single()["eliminados"] > 0
