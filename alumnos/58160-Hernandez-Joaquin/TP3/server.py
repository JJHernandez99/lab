import socketserver
from threading import Thread
import argparse
import os
import array
from cliente import parser, normal, datos, ppm

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0] #Obtengo la primera linea
        encabezado, archivo, extension, query = datos(self.data)
        
        if extension == 'ppm' :
            header, body = ppm(encabezado, archivo, extension)
        else:
            header, body = normal(encabezado, archivo, extension)           
           
        # respuesta = header + body
        self.request.sendall(header)
        self.request.sendall(body) 
    
args = parser()
socketserver.ThreadingTCPServer.allow_reuse_address = True
server =  socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
server.serve_forever()