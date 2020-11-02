import asyncio
import socket
import os
from argumentos import parser
from funciones import normal, logs, index

global abspath

async def handler(reader, writer):
    address = writer.get_extra_info('peername')
    asyncio.create_task(logs(address[0],address[1]))
    data = (await reader.read(args.size)).decode()

    if "GET" in data:
        archivo = data.split(" ")[1]
        path = '/home/joaquin/computacion2/lab/alumnos/58160-Hernandez-Joaquin/TP4'
        os.chdir(path)
        if archivo == "/":
            path = f"{path}/index.html"
        else:
            path = f"{path}{archivo}"
        path, header = normal(path)
        writer.write(header)
        fd = os.open(path,os.O_RDONLY)
        while True:
            body = os.read(fd,args.size)
            writer.write(body)
            if(len(body)!= args.size):
                break
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        os.close(fd)

async def server(port):
    server = await asyncio.start_server(handler,["127.0.0.1","::1"],port,family=socket.AF_UNSPEC)
    async with server:
        await server.serve_forever()

index()

if __name__ == "__main__":
    # abspath=os.getcwd()
    args=parser()
    asyncio.run(server(args.port))