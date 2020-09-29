import os
import array
from concurrent import futures

def hilos(size_file):
    if size_file < 10000:
        size_file = 10000
    if size_file % 3 != 0: #Verifico que sea multiplo de 3
        size_file += (3 - (size_file % 3))
    # Vemos la cantidad de hilos
    cant_hilos = round((size_file / size_file)+0.5)
    print(cant_hilos)
    return cant_hilos, size_file

def calcular_posicion(imagen): #imagen = archivo
    for i in range(imagen.count(b"\n# ")):  # Si hay comentarios en la imagen
        barra_n_numeral = imagen.find(b"\n#")+1
        barra_n = imagen.find(b"\n", barra_n_numeral)
        # Ultimo barra antes de arrancar con la imagen
    if imagen.count(b"\n# ") == 0:  # Si no hay comentarios
        barra_n = imagen.find(b"\n")
    medidas = imagen.find(b"\n", barra_n + 1)
    profundidad = imagen.find(b"\n", medidas+1)
    return profundidad + 1 #posicion de arranca la imagen en pixeles

def procesar_imagen(cant_hilos, size, files, filtro, intensidad):
    #abro el archivo
    archivo = os.open(files, os.O_RDONLY)
    if size % 3 != 0: #VEO si es multiplo de 3
        size += (3 - (size % 3))
    imagen = os.read(archivo, size)
    # calculo la posicion donde comienza el cuerpo de la imagen
    posicion = calcular_posicion(imagen)
    encabezado = imagen[:posicion]
    encabezado = [i for i in encabezado]
    # Inicio el curpo en la imagen
    os.lseek(archivo, posicion, 0)
    body = ""
    lista = []
    lista2 = []
    cuerpo = array.array('B', encabezado)
    hilos = futures.ThreadPoolExecutor(max_workers=cant_hilos)
    for i in range(cant_hilos):
        body = os.read(archivo, size)
        lista = [i for i in body]
        if filtro == 'rojo':
            lista2.append(hilos.submit(filtro_rojo, lista, intensidad))
        elif filtro == 'verde':
            lista2.append(hilos.submit(filtro_verde, lista, intensidad))
        elif filtro == 'azul':
            lista2.append(hilos.submit(filtro_azul, lista, intensidad))
        elif filtro == 'bw':
            lista2.append(hilos.submit(filtro_bw, lista, intensidad))
            
    for i in lista2:
        cuerpo += array.array('B', i.result())
    os.close(archivo)
    return cuerpo

def filtro_rojo(lista, intensidad):
    for i in range(0, len(lista)-3, 3):
        lista[i] = round(float(lista[i]) * float(intensidad))
        if lista[i] > 255:
            lista[i] = 255 
        lista[i + 1] = 0
        lista[i + 2] = 0
    return lista

def filtro_verde(lista, intensidad):
    for i in range(0, len(lista)-3, 3):
        lista[i] = 0
        lista[i + 1] = round(float(lista[i + 1]) * float(intensidad))
        if lista[i + 1] > 255:
            lista[i + 1] = 255 
        lista[i + 2] = 0
    return lista

def filtro_azul(lista, intensidad):
    for i in range(0, len(lista)-3, 3):
        lista[i] = 0
        lista[i + 1] = 0
        lista[i + 2] = round(float(lista[i + 2]) * float(intensidad))
        if lista[i + 2] > 255:
            lista[i + 2] = 255 
    return lista

def filtro_bw(lista, intensidad):
    for i in range(0, len(lista)-3, 3):
        pixel_bw = round((lista[i] + lista[i + 1] + lista[i + 2])/3)
        pixel_bw = round(pixel_bw * float(intensidad))
        if pixel_bw > 255:
            pixel_bw = 255 

        lista[i] = pixel_bw
        lista[i + 1] = pixel_bw
        lista[i + 2] = pixel_bw
    return lista