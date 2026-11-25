from Conexion import driver, BASE_DATOS

# Registrar un usuario
def registrar_usuario(nombre, apellido, correo):
    nombre_completo = nombre.strip() + " " + apellido.strip()

    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        CREATE (u:User {
            name: $nombre_completo,
            email: $correo
        })
        RETURN u
        """

        resultado = session.run(
            consulta,
            nombre_completo=nombre_completo,
            correo=correo
        )

        return resultado.single() is not None

# Consultar todos los usuarios
def consultar_usuarios():
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User)
        RETURN u.name AS nombre, u.email AS correo
        ORDER BY u.name
        """
        resultado = session.run(consulta)
        usuarios = []

        for registro in resultado:
            usuarios.append({
                "nombre": registro["nombre"],
                "correo": registro["correo"]
            })

        return usuarios

# Modificar un usuario
def modificar_usuario(correo, nuevo_nombre, nuevo_apellido, nuevo_correo):
    nombre_completo = nuevo_nombre.strip() + " " + nuevo_apellido.strip()

    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User {email: $correo})
        SET u.name = $nombre_completo,
            u.email = $nuevo_correo
        RETURN u
        """
        resultado = session.run(
            consulta,
            correo=correo,
            nombre_completo=nombre_completo,
            nuevo_correo=nuevo_correo
        )

        return resultado.single() is not None

# Eliminar un usuario
def eliminar_usuario(correo):
    with driver.session(database=BASE_DATOS) as session:
        consulta = """
        MATCH (u:User {email: $correo})
        DETACH DELETE u
        RETURN count(u) AS eliminados
        """
        resultado = session.run(consulta, correo=correo)
        return resultado.single()["eliminados"] > 0