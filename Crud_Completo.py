import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_hack"
)

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("CRUD Clientes")
ventana.configure(bg="silver")

# Estilo de los widgets
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# Crear el Frame para los botones
frame_botones = ttk.Frame(ventana)
frame_botones.pack(pady=10)

# Estilo de los widgets
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), foreground="black", background="red")  # Color de los botones


# Función para mostrar los datos de la tabla "clientes"
def mostrar_datos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    datos = cursor.fetchall()
    tree.delete(*tree.get_children())  # Limpiar los datos anteriores
    for dato in datos:
        tree.insert("", tk.END, values=dato)


# Función para buscar un cliente por ID
def buscar_cliente():
    id_cliente = entry_buscar.get()
    if id_cliente:
        cursor = conexion.cursor()
        consulta = "SELECT * FROM clientes WHERE ID=%s"
        valor = (id_cliente,)
        cursor.execute(consulta, valor)
        datos = cursor.fetchone()
        if datos:
            tree.delete(*tree.get_children())  # Limpiar los datos anteriores
            tree.insert("", tk.END, values=datos)
        else:
            messagebox.showinfo("Información", "No se encontró ningún cliente con el ID proporcionado")
    else:
        messagebox.showinfo("Información", "Por favor, ingrese un ID de cliente")


# --------------------------------------------------------------------------------------------------------
# Función para agregar un cliente
def agregar_cliente():
    # Crear una ventana adicional para agregar un cliente
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Cliente")

    def insertar():
        # Obtener los valores de los campos de entrada
        nombre_cliente = entry_nombre.get()
        fecha_cliente = entry_fecha.get()
        direccion_cliente = entry_direccion.get()
        localidad_cliente = entry_localidad.get()
        telefono_cliente = entry_telefono.get()
        correo_cliente = entry_correo.get()
        fecha_alta_cliente = entry_fecha_alta.get()
        grupo_cliente = entry_grupo.get()

        # Validar que todos los campos estén completos
        if nombre_cliente and fecha_cliente and direccion_cliente and localidad_cliente and telefono_cliente and correo_cliente and fecha_alta_cliente and grupo_cliente:
            # Insertar los datos del cliente en la base de datos
            cursor = conexion.cursor()
            consulta = "INSERT INTO clientes (Nombre, Fecha, Dirección, Localidad, Teléfono, Correo, Fecha_alta, GRUPO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                nombre_cliente, fecha_cliente, direccion_cliente, localidad_cliente, telefono_cliente, correo_cliente,
                fecha_alta_cliente, grupo_cliente)
            cursor.execute(consulta, valores)
            conexion.commit()

            # Cerrar la ventana de agregar
            ventana_agregar.destroy()

            # Actualizar los datos en el Treeview
            mostrar_datos()
        else:
            messagebox.showinfo("Información", "Por favor, complete todos los campos")

    # Crear los campos de entrada y etiquetas para agregar un cliente
    label_nombre = ttk.Label(ventana_agregar, text="Nombre:")
    label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="E")
    entry_nombre = ttk.Entry(ventana_agregar)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    label_fecha = ttk.Label(ventana_agregar, text="Fecha:")
    label_fecha.grid(row=1, column=0, padx=5, pady=5, sticky="E")
    entry_fecha = ttk.Entry(ventana_agregar)
    entry_fecha.grid(row=1, column=1, padx=5, pady=5)

    label_direccion = ttk.Label(ventana_agregar, text="Dirección:")
    label_direccion.grid(row=2, column=0, padx=5, pady=5, sticky="E")
    entry_direccion = ttk.Entry(ventana_agregar)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5)

    label_localidad = ttk.Label(ventana_agregar, text="Localidad:")
    label_localidad.grid(row=3, column=0, padx=5, pady=5, sticky="E")
    entry_localidad = ttk.Entry(ventana_agregar)
    entry_localidad.grid(row=3, column=1, padx=5, pady=5)

    label_telefono = ttk.Label(ventana_agregar, text="Teléfono:")
    label_telefono.grid(row=4, column=0, padx=5, pady=5, sticky="E")
    entry_telefono = ttk.Entry(ventana_agregar)
    entry_telefono.grid(row=4, column=1, padx=5, pady=5)

    label_correo = ttk.Label(ventana_agregar, text="Correo:")
    label_correo.grid(row=5, column=0, padx=5, pady=5, sticky="E")
    entry_correo = ttk.Entry(ventana_agregar)
    entry_correo.grid(row=5, column=1, padx=5, pady=5)

    label_fecha_alta = ttk.Label(ventana_agregar, text="Fecha Alta:")
    label_fecha_alta.grid(row=6, column=0, padx=5, pady=5, sticky="E")
    entry_fecha_alta = ttk.Entry(ventana_agregar)
    entry_fecha_alta.grid(row=6, column=1, padx=5, pady=5)

    label_grupo = ttk.Label(ventana_agregar, text="Grupo:")
    label_grupo.grid(row=7, column=0, padx=5, pady=5, sticky="E")
    entry_grupo = ttk.Entry(ventana_agregar)
    entry_grupo.grid(row=7, column=1, padx=5, pady=5)

    # Crear el botón para agregar un cliente
    button_insertar = ttk.Button(ventana_agregar, text="Agregar", command=insertar)
    button_insertar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


# Función para actualizar un cliente
def actualizar_cliente():
    # Obtener el cliente seleccionado en el Treeview
    item_seleccionado = tree.focus()
    if item_seleccionado:
        valores_seleccionados = tree.item(item_seleccionado)["values"]

        # Crear una ventana adicional para actualizar el cliente
        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Cliente")

        def actualizar():
            # Obtener los valores de los campos de entrada
            nombre_cliente = entry_nombre.get()
            fecha_cliente = entry_fecha.get()
            direccion_cliente = entry_direccion.get()
            localidad_cliente = entry_localidad.get()
            telefono_cliente = entry_telefono.get()
            correo_cliente = entry_correo.get()
            fecha_alta_cliente = entry_fecha_alta.get()
            grupo_cliente = entry_grupo.get()

            # Validar que todos los campos estén completos
            if nombre_cliente and fecha_cliente and direccion_cliente and localidad_cliente and telefono_cliente and correo_cliente and fecha_alta_cliente and grupo_cliente:
                # Actualizar los datos del cliente en la base de datos
                cursor = conexion.cursor()
                consulta = "UPDATE clientes SET Nombre=%s, Fecha=%s, Dirección=%s, Localidad=%s, Teléfono=%s, Correo=%s, Fecha_alta=%s, GRUPO=%s WHERE ID=%s"
                valores = (
                    nombre_cliente, fecha_cliente, direccion_cliente, localidad_cliente, telefono_cliente,
                    correo_cliente, fecha_alta_cliente, grupo_cliente, valores_seleccionados[0])
                cursor.execute(consulta, valores)
                conexion.commit()

                # Cerrar la ventana de actualizar
                ventana_actualizar.destroy()

                # Actualizar los datos en el Treeview
                mostrar_datos()
            else:
                messagebox.showinfo("Información", "Por favor, complete todos los campos")

        # Crear los campos de entrada y etiquetas para actualizar el cliente
        label_nombre = ttk.Label(ventana_actualizar, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        entry_nombre = ttk.Entry(ventana_actualizar)
        entry_nombre.insert(tk.END, valores_seleccionados[1])
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        label_fecha = ttk.Label(ventana_actualizar, text="Fecha:")
        label_fecha.grid(row=1, column=0, padx=5, pady=5, sticky="E")
        entry_fecha = ttk.Entry(ventana_actualizar)
        entry_fecha.insert(tk.END, valores_seleccionados[2])
        entry_fecha.grid(row=1, column=1, padx=5, pady=5)

        label_direccion = ttk.Label(ventana_actualizar, text="Dirección:")
        label_direccion.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        entry_direccion = ttk.Entry(ventana_actualizar)
        entry_direccion.insert(tk.END, valores_seleccionados[3])
        entry_direccion.grid(row=2, column=1, padx=5, pady=5)

        label_localidad = ttk.Label(ventana_actualizar, text="Localidad:")
        label_localidad.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        entry_localidad = ttk.Entry(ventana_actualizar)
        entry_localidad.insert(tk.END, valores_seleccionados[4])
        entry_localidad.grid(row=3, column=1, padx=5, pady=5)

        label_telefono = ttk.Label(ventana_actualizar, text="Teléfono:")
        label_telefono.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        entry_telefono = ttk.Entry(ventana_actualizar)
        entry_telefono.insert(tk.END, valores_seleccionados[5])
        entry_telefono.grid(row=4, column=1, padx=5, pady=5)

        label_correo = ttk.Label(ventana_actualizar, text="Correo:")
        label_correo.grid(row=5, column=0, padx=5, pady=5, sticky="E")
        entry_correo = ttk.Entry(ventana_actualizar)
        entry_correo.insert(tk.END, valores_seleccionados[6])
        entry_correo.grid(row=5, column=1, padx=5, pady=5)

        label_fecha_alta = ttk.Label(ventana_actualizar, text="Fecha Alta:")
        label_fecha_alta.grid(row=6, column=0, padx=5, pady=5, sticky="E")
        entry_fecha_alta = ttk.Entry(ventana_actualizar)
        entry_fecha_alta.insert(tk.END, valores_seleccionados[7])
        entry_fecha_alta.grid(row=6, column=1, padx=5, pady=5)

        label_grupo = ttk.Label(ventana_actualizar, text="Grupo:")
        label_grupo.grid(row=7, column=0, padx=5, pady=5, sticky="E")
        entry_grupo = ttk.Entry(ventana_actualizar)
        entry_grupo.insert(tk.END, valores_seleccionados[8])
        entry_grupo.grid(row=7, column=1, padx=5, pady=5)

        # Crear el botón para actualizar el cliente
        button_actualizar = ttk.Button(ventana_actualizar, text="Actualizar", command=actualizar)
        button_actualizar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


# Función para eliminar un cliente
def eliminar_cliente():
    # Obtener el cliente seleccionado en el Treeview
    item_seleccionado = tree.focus()
    if item_seleccionado:
        valores_seleccionados = tree.item(item_seleccionado)["values"]

        # Mostrar un mensaje de confirmación antes de eliminar el cliente
        respuesta = messagebox.askyesno("Confirmación", f"¿Está seguro de eliminar al cliente con ID: {valores_seleccionados[0]}?")
        if respuesta:
            # Eliminar el cliente de la base de datos
            cursor = conexion.cursor()
            consulta = "DELETE FROM clientes WHERE ID=%s"
            valor = (valores_seleccionados[0],)
            cursor.execute(consulta, valor)
            conexion.commit()

            # Actualizar los datos en el Treeview
            mostrar_datos()
    else:
        messagebox.showinfo("Información", "Por favor, seleccione un cliente")


# Crear el botón para mostrar los datos
button_mostrar = ttk.Button(frame_botones, text="Mostrar Datos", command=mostrar_datos)
button_mostrar.grid(row=0, column=0, padx=5, pady=5)

# Crear el campo de entrada y el botón para buscar un cliente por ID
label_buscar = ttk.Label(frame_botones, text="Buscar por ID:")
label_buscar.grid(row=0, column=1, padx=5, pady=5, sticky="E")
entry_buscar = ttk.Entry(frame_botones)
entry_buscar.grid(row=0, column=2, padx=5, pady=5)
button_buscar = ttk.Button(frame_botones, text="Buscar", command=buscar_cliente)
button_buscar.grid(row=0, column=3, padx=5, pady=5)

# Crear el botón para agregar un cliente
button_agregar = ttk.Button(frame_botones, text="Agregar Cliente", command=agregar_cliente)
button_agregar.grid(row=0, column=4, padx=5, pady=5)

# Crear el Treeview para mostrar los datos
tree = ttk.Treeview(ventana, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings")
tree.pack(pady=10)

# Configurar las columnas del Treeview
tree.heading(1, text="ID")
tree.heading(2, text="Nombre")
tree.heading(3, text="Fecha")
tree.heading(4, text="Dirección")
tree.heading(5, text="Localidad")
tree.heading(6, text="Teléfono")
tree.heading(7, text="Correo")
tree.heading(8, text="Fecha Alta")
tree.column(1, width=50)
tree.column(2, width=200)
tree.column(3, width=100)
tree.column(4, width=200)
tree.column(5, width=100)
tree.column(6, width=100)
tree.column(7, width=200)
tree.column(8, width=100)

# Configurar el scrollbar para el Treeview
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Crear el botón para actualizar un cliente
button_actualizar = ttk.Button(frame_botones, text="Actualizar Cliente", command=actualizar_cliente)
button_actualizar.grid(row=0, column=5, padx=5, pady=5)

# Crear el botón para eliminar un cliente
button_eliminar = ttk.Button(frame_botones, text="Eliminar Cliente", command=eliminar_cliente)
button_eliminar.grid(row=0, column=6, padx=5, pady=5)

# Mostrar los datos al iniciar la aplicación
mostrar_datos()

# Ejecutar la aplicación
ventana.mainloop()
