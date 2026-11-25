import tkinter as tk
from tkinter import ttk, messagebox

# Importacion de las funciones para trabajar con la base de datos.
from Conexion import cerrar_conexion

from usuarios import (
    registrar_usuario,
    consultar_usuarios,
    modificar_usuario,
    eliminar_usuario
)

from articulos import (
    registrar_articulo,
    consultar_articulos,
    modificar_articulo,
    eliminar_articulo
)

from comentarios import (
    registrar_comentario,
    consultar_comentarios,
    modificar_comentario,
    eliminar_comentario
)

from etiquetas import (
    registrar_etiqueta,
    consultar_etiquetas,
    modificar_etiqueta,
    eliminar_etiqueta,
    asignar_etiqueta
)

from categorias import (
    registrar_categoria,
    consultar_categorias,
    modificar_categoria,
    eliminar_categoria,
    asignar_categoria
)


# Configuracion de la app
COLOR_OSCURO = "#263238"
COLOR_SELECCION = "#CFD8DC"
ANCHO_SCROLL = 17

# Configuracion de la ventana principal
ventana = tk.Tk()
ventana.title("Leonexo Tech | Administracion del Blog")
ventana.geometry("1200x750")
ventana.minsize(1100, 700)
ventana.resizable(False, False)

# Encabezado con el nombre del blog y los datos del administrador
encabezado = tk.Frame(ventana, bg=COLOR_OSCURO, height=90)
encabezado.pack(fill="x")

titulo = tk.Label(
    encabezado,
    text="LEONEXO TECH",
    font=("Arial", 18, "bold"),
    fg="white",
    bg=COLOR_OSCURO
)
titulo.pack(pady=(15, 0))

subtitulo = tk.Label(
    encabezado,
    text="ADMINISTRADOR: Leonel Valles Chavez 338997",
    font=("Arial", 10),
    fg="#CFD8DC",
    bg=COLOR_OSCURO
)
subtitulo.pack(pady=(5, 15))

# Contenedor que divide la interfaz en menu lateral y contenido
contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True, padx=20, pady=20)

menu = tk.Frame(contenedor, width=180, bg="#eceff1")
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

contenido = tk.Frame(contenedor, bg="white")
contenido.pack(side="right", fill="both", expand=True, padx=15)

