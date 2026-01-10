from datetime import datetime
from tkinter import *
import tkinter as tk
import baseDeDatos as bd
from tkinter import messagebox as mb
from tkinter import ttk
import csv
import pandas as pd

class Funcionalidades():
    
    ventana_editar = None

    def crear_subventana(parent):
        subventana=Toplevel(parent)
        subventana.transient(parent)
        subventana.grab_set()
        return subventana

    def centrarSubventana(subventana):
        subventana.update()
        w=subventana.winfo_width()
        h=subventana.winfo_height()
        ws=subventana.winfo_screenwidth()
        hs=subventana.winfo_screenheight()
        x=int(ws/2 - w/2)
        y=int(hs/2 - h/2)
        subventana.geometry(f'{w}x{h}+{x}+{y}')


    def indices(parent):
        treeview=ttk.Treeview(parent)
        treeview['columns']=('id','Nombre','Autor','Categoria','Fecha')
        treeview.pack(side=LEFT, fill='both',expand=True)
        treeview.column('#0', width=50, stretch=NO)
        treeview.heading('#0', text='')
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

    def ajustarFontSize(root, fuente,event=None):
        window_width = event.width if event else root.winfo_width()
        new_size = 10 + int(window_width * 0.01)
        fuente.configure(size=new_size)


    def añadir_scroll(subventana,treeview):
        scrollbar=Scrollbar(subventana, orient=VERTICAL, command=treeview.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand']=scrollbar.set
        

    def dataframe():
        try:
            lista=bd.mostrar_items()
            df=pd.DataFrame((),columns=['Nombre','Autor','Categoria','Fecha'])
            for i, elemento in enumerate(lista):
                print(elemento)
                df.loc[i,'Nombre']=elemento[1]
                df.loc[i,'Autor']=elemento[2]
                df.loc[i,'Categoria']=elemento[3]
                df.loc[i,'Fecha']=elemento[4]
                ultimo=i
            print(df)
            return ultimo,df
        except Exception as e:
            mb.showwarning(title='Error al crear el DataFrame',message=e)
            
    def fichero(df,posicion,nombre,autor,categoria,fecha):
        try:
            df.loc[posicion,'Nombre']=nombre
            df.loc[posicion,'Autor']=autor
            df.loc[posicion,'Categoria']=categoria
            df.loc[posicion,'Fecha']=fecha
            df.to_csv('fichero.csv', index=False)
            print(df)
        except Exception as e:
            mb.showwarning(title='Error al crear el fichero',message=e)

    def enviardatos(subventana,nombre,autor,categoria,fecha,actualizar,id=None):
        try:
            nombre1=nombre.get()
            autor1=autor.get()
            categoria1=categoria.get()
            fecha1=fecha.get().strip()
            posicion,df=Funcionalidades.dataframe()
            if actualizar==2:
                id_lista=bd.buscar_item(nombre1,autor1,categoria1,fecha1)
                if len(id_lista)==1:
                    for (id) in id_lista:
                        id=id[0]
                        Funcionalidades.mostrar_item(id, subventana)
                elif len(id_lista)>1:
                    lista=list()
                    for ids in id_lista:
                        lista.append(ids[0])
                    Funcionalidades.mostrar_items(lista,subventana)
                else:
                    mb.showinfo("Buscar", "No se encontraron resultados")
            else:
                if (nombre1!="") & (autor1!="") & (categoria1!="") & (fecha1!=""):
                    try:
                        datetime.strptime(fecha1, "%Y-%m-%d")
                        if actualizar==0:
                            mb.showinfo('Libro: ', f'El libro {nombre1} del autor {autor1} ha sido añadido correctamente.')
                            bd.añadir_item(nombre1,autor1,categoria1,fecha1)
                            posicion+=1
                            Funcionalidades.fichero(df,posicion,nombre1,autor1,categoria1,fecha1)
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

            
    def mostrar_items(ids,parent,subventana=None):
        try:
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            subventana.geometry("500x500")
            treeview=Funcionalidades.indices(subventana)
            Funcionalidades.añadir_scroll(subventana,treeview)
            lista=bd.mostrar_varios_items(ids)
            for elemento in lista:
                treeview.insert(parent='',index='end',values=elemento)
        except Exception as e:
            mb.showwarning(title='Error al mostrar datos',message=e)      
            
    def mostrar_item(id,parent,subventana=None):
        try:
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            subventana.geometry("500x500")
            treeview=Funcionalidades.indices(subventana)
            lista=bd.mostrar_item(id)
            for elemento in lista:
                treeview.insert(parent='',index='end',values=elemento)
        except Exception as e:
            mb.showwarning(title='Error al mostrar el dato',message=e)

    def añadirItem(parent,subventana=None):
        try:
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                Funcionalidades.centrarSubventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            frame1=Frame(subventana)
            frame1.pack()
            Label(frame1, text='Nombre: ').grid(row=0, column=0)
            nombre=Entry(frame1)
            nombre.grid(row=0, column=1)
            Label(frame1, text='Autor: ').grid(row=1, column=0)
            autor=Entry(frame1)
            autor.grid(row=1, column=1)
            Label(frame1, text='Categoria: ').grid(row=2, column=0)
            categoria=Entry(frame1)
            categoria.grid(row=2, column=1)
            Label(frame1, text='Fecha: ').grid(row=3, column=0)
            fecha=Entry(frame1)
            fecha.grid(row=3, column=1)
            actualizar=0
            boton=Button(frame1, text='Añadir', command=lambda:Funcionalidades.enviardatos(subventana,nombre,autor,categoria,fecha,actualizar))
            boton.grid(row=4,column=1)
        except Exception as e:
            mb.showwarning(title='Error al añadir los datos',message=e)



    def mostrar_catalogo(parent):
        try:
            subventana=Funcionalidades.crear_subventana(parent)
            subventana.geometry("500x500")
            Funcionalidades.centrarSubventana(subventana)
            treeview=Funcionalidades.indices(subventana)
            Funcionalidades.añadir_scroll(subventana,treeview)
            lista=bd.mostrar_items()
            for  registro in lista:
                treeview.insert(parent='',index='end',values=registro)
        except Exception as e:
            mb.showwarning(title='Error al mostrar el catalogo',message=e)

    def abrir_editar_items(parent):
            Funcionalidades.ventana_editar = Funcionalidades.editar_items(parent)


    def editar_items(parent, subventana=None):
        try:
            if subventana==None:
                subventana=Funcionalidades.crear_subventana(parent)
                subventana.geometry("500x500")
                Funcionalidades.centrarSubventana(subventana)
            for widget in subventana.winfo_children():
                widget.destroy()
            treeview=Funcionalidades.indices(subventana)
            Funcionalidades.añadir_scroll(subventana,treeview)
            lista=bd.mostrar_items()
            for  registro in lista:
                treeview.insert(parent='',index='end',values=registro)      
            def editar_item(event):
                item = treeview.identify_row(event.y)
                valores=treeview.item(item,'values')
                nueva_ventana=Funcionalidades.crear_subventana(subventana)
                Funcionalidades.centrarSubventana(nueva_ventana)
                def cambios(*args):
                    boton.config(state='normal')
                id=valores[0]
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
                actualizar=1
                def guardar():
                    Funcionalidades.enviardatos(nueva_ventana,nombre1,autor1,categoria1,fecha1,actualizar,id)
                boton=Button(nueva_ventana,text='Guardar',command=guardar,state='disabled')
                boton.grid(row=4,column=1)      
            treeview.bind("<Double-1>", editar_item)
            return subventana
        except Exception as e:
            mb.showwarning(title='Error al editar registro',message=e)

    def buscar_item(parent):
        try:
            subventana=Funcionalidades.crear_subventana(parent)
            Funcionalidades.centrarSubventana(subventana)
            frame1=Frame(subventana)
            frame1.pack()
            Boton = None
            def cambios(*args):
                nonlocal Boton
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
            actualizar=2
            tk.Button(frame1, text="Buscar Item", command=lambda:Funcionalidades.enviardatos(subventana,nombre,autor,categoria,fecha,actualizar)).grid(row=4, column=0, pady=20)
        except Exception as e:
            mb.showwarning(title='Error al buscar registro',message=e)
        