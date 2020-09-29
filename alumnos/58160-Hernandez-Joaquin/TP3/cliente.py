import sys
import os
import array
from filtros import hilos, procesar_imagen, filtro_rojo, filtro_verde, filtro_azul, filtro_bw
from verificar_query import verificar_query
from argumentos import parser

def datos(datos):
     encabezado = datos.decode().splitlines()[0] #Obtengo la primera linea
     archivo = "." + encabezado.split()[1] #Obtengo lo que me solicita el cliente datos -> encabezado
     archivo = index(archivo)
     
     try:
          extension = archivo.split('.')[2]  # obtengo la extension del archivo
     except IndexError:
          extension = archivo
     try:
          if (archivo.split('.')[2])[3] == "?":
               extension = archivo.split('.')[2]
               query = extension.split('?')[1]
               extension = extension.split('?')[0]
          else:
               query = ""
     except IndexError:
        query = ""
     return encabezado, archivo, extension, query
     
def index(archivo):
     if archivo == './':
          archivo = './index.html'
     return archivo

def error400(archivo):
     if os.path.isfile(archivo) == False: #si no esta el archivo
          archivo = './400error.html'
     return archivo
      

def normal(encabezado, archivo, extension):
     args = parser()
     dic={"txt":" text/plain","jpg":" image/jpeg","ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
     
     if archivo == './index.html':
          path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP3'
          os.chdir(path)
          extension = archivo.split('.')[2]
     else:
          path = args.document_root
          os.chdir(path)
          archivo = error400(archivo)
          extension = archivo.split('.')[2]
     
     if args.size % 3 != 0:
          args.size += (3 - (args.size % 3))
     
     if archivo == './400error.html':
          path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP3'
          os.chdir(path)
          fd = os.open(archivo, os.O_RDONLY)
          body = ""
          lista =[]
          while True:
               body = os.read(fd, args.size)
               lista += [i for i in body]
               if len(body) != args.size:
                    break
          body = array.array('B', lista)
          os.close(fd)
          header = bytearray("HTTP/1.1 404 Not Found\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
          
     else:
          fd = os.open(archivo, os.O_RDONLY)
          body = ""
          lista =[]
          while True:
               body = os.read(fd, args.size)
               lista += [i for i in body]
               if len(body) != args.size:
                    break
          body = array.array('B', lista)
          os.close(fd)
          header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
     return header, body

def ppm(encabezado, archivo, extension):
     args = parser()
     dic={"txt":" text/plain","jpg":" image/jpeg","ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
     query_posicion = archivo.find('m')
     query = archivo[query_posicion+1:] # a partir de ? incluido
     if query == "": #si la despues de la extension ppm es vacio
          header, body = normal(encabezado, archivo, extension)
     
     elif query != "": #si despues de ppm sigue la query 
              
          #query = filtro & escala
          query.lower()
          archivo = verificar_query(query, archivo)
          
          if archivo == './400error.html' or archivo == './500error.html' :
               archivo = archivo
          else:
               try:
                    v_intensidad = float((query[1:].split('&')[1]).split('=')[1])
               except ValueError():
                    archivo = './400error.html'
          
          if archivo == './400error.html' or archivo == './500error.html' :
               archivo = archivo
          else:
               archivo = archivo.split('?')[0]

          if archivo == './400error.html':
               fd = os.open(archivo, os.O_RDONLY)
               path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP3'
               os.chdir(path)
               extension = archivo.split('.')[2] 
               body = ""
               lista =[]
               while True:
                    body = os.read(fd, args.size)
                    lista += [i for i in body]
                    if len(body) != args.size:
                         break
               body = array.array('B', lista)
               os.close(fd)
               header = bytearray("HTTP/1.1 404 Not Found\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
               os.close(fd)

          elif archivo == './500error.html':
               fd = os.open(archivo, os.O_RDONLY)
               path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP3'
               os.chdir(path)
               extension = archivo.split('.')[2] 
               body = ""
               lista =[]
               while True:
                    body = os.read(fd, args.size)
                    lista += [i for i in body]
                    if len(body) != args.size:
                         break
               body = array.array('B', lista)
               os.close(fd)
               header = bytearray("HTTP/1.1 500 Internal Server Error\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
               
          else:
               filtre = (query.split('&')[0]).split('=')[1]
               size_file = os.stat(archivo).st_size # cantidad en bytes- bites
               cant_hilos, size = hilos(size_file)# cantidad de hilos
               body = procesar_imagen(cant_hilos, size, archivo, filtre, v_intensidad)
               extension = archivo.split('.')[2]
               header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
     return header, body
