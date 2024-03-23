import sys
import os

ENCODING_INICIAL = "ISO-8859-1"
ENCODING = "utf-8"

import generador_archivos

def procesarArchivo(nombreArchivo): 
    nombreTemp = "/".join(nombreArchivo.split("/")[:-1]) + "/temp"
    with open(nombreArchivo, "r", encoding = ENCODING_INICIAL) as archivo:
        with open(nombreTemp, "w", encoding = ENCODING) as archivoDecodeficado:
            for linea in archivo.readlines():
                linea = linea.encode(ENCODING_INICIAL).decode(ENCODING)
                archivoDecodeficado.write(linea)

    os.replace(nombreTemp, nombreArchivo)

def main(argv):
    if len(argv) <= 1:
        print("No se paso un directorio a buscar")
        return -1

    config = {
        "dirAFiltrar": ["git", "github", ".configuracion"],
        "extAFiltrar": ["png", "jpg", "svg"],
    }

    directorio = argv[1]

    generador = generador_archivos.GenArchivos(directorio)
    for archivo in generador:
        if generador_archivos.filtrar(archivo, config):
            continue
        procesarArchivo(archivo)

if __name__ == "__main__":
    main(sys.argv)

