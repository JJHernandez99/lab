import argparse
import sys

def parser():
   # creo la instancia del parser
    parser = argparse.ArgumentParser(description='Trabajo Practico Nº4 - Servidor Web asincronico')
    parser.add_argument('-p', '--port', default=5000 ,help='Puerto donde se esperan conexiones nuevas', type=int)
    parser.add_argument('-d', '--document_root', default='', help='directorio donde se encuentran los documentos web', type=str)
    parser.add_argument('-s', '--size', default=1026, help='Bloque de lectura', type=int)

    args = parser.parse_args()  

    if args.size % 3 != 0:
          args.size += (3 - (args.size % 3))
     
    if args.size <= 0:
        print("ERROR!!! El tamaño del bloque no es correcto")
        sys.exit()

    if args.port <= 0 or args.port == 80:
        print("ERROR!!! El numero del puerto no es correcto") 
        sys.exit()

    

    return args