# Clase de las tablas con scroll para poder ver todo el contenido
class TablaScroll:
    def __init__(self, padre, columnas, al_seleccionar=None):
        self.columnas = columnas
        self.al_seleccionar = al_seleccionar
        self.seleccionado = None
        self.filas_widgets = []

        marco = tk.Frame(padre, bg="white")
        marco.pack(fill="both", expand=True, padx=20, pady=5)

        # Encabezado de las columnas
        barra_enc = tk.Frame(marco, bg=COLOR_OSCURO)
        barra_enc.pack(fill="x")

        tk.Frame(barra_enc, width=ANCHO_SCROLL, bg=COLOR_OSCURO).pack(side="right", fill="y")

        enc_cols = tk.Frame(barra_enc, bg=COLOR_OSCURO)
        enc_cols.pack(side="left", fill="x", expand=True)

        for i, (nombre, ancho, _) in enumerate(columnas):
            enc_cols.grid_columnconfigure(i, minsize=ancho, weight=ancho)
            tk.Label(
                enc_cols,
                text=nombre,
                bg=COLOR_OSCURO,
                fg="white",
                font=("Arial", 10, "bold"),
                anchor="w",
                padx=5,
                pady=7
            ).grid(row=0, column=i, sticky="nsew")
        cuerpo = tk.Frame(marco, bg="white")
        cuerpo.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(cuerpo, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(cuerpo, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.filas = tk.Frame(self.canvas, bg="white")
        self.ventana_filas = self.canvas.create_window((0, 0), window=self.filas, anchor="nw")

        self.filas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.ventana_filas, width=e.width)
        )
        self.canvas.bind("<Enter>", self._activar_rueda)
        self.canvas.bind("<Leave>", self._desactivar_rueda)
        self.filas.bind("<Enter>", self._activar_rueda)
        self.canvas.bind("<Destroy>", self._desactivar_rueda)

    def _activar_rueda(self, evento=None):
        self.canvas.bind_all("<MouseWheel>", self._rueda)
        self.canvas.bind_all("<Button-4>", self._rueda)
        self.canvas.bind_all("<Button-5>", self._rueda)

    def _desactivar_rueda(self, evento=None):
        try:
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        except tk.TclError:
            pass

    def _rueda(self, evento):
        try:
            if self.canvas.yview() == (0.0, 1.0):
                return

            if getattr(evento, "num", None) == 4:
                paso = -1
            elif getattr(evento, "num", None) == 5:
                paso = 1
            else:
                paso = -1 if evento.delta > 0 else 1

            self.canvas.yview_scroll(paso, "units")
        except tk.TclError:
            pass

    # Cambia el color de las filas para identificar la seleccion
    def _pintar(self, fila, color):
        fila.configure(bg=color)
        for hijo in fila.winfo_children():
            hijo.configure(bg=color)

    # Guarda el registro seleccionado y llena el formulario correspondiente
    def _seleccionar(self, registro, fila):
        self.seleccionado = registro

        for otra in self.filas_widgets:
            self._pintar(otra, "white")

        self._pintar(fila, COLOR_SELECCION)

        if self.al_seleccionar:
            self.al_seleccionar(registro)

    # Actualiza las filas de la tabla con los registros recibidos
    def cargar(self, registros):
        for widget in self.filas.winfo_children():
            widget.destroy()

        self.filas_widgets = []
        self.seleccionado = None

        for registro in registros:
            fila = tk.Frame(
                self.filas,
                bg="white",
                highlightbackground="#B0BEC5",
                highlightthickness=1
            )
            fila.pack(fill="x", pady=1)
            self.filas_widgets.append(fila)

            for i, (_, ancho, clave) in enumerate(self.columnas):
                fila.grid_columnconfigure(i, minsize=ancho, weight=ancho)

                etiqueta = tk.Label(
                    fila,
                    text=str(registro.get(clave, "")),
                    bg="white",
                    font=("Arial", 9),
                    wraplength=ancho - 14,
                    justify="left",
                    anchor="nw",
                    padx=5,
                    pady=8
                )
                etiqueta.grid(row=0, column=i, sticky="nsew")
                etiqueta.bind(
                    "<Button-1>",
                    lambda e, r=registro, f=fila: self._seleccionar(r, f)
                )

            fila.bind(
                "<Button-1>",
                lambda e, r=registro, f=fila: self._seleccionar(r, f)
            )

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(0)

# Funciones auxiliares
# Muestra el titulo de cada apartado
def titulo_de_seccion(texto):
    tk.Label(
        contenido,
        text=texto,
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=(5, 5))


# Genera los formularios a partir de una lista de campos
def crear_formulario(campos, ancho=45):
    formulario = tk.Frame(contenido, bg="white")
    formulario.pack(pady=5)

    entradas = []
    for fila, texto in enumerate(campos):
        tk.Label(formulario, text=texto, bg="white").grid(
            row=fila, column=0, padx=5, pady=3, sticky="e"
        )
        entrada = tk.Entry(formulario, width=ancho)
        entrada.grid(row=fila, column=1, padx=5, pady=3)
        entradas.append(entrada)

    return entradas

# Crea los botones para las operaciones de registro, modificacion, eliminacion y actualizacion de los apartados
def crear_botones(registrar, modificar, eliminar, actualizar):
    botones = tk.Frame(contenido, bg="white")
    botones.pack(pady=5)

    tk.Button(botones, text="Registrar", width=12, command=registrar).grid(row=0, column=0, padx=5)
    tk.Button(botones, text="Modificar", width=12, command=modificar).grid(row=0, column=1, padx=5)
    tk.Button(botones, text="Eliminar", width=12, command=eliminar).grid(row=0, column=2, padx=5)

    tk.Button(
        botones,
        text="↻",
        command=actualizar,
        font=("Arial", 12),
        width=3,
        relief="flat",
        bg="white",
        fg=COLOR_OSCURO,
        cursor="hand2"
    ).grid(row=0, column=3, padx=(20, 5))

def llenar(entrada, valor):
    entrada.delete(0, tk.END)
    entrada.insert(0, str(valor))

def vaciar(*entradas):
    for entrada in entradas:
        entrada.delete(0, tk.END)

# Muestra la seccion elegida desde el menu lateral
def mostrar_seccion(nombre):

    # Limpia el contenido anterior antes de mostrar otro apartado
    for elemento in contenido.winfo_children():
        elemento.destroy()

    if nombre == "Bienvenido":
        mostrar_bienvenida()

    elif nombre == "Usuarios":
        mostrar_usuarios()

    elif nombre == "Articulos":
        mostrar_articulos()

    elif nombre == "Comentarios":
        mostrar_comentarios()

    elif nombre == "Etiquetas":
        mostrar_etiquetas()

    elif nombre == "Categorias":
        mostrar_categorias()

