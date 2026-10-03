# Tienda - Inicio de sesión y registro de clientes

Actividad semana 7: interfaces con widgets de Tkinter según la historia de usuario HU-AUT-001, hecho con POO.

**Estudiante:** Rosbely Contreras
## Cómo ejecutar

```
python principal.py
```

Usuarios de prueba:
- `admin@tienda.com` / `admin123` (Usuario)
- `laura@correo.com` / `laura123` (Cliente)
- `carlos@correo.com` / `carlos123` (Cliente)

## Archivos

- `principal.py`: código principal, crea los objetos y abre la ventana.
- `inicio_sesion.py`: clases `Persona`, `Usuario`, `FormularioBase` e `InicioSesion`.
- `registro_usuario.py`: clases `Cliente` y `RegistroUsuario`.

## Widgets usados

| Pregunta | Widget |
|---|---|
| Correo / usuario | Label + Entry |
| Contraseña | Label + Entry con `show="*"` |
| Mostrar contraseña / Recordar sesión | Checkbutton |
| Ingresar, Registrarse, Enviar, Limpiar, Salir | Button |
| Nombre, documento, teléfono, dirección | Label + Entry |
| Fecha de nacimiento | Entry guiado (dd/mm/aaaa) |
| Tipo de documento | Combobox |
| Género | Radiobutton |
| Intereses | Checkbutton |
| Ciudad | Listbox + Scrollbar |
| Nivel de satisfacción | Scale |
| Observaciones | Text |
| Mensajes | Label y messagebox |

## Pilares de la POO

1. **Abstracción:** `Persona` y `FormularioBase` son clases abstractas (`ABC`) con métodos abstractos.
2. **Encapsulamiento:** atributos privados como `self.__nombre`, `self.__contrasena` y el arreglo `self.__usuarios`. La contraseña solo se puede comparar con `verificar_contrasena()`.
3. **Herencia:** `Cliente` → `Usuario` → `Persona`, y `InicioSesion` y `RegistroUsuario` heredan de `FormularioBase`.
4. **Polimorfismo:** `mostrar_datos()` es distinto en `Usuario` y `Cliente`. `RegistroUsuario` sobrescribe `tomar_datos()` y `validar_campos()` del padre.

## Lo que usé de los talleres de clase

- **Arreglo de diccionarios:** en `principal.py` los clientes de ejemplo están en una lista de diccionarios (como el inventario de sillas), y `obtener_clientes()` devuelve los clientes como diccionarios.
- **Arreglo de duplas:** `self.campos` (pregunta de cada Entry), `campos_cliente` y `campos_resumen` (clave, texto) se recorren con `for clave, etiqueta in ...` para crear las preguntas y mostrar los datos.
- **Menús como diccionarios:** los botones salen de `self.menuBotones` y los informes de `self.menuInformes`, con el formato `opción -> (texto, función)`.
- **Métodos de listas:** `append()` para guardar un cliente, `extend()` para agregar los clientes de ejemplo, `count()` en clientes por ciudad, `sort()` en ordenar por nombre e `index()` en buscar por documento.
- **Informes:** total de clientes, promedio de satisfacción, clientes por ciudad, ordenar por nombre y buscar por documento.
