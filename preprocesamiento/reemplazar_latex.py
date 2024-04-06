import sys
import time
import os

EXTENSION = "tex"
EXTENSION_FINAL = "svg"
PATRON_INICIAL = "```tikz"
PATRON_FINAL = "```"
PREFIX_TIKZ = "tikz"
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
        "\\documentclass[tikz]{standalone}",
        "\\usepackage{tikz}",
        "\\usepackage[dvipsnames]{xcolor}",
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


    with open(f"{nombreImagen}.tex", "w", encoding = ENCODING) as imagen:
        for linea in preambulo:
            imagen.write(f"{linea}\n")

        for linea in contenido:
            if len(tieneLibreria(librerias, [linea])) > 0:
                continue

            if linea.strip().startswith("%"):
                continue
            imagen.write(linea.replace("\n", ""))

    print(f"{nombreArchivo}:{nombreImagen}")

def main(index, nombreArchivo, directorio):
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
                nombreImagen = f"img/imagen_{index}_{cantidad}"
                procesarImagen(nombreArchivo, f"{directorio}/{nombreImagen}", imagen)
                imagen = []

                temp.write('\n\n<div class="tikz_svg">\n\n')
                temp.write(f"\n![[{nombreImagen}.svg]]\n\n")
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

if __name__ == "__main__":
    try:
        for contador, linea in enumerate(sys.stdin.readlines()):
            archivo, directorio = linea.replace("\n", "").split(":")
            main(contador, archivo, directorio)
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass
