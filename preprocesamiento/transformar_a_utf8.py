import sys
import os

ENCODING = "utf-8"

import generador_archivos

def procesarArchivo(nombreArchivo, encodingInicial): 
    nombreTemp = "/".join(nombreArchivo.split("/")[:-1]) + "/temp"
    with open(nombreArchivo, "r", encoding = encodingInicial) as archivo:
        with open(nombreTemp, "w", encoding = ENCODING) as archivoDecodeficado:
            for linea in archivo.readlines():
                linea = linea.encode(encodingInicial).decode(ENCODING)
                archivoDecodeficado.write(linea)

    os.replace(nombreTemp, nombreArchivo)

def main(argv):
    if len(argv) <= 2:
        print("No se paso un directorio a buscar ")
        return -1

    if len(argv) <= 3:
        print("No se paso un encoding de los archivos")
        return -1

    config = {
        "dirAFiltrar": ["git", "github", ".configuracion"],
        "extAFiltrar": ["png", "jpg", "svg"],
    }

    directorio = argv[1]
    encoding = argv[2]

    generador = generador_archivos.GenArchivos(directorio)
    for archivo in generador:
        if generador_archivos.filtrar(archivo, config):
            continue
        try:
            procesarArchivo(archivo, encoding)
            print(f"{archivo}:{directorio}")
        except:
            pass

if __name__ == "__main__":
    main(sys.argv)

