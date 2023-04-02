from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import *
import sqlite3





###Interfaz###

root  = Tk()
root.title("Control de Gastos")
root.geometry("572x380")
root.resizable(False,False)
root.iconbitmap("icono.ico")
#cal = Calendar(root, selectmode = 'day')

###Base de datos###

id = StringVar()
fecha = StringVar()
gasto = StringVar()
importe = DoubleVar()
categoria = StringVar()
tipo = StringVar(None,"Gasto")


def conexion_base():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        mi_cursor.execute('''
        CREATE TABLE gastos(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FECHA VARCHAR(50) NOT NULL,
        GASTO VARCHAR(50) NOT NULL,
        IMPORTE FLOAT NOT NULL,
        CATEGORIA VARCHAR(50) NOT NULL,
        TIPO VARCHAR(50) NOT NULL
        )''')
        print("Base creada correctamente")
    except :
        print("Conexión realizada correctamente")


def eliminarBBDD():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()
    if messagebox.askyesno("ADVERTENCIA", message="Los datos se perderán permanentemente. ¿Desea continuar?"):
        mi_cursor.execute("DROP TABLE gastos")
        messagebox.showinfo(message="Base eliminada correctamente", title="ADVERTENCIA")
    mostrar()

def salirAplicacion():
    if messagebox.askyesno("Salir", "¿Salir de la aplicación?"):
        root.quit()
    
    limpiarCampos()
    mostrar()

def limpiarCampos():
    id.set("")
    fecha.set("")
    gasto.set("")
    importe.set("")
    categoria.set("")
    tipo.set("Gasto")



def crear():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        datos = fecha.get(), gasto.get(), importe.get(), categoria.get(), tipo.get()
        mi_cursor.execute("INSERT INTO gastos VALUES(NULL,?,?,?,?,?)", (datos))
        mi_conexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Error al crear el registro. Verificar conexión con la base")
    limpiarCampos()
    mostrar()

def mostrar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        mi_cursor.execute("SELECT * FROM gastos")
        for row in mi_cursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
    except:
        pass 
###TABLA###

sb = Scrollbar(root)  

sb.pack(side=RIGHT, fill=Y, pady=(140,0))
sb.config()

style=ttk.Style()
style.theme_use('clam')

tree = ttk.Treeview(height=11, columns=('#0', '#1', '#2', '#3', '#4'), yscrollcommand = sb.set)

tree.column('#0',anchor=CENTER, stretch=NO, width=50)
tree.heading('#0', text="ID") 
tree.column('#1',anchor=CENTER, stretch=NO, width=100)
tree.heading('#1', text="Fecha")
tree.column('#2',anchor=CENTER, stretch=NO, width=100)
tree.heading('#2', text="Gasto")
tree.column('#3',anchor=CENTER, stretch=NO, width=100)
tree.heading('#3', text="Importe")
tree.column('#4',anchor=CENTER, stretch=NO, width=100)
tree.heading('#4', text="Categoría")
tree.column('#5',anchor=CENTER, stretch=NO, width=100)
tree.heading('#5', text="Tipo")

tree.place(x=1, y=127)
sb.config( command = tree.yview )  

def seleccionarUsandoClick(event):
    item=tree.identify('item', event.x, event.y)
    id.set(tree.item(item,"text"))
    fecha.set(tree.item(item,"values")[0])
    gasto.set(tree.item(item,"values")[1])
    importe.set(tree.item(item,"values")[2])
    categoria.set(tree.item(item,"values")[3])
    tipo.set(tree.item(item,"values")[4])

tree.bind("<Double-1>", seleccionarUsandoClick)



def actualizar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        datos = fecha.get(), gasto.get(), importe.get(), categoria.get(), tipo.get()
        mi_cursor.execute("UPDATE gastos SET FECHA=?, GASTO=?,IMPORTE=?,CATEGORIA=?,TIPO=? WHERE ID="+id.get(), (datos))
        mi_conexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Error al actualizar el registro.")
    limpiarCampos()
    mostrar()


def borrar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        if messagebox.askyesno(message="¿Eliminar registro?", title="ADVERTENCIA"):
            mi_cursor.execute("DELETE FROM gastos WHERE ID="+id.get())
            mi_conexion.commit()
    except:
         messagebox.showwarning("ADVERTENCIA", "Error al borrar el registro.")
         print(id.get())
    limpiarCampos()
    mostrar()

####Calendario####

def elegir_fecha(event):
    global cal, ventana_fecha
    ventana_fecha = Toplevel()
    ventana_fecha.grab_set()
    ventana_fecha.title("Elegir fecha")
    ventana_fecha.geometry('250x220+590+370')
    cal = Calendar(ventana_fecha, selectmode="day", date_pattern="dd/mm/yyyy")
    cal.place(x=0,y=0)

    submit_btn = Button(ventana_fecha, text="Guardar", command=obtener_fecha)
    submit_btn.place(x=80,y=190)

def obtener_fecha():
    e2.delete(0,END)
    e2.insert(0,cal.get_date())
    ventana_fecha.destroy()

###Interfaz###

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexion_base)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Limpiar campos", command=limpiarCampos)
menubasedat.add_separator()
menubasedat.add_command(label="Salir", command=salirAplicacion)

menubar.add_cascade(label="Inicio", menu=menubasedat)

e1 = Entry(root, textvariable=id)


l2 = Label(root, text="Fecha")
l2.place(x=25, y=10)
e2 = Entry(root, textvariable=fecha, width=50)
e2.place(x=75, y=10)
#e2.insert(0, "dd/mm/yyyy")
e2.bind("<1>", elegir_fecha)

l3 = Label(root, text="Gasto")
l3.place(x=215, y=10)
e3 = Entry(root, textvariable=gasto, width=25)
e3.place(x=250, y=10)

l4 = Label(root, text="Importe")
l4.place(x=25, y=50)
e4 = Entry(root, textvariable=importe, width=20)
e4.place(x=75, y=50)

categorias = ["Comestibles", 
              "Entretenimiento",
              "Higiene",
              "Servicios",
              "Educación",
              "Medicina",
              "Otros"]

l5 = Label(root, text="Categoría")
l5.place(x=195, y=50)
e5 = ttk.Combobox(root, value=categorias, textvariable=categoria, state="readonly", width=25)
e5.place(x=250, y=50)


l6 = Label(root, text="Tipo")
l6.place(x=25, y=90)
e61 = Radiobutton(root, text="Ingreso", variable=tipo, value="Ingreso")
e61.place(x=75, y=90)
e62 = Radiobutton(root, text="Gasto", variable=tipo, value="Gasto")
e62.place(x=150, y=90)
# e6 = Entry(root, textvariable=tipo, width=25)
# e6.place(x=75, y=90)



root.config(menu=menubar)

b1 = Button(root, text="Crear Registro",bg="green", fg="white", command=crear, width=15)
b1.place(x=435, y=10)
b2 = Button(root, text="Modificar Registro", bg="blue", fg="white", command=actualizar,width=15)
b2.place(x=435, y=50)
b3 = Button(root, text="Actualizar Lista", command=mostrar)
b3.place(x=280, y=85)
b4 = Button(root, text="Eliminar Registro", bg="red", fg="white", command=borrar, width=15)
b4.place(x=435, y=90)

conexion_base()
mostrar()
root.mainloop()