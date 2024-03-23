import sys
import os

import generador_archivos

EXTENSION = "tex"
EXTENSION_FINAL = "svg"
PATRON_INICIAL = "```tikz"
PATRON_FINAL = "```"
ENCODING = "utf-8"

def cambiarExtension(nombreArchivo, ext):
    path = nombreArchivo.split("/")
    directorio = "/".join(path[:-1])
    nombreArchivoSinExt = ".".join(path[-1].split(".")[:-1])
    return f"{directorio}/{nombreArchivoSinExt}.{ext}"

def tieneLibreria(librerias, contenido):
    nombreLibreria = lambda lib: "usepackage{" + lib + "}"
    libreriasContenidas = []

    for libreria in librerias:
        if any((nombreLibreria(libreria) in linea) for linea in contenido):
            libreriasContenidas.append(libreria)

    return libreriasContenidas

def procesarImagen(nombreArchivo, nombreImagen, contenido):
    contenido[0] = contenido[0].replace(PATRON_INICIAL, "", 1)
    contenido[-1] = contenido[-1].replace(PATRON_FINAL, "", 1)

    preambulo = [
        "\\documentclass[tikz, dvipsnames]{standalone}",
        "\\usepackage{tikz}",
        "\\usepackage{xcolor}",
        "\\color{white}",
    ]

    librerias = ["pgfplots", "circuitikz"]
    posiblesLibrerias = tieneLibreria(librerias, contenido)

    if "pgfplots" in posiblesLibrerias:
        preambulo.append("\\usepackage{pgfplots}")
        preambulo.append("\\pgfplotsset{compat=1.18}")
    if "circuitikz" in posiblesLibrerias:
        preambulo.append("\\usepackage{circuitikz}")
        preambulo.append("\\circuitikzset{color=.}")


    with open(nombreImagen, "w", encoding = ENCODING) as imagen:
        for linea in preambulo:
            imagen.write(f"{linea}\n")

        for linea in contenido:
            if len(tieneLibreria(librerias, [linea])) > 0:
                continue

            if linea.strip().startswith("%"):
                continue
            imagen.write(linea.replace("\n", ""))

    nombreImagen = ".".join(nombreImagen.split(".")[:-1])
    print(f"{nombreArchivo}:{nombreImagen}")

def procesarArchivo(index, nombreArchivo, directorio):
    nombreTemp = f"{directorio}/temp.txt"

    patronEncontrado = False
    seEncontroPatron = False

    archivo = open(nombreArchivo, "r", encoding = ENCODING)
    temp = open(nombreTemp, "w", encoding = ENCODING)
    imagen = []
    cantidad = 0

    for linea in archivo.readlines():
        if not patronEncontrado:
            if PATRON_INICIAL in linea:
                patronEncontrado = True
                seEncontroPatron = True
                indexPatron = linea.index(PATRON_INICIAL)
                
                temp.write(linea[:indexPatron])
                imagen.append(linea[indexPatron:])

            else:
                temp.write(linea)

            continue
        else:
            if PATRON_FINAL in linea:
                patronEncontrado = False
                indexPatron = linea.index(PATRON_FINAL) + len(PATRON_FINAL)

                imagen.append(linea[:indexPatron])
                nombreImagen = f"{directorio}/img/imagen ({index},{cantidad}).{EXTENSION}"
                procesarImagen(nombreArchivo, nombreImagen, imagen)
                imagen = []

                nombreImagenFinal = f"img/imagen ({index},{cantidad}).{EXTENSION_FINAL}"

                temp.write('\n\n<div class="tikz_svg">\n\n')
                temp.write(f"\n![[{nombreImagenFinal}]]\n\n")
                temp.write('\n\n</div>\n\n')
                temp.write(linea[indexPatron:])

                cantidad += 1

            else:
                imagen.append(linea)

    archivo.close()
    temp.close()

    if seEncontroPatron:
        os.replace(nombreTemp, nombreArchivo)
    else:
        os.remove(nombreTemp)


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

    for i, archivo in enumerate(generador):
        if generador_archivos.filtrar(archivo, config):
            continue
        procesarArchivo(i, archivo, directorio)


if __name__ == "__main__":
    main(sys.argv)
