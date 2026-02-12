#Importaciones necesarias
from tkinter import * 
import Funcionalidades as fun
from tkinter import font as tkFont 

#Creamos la raiz de Tkinter
root= Tk()

#Le asiganamos un titulo y una imagen como icono
root.title('Libreria')
img = PhotoImage(file='iconoLibro.png')   
root.tk.call('wm', 'iconphoto', root._w, img)

#Ajustamos la pantalla para que este centrada y tenga el tamaño correcto 
root.resizable(True, True)
root.update()
w=root.winfo_width()
h=root.winfo_height()
ws=root.winfo_screenwidth()
hs=root.winfo_screenheight()
x=int(ws/2 - w/2)
y=int(hs/2 - h/2)
root.geometry(f'{w}x{h}+{x}+{y}')

#Creamos un frame y ajustamos los pesos de cada columna que vamos a usar
frame=Frame(root)
frame.pack(expand=True,fill='both')
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1) 
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1) 
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)


#Cambiamos la fuente y su tamaño
fuente = tkFont.Font(family="Helvetica", size=10)

#Creamos las diferentes label con sus botones correspondientes ubicandolas en las filas y columnas correcta, ademas en los botones llamamos a la funcion correspondiente del fichero Funcionalidades
Label(frame, text='Añadir Item: ',font=fuente).grid(row=0, column=0,sticky='nsew',padx=5,pady=5)
Button(frame, text='Añadir',font=fuente, command=lambda:fun.Funcionalidades.añadirItem(root)).grid(row=0, column=1,sticky='ew',padx=5,pady=5)

Label(frame, text='Editar Item: ',font=fuente).grid(row=1, column=0,sticky='nsew',padx=5,pady=5)
Button(frame, text='Editar',font=fuente, command=lambda:fun.Funcionalidades.abrir_editar_items(root)).grid(row=1, column=1,sticky='ew',padx=5,pady=5)

Label(frame, text='Buscar Item: ',font=fuente).grid(row=2, column=0,sticky='nsew',padx=5,pady=5)
Button(frame, text='Buscar',font=fuente, command=lambda:fun.Funcionalidades.buscar_item(root)).grid(row=2, column=1,sticky='ew',padx=5,pady=5)

Label(frame, text='Mostrar Catalogo: ',font=fuente).grid(row=3, column=0,sticky='nsew',padx=5,pady=5)
Button(frame, text='Catalogo',font=fuente, command=lambda:fun.Funcionalidades.mostrar_catalogo(root)).grid(row=3, column=1,sticky='ew',padx=5,pady=5)

#Detectamos si cambia el evento para ajustar el tamaño de la fuente en caso afirmativo
def detectar_evento(evento):
    fun.Funcionalidades.ajustarFontSize(root,fuente,evento)

root.bind('<Configure>', detectar_evento)

#Ejecutamos la interfaz gráfica 
root.mainloop()