# Crud de usuarios
# Interfaz para registrar, consultar, modificar y eliminar usuarios
def mostrar_usuarios():

    titulo_de_seccion("Administracion de usuarios")

    entrada_nombre, entrada_apellido, entrada_correo = crear_formulario(
        ["Nombre:", "Apellido:", "Correo:"]
    )

    # Coloca en el formulario los datos del usuario seleccionado
    def al_seleccionar(registro):
        nombre_completo = registro["nombre"].split(" ", 1)

        llenar(entrada_nombre, nombre_completo[0])

        if len(nombre_completo) > 1:
            llenar(entrada_apellido, nombre_completo[1])
        else:
            llenar(entrada_apellido, "")

        llenar(entrada_correo, registro["correo"])

    # Consulta los usuarios y actualiza la tabla
    def actualizar_tabla():
        tabla.cargar(consultar_usuarios())

    # Valida los campos y registra un usuario en Neo4j
    def registrar():
        nombre_usuario = entrada_nombre.get().strip()
        apellido_usuario = entrada_apellido.get().strip()
        correo_usuario = entrada_correo.get().strip()

        if nombre_usuario == "" or apellido_usuario == "" or correo_usuario == "":
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        try:
            if registrar_usuario(nombre_usuario, apellido_usuario, correo_usuario):
                messagebox.showinfo("Correcto", "Usuario registrado.")
                vaciar(entrada_nombre, entrada_apellido, entrada_correo)
                actualizar_tabla()
            else:
                messagebox.showwarning("Aviso", "No se pudo registrar el usuario.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Modifica los datos del usuario seleccionado
    def modificar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario.")
            return

        correo_anterior = tabla.seleccionado["correo"]
        nuevo_nombre = entrada_nombre.get().strip()
        nuevo_apellido = entrada_apellido.get().strip()
        nuevo_correo = entrada_correo.get().strip()

        if nuevo_nombre == "" or nuevo_apellido == "" or nuevo_correo == "":
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        try:
            if modificar_usuario(
                correo_anterior,
                nuevo_nombre,
                nuevo_apellido,
                nuevo_correo
            ):
                messagebox.showinfo("Correcto", "Usuario modificado.")
                actualizar_tabla()
            else:
                messagebox.showwarning("Aviso", "No se encontro el usuario.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina el usuario seleccionado despues de confirmar la operacion
    def eliminar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario.")
            return

        correo_usuario = tabla.seleccionado["correo"]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este usuario?"):
            try:
                if eliminar_usuario(correo_usuario):
                    messagebox.showinfo("Correcto", "Usuario eliminado.")
                    vaciar(entrada_nombre, entrada_apellido, entrada_correo)
                    actualizar_tabla()
                else:
                    messagebox.showwarning("Aviso", "No se encontro el usuario.")

            except Exception as error:
                messagebox.showerror("Error", str(error))

    crear_botones(registrar, modificar, eliminar, actualizar_tabla)

    tabla = TablaScroll(
        contenido,
        [("Nombre completo", 330, "nombre"), ("Correo", 560, "correo")],
        al_seleccionar
    )

    actualizar_tabla()

# Crud de articulos
# Interfaz para administrar los articulos publicados en el blog.
def mostrar_articulos():

    titulo_de_seccion("Administracion de articulos")

    (entrada_titulo, entrada_fecha,
     entrada_texto, entrada_correo) = crear_formulario(
        ["Titulo:", "Fecha:", "Texto:", "Nombre del autor:"]
    )

    def al_seleccionar(registro):
        llenar(entrada_titulo, registro["titulo"])
        llenar(entrada_fecha, registro["fecha"])
        llenar(entrada_texto, registro["texto"])
        llenar(entrada_correo, registro["autor"])

    def actualizar_tabla():
        tabla.cargar(consultar_articulos())

    # Registra un articulo y lo relaciona con el usuario indicado
    def registrar():
        titulo = entrada_titulo.get().strip()
        fecha = entrada_fecha.get().strip()
        texto = entrada_texto.get().strip()
        correo = entrada_correo.get().strip()

        if not titulo or not fecha or not texto or not correo:
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        try:
            if registrar_articulo(titulo, fecha, texto, correo):
                messagebox.showinfo("Correcto", "Articulo registrado.")
                vaciar(entrada_titulo, entrada_fecha, entrada_texto, entrada_correo)
                actualizar_tabla()
            else:
                messagebox.showwarning("Aviso", "No se encontro el usuario indicado.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Modifica la fecha y el texto del articulo seleccionado
    def modificar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un articulo.")
            return

        titulo_anterior = tabla.seleccionado["titulo"]
        nueva_fecha = entrada_fecha.get().strip()
        nuevo_texto = entrada_texto.get().strip()

        if not nueva_fecha or not nuevo_texto:
            messagebox.showwarning("Aviso", "Escribe la nueva fecha y el nuevo texto.")
            return

        try:
            if modificar_articulo(titulo_anterior, nueva_fecha, nuevo_texto):
                messagebox.showinfo("Correcto", "Articulo modificado.")
                actualizar_tabla()
            else:
                messagebox.showwarning("Aviso", "No se encontro el articulo.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina el articulo seleccionado
    def eliminar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un articulo.")
            return

        titulo_articulo = tabla.seleccionado["titulo"]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este articulo?"):
            try:
                if eliminar_articulo(titulo_articulo):
                    messagebox.showinfo("Correcto", "Articulo eliminado.")
                    vaciar(entrada_titulo, entrada_fecha, entrada_texto, entrada_correo)
                    actualizar_tabla()
                else:
                    messagebox.showwarning("Aviso", "No se encontro el articulo.")

            except Exception as error:
                messagebox.showerror("Error", str(error))

    crear_botones(registrar, modificar, eliminar, actualizar_tabla)

    tabla = TablaScroll(
        contenido,
        [
            ("Titulo", 200, "titulo"),
            ("Fecha", 100, "fecha"),
            ("Texto", 420, "texto"),
            ("Autor", 170, "autor"),
        ],
        al_seleccionar
    )

    actualizar_tabla()

# Crud de comentarios
# Interfaz para administrar los comentarios del blog
def mostrar_comentarios():

    titulo_de_seccion("Administracion de comentarios")

    (entrada_nombre, entrada_url,
     entrada_correo, entrada_articulo) = crear_formulario(
        ["Comentario:", "URL:", "Nombre del usuario:", "Titulo del articulo:"]
    )

    def al_seleccionar(registro):
        llenar(entrada_nombre, registro["comentario"])
        llenar(entrada_url, registro["url"])
        llenar(entrada_correo, registro["usuario"])
        llenar(entrada_articulo, registro["articulo"])

    def actualizar_tabla():
        tabla.cargar(consultar_comentarios())

    # Registra un comentario y lo relaciona con un usuario y un articulo
    def registrar():
        nombre = entrada_nombre.get().strip()
        url = entrada_url.get().strip()
        correo = entrada_correo.get().strip()
        articulo = entrada_articulo.get().strip()

        if not nombre or not url or not correo or not articulo:
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        try:
            if registrar_comentario(nombre, url, correo, articulo):
                messagebox.showinfo("Correcto", "Comentario registrado.")
                vaciar(entrada_nombre, entrada_url, entrada_correo, entrada_articulo)
                actualizar_tabla()
            else:
                messagebox.showwarning(
                    "Aviso",
                    "No se encontro el usuario o articulo indicado."
                )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Modifica el contenido y la URL del comentario seleccionado
    def modificar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un comentario.")
            return

        nombre_anterior = tabla.seleccionado["comentario"]
        nuevo_nombre = entrada_nombre.get().strip()
        nueva_url = entrada_url.get().strip()

        if not nuevo_nombre or not nueva_url:
            messagebox.showwarning("Aviso", "Escribe el nuevo comentario y URL.")
            return

        try:
            if modificar_comentario(nombre_anterior, nuevo_nombre, nueva_url):
                messagebox.showinfo("Correcto", "Comentario modificado.")
                actualizar_tabla()
            else:
                messagebox.showwarning("Aviso", "No se encontro el comentario.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina el comentario seleccionado
    def eliminar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un comentario.")
            return

        nombre = tabla.seleccionado["comentario"]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este comentario?"):
            try:
                if eliminar_comentario(nombre):
                    messagebox.showinfo("Correcto", "Comentario eliminado.")
                    vaciar(entrada_nombre, entrada_url, entrada_correo, entrada_articulo)
                    actualizar_tabla()
                else:
                    messagebox.showwarning("Aviso", "No se encontro el comentario.")

            except Exception as error:
                messagebox.showerror("Error", str(error))

    crear_botones(registrar, modificar, eliminar, actualizar_tabla)

    tabla = TablaScroll(
        contenido,
        [
            ("Comentario", 330, "comentario"),
            ("URL", 200, "url"),
            ("Usuario", 160, "usuario"),
            ("Articulo", 200, "articulo"),
        ],
        al_seleccionar
    )

    actualizar_tabla()

# Crud de etiquetas
# Interfaz para administrar las etiquetas del blog
def mostrar_etiquetas():

    titulo_de_seccion("Administracion de etiquetas")

    entrada_nombre, entrada_url = crear_formulario(
        ["Nombre:", "URL:"]
    )

    def al_seleccionar(registro):
        llenar(entrada_nombre, registro["nombre"])
        llenar(entrada_url, registro["url"])

    def actualizar_tabla():
        tabla.cargar(consultar_etiquetas())

    # Registra una nueva etiqueta despues de validar sus datos
    def registrar():
        nombre = entrada_nombre.get().strip()
        url = entrada_url.get().strip()

        if nombre == "" or url == "":
            messagebox.showwarning("Aviso", "Completa el nombre y la URL.")
            return

        try:
            if registrar_etiqueta(nombre, url):
                messagebox.showinfo("Exito", "Etiqueta registrada correctamente.")
                vaciar(entrada_nombre, entrada_url)
                actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo registrar la etiqueta.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Modifica los datos de la etiqueta seleccionada
    def modificar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una etiqueta.")
            return

        nombre = tabla.seleccionado["nombre"]
        nuevo_nombre = entrada_nombre.get().strip()
        nueva_url = entrada_url.get().strip()

        if nuevo_nombre == "" or nueva_url == "":
            messagebox.showwarning("Aviso", "Completa el nombre y la URL.")
            return

        try:
            if modificar_etiqueta(nombre, nuevo_nombre, nueva_url):
                messagebox.showinfo("Exito", "Etiqueta modificada correctamente.")
                actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se encontro la etiqueta.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina la etiqueta seleccionada
    def eliminar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una etiqueta.")
            return

        nombre = tabla.seleccionado["nombre"]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta etiqueta?"):
            try:
                if eliminar_etiqueta(nombre):
                    messagebox.showinfo("Exito", "Etiqueta eliminada correctamente.")
                    vaciar(entrada_nombre, entrada_url)
                    actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se encontro la etiqueta.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

    crear_botones(registrar, modificar, eliminar, actualizar_tabla)

    tabla = TablaScroll(
        contenido,
        [("Nombre", 300, "nombre"), ("URL", 590, "url")],
        al_seleccionar
    )

    actualizar_tabla()

# Crud de categorias
# Interfaz para administrar las categorias de los articulos
def mostrar_categorias():

    titulo_de_seccion("Administracion de categorias")

    entrada_nombre, entrada_url = crear_formulario(
        ["Nombre:", "URL:"]
    )

    def al_seleccionar(registro):
        llenar(entrada_nombre, registro["nombre"])
        llenar(entrada_url, registro["url"])

    def actualizar_tabla():
        tabla.cargar(consultar_categorias())

    # Registra una nueva categoria
    def registrar():
        nombre = entrada_nombre.get().strip()
        url = entrada_url.get().strip()

        if nombre == "" or url == "":
            messagebox.showwarning("Aviso", "Completa el nombre y la URL.")
            return

        try:
            if registrar_categoria(nombre, url):
                messagebox.showinfo("Exito", "Categoria registrada correctamente.")
                vaciar(entrada_nombre, entrada_url)
                actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo registrar la categoria.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Modifica la categoria seleccionada
    def modificar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una categoria.")
            return

        nombre = tabla.seleccionado["nombre"]
        nuevo_nombre = entrada_nombre.get().strip()
        nueva_url = entrada_url.get().strip()

        if nuevo_nombre == "" or nueva_url == "":
            messagebox.showwarning("Aviso", "Completa el nombre y la URL.")
            return

        try:
            if modificar_categoria(nombre, nuevo_nombre, nueva_url):
                messagebox.showinfo("Exito", "Categoria modificada correctamente.")
                actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se encontro la categoria.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    # Elimina la categoria seleccionada
    def eliminar():
        if tabla.seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una categoria.")
            return

        nombre = tabla.seleccionado["nombre"]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta categoria?"):
            try:
                if eliminar_categoria(nombre):
                    messagebox.showinfo("Exito", "Categoria eliminada correctamente.")
                    vaciar(entrada_nombre, entrada_url)
                    actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se encontro la categoria.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

    crear_botones(registrar, modificar, eliminar, actualizar_tabla)

    tabla = TablaScroll(
        contenido,
        [("Nombre", 300, "nombre"), ("URL", 590, "url")],
        al_seleccionar
    )

    actualizar_tabla()

# Pantalla de la bienvenida
def mostrar_bienvenida():

    tk.Label(
        contenido,
        text="LEONEXO TECH",
        font=("Arial", 27, "bold"),
        bg="white",
        fg=COLOR_OSCURO
    ).pack(pady=(20, 3))

    tk.Label(
        contenido,
        text="CONECTANDO IDEAS CON TECNOLOGIA",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#607D8B"
    ).pack(pady=3)

    tk.Frame(
        contenido,
        bg="#CFD8DC",
        height=2
    ).pack(fill="x", padx=60, pady=12)

    tk.Label(
        contenido,
        text="¡Bienvenido a Leonexo Tech!",
        font=("Arial", 17, "bold"),
        bg="white",
        fg=COLOR_OSCURO
    ).pack(pady=5)

    tk.Label(
        contenido,
        text=(
            "Un blog dedicado a compartir conocimientos, experiencias "
            "y novedades sobre tecnologia.\n"
            "Explora nuestros contenidos sobre programacion, software, "
            "bases de datos e innovacion."
        ),
        font=("Arial", 10),
        bg="white",
        fg="#455A64",
        justify="center",
        wraplength=730
    ).pack(pady=8)

    tk.Label(
        contenido,
        text="TEMAS PRINCIPALES",
        font=("Arial", 12, "bold"),
        bg="white",
        fg=COLOR_OSCURO
    ).pack(pady=(10, 5))

    temas = tk.Frame(contenido, bg="white")
    temas.pack(pady=3)

    # Temas de los que se habla en la pantalla principal.
    informacion = [
        ("DESARROLLO DE SOFTWARE", "Programacion y aplicaciones"),
        ("BASES DE DATOS", "Almacenamiento y gestion de informacion"),
        ("INTELIGENCIA ARTIFICIAL", "Aprendizaje y nuevas tecnologias"),
        ("CIBERSEGURIDAD", "Proteccion de sistemas y datos"),
        ("INNOVACION TECNOLOGICA", "Tendencias y avances")
    ]

    for i, (tema, detalle) in enumerate(informacion):

        tarjeta = tk.Frame(
            temas,
            bg="#ECEFF1",
            width=240,
            height=65
        )

        tarjeta.grid(
            row=i // 2,
            column=i % 2,
            padx=8,
            pady=5
        )

        tarjeta.pack_propagate(False)

        tk.Label(
            tarjeta,
            text=tema,
            font=("Arial", 9, "bold"),
            bg="#ECEFF1",
            fg=COLOR_OSCURO
        ).pack(pady=(10, 3))

        tk.Label(
            tarjeta,
            text=detalle,
            font=("Arial", 8),
            bg="#ECEFF1",
            fg="#455A64"
        ).pack()

    # Presentacion del proyecto
    tk.Label(
        contenido,
        text=(
            "UNIVERSIDAD AUTONOMA DE CHIHUAHUA\n"
            "Ingenieria en Sistemas Computacionales en Hardware\n"
            "Grupo: 7CC2\n"
            "Proyecto Final | Bases de Datos Avanzadas"
        ),
        font=("Arial", 9),
        bg="white",
        fg="#607D8B",
        justify="center"
    ).pack(pady=10)

# Botones del menu lateral
# Opciones disponibles para navegar por el sistema
secciones = [
    "Inicio",
    "Usuarios",
    "Articulos",
    "Comentarios",
    "Etiquetas",
    "Categorias"
]

for seccion in secciones:

    boton = tk.Button(
        menu,
        text=seccion,
        font=("Arial", 11),
        width=18,
        command=lambda nombre=seccion: mostrar_seccion(
            "Bienvenido" if nombre == "Inicio" else nombre
        )
    )

    boton.pack(pady=10)

# Inicio y cierre de la aplicacion
# Muestra la pantalla de bienvenida al iniciar el programa
mostrar_seccion("Bienvenido")

# Cierra la conexion con Neo4j antes de cerrar la ventana
def salir():
    cerrar_conexion()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", salir)

# Mantiene activa la interfaz grafica
ventana.mainloop()
