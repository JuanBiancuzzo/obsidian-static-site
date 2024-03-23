import sys
import os

import generador_archivos 

PATRON = "$$"
LEN_PATRON = len(PATRON)
ENCODING = "utf-8"

def procesarArchivo(nombreArchivo, directorio):
    nombreTemp = f"{directorio}/temp.txt"

    patronEncontrado = False

    archivo = open(nombreArchivo, "r", encoding = ENCODING)
    temp = open(nombreTemp, "w", encoding = ENCODING)
    ecuacion = []

    for linea in archivo.readlines():
        while PATRON in linea:
            if not patronEncontrado:
                patronEncontrado = True
                indexPatron = linea.index(PATRON)

                temp.write(f"{linea[:indexPatron]}")

                linea = linea[indexPatron + LEN_PATRON:] 
            else:
                patronEncontrado = False
                indexPatron = linea.index(PATRON)

                ecuacion.append(linea[:indexPatron])

                temp.write("\n\n<div class=ecuacion>\n\n$$\n")
                for lineaEcuacion in ecuacion:
                    lineaEcuacion = lineaEcuacion.strip().replace("\n", "")
                    temp.write(f"{lineaEcuacion} ")
                temp.write("\n$$\n\n</div>\n\n")

                ecuacion = []

                linea = linea[indexPatron + LEN_PATRON:]
        else:
            if patronEncontrado:
                ecuacion.append(linea)
            else:
                temp.write(linea)



    for linea in archivo.readlines():

        while PATRON in linea:
            if not patronEncontrado:
                patronEncontrado = True
                indexPatron = linea.index(PATRON)

                temp.write(f"{linea[:indexPatron]}\n")
                temp.write(f"\n{linea[indexPatron:indexPatron + LEN_PATRON]}")

                linea = linea[indexPatron + LEN_PATRON:] 
            else:
                patronEncontrado = False
                indexPatron = linea.index(PATRON) + LEN_PATRON

                temp.write(f"{linea[:indexPatron]}\n")

                linea = linea[indexPatron:]
        else:
            temp.write(linea)

    archivo.close()
    temp.close()
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
        procesarArchivo(archivo, directorio)


if __name__ == "__main__":
    main(sys.argv)
