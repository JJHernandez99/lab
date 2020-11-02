import asyncio
import datetime 
import os
from os import scandir

global abspath

async def logs(ip,port):
    path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP4'
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro="| Cliente: {} | Puerto: {} | Fecha: {} |\n".format(ip,port,time)
    with open(f"{path}/log.txt","a") as file:
        file.write(registro)
    file.close()

def normal(path):
    abspath = os.getcwd()
    # path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP4'
    dic ={"jpg":"image/jpeg","pdf":"application/pdf","html":"text/html","ppm": "image/x-portable-pixmap", "txt": "text/txt"}
    if os.path.exists(path):
            try:
                extension = path.split(".")[1]
                extension = dic[extension]
                resultado = "HTTP/1.1 200 OK"
            except KeyError:
                resultado = "HTTP/1.1 500 Internal Server Error"
                path =f"{abspath}/html/500error.html"
    else:
        path=f"{abspath}/html/400error.html"
        resultado = "HTTP/1.1 404 Not Found"
    extension = path.split(".")[1]
    size = str(os.stat(path).st_size)
    header = bytearray(resultado + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:" + size +"\r\n\r\n",'utf8')
    return path, header

def index():
    html = "<!DOCTYPE html>\n<html>\n<head><meta charset=\"UTF-8\">\n<title>Index</title>\n</head>\n<body>\n"
    html += "<h3>Bienvenido a la catedra de Computacion 2</h3>\n<h4>Archvios:</h4>"
    path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP4'
    archivos = [obj.name for obj in scandir(path) if obj.is_file()]
    for archivo in archivos:
        if not ".py" in archivo:
            html+="<BLOCKQUOTE><li><a href=\"{}\">{}</a></li></BLOCKQUOTE>\n".format(archivo,archivo)
    html += "</body>\n</html>"
    file = open(f"{path}/index.html","w")
    file.write(html)
    file.close()