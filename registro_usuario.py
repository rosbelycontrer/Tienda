import tkinter as Ventana
from tkinter import ttk, messagebox
from datetime import datetime

from inicio_sesion import Usuario, FormularioBase


# ============================================================
#   ARRAY DE DUPLAS: (clave del diccionario, texto que se muestra)
#   Sirve para mostrar los datos de un cliente (como campos_silla)
# ============================================================
campos_cliente = [
    ("nombre", "Nombre"),
    ("correo", "Correo"),
    ("tipo_documento", "Tipo de documento"),
    ("documento", "Documento"),
    ("fecha", "Fecha de nacimiento"),
    ("genero", "Género"),
    ("telefono", "Teléfono"),
    ("ciudad", "Ciudad"),
    ("direccion", "Dirección"),
    ("intereses", "Intereses"),
    ("satisfaccion", "Satisfacción"),
    ("observaciones", "Observaciones")
]

# duplas mas cortas para el listado de la ventana
campos_resumen = [
    ("nombre", "Nombre"),
    ("documento", "Doc"),
    ("correo", "Correo"),
    ("ciudad", "Ciudad")
]


# ============================================================
#   CLASE CLIENTE
# ============================================================

# HERENCIA: Cliente hereda de Usuario (y Usuario de Persona)
class Cliente(Usuario):

    def __init__(self, nombre, correo, contrasena, tipo_documento, documento, fecha,
                 genero, telefono, ciudad, direccion, intereses, satisfaccion, observaciones):
        super().__init__(nombre, correo, contrasena)
        # ENCAPSULAMIENTO: todo privado
        self.__tipo_documento = tipo_documento
        self.__documento = documento
        self.__fecha = fecha
        self.__genero = genero
        self.__telefono = telefono
        self.__ciudad = ciudad
        self.__direccion = direccion
        self.__intereses = intereses
        self.__satisfaccion = satisfaccion
        self.__observaciones = observaciones

    # convierte el objeto en un DICCIONARIO (como cada silla del inventario)
    def a_diccionario(self):
        return {
            "nombre": self.get_nombre(),
            "correo": self.get_correo(),
            "tipo_documento": self.__tipo_documento,
            "documento": self.__documento,
            "fecha": self.__fecha,
            "genero": self.__genero,
            "telefono": self.__telefono,
            "ciudad": self.__ciudad,
            "direccion": self.__direccion,
            "intereses": self.__intereses,
            "satisfaccion": self.__satisfaccion,
            "observaciones": self.__observaciones
        }

    # POLIMORFISMO: el mismo metodo de Usuario pero muestra mas datos.
    # Se recorren las duplas para mostrar cada dato del diccionario
    def mostrar_datos(self):
        cliente = self.a_diccionario()
        texto = "Tipo: Cliente\n"
        for clave, etiqueta in campos_cliente:
            valor = cliente[clave]
            if clave == "intereses":
                if len(valor) > 0:
                    valor = ", ".join(valor)
                else:
                    valor = "Ninguno"
            elif clave == "satisfaccion":
                valor = f"{valor}/10"
            elif clave == "observaciones" and valor == "":
                valor = "Sin observaciones"
            texto += f"{etiqueta}: {valor}\n"
        return texto


# Crea un objeto Cliente a partir de un diccionario
def crear_cliente(datos):
    return Cliente(datos["nombre"], datos["correo"], datos["contrasena"],
                   datos["tipo_documento"], datos["documento"], datos["fecha"],
                   datos["genero"], datos["telefono"], datos["ciudad"],
                   datos["direccion"], datos["intereses"], datos["satisfaccion"],
                   datos["observaciones"])


# ============================================================
#   FORMULARIO DE REGISTRO
# ============================================================

# HERENCIA: RegistroUsuario hereda de FormularioBase
class RegistroUsuario(FormularioBase):

    # ------------------------------------------------------------
    # 1. Constructor
    # ------------------------------------------------------------
    def __init__(self, usuarios):
        super().__init__("Registro de Cliente - Tienda", "1100x840")
        self.__usuarios = usuarios     # el mismo arreglo que usa el login
        self.errores = []

        # campos de texto (Label + Entry)
        self.campos = [
            ("nombre", "Nombre completo:"),
            ("documento", "N° de documento:"),
            ("fecha", "Fecha nac. (dd/mm/aaaa):"),
            ("telefono", "Teléfono:"),
            ("correo", "Correo:"),
            ("direccion", "Dirección:"),
            ("contrasena", "Contraseña:")
        ]

        # opciones de los otros widgets
        self.tiposDocumento = ["Cédula de ciudadanía", "Tarjeta de identidad",
                               "Cédula de extranjería", "Pasaporte"]
        self.generos = ["Femenino", "Masculino", "Otro"]
        self.listaIntereses = ["Ropa", "Tecnología", "Hogar", "Deportes", "Juguetes", "Ofertas"]
        self.ciudades = ["Barranquilla", "Bogotá", "Medellín", "Cali", "Cartagena",
                         "Santa Marta", "Bucaramanga", "Pereira", "Montería", "Valledupar"]

        # widgets que se crean despues
        self.comboTipo = None
        self.varGenero = None
        self.varsIntereses = []
        self.listaCiudad = None
        self.escalaSatisfaccion = None
        self.textoObservaciones = None
        self.labelResultado = None

        # MENU COMO DICCIONARIO: opcion -> (texto del boton, funcion)
        self.menuBotones = {
            "1": ("Enviar", self.procesar_formulario),
            "2": ("Limpiar", self.limpiar_campos),
            "3": ("Cerrar", self.cerrar)
        }

        # MENU DE INFORMES (como menu_informes del taller de las sillas)
        self.menuInformes = {
            "1": ("Ver clientes", self.imprimir_datos),
            "2": ("Total clientes", self.total_clientes),
            "3": ("Promedio satisfacción", self.promedio_satisfaccion),
            "4": ("Clientes por ciudad", self.clientes_por_ciudad),
            "5": ("Ordenar por nombre", self.ordenar_por_nombre),
            "6": ("Buscar documento", self.buscar_por_documento)
        }

    # se llama desde el boton "Registrarse" del login
    def abrir(self):
        # si ya esta abierta no se abre otra
        if self.formulario is not None and self.formulario.winfo_exists():
            self.formulario.lift()
            return
        self.iniciar_ventana()
        self.iniciar_preguntas()

    # ------------------------------------------------------------
    # 2. Crea la ventana (Toplevel porque es una ventana secundaria)
    # ------------------------------------------------------------
    def iniciar_ventana(self):
        self.formulario = Ventana.Toplevel()
        self.configurar_ventana()
        return self.formulario

    # ------------------------------------------------------------
    # 3. Crea todas las preguntas y widgets
    # ------------------------------------------------------------
    def iniciar_preguntas(self):
        self.entries = {}
        self.labelsEstado = {}
        self.crear_titulo("REGISTRO DE CLIENTE")

        contenedor = Ventana.Frame(self.formulario, bg=self.colorFondo)
        contenedor.pack(padx=10)

        # ---------- lado izquierdo: Label + Entry ----------
        izquierda = Ventana.Frame(contenedor, bg=self.colorFondo)
        izquierda.grid(row=0, column=0, sticky="n", padx=5)

        fila = 0
        for clave, texto in self.campos:
            self.crear_fila(izquierda, fila, clave, texto, ancho_label=22,
                            oculto=(clave == "contrasena"))
            fila += 1

        # Observaciones -> Text (texto largo)
        self.crear_pregunta(izquierda, "Observaciones (opcional):").grid(
            row=fila, column=0, padx=5, pady=5, sticky="n")
        self.textoObservaciones = Ventana.Text(izquierda, width=36, height=4, font=("Arial", 11))
        self.textoObservaciones.grid(row=fila, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # ---------- lado derecho: selecciones ----------
        derecha = Ventana.LabelFrame(contenedor, text=" Más información ", bg=self.colorFondo,
                                     fg=self.colorAmarillo, font=("Arial", 12, "bold"), padx=10, pady=5)
        derecha.grid(row=0, column=1, sticky="n", padx=10)

        # Tipo de documento -> Combobox
        self.crear_texto(derecha, "Tipo de documento:").pack(anchor="w")
        self.comboTipo = ttk.Combobox(derecha, values=self.tiposDocumento, state="readonly",
                                      width=30, font=("Arial", 11))
        self.comboTipo.pack(anchor="w", pady=(0, 8))

        # Genero -> Radiobutton (solo uno)
        self.crear_texto(derecha, "Género:").pack(anchor="w")
        marcoGenero = Ventana.Frame(derecha, bg=self.colorFondo)
        marcoGenero.pack(anchor="w", pady=(0, 8))
        self.varGenero = Ventana.StringVar(value="Ninguno")
        for genero in self.generos:
            radio = Ventana.Radiobutton(marcoGenero, text=genero, value=genero, variable=self.varGenero)
            self.estilo_opcion(radio)
            radio.pack(side="left")

        # Intereses -> Checkbutton (varios)
        self.crear_texto(derecha, "¿Qué productos le interesan?").pack(anchor="w")
        marcoIntereses = Ventana.Frame(derecha, bg=self.colorFondo)
        marcoIntereses.pack(anchor="w", pady=(0, 8))
        self.varsIntereses = []
        posicion = 0
        for interes in self.listaIntereses:
            variable = Ventana.BooleanVar()
            check = Ventana.Checkbutton(marcoIntereses, text=interes, variable=variable)
            self.estilo_opcion(check)
            check.grid(row=posicion // 3, column=posicion % 3, sticky="w")
            self.varsIntereses.append((interes, variable))
            posicion += 1

        # Ciudad -> Listbox con scrollbar
        self.crear_texto(derecha, "Ciudad:").pack(anchor="w")
        marcoCiudad = Ventana.Frame(derecha)
        marcoCiudad.pack(anchor="w", pady=(0, 8))
        self.listaCiudad = Ventana.Listbox(marcoCiudad, height=4, width=30, font=("Arial", 11),
                                           exportselection=False)
        barra = Ventana.Scrollbar(marcoCiudad, command=self.listaCiudad.yview)
        self.listaCiudad.configure(yscrollcommand=barra.set)
        for ciudad in self.ciudades:
            self.listaCiudad.insert(Ventana.END, ciudad)
        self.listaCiudad.pack(side="left")
        barra.pack(side="right", fill="y")

        # Satisfaccion -> Scale (rango)
        self.crear_texto(derecha, "Nivel de satisfacción (1 a 10):").pack(anchor="w")
        self.escalaSatisfaccion = Ventana.Scale(derecha, from_=1, to=10, orient="horizontal", length=280)
        self.escalaSatisfaccion.configure(bg=self.colorFondo, fg=self.colorBlanco, highlightthickness=0,
                                          troughcolor=self.colorAmarillo)
        self.escalaSatisfaccion.set(5)
        self.escalaSatisfaccion.pack(anchor="w")

        # ---------- botones (se crean recorriendo el diccionario) ----------
        marcoBotones = Ventana.Frame(self.formulario, bg=self.colorFondo)
        marcoBotones.pack(pady=(10, 0))
        self.crear_botones(marcoBotones, self.menuBotones, 3)

        # ---------- informes (tambien desde un diccionario) ----------
        marcoInformes = Ventana.LabelFrame(self.formulario, text=" Informes ", bg=self.colorFondo,
                                           fg=self.colorAmarillo, font=("Arial", 11, "bold"))
        marcoInformes.pack(pady=5)
        posicion = 0
        for opcion, (texto, funcion) in self.menuInformes.items():
            boton = Ventana.Button(marcoInformes, text=texto, command=funcion, width=19,
                                   font=("Arial", 10, "bold"))
            boton.grid(row=0, column=posicion, padx=3, pady=5)
            posicion += 1

        # Mensaje de exito o error
        self.labelMensaje = Ventana.Label(self.formulario, text="", justify="center")
        self.labelMensaje.configure(bg=self.colorFondo, font=("Arial", 12, "bold"))
        self.labelMensaje.pack()

        # Aqui se muestran los clientes guardados
        self.labelResultado = Ventana.Label(self.formulario, text="")
        self.labelResultado.configure(bg=self.colorAmarillo, font=("Arial", 11), justify="left",
                                      anchor="nw", wraplength=980, padx=10, pady=8)
        self.labelResultado.pack(padx=10, pady=10, fill="x")
        self.imprimir_datos()

    # pregunta con el mismo estilo de crear_fila
    def crear_pregunta(self, marco, texto):
        label = Ventana.Label(marco, text=texto)
        label.configure(bg=self.colorAmarillo, fg=self.colorFondo, font=("Arial", 11, "bold"))
        label.configure(borderwidth=2, relief="raised", width=22, anchor="w")
        return label

    def crear_texto(self, marco, texto):
        return Ventana.Label(marco, text=texto, bg=self.colorFondo, fg=self.colorAmarillo,
                             font=("Arial", 11, "bold"))

    def estilo_opcion(self, widget):
        widget.configure(bg=self.colorFondo, fg=self.colorBlanco, selectcolor=self.colorFondo,
                         activebackground=self.colorFondo, activeforeground=self.colorBlanco,
                         font=("Arial", 11))

    # ------------------------------------------------------------
    # 4. Funcion GENERAL: la llama el boton Enviar
    # ------------------------------------------------------------
    def procesar_formulario(self):
        datos = self.tomar_datos()

        if self.validar_campos(datos):
            self.almacenar_datos(datos)
            self.imprimir_datos()
            self.limpiar_campos()
            self.mostrar_mensaje("Cliente registrado correctamente.", self.colorAmarillo)
        else:
            texto = "Revise los campos marcados en rojo."
            if len(self.errores) > 0:
                texto += "\n" + "\n".join(self.errores)
            self.mostrar_mensaje(texto, self.colorBlanco)

    # ------------------------------------------------------------
    # 5. POLIMORFISMO: se sobrescribe tomar_datos para agregar los
    #    datos de los otros widgets (combobox, radio, check...)
    # ------------------------------------------------------------
    def tomar_datos(self):
        datos = super().tomar_datos()      # trae lo de los entry
        datos["tipo_documento"] = self.comboTipo.get()
        datos["genero"] = self.varGenero.get()

        intereses = []
        for interes, variable in self.varsIntereses:
            if variable.get():
                intereses.append(interes)
        datos["intereses"] = intereses

        seleccion = self.listaCiudad.curselection()
        if len(seleccion) > 0:
            datos["ciudad"] = self.listaCiudad.get(seleccion[0])
        else:
            datos["ciudad"] = ""

        datos["satisfaccion"] = self.escalaSatisfaccion.get()
        datos["observaciones"] = self.textoObservaciones.get("1.0", Ventana.END).strip()
        return datos

    # ------------------------------------------------------------
    # 6. POLIMORFISMO: validar_campos hace lo del padre (vacios)
    #    y ademas revisa que los datos esten bien escritos
    # ------------------------------------------------------------
    def validar_campos(self, datos):
        correcto = super().validar_campos(datos)
        self.errores = []

        if datos["documento"] != "" and not datos["documento"].isdigit():
            self.marcar_estado("documento", "✘ Solo números", self.colorRojo)
            correcto = False

        if datos["fecha"] != "" and not self.fecha_valida(datos["fecha"]):
            self.marcar_estado("fecha", "✘ dd/mm/aaaa", self.colorRojo)
            correcto = False

        if datos["telefono"] != "" and (not datos["telefono"].isdigit() or len(datos["telefono"]) != 10):
            self.marcar_estado("telefono", "✘ 10 números", self.colorRojo)
            correcto = False

        if datos["correo"] != "":
            if "@" not in datos["correo"] or "." not in datos["correo"]:
                self.marcar_estado("correo", "✘ Inválido", self.colorRojo)
                correcto = False
            elif self.correo_existe(datos["correo"]):
                self.marcar_estado("correo", "✘ Ya existe", self.colorRojo)
                correcto = False

        if datos["contrasena"] != "" and len(datos["contrasena"]) < 6:
            self.marcar_estado("contrasena", "✘ Mín. 6", self.colorRojo)
            correcto = False

        if datos["tipo_documento"] == "":
            self.errores.append("• Seleccione el tipo de documento.")
        if datos["genero"] == "Ninguno":
            self.errores.append("• Seleccione un género.")
        if datos["ciudad"] == "":
            self.errores.append("• Seleccione una ciudad.")
        if len(self.errores) > 0:
            correcto = False

        return correcto

    def fecha_valida(self, fecha):
        try:
            fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y")
            return fecha_convertida <= datetime.now()   # no puede ser futura
        except ValueError:
            return False

    def correo_existe(self, correo):
        for usuario in self.__usuarios:
            if usuario.get_correo() == correo:
                return True
        return False

    # ------------------------------------------------------------
    # 7. Crea el objeto Cliente y lo guarda en el arreglo
    # ------------------------------------------------------------
    def almacenar_datos(self, datos):
        cliente = crear_cliente(datos)
        self.__usuarios.append(cliente)          # APPEND: se agrega al final del arreglo
        print("Cliente guardado:\n" + cliente.mostrar_datos())   # se ve en la consola
        messagebox.showinfo("Registro exitoso", "Ya puede iniciar sesión con su correo y contraseña.",
                            parent=self.formulario)

    # ------------------------------------------------------------
    # 8. ARRAY DE DICCIONARIOS: devuelve los clientes como diccionarios
    # ------------------------------------------------------------
    def obtener_clientes(self):
        clientes = []
        for usuario in self.__usuarios:
            if isinstance(usuario, Cliente):
                clientes.append(usuario.a_diccionario())
        return clientes

    def mostrar_resultado(self, texto):
        self.labelResultado.configure(text=texto)

    # Muestra en la ventana todos los clientes (como consultar_inventario)
    def imprimir_datos(self):
        clientes = self.obtener_clientes()
        if len(clientes) == 0:
            self.mostrar_resultado("Aún no hay clientes registrados.")
            return

        texto = f"Clientes registrados: {len(clientes)}\n\n"
        contador = 1
        for cliente in clientes:
            valores = []
            # se recorren las duplas para sacar cada dato del diccionario
            for clave, etiqueta in campos_resumen:
                valores.append(f"{etiqueta}: {cliente[clave]}")
            texto += f"{contador}. " + " | ".join(valores) + "\n"
            contador += 1
        self.mostrar_resultado(texto)

    # ---------------- FUNCIONES DE INFORMES ----------------
    def total_clientes(self):
        self.mostrar_resultado(f"Total de clientes registrados: {len(self.obtener_clientes())}")

    def promedio_satisfaccion(self):
        clientes = self.obtener_clientes()
        if len(clientes) == 0:
            self.mostrar_resultado("No hay clientes para calcular el promedio.")
            return
        suma = 0
        for cliente in clientes:
            suma += cliente["satisfaccion"]
        self.mostrar_resultado(f"Promedio de satisfacción: {suma / len(clientes):.1f} / 10")

    def clientes_por_ciudad(self):
        clientes = self.obtener_clientes()
        if len(clientes) == 0:
            self.mostrar_resultado("No hay clientes registrados.")
            return
        ciudades = []
        for cliente in clientes:
            ciudades.append(cliente["ciudad"])

        texto = "Clientes por ciudad:\n"
        for ciudad in self.ciudades:
            cantidad = ciudades.count(ciudad)       # COUNT: cuantas veces aparece
            if cantidad > 0:
                texto += f"   {ciudad}: {cantidad}\n"
        self.mostrar_resultado(texto)

    def ordenar_por_nombre(self):
        clientes = self.obtener_clientes()
        if len(clientes) == 0:
            self.mostrar_resultado("No hay clientes registrados.")
            return
        nombres = []
        for cliente in clientes:
            nombres.append(cliente["nombre"])
        nombres.sort()                              # SORT: ordena alfabeticamente

        texto = "Clientes ordenados por nombre:\n"
        contador = 1
        for nombre in nombres:
            texto += f"   {contador}. {nombre}\n"
            contador += 1
        self.mostrar_resultado(texto)

    def buscar_por_documento(self):
        documento = self.entries["documento"].get().strip()
        if documento == "":
            self.mostrar_resultado("Escriba el número de documento en el campo 'N° de documento' y vuelva a buscar.")
            return

        # dos listas en el mismo orden: los objetos y sus documentos
        objetos = []
        documentos = []
        for usuario in self.__usuarios:
            if isinstance(usuario, Cliente):
                objetos.append(usuario)
                documentos.append(usuario.a_diccionario()["documento"])

        if documento in documentos:
            posicion = documentos.index(documento)  # INDEX: posicion en la lista
            cliente = objetos[posicion]
            self.mostrar_resultado(f"Cliente encontrado en la posición {posicion}:\n\n"
                                   + cliente.mostrar_datos())
        else:
            self.mostrar_resultado(f"No hay ningún cliente con el documento {documento}.")

    def cerrar(self):
        self.formulario.destroy()

    # ------------------------------------------------------------
    # 9. Deja el formulario listo para el siguiente cliente
    # ------------------------------------------------------------
    def limpiar_campos(self):
        for clave, texto in self.campos:
            self.entries[clave].delete(0, Ventana.END)
            self.labelsEstado[clave].configure(text="")
        self.comboTipo.set("")
        self.varGenero.set("Ninguno")
        for interes, variable in self.varsIntereses:
            variable.set(False)
        self.listaCiudad.selection_clear(0, Ventana.END)
        self.escalaSatisfaccion.set(5)
        self.textoObservaciones.delete("1.0", Ventana.END)
        self.labelMensaje.configure(text="")
        self.entries["nombre"].focus()
