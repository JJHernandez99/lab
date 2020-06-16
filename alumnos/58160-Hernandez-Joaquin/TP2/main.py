import os
import threading
import array
import sys 
import concurrent.futures
import argparse
from leer_mensaje import leer_mensaje
from encabezado import eliminar_comentario, header, calcular_posicion



global lista
lista = []
global imagen_leida
imagen_leida = ""
b = threading.Barrier(4)
lc = threading.Lock()
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
    mensaje = open(path + "/" + args.message, "rb") #ABRO MENSAJE HA ENCRIPTAR
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
    print(len(cabecera)) #Longitud cabecera
    
    
    output = open(args.output, "wb", os.O_CREAT) #
    output.write(bytearray(cabecera, 'ascii'))
    hilos = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    for i in range(3):
        hilos.submit(encriptar, interleave, offset, mensaje, i, size)  # i = indice
    
    
    global imagen_leida #Variable de la imagen en hexa
    global lista 
    while True:         # Pongo un lock para leer la imagen
        lc.acquire()
        imagen_leida = os.read(archivo, size)
        lista += [i for i in imagen_leida] #Guardo imagen del bloque leia en 
        lc.release()
        print("hola")
        b.wait()
        print("chau")
        imagen_nueva = array.array('B', lista)
        imagen_nueva.tofile(output)
        if len(imagen_leida) != size:
            break
    output.close()
    print("se genero correctamente")
    


def encriptar(interleave, offset, mensaje, indice, size):
    global imagen_leida
    global lista
    c_r = 0 # 0, 3, 6, 9
    c_v = 1 # 1, 4, 7, 10
    c_b = 2 # 2, 5, 8, 11
    
    while True:
        if indice == 0:  # rojo
            # offset == pixel en el cual comienza , interleave == Saltos de pixel
            # offset 0 == 1° pixel, interleave 1 == proximo pixel
            # offset 0 e interleave 1 el rojo se mueve cada 9 lugares
            # offset se multiplica por 3 y el interleva tambien
            lc.acquire()
            for j in range(0, len(lista), (interleave*9)):
                if c_r < len(mensaje):
                    if lista[j + offset * 3] % 2 == 0:
                        if mensaje[c_r] == "0":
                            lista[j + offset * 3] = lista[j + offset * 3]
                        else:
                            lista[j + offset * 3] += 1
                    else:
                        if mensaje[c_r] == "1":
                            lista[j + offset * 3] = lista[j + offset * 3]
                        else:
                            lista[j + offset * 3] -= 1
                c_r += 3
                lc.release()
        elif indice == 1:
            lc.acquire()
            for j in range(0, len(lista), interleave*9):
                if c_v < len(mensaje):
                    if lista[j + 1 + offset * 3 + interleave*3] % 2 == 0:
                        if mensaje[c_v] == "0":
                            lista[j + 1 + offset * 3 + interleave*3] = lista[j + 1 + offset * 3 + interleave*3]
                        else:
                            lista[j + 1 + offset * 3 + interleave*3] += 1
                    else:
                        if mensaje[c_v] == "1":
                            lista[j + 1 + offset * 3 + interleave*3] = lista[j + 1 + offset * 3 + interleave*3]
                        else:
                            lista[j + 1 + offset * 3 + interleave*3] -= 1
                c_v += 3
                lc.release()
        else:
            lc.acquire()
            for j in range(0, len(lista), interleave*9):
                if c_b < len(mensaje):
                    if lista[j + 2 + offset * 3 + interleave*6] % 2 == 0:
                        if mensaje[c_b] == "0":
                            lista[j + 2 + offset * 3 + interleave*6] = lista[j + 2 + offset * 3 + interleave*6]
                        else:
                            lista[j + 2 + offset * 3 + interleave*6] += 1
                    else:
                        if mensaje[c_b] == "1":
                            lista[j + 2 + offset * 3 + interleave*6] = lista[j + 2 + offset * 3 + interleave*6]
                        else:
                            lista[j + 2 + offset * 3 + interleave*6] -= 1
                    c_b += 3
                    lc.release()
        b.wait()    
        if len(imagen_leida) < size:
            break
       




if __name__ == "__main__":
    main()
