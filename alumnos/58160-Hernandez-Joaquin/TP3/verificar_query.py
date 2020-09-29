
def verificar_query(query, archivo):
    if len(query) == 19 or len(query) == 21 or len(query) == 22 or len(query) == 23 or len(query) == 24:
        query = query[1:]    
        filtro = query.split('&')[0]
        filtro = filtro.split('=')[0] #palabra filtro
        escala = query.split('&')[1] #palabra escala
        if filtro == "filtro":
            valor_filtro = (query.split('&')[0]).split('=')[1]
            if valor_filtro == "rojo" or valor_filtro == "verde" or valor_filtro == "azul" or valor_filtro == "bw":
                escala = (query.split('&')[1]).split('=')[0]
                if escala == "escala":
                    valor_intensidad = (query[1:].split('&')[1]).split('=')[1]
                    if escala != "":
                        archivo = archivo
                    else:
                        archivo = './400error.html'
                else:
                    archivo = './400error.html'
            else:
                archivo = './400error.html'
        else:
            archivo = './400error.html'
    else:
        archivo = './500error.html'
    return archivo
        