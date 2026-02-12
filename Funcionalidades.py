#Importaciones necesarias
from datetime import datetime
import sqlite3
from tkinter import *
import tkinter as tk
import baseDeDatos as bd
from tkinter import messagebox as mb
from tkinter import ttk
import pandas as pd

 #Clase con todas las funcionalidades
class Funcionalidades():
    
    #Metodo init que se conecta a la base de datos
    def __init__(self):
        self.conexion = sqlite3.connect("libreria.db")

    ##Importaciones necesarias
from datetime import datetime
import sqlite3
from tkinter import *
import tkinter as tk
import baseDeDatos as bd
from tkinter import messagebox as mb
from tkinter import ttk
import pandas as pd

 #Clase con todas las funcionalidades
class Funcionalidades():
    
    # Establece conexión con la base de datos SQLite
    # Si no existe el archivo, lo crea
    def __init__(self):
        self.conexion = sqlite3.connect("libreria.db")

    # Variable de clase que almacenará la ventana de edición
    # Se usa para poder actualizarla dinámicamente 
    ventana_editar = None

    #Crear subventana hija modal
    def crear_subventana(parent):
        subventana=Toplevel(parent)
        subventana.transient(parent) # Asociada a la ventana principal
        subventana.grab_set() # Bloquea interacción con ventana padre
        return subventana

    # Centrar una subventana
    def centrarSubventana(subventana):
        subventana.update()
        # Ancho y alto de la ventana
        w=subventana.winfo_width()
        h=subventana.winfo_height()
        # Ancho y alto de la pantalla
        ws=subventana.winfo_screenwidth()
        hs=subventana.winfo_screenheight()
        # Cálculo de coordenadas centradas
        x=int(ws/2 - w/2)
        y=int(hs/2 - h/2)
        # Aplica la nueva geometría
        subventana.geometry(f'{w}x{h}+{x}+{y}')

    # Crear Treeview con columnas
    def indices(parent):
        """
        Crea un Treeview con las columnas del catálogo.
        Devuelve el objeto para poder insertar registros.
        """
        treeview=ttk.Treeview(parent)
        # Definición de columnas
        treeview['columns']=('id','Nombre','Autor','Categoria','Fecha')
        # Ajuste del layout
        treeview.pack(side=LEFT, fill='both',expand=True)
        # Configuración columna fantasma (#0)
        treeview.column('#0', width=50, stretch=NO)
        treeview.heading('#0', text='')
        # Configuración individual de cada columna
        treeview.column('id', anchor=CENTER, width=0, stretch=NO)
        treeview.heading('id', text='ID', anchor=CENTER)
        treeview.column('Nombre', anchor=CENTER, width=100, stretch=NO)
        treeview.heading('Nombre', text='Nombre', anchor=CENTER)
        treeview.column('Autor', anchor=CENTER, width=100, stretch=NO)
        treeview.heading('Autor', text='Autor', anchor=CENTER)
        treeview.column('Categoria', anchor=CENTER, width=100, stretch=NO)
        treeview.heading('Categoria', text='Categoria', anchor=CENTER)
        treeview.column('Fecha', anchor=CENTER, width=100, stretch=NO)
        treeview.heading('Fecha', text='Fecha', anchor=CENTER)
        return treeview

    # Ajustar tamaño de fuente dinámico
    def ajustarFontSize(root, fuente,event=None):
        window_width = event.width if event else root.winfo_width()
        new_size = 10 + int(window_width * 0.01)
        fuente.configure(size=new_size)

    # Añadir barra de desplazamiento
    def añadir_scroll(subventana,treeview):
        scrollbar=Scrollbar(subventana, orient=VERTICAL, command=treeview.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand']=scrollbar.set
        
    # Crear DataFrame con datos BD
    def dataframe():
        try:
            lista=bd.mostrar_items()
             # Crear DataFrame vacío con columnas definidas
            df=pd.DataFrame((),columns=['Nombre','Autor','Categoria','Fecha'])
            # Insertar cada elemento en el DataFrame
            for i, elemento in enumerate(lista):
                print(elemento)
                df.loc[i,'Nombre']=elemento[1]
                df.loc[i,'Autor']=elemento[2]
                df.loc[i,'Categoria']=elemento[3]
                df.loc[i,'Fecha']=elemento[4]
                ultimo=i # Guardar último índice usado
            print(df)
            return ultimo,df
        except Exception as e:
            mb.showwarning(title='Error al crear el DataFrame',message=e)
    
    # Guardar datos en fichero CSV
    def fichero(df,posicion,nombre,autor,categoria,fecha):
        """
        Actualiza el DataFrame en una posición concreta
        y lo exporta como fichero CSV.
        """
        try:
            df.loc[posicion,'Nombre']=nombre
            df.loc[posicion,'Autor']=autor
            df.loc[posicion,'Categoria']=categoria
            df.loc[posicion,'Fecha']=fecha
            # Guarda el archivo sin incluir índice
            df.to_csv('fichero.csv', index=False)
            print(df)
        except Exception as e:
            mb.showwarning(title='Error al crear el fichero',message=e)

    # Función principal para enviar datos
    # (añadir, actualizar o buscar)
    def enviardatos(subventana,nombre,autor,categoria,fecha,actualizar,id=None):
        """
        Función central que controla:
        - Añadir registros
        - Editar registros
        - Buscar registros

        actualizar:
        0 → Añadir
        1 → Editar
        2 → Buscar
        """
        try:
            # Obtener valores desde los Entry
            nombre1=nombre.get()
            autor1=autor.get()
            categoria1=categoria.get()
            fecha1=fecha.get().strip()
            posicion,df=Funcionalidades.dataframe()
            # MODO BUSCAR
            if actualizar==2:
                id_lista=bd.buscar_item(nombre1,autor1,categoria1,fecha1)
                # Si hay un solo resultado
                if len(id_lista)==1:
                    for (id) in id_lista:
                        id=id[0]
                        Funcionalidades.mostrar_item(id, subventana)
                # Si hay varios resultados
                elif len(id_lista)>1:
                    lista=list()
                    for ids in id_lista:
                        lista.append(ids[0])
                    Funcionalidades.mostrar_items(lista,subventana)
                # Si no hay resultados
                else:
                    mb.showinfo("Buscar", "No se encontraron resultados")
            # MODO AÑADIR / EDITAR
            else:
                # Verifica que ningún campo esté vacío
                if not (nombre1 and autor1 and categoria1 and fecha1):
                    mb.showerror("Error", "Campos incompletos.")
                    return
                if (nombre1!="") & (autor1!="") & (categoria1!="") & (fecha1!=""):
                    try:
                        # Validar formato de fecha
                        datetime.strptime(fecha1, "%Y-%m-%d")
                         # AÑADIR
                        if actualizar==0:
                            mb.showinfo('Libro: ', f'El libro {nombre1} del autor {autor1} ha sido añadido correctamente.')
                            bd.añadir_item(nombre1,autor1,categoria1,fecha1)
                            posicion+=1
                            Funcionalidades.fichero(df,posicion,nombre1,autor1,categoria1,fecha1)
                        # EDITAR
                        elif actualizar==1:
                            mb.showinfo('Libro: ', f'El libro {nombre1} del autor {autor1} ha sido actualizado correctamente.')
                            bd.modificar_item(id,nombre1,autor1,categoria1,fecha1)
                            id=int(id)
                            Funcionalidades.fichero(df,id,nombre1,autor1,categoria1,fecha1)
                            Funcionalidades.editar_items(parent=Funcionalidades.ventana_editar.master, subventana=Funcionalidades.ventana_editar)
                            subventana.destroy()
                    except ValueError:
                        mb.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
                
        except Exception as e:
            mb.showwarning(title='Error al crear al enviar los datos',message=e)    

    # - mostrar_items → Muestra varios registros     
    def mostrar_items(ids,parent,subventana=None):
        """
        Muestra varios registros de la base de datos en una ventana secundaria.

        Parámetros:
        - ids: lista de IDs de los registros que queremos mostrar
        - parent: ventana principal sobre la que se crea la subventana
        - subventana: ventana secundaria opcional (si ya existe, se reutiliza)
        """
        try:
            # Si no se pasó una ventana secundaria, se crea una nueva
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            # Centra la subventana
            Funcionalidades.centrarSubventana(subventana)
            subventana.geometry("500x500")
            # Crea el Treeview (tabla) dentro de la subventana
            treeview=Funcionalidades.indices(subventana)
            # Añade scroll vertical a la tabla
            Funcionalidades.añadir_scroll(subventana,treeview)
            # Obtiene los datos de varios items desde la base de datos
            lista=bd.mostrar_varios_items(ids)
            # Inserta cada registro en el Treeview
            for elemento in lista:
                treeview.insert(parent='',index='end',values=elemento)
        except Exception as e:
            # Muestra advertencia si ocurre algún error
            mb.showwarning(title='Error al mostrar datos',message=e)      

    # - mostrar_item → Muestra un solo registro        
    def mostrar_item(id,parent,subventana=None):
        """
        Muestra un solo registro en un Treeview.

        Parámetros:
        - id: ID del registro a mostrar
        - parent: ventana principal
        - subventana: ventana secundaria opcional
        """
        try:
            # Si no se pasó una ventana secundaria, se crea una nueva
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            # Centra la subventana
            Funcionalidades.centrarSubventana(subventana)
            subventana.geometry("500x500")
            # Crea el Treeview (tabla) dentro de la subventana
            treeview=Funcionalidades.indices(subventana)
            # Recupera el registro desde la BD
            lista=bd.mostrar_item(id)
            # Inserta los datos en el Treeview
            for elemento in lista:
                treeview.insert(parent='',index='end',values=elemento)
        except Exception as e:
            mb.showwarning(title='Error al mostrar el dato',message=e)

    # - añadirItem → Ventana para añadir libro
    def añadirItem(parent,subventana=None):
        """
        Crea una ventana para añadir un nuevo registro de libro.
        Se crean campos de texto (Nombre, Autor, Categoria, Fecha)
        y un botón que llama a la función `enviardatos` para guardarlo.
        """
        try:
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            # Frame principal para organizar los widgets
            frame1=Frame(subventana)
            frame1.pack()
            # Campo Nombre
            Label(frame1, text='Nombre: ').grid(row=0, column=0)
            nombre=Entry(frame1)
            nombre.grid(row=0, column=1)
            # Campo Autor
            Label(frame1, text='Autor: ').grid(row=1, column=0)
            autor=Entry(frame1)
            autor.grid(row=1, column=1)
            # Campo Categoria
            Label(frame1, text='Categoria: ').grid(row=2, column=0)
            categoria=Entry(frame1)
            categoria.grid(row=2, column=1)
            # Campo Fecha
            Label(frame1, text='Fecha: ').grid(row=3, column=0)
            fecha=Entry(frame1)
            fecha.grid(row=3, column=1)
            # Variable de control: 0 = añadir
            actualizar=0
            # Botón para añadir el registro
            boton=Button(frame1, text='Añadir', command=lambda:Funcionalidades.enviardatos(subventana,nombre,autor,categoria,fecha,actualizar))
            boton.grid(row=4,column=1)
        except Exception as e:
            mb.showwarning(title='Error al añadir los datos',message=e)

    #- mostrar_catalogo → Muestra todo el catálogo
    def mostrar_catalogo(parent):
        """
        Abre una ventana y muestra todos los registros de la BD
        en un Treeview con scroll.
        """
        try:
            subventana=Funcionalidades.crear_subventana(parent)
            subventana.geometry("500x500")
            Funcionalidades.centrarSubventana(subventana)
            treeview=Funcionalidades.indices(subventana)
            Funcionalidades.añadir_scroll(subventana,treeview)
            # Recupera todos los registros de la BD
            lista=bd.mostrar_items()
            # Inserta todos los registros en la tabla
            for  registro in lista:
                treeview.insert(parent='',index='end',values=registro)
        except Exception as e:
            mb.showwarning(title='Error al mostrar el catalogo',message=e)

    
    def abrir_editar_items(parent):
            """
            Almacena la ventana de edición en la variable de clase
            para poder actualizarla y reutilizarla.
            """
            Funcionalidades.ventana_editar = Funcionalidades.editar_items(parent)

    #- editar_items → Permite editar con doble clic
    def editar_items(parent, subventana=None):
        """
        Crea una ventana con un Treeview editable.
        Permite hacer doble clic sobre un registro para abrir
        un formulario de edición.
        """
        try:
            # Crear subventana si no existe
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                subventana.geometry("500x500")
                Funcionalidades.centrarSubventana(subventana)
            # Limpiar cualquier widget existente
            for widget in subventana.winfo_children():
                widget.destroy()
            # Treeview con registros
            treeview=Funcionalidades.indices(subventana)
            Funcionalidades.añadir_scroll(subventana,treeview)
            lista=bd.mostrar_items()
            # Insertar los registros
            for  registro in lista:
                treeview.insert(parent='',index='end',values=registro) 
            # Función que se ejecuta al hacer doble clic en un registro     
            def editar_item(event):
                item = treeview.identify_row(event.y)
                valores=treeview.item(item,'values')
                nueva_ventana=Funcionalidades.crear_subventana(subventana)
                Funcionalidades.centrarSubventana(nueva_ventana)
                # Función que habilita el botón de guardar si hay cambios
                def cambios(*args):
                    boton.config(state='normal')
                # Extraer ID del registro
                id=valores[0]
                # Crear campos con los valores actuales para editar
                Label(nueva_ventana, text='Nombre: ').grid(row=0, column=0)
                nombre1=tk.StringVar(master=nueva_ventana,value=valores[1])
                nombre=Entry(nueva_ventana,textvariable=nombre1)
                nombre.grid(row=0, column=1)
                nombre1.trace_add("write",cambios)
                autor1=tk.StringVar(master=nueva_ventana,value=valores[2])
                Label(nueva_ventana, text='Autor: ').grid(row=1, column=0)
                autor=Entry(nueva_ventana,textvariable=autor1)
                autor.grid(row=1, column=1)
                autor1.trace_add("write",cambios)
                categoria1=tk.StringVar(master=nueva_ventana,value=valores[3])
                Label(nueva_ventana, text='Categoria: ').grid(row=2, column=0)
                categoria=Entry(nueva_ventana,textvariable=categoria1)
                categoria.grid(row=2, column=1)
                categoria1.trace_add("write",cambios)
                fecha1=tk.StringVar(master=nueva_ventana,value=valores[4])
                Label(nueva_ventana, text='Fecha: ').grid(row=3, column=0)
                fecha=Entry(nueva_ventana,textvariable=fecha1)
                fecha.grid(row=3, column=1)
                fecha1.trace_add("write",cambios)
                actualizar=1 # Modo edición
                # Botón para guardar cambios (inicialmente deshabilitado)
                def guardar():
                    Funcionalidades.enviardatos(nueva_ventana,nombre1,autor1,categoria1,fecha1,actualizar,id)
                boton=Button(nueva_ventana,text='Guardar',command=guardar,state='disabled')
                boton.grid(row=4,column=1)
            # Asociar doble clic a la función editar_item      
            treeview.bind("<Double-1>", editar_item)
            return subventana
        except Exception as e:
            mb.showwarning(title='Error al editar registro',message=e)

     # - buscar_item → Ventana para buscar registros
    def buscar_item(parent):
        """
        Crea una ventana con campos de búsqueda.
        Permite buscar por Nombre, Autor, Categoria y Fecha.
        Al hacer clic en "Buscar Item" llama a enviardatos() en modo búsqueda.
        """
        try:
            subventana=Funcionalidades.crear_subventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            frame1=Frame(subventana)
            frame1.pack()
            Boton = None # placeholder para habilitar/deshabilitar botones
            def cambios(*args):
                nonlocal Boton
            # Campos de búsqueda
            Label(frame1, text='Nombre: ').grid(row=0, column=0)
            nombre1=tk.StringVar()
            nombre1.trace_add("write",cambios)
            nombre=Entry(frame1,textvariable=nombre1)
            nombre.grid(row=0, column=1)        
            Label(frame1, text='Autor: ').grid(row=1, column=0)
            autor1=tk.StringVar()
            autor1.trace_add("write",cambios)
            autor=Entry(frame1,textvariable=autor1)
            autor.grid(row=1, column=1)
            Label(frame1, text='Categoria: ').grid(row=2, column=0)
            categoria1=tk.StringVar()
            categoria1.trace_add("write",cambios)
            categoria=Entry(frame1,textvariable=categoria1)
            categoria.grid(row=2, column=1)        
            Label(frame1, text='Fecha: ').grid(row=3, column=0)
            fecha1=tk.StringVar()
            fecha1.trace_add("write",cambios)
            fecha=Entry(frame1,textvariable=fecha1)
            fecha.grid(row=3, column=1)
            actualizar=2 # Modo búsqueda
            # Botón para ejecutar la búsqueda
            tk.Button(frame1, text="Buscar Item", command=lambda:Funcionalidades.enviardatos(subventana,nombre,autor,categoria,fecha,actualizar)).grid(row=4, column=0, pady=20)
        except Exception as e:
            mb.showwarning(title='Error al buscar registro',message=e)
        
        