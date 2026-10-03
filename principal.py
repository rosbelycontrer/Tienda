# ****** codigo principal ******
from inicio_sesion import InicioSesion, Usuario
from registro_usuario import RegistroUsuario, crear_cliente

# ARRAY DE DICCIONARIOS: clientes de ejemplo (como el inventario de sillas)
clientes_ejemplo = [
    {"nombre": "Laura Pérez", "correo": "laura@correo.com", "contrasena": "laura123",
     "tipo_documento": "Cédula de ciudadanía", "documento": "1045678901", "fecha": "12/05/2002",
     "genero": "Femenino", "telefono": "3004567890", "ciudad": "Barranquilla",
     "direccion": "Calle 72 # 45-10", "intereses": ["Ropa", "Ofertas"], "satisfaccion": 9,
     "observaciones": ""},
    {"nombre": "Carlos Martínez", "correo": "carlos@correo.com", "contrasena": "carlos123",
     "tipo_documento": "Cédula de ciudadanía", "documento": "1001234567", "fecha": "03/11/1999",
     "genero": "Masculino", "telefono": "3157894561", "ciudad": "Cartagena",
     "direccion": "Carrera 10 # 20-35", "intereses": ["Tecnología"], "satisfaccion": 7,
     "observaciones": "Prefiere que lo contacten por WhatsApp"}
]

usuarios = []                                                          # 1. arreglo de usuarios
usuarios.append(Usuario("Administrador", "admin@tienda.com", "admin123"))   # APPEND

objetos_clientes = []
for datos in clientes_ejemplo:                                         # 2. diccionario -> objeto
    objetos_clientes.append(crear_cliente(datos))
usuarios.extend(objetos_clientes)                                      # EXTEND: agrega varios

objRegistro = RegistroUsuario(usuarios)                                # 3. objeto del registro
objInicio = InicioSesion(usuarios, objRegistro)                        # 4. objeto del login

auxVentana = objInicio.iniciar_ventana()                               # 5. se crea la ventana
objInicio.iniciar_preguntas()                                          # 6. preguntas y botones

auxVentana.mainloop()                                                  # 7. mantiene la ventana abierta
