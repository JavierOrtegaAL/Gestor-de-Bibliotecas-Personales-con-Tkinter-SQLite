#Importacion necesaria
import sqlite3

#Nos conectamos a la base de datos y creamos el cursor
conexion=sqlite3.connect('libros.db')
cursor=conexion.cursor()

#Creamos las diferentes tablas que vamos a utilizar, solo se jecuta este fichero la primera vez
cursor.execute("CREATE TABLE IF NOT EXISTS autores (idAutor INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, apellido TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS categorias (idCategoria INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS libros (idLibro INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, autor TEXT NOT NULL, categoria TEXT NOT NULL, FOREIGN KEY(autor) REFERENCES autores(idAutor) , FOREIGN KEY(categoria) REFERENCES categorias(idCategoria))")

"""
Metodo create, recibe el nombre, el autor la categoria y la fecha.
Se conecta a la base de datos y crea un cursor sobre ella.
A traves del metodo insert, inserta los campos en la nueva instancia.
Guarda y cierra la conexion a la base de datos.
En caso de error imprime por pantalla el error. 
"""
def añadir_item(nombre, autor,categoria,fecha):
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        cursor.execute('INSERT INTO libros (nombre,autor,categoria,fecha) VALUES (?,?,?,?)',(nombre,autor,categoria,fecha))
        conexion.commit()
        conexion.close()
    except Exception as e:
            print(e)

"""
Metodo read
Se conecta a la base de datos y crea un cursor sobre ella.
A traves del metodo select, recupera todas las instancias que hay en la base de datos.
Los alamacena en una variable a la que parseamos a tipo list y la retornamos despues de cerrar la conexión.
En caso de error imprime por pantalla el error. 
"""
def mostrar_items():
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        lista=cursor.execute("SELECT * FROM libros")
        lista=list(lista)
        conexion.close()
        return lista
    except Exception as e:
            print(e)

"""
Metodo read a partir de un id que recibe
Se conecta a la base de datos y crea un cursor sobre ella.
A traves del metodo select y filtrando por el id, recupera la instancia que hay en la base de datos con ese id.
Lo alamacena en una variable a la que parseamos a tipo list y la retornamos despues de cerrar la conexión.
En caso de error imprime por pantalla el error. 
"""
def mostrar_item(id):
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM libros WHERE idLibro=?",(id,))
        lista=cursor.fetchall()
        lista=list(lista)
        conexion.close()
        return lista
    except Exception as e:
            print(e)

"""
Metodo read a partir de varios ids que recibe
Se conecta a la base de datos y crea un cursor sobre ella.
A traves del metodo select y filtrando por los ids, recupera las instancias que hay en la base de datos con esos ids.
Creamos una variable WHERE para poder concatenar los diferentes ids y creamos un bucle for que conactena los diferentes where y añade a una lista, previamente creada los ids.
Lo alamacena en una variable a la que parseamos a tipo list y la retornamos despues de cerrar la conexión.
En caso de error imprime por pantalla el error. 
"""
def mostrar_varios_items(ids):
    try:
        print(ids)
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        where="WHERE "
        lista=list()
        for id in ids:
            where=f"{where}"+"idlibro=? or "
            lista.append(id)
        where=where[:-4]
        cursor.execute(f"SELECT * FROM libros {where}",lista)
        elementos=cursor.fetchall()
        elementos=list(elementos)
        conexion.close()
        return elementos
    except Exception as e:
            print(e)

"""
Metodo update a partir de un id y con los valores nombre, autor, categoria que recibe
Se conecta a la base de datos y crea un cursor sobre ella.
A traves del metodo update cambia el nombre, el autor, la fecha y la categoria a partir del id que le damos.
Guarda y cierra la conexion a la base de datos.
En caso de error imprime por pantalla el error. 
"""
def modificar_item(id,nombre,autor,categoria,fecha):
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        cursor.execute('UPDATE libros set nombre=?, autor=?,categoria=?,fecha=? WHERE idlibro=?',(nombre,autor,categoria,fecha,id))
        conexion.commit()
        conexion.close()
    except Exception as e:
            print(e)

"""
Metodo read a partir del nombre, autor, categoria y/o fecha
Creamos un diccionario con los campos vacios y en caso de que los parametros no esten vacios los alamacenaos en su clave correspondiente.
Se conecta a la base de datos y crea un cursor sobre ella.
Creamos una variable WHERE para poder concatenar los diferentes ids y creamos un bucle for que conactena los diferentes where y añade a una lista, previamente creada los ids.
A traves del metodo select, recupera todas las instancias que hay en la base de datos con esos ids.
Los alamacena en una variable a la que parseamos a tipo list y la retornamos despues de cerrar la conexión.
Guarda y cierra la conexion a la base de datos.
Retornamos los ids. 
En caso de error imprime por pantalla el error. 
"""
def buscar_item(nombre,autor,categoria,fecha):
    try:
        diccionario={"nombre":"","autor":"","categoria":"","fecha":""}
        if nombre!="":
            diccionario["nombre"]=nombre
        if autor!="":
            diccionario["autor"]=autor
        if categoria!="":
            diccionario["categoria"]=categoria
        if fecha!="":
            diccionario["fecha"]=fecha
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        where="WHERE "
        lista=list()
        for clave,valor in diccionario.items():
            if valor!="":
                where=f"{where}"+f"{clave}=? and "
                lista.append(valor)
        where=where[:-5]
        cursor.execute(f"SELECT idlibro FROM libros {where}",lista)
        id=cursor.fetchall()
        id=list(id)
        conexion.commit()
        conexion.close()
        return id
    except Exception as e:
            print(e)

#Cerramos la conexion
conexion.close()
