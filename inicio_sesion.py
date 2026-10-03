import tkinter as Ventana
from tkinter import messagebox
from abc import ABC, abstractmethod


# ============================================================
#   CLASES DE LAS PERSONAS
# ============================================================

# ABSTRACCION: Persona es abstracta, no se pueden crear objetos de ella
class Persona(ABC):

    def __init__(self, nombre, correo):
        # ENCAPSULAMIENTO: atributos privados (doble guion bajo)
        self.__nombre = nombre
        self.__correo = correo

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    # cada clase hija tiene que hacer este metodo
    @abstractmethod
    def mostrar_datos(self):
        pass


# HERENCIA: Usuario hereda de Persona
class Usuario(Persona):

    def __init__(self, nombre, correo, contrasena):
        super().__init__(nombre, correo)
        self.__contrasena = contrasena   # privada, no tiene get

    # la contraseña no se muestra, solo se compara
    def verificar_contrasena(self, contrasena):
        return self.__contrasena == contrasena

    # POLIMORFISMO: Usuario muestra sus datos de esta forma
    def mostrar_datos(self):
        return f"Tipo: Usuario\nNombre: {self.get_nombre()}\nCorreo: {self.get_correo()}"


# ============================================================
#   CLASE PADRE DE LOS FORMULARIOS
# ============================================================

# ABSTRACCION: clase base de todas las ventanas (login y registro)
class FormularioBase(ABC):

    # ------------------------------------------------------------
    # 1. Constructor: atributos que comparten todos los formularios
    # ------------------------------------------------------------
    def __init__(self, titulo, tamano):
        self.colorFondo = "#2c3e50"
        self.colorAmarillo = "#f9d342"
        self.colorAzul = "#2e86de"
        self.colorVerde = "#27ae60"
        self.colorRojo = "#e74c3c"
        self.colorBlanco = "white"
        self.titulo = titulo
        self.tamano = tamano
        self.formulario = None
        self.labelMensaje = None
        self.campos = []          # lista de duplas (clave, pregunta)
        self.entries = {}
        self.labelsEstado = {}

    # ------------------------------------------------------------
    # 2. Configura la ventana (lo heredan todos)
    # ------------------------------------------------------------
    def configurar_ventana(self):
        self.formulario.title(self.titulo)
        self.formulario.geometry(self.tamano)
        self.formulario.resizable(False, False)
        self.formulario.configure(bg=self.colorFondo)
        self.formulario.configure(cursor="hand2")

    # ------------------------------------------------------------
    # 3. Pone el titulo grande arriba
    # ------------------------------------------------------------
    def crear_titulo(self, texto):
        titulo = Ventana.Label(self.formulario, text=texto)
        titulo.configure(bg=self.colorFondo, fg=self.colorAmarillo, font=("Arial", 22, "bold"))
        titulo.pack(pady=15)

    # ------------------------------------------------------------
    # 4. Crea una fila: pregunta | entry | estado
    # ------------------------------------------------------------
    def crear_fila(self, marco, fila, clave, texto, ancho_label=12, oculto=False):
        label = Ventana.Label(marco, text=texto)
        label.configure(bg=self.colorAmarillo, fg=self.colorFondo, font=("Arial", 11, "bold"))
        label.configure(borderwidth=2, relief="raised", width=ancho_label, anchor="w")
        label.grid(row=fila, column=0, padx=5, pady=5)

        entry = Ventana.Entry(marco)
        entry.configure(font=("Arial", 12), width=22)
        if oculto:
            entry.configure(show="*")    # para la contraseña
        entry.grid(row=fila, column=1, padx=5, pady=5)

        estado = Ventana.Label(marco, text="", width=14)
        estado.configure(bg=self.colorBlanco, font=("Arial", 10, "bold"))
        estado.grid(row=fila, column=2, padx=5, pady=5)

        self.entries[clave] = entry
        self.labelsEstado[clave] = estado

    # ------------------------------------------------------------
    # 5. Toma lo escrito en cada entry y lo guarda en un diccionario
    # ------------------------------------------------------------
    def tomar_datos(self):
        datos = {}
        for clave, texto in self.campos:
            datos[clave] = self.entries[clave].get().strip()
        return datos

    # ------------------------------------------------------------
    # 6. Revisa si cada campo esta vacio o diligenciado
    # ------------------------------------------------------------
    def validar_campos(self, datos):
        todos_llenos = True
        for clave, texto in self.campos:
            if datos[clave] == "":
                self.marcar_estado(clave, "✘ Vacío", self.colorRojo)
                todos_llenos = False
            else:
                self.marcar_estado(clave, "✔ Diligenciado", self.colorVerde)
        return todos_llenos

    # ------------------------------------------------------------
    # 7. Crea los botones recorriendo un MENU COMO DICCIONARIO
    #    opcion -> dupla (texto, funcion)   (igual que en el taller de las sillas)
    # ------------------------------------------------------------
    def crear_botones(self, marco, menu, columnas):
        posicion = 0
        for opcion, (texto, funcion) in menu.items():
            boton = Ventana.Button(marco, text=texto, command=funcion, width=14,
                                   font=("Arial", 12, "bold"))
            if texto == "Salir" or texto == "Cerrar":
                boton.configure(bg=self.colorRojo, fg=self.colorBlanco)
            elif opcion == "1":
                boton.configure(bg=self.colorAzul, fg=self.colorBlanco)
            else:
                boton.configure(bg=self.colorAmarillo, fg=self.colorFondo)
            boton.grid(row=posicion // columnas, column=posicion % columnas, padx=5, pady=4)
            posicion += 1

    def marcar_estado(self, clave, texto, color):
        self.labelsEstado[clave].configure(text=texto, fg=color)

    def mostrar_mensaje(self, texto, color):
        self.labelMensaje.configure(text=texto, fg=color)

    # Metodos abstractos: cada formulario los hace a su manera
    @abstractmethod
    def iniciar_ventana(self):
        pass

    @abstractmethod
    def iniciar_preguntas(self):
        pass

    @abstractmethod
    def procesar_formulario(self):
        pass

    @abstractmethod
    def limpiar_campos(self):
        pass


# ============================================================
#   FORMULARIO DE INICIO DE SESION
# ============================================================

# HERENCIA: InicioSesion hereda de FormularioBase
class InicioSesion(FormularioBase):

    # ------------------------------------------------------------
    # 1. Constructor
    # ------------------------------------------------------------
    def __init__(self, usuarios, registro):
        super().__init__("Inicio de Sesión - Tienda", "600x520")
        self.__usuarios = usuarios       # arreglo de usuarios (privado)
        self.registro = registro         # objeto del registro para abrirlo
        self.campos = [
            ("correo", "Correo:"),
            ("contrasena", "Contraseña:")
        ]
        self.varMostrar = None
        self.varRecordar = None

        # MENU COMO DICCIONARIO: opcion -> (texto del boton, funcion)
        self.menuBotones = {
            "1": ("Ingresar", self.procesar_formulario),
            "2": ("Registrarse", self.abrir_registro),
            "3": ("Limpiar", self.limpiar_campos),
            "4": ("Salir", self.salir)
        }

    # ------------------------------------------------------------
    # 2. Crea la ventana principal
    # ------------------------------------------------------------
    def iniciar_ventana(self):
        self.formulario = Ventana.Tk()
        self.configurar_ventana()
        return self.formulario

    # ------------------------------------------------------------
    # 3. Crea las preguntas, checkbuttons y botones
    # ------------------------------------------------------------
    def iniciar_preguntas(self):
        self.crear_titulo("INICIO DE SESIÓN")

        marco = Ventana.Frame(self.formulario, bg=self.colorFondo)
        marco.pack(padx=10, pady=10)

        fila = 0
        for clave, texto in self.campos:
            self.crear_fila(marco, fila, clave, texto, oculto=(clave == "contrasena"))
            fila += 1

        # Checkbutton para ver la contraseña
        self.varMostrar = Ventana.BooleanVar()
        checkMostrar = Ventana.Checkbutton(marco, text="Mostrar contraseña", variable=self.varMostrar,
                                           command=self.mostrar_contrasena)
        self.estilo_check(checkMostrar)
        checkMostrar.grid(row=fila, column=1, sticky="w")

        # Checkbutton recordar sesion (si / no)
        self.varRecordar = Ventana.BooleanVar()
        checkRecordar = Ventana.Checkbutton(marco, text="Recordar sesión", variable=self.varRecordar)
        self.estilo_check(checkRecordar)
        checkRecordar.grid(row=fila + 1, column=1, sticky="w")

        # Botones: se crean recorriendo el diccionario del menu
        marcoBotones = Ventana.Frame(self.formulario, bg=self.colorFondo)
        marcoBotones.pack(pady=10)
        self.crear_botones(marcoBotones, self.menuBotones, 2)

        # Mensaje de error o de bienvenida
        self.labelMensaje = Ventana.Label(self.formulario, text="")
        self.labelMensaje.configure(bg=self.colorFondo, font=("Arial", 13, "bold"))
        self.labelMensaje.pack(pady=10)

        ayuda = Ventana.Label(self.formulario, text="Usuario de prueba: admin@tienda.com / admin123")
        ayuda.configure(bg=self.colorFondo, fg="#bdc3c7", font=("Arial", 10))
        ayuda.pack(side="bottom", pady=10)

    def estilo_check(self, check):
        check.configure(bg=self.colorFondo, fg=self.colorBlanco, selectcolor=self.colorFondo,
                        activebackground=self.colorFondo, activeforeground=self.colorBlanco,
                        font=("Arial", 11))

    # ------------------------------------------------------------
    # 4. Funcion GENERAL: la llama el boton Ingresar
    # ------------------------------------------------------------
    def procesar_formulario(self):
        datos = self.tomar_datos()

        if not self.validar_campos(datos):
            self.mostrar_mensaje("Hay campos vacíos. Por favor complétalos.", self.colorBlanco)
            return

        usuario = self.buscar_usuario(datos["correo"], datos["contrasena"])
        if usuario is None:
            self.mostrar_mensaje("Correo o contraseña incorrectos.", self.colorRojo)
            self.entries["contrasena"].delete(0, Ventana.END)
            return

        self.mostrar_mensaje(f"Bienvenido(a) {usuario.get_nombre()}", self.colorAmarillo)
        # POLIMORFISMO: si es Usuario o Cliente, mostrar_datos() muestra cosas distintas
        messagebox.showinfo("Bienvenido", usuario.mostrar_datos())

        self.limpiar_campos()
        if self.varRecordar.get():
            self.entries["correo"].insert(0, datos["correo"])   # recuerda el correo
            self.varRecordar.set(True)

    # ------------------------------------------------------------
    # 5. Busca el usuario en el arreglo
    # ------------------------------------------------------------
    def buscar_usuario(self, correo, contrasena):
        for usuario in self.__usuarios:
            if usuario.get_correo() == correo and usuario.verificar_contrasena(contrasena):
                return usuario
        return None

    def mostrar_contrasena(self):
        if self.varMostrar.get():
            self.entries["contrasena"].configure(show="")
        else:
            self.entries["contrasena"].configure(show="*")

    def abrir_registro(self):
        self.registro.abrir()

    # ------------------------------------------------------------
    # 6. Deja el formulario limpio
    # ------------------------------------------------------------
    def limpiar_campos(self):
        for clave, texto in self.campos:
            self.entries[clave].delete(0, Ventana.END)
            self.labelsEstado[clave].configure(text="")
        self.varMostrar.set(False)
        self.varRecordar.set(False)
        self.mostrar_contrasena()
        self.entries["correo"].focus()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que desea salir?"):
            self.formulario.destroy()
