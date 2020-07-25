import os
import threading
import array
import sys 
import argparse
import concurrent.futures
from leer_mensaje import leer_mensaje
from encabezado import eliminar_comentario, header, calcular_posicion
from time import time



global lista
lista = []
global imagen_leida
imagen_leida = ""

candado = threading.Lock()
text = ""


def main():
    
      # creo la instancia del parser
    parser = argparse.ArgumentParser(description='Trabajo Practico Nº2 - Procesa ppm')
    parser.add_argument('-f', '--file', default='',help='archivo portador', type=str)
    parser.add_argument('-s', '--size', default=1026, help='bloque de lectura', type=int)
    parser.add_argument('-m', '--message', default='', help='mensaje esteganográfico', type=str)
    parser.add_argument('-e', '--offset', default=1, help='offset en pixels del inicio del raster', type=int)
    parser.add_argument('-i', '--interleave', default=1, help='interleave de modificacion en pixel', type=int)
    parser.add_argument('-o', '--output', default='encriptado.ppm', help='entrego mesaje', type=str)
    
    args = parser.parse_args()  

    if(args.size<=0):
        print("ERROR!!! El tamaño del bloque no es correcto")
        sys.exit()

   
    try:
        archivo = os.open(args.file, os.O_RDONLY)
    except:
        print("El archivo no se encuentra en el directorio")
        sys.exit()

      
    size = int(args.size)
    if size % 3 != 0:
        size += (3 - (size % 3))
    path = os.path.abspath(os.getcwd())
    archivo = os.open(args.file, os.O_RDONLY) #ABRO IMAGEN
    imagen = os.read(archivo, size) #LEO IMAGEN
    # mensaje = open(path + "/" + args.message, "rb") #ABRO MENSAJE HA ENCRIPTAR
    mensaje, long_men = leer_mensaje(args.message, size) #LEO MENSAJE
    interleave = int(args.interleave)
    offset = int(args.offset)
    posicion = calcular_posicion(imagen) #POSICION ANTES DE ARRANCAR EL CUERPO DE LA IMAGEN
    os.lseek(archivo, posicion, 0)
    comentario = "#UMCOMPU2 {} {} {}".format(offset, interleave, long_men)
    texto1 = eliminar_comentario(imagen) #ELIMINO #Imagen ppm
    cabecera = header(texto1, comentario)
    # print("\n")
    # print(texto1)
    # print("\n")
    #print(cabecera)
    #print(len(cabecera)) #Longitud cabecera
    
    
    output = open(args.output, "wb", os.O_CREAT) 
    output.write(bytearray(cabecera, 'ascii'))

    while True:
        hilo_rojo = threading.Thread(target=encriptar_rojo, args=(interleave, offset, mensaje))
        hilo_verde = threading.Thread(target=encriptar_verde, args=(interleave, offset, mensaje))
        hilo_azul = threading.Thread(target=encripar_azul, args=(interleave, offset, mensaje))
        
        global imagen_leida #Variable de la imagen en hexa
        global lista 
            # Pongo un lock para leer la imagen
            
        imagen_leida = os.read(archivo, size)
        lista = [i for i in imagen_leida] #Guardo imagen del bloque leida
        if len(imagen_leida) != size:
            break

        hilo_rojo.start()
        hilo_verde.start()
        hilo_azul.start()
    
        hilo_rojo.join()
        hilo_verde.join()
        hilo_azul.join()
        
        imagen_nueva = array.array('B', lista)
        imagen_nueva.tofile(output)
    output.close()
    print("se genero correctamente")
    t_inicio= time()
    print("El tiempo de ejecucion es",time() - t_inicio,"segundos")

def encriptar_rojo(interleave, offset, mensaje):
    # Indices del mensaje para cada color
    c_r = 0  # 0, 3, 6, 9
    global imagen_leida
    global lista
    # Indices para la lista
    # Rojo
    ini_r = 0 + ((3*offset))
    fin_r = len(lista) 
    
    
    for j in range(ini_r, fin_r, (interleave*9)):
        if c_r < len(mensaje):
            candado.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_r] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_r] == "1":
                    lista[j] = lista[j]
                else:
                    lista[j] -= 1
            candado.release()
            c_r += 3
    


def encriptar_verde(interleave, offset, mensaje):
    c_v = 1  # 1, 4, 7, 10
    global imagen_leida
    global lista
    # verde
    ini_v = 1 + (3*(offset) + ((interleave)*3))
    fin_v = len(lista)

    
    for j in range(ini_v, fin_v, (interleave*9)):
        if c_v < len(mensaje):
            candado.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_v] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_v] == "1":
                    lista[j] = lista[j]
                else:
                    lista[j] -= 1
            candado.release()
            c_v += 3
    


def encripar_azul(interleave, offset, mensaje):
    c_b = 2  # 2, 5, 8, 11
    global imagen_leida
    global lista
    # azul
    ini_b = 2 + (3*(offset) + ((interleave)*6))
    fin_b = len(lista)
    
    for j in range(ini_b, fin_b, (interleave*9)):
        if c_b < len(mensaje):
            candado.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_b] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_b] == "1":
                    lista[j] = lista[j]
                else:
                   lista[j] -= 1
            candado.release()
            c_b += 3
            
    
# if len(imagen_leida) < size:
#     break
if __name__ == "__main__":
    main()
