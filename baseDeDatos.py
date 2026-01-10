import sqlite3

conexion=sqlite3.connect('libros.db')
cursor=conexion.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS autores (idAutor INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, apellido TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS categorias (idCategoria INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS libros (idLibro INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, autor TEXT NOT NULL, categoria TEXT NOT NULL, FOREIGN KEY(autor) REFERENCES autores(idAutor) , FOREIGN KEY(categoria) REFERENCES categorias(idCategoria))")


def añadir_item(nombre, autor,categoria,fecha):
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        cursor.execute('INSERT INTO libros (nombre,autor,categoria,fecha) VALUES (?,?,?,?)',(nombre,autor,categoria,fecha))
        conexion.commit()
        conexion.close()
    except Exception as e:
            print(e)

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

def modificar_item(id,nombre,autor,categoria,fecha):
    try:
        conexion=sqlite3.connect('libros.db')
        cursor=conexion.cursor()
        cursor.execute('UPDATE libros set nombre=?, autor=?,categoria=?,fecha=? WHERE idlibro=?',(nombre,autor,categoria,fecha,id))
        conexion.commit()
        conexion.close()
    except Exception as e:
            print(e)

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

conexion.close()
