// Base de datos de Leonexo Tech
// Ejecutar en la base de datos "blog".

MATCH (n)
DETACH DELETE n;

// Restricciones para evitar registros duplicados
CREATE CONSTRAINT usuario_email_unico IF NOT EXISTS
FOR (u:User)
REQUIRE u.email IS UNIQUE;

CREATE CONSTRAINT articulo_titulo_unico IF NOT EXISTS
FOR (a:Article)
REQUIRE a.title IS UNIQUE;

CREATE CONSTRAINT categoria_nombre_unico IF NOT EXISTS
FOR (c:Category)
REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT etiqueta_nombre_unico IF NOT EXISTS
FOR (t:Tag)
REQUIRE t.name IS UNIQUE;

// Crear los usuarios
CREATE
    (:User {name: "Ana Trevizo Guerra", email: "a523675@auch.mx"}),
    (:User {name: "Carlos Velazquez de Leon", email: "a455782@uach.mx"}),
    (:User {name: "Leonel Valles Chavez", email: "a338997@uach.mx"}),
    (:User {name: "Pedro Lopez Arreaga", email: "a365890@uach.mx"});

// Crear los articulos
CREATE
    (:Article {
        title: "Introduccion a las bases de datos orientadas a grafos",
        date: "2026-11-20",
        text: "Las bases de datos orientadas a grafos permiten representar informacion mediante nodos y relaciones. A diferencia de las bases de datos tradicionales, facilitan la conexion entre diferentes elementos. Neo4j es una herramienta que permite almacenar, consultar y administrar este tipo de informacion."
    }),
    (:Article {
        title: "Python y su importancia en el desarrollo de software",
        date: "2026-11-21",
        text: "Python es un lenguaje de programacion utilizado en diferentes areas del desarrollo de software. Su sintaxis sencilla permite crear aplicaciones, automatizar tareas y trabajar con bases de datos. Ademas, cuenta con una gran variedad de bibliotecas que facilitan el desarrollo de proyectos tecnologicos."
    }),
    (:Article {
        title: "La importancia de la innovacion tecnologica",
        date: "2026-11-23",
        text: "La innovacion tecnologica permite desarrollar nuevas herramientas y soluciones para facilitar las actividades cotidianas. Actualmente, tecnologias como la inteligencia artificial, las aplicaciones web y las bases de datos contribuyen al crecimiento de diferentes sectores."
    });

// Crear las categorias
CREATE
    (:Category {name: "Bases de datos", url: "https://blog.com/categoria/bases-datos"}),
    (:Category {name: "Desarrollo de software", url: "https://blog.com/category/desarrollo-software"}),
    (:Category {name: "Inteligencia artificial", url: "https://blog.com/category/inteligencia-artificial"}),
    (:Category {name: "Ciberseguridad", url: "https://blog.com/category/ciberseguridad"}),
    (:Category {name: "Innovacion tecnologica", url: "https://blog.com/category/innovacion-tecnologica"});

// Crear los comentarios
CREATE
    (:Comment {
        name: "Es interesante conocer como funcionan las bases de datos orientadas a grafos y sus aplicaciones.",
        url: "https://blog.com/comentario1"
    }),
    (:Comment {
        name: "La innovacion tecnologica es fundamental para desarrollar nuevas soluciones y mejorar nuestro entorno.",
        url: "https://blog.com/comentario2"
    });

// Crear las etiquetas
CREATE
    (:Tag {name: "Bases de datos", url: "https://blog.com/tag/bases-datos"}),
    (:Tag {name: "Neo4j", url: "https://blog.com/tag/neo4j"}),
    (:Tag {name: "Innovacion tecnologica", url: "https://blog.com/tag/innovacion-tecnologica"}),
    (:Tag {name: "Tecnologia e innovacion", url: "https://blog.com/tag/tecnologia-innovacion"}),
    (:Tag {name: "Desarrollo de software", url: "https://blog.com/tag/desarrollo-software"}),
    (:Tag {name: "Python", url: "https://blog.com/tag/python"});

// Crear las relaciones entre usuarios y articulos, comentarios y categorias
MATCH
    (carlos:User {email: "a455782@uach.mx"}),
    (leonel:User {email: "a338997@uach.mx"}),
    (articulo_grafos:Article {title: "Introduccion a las bases de datos orientadas a grafos"}),
    (articulo_python:Article {title: "Python y su importancia en el desarrollo de software"}),
    (articulo_innovacion:Article {title: "La importancia de la innovacion tecnologica"}),
    (comentario_grafos:Comment {url: "https://blog.com/comentario1"}),
    (comentario_innovacion:Comment {url: "https://blog.com/comentario2"}),
    (categoria_bd:Category {name: "Bases de datos"}),
    (categoria_desarrollo:Category {name: "Desarrollo de software"}),
    (categoria_innovacion:Category {name: "Innovacion tecnologica"})
CREATE
    (carlos)-[:ESCRIBE]->(comentario_grafos),
    (carlos)-[:ESCRIBE]->(comentario_innovacion),
    (articulo_grafos)-[:PERTENECE_A]->(categoria_bd),
    (articulo_python)-[:PERTENECE_A]->(categoria_desarrollo),
    (articulo_innovacion)-[:PERTENECE_A]->(categoria_innovacion),
    (leonel)-[:PUBLICA]->(articulo_grafos),
    (leonel)-[:PUBLICA]->(articulo_innovacion),
    (carlos)-[:PUBLICA]->(articulo_python),
    (articulo_grafos)-[:TIENE_COMENTARIO]->(comentario_grafos),
    (articulo_innovacion)-[:TIENE_COMENTARIO]->(comentario_innovacion);

// Crear las relaciones entre articulos y etiquetas
MATCH
    (articulo_grafos:Article {title: "Introduccion a las bases de datos orientadas a grafos"}),
    (articulo_python:Article {title: "Python y su importancia en el desarrollo de software"}),
    (articulo_innovacion:Article {title: "La importancia de la innovacion tecnologica"}),
    (tag_bd:Tag {name: "Bases de datos"}),
    (tag_neo4j:Tag {name: "Neo4j"}),
    (tag_innovacion:Tag {name: "Innovacion tecnologica"}),
    (tag_tecnologia:Tag {name: "Tecnologia e innovacion"}),
    (tag_desarrollo:Tag {name: "Desarrollo de software"}),
    (tag_python:Tag {name: "Python"})
CREATE
    (articulo_grafos)-[:TIENE_ETIQUETA]->(tag_bd),
    (articulo_grafos)-[:TIENE_ETIQUETA]->(tag_neo4j),
    (articulo_innovacion)-[:TIENE_ETIQUETA]->(tag_innovacion),
    (articulo_innovacion)-[:TIENE_ETIQUETA]->(tag_tecnologia),
    (articulo_python)-[:TIENE_ETIQUETA]->(tag_desarrollo),
    (articulo_python)-[:TIENE_ETIQUETA]->(tag_python);

// Verificar la cantidad de nodos por tipo
MATCH (n)
RETURN labels(n) AS Tipo, count(n) AS Cantidad
ORDER BY Tipo;

// Verificar la cantidad de relaciones por tipo
MATCH ()-[r]->()
RETURN type(r) AS Relacion, count(r) AS Cantidad
ORDER BY Relacion;
