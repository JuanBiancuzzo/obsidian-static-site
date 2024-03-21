import sys
import os

PATRON = "$$"
LEN_PATRON = len(PATRON)
ENCODING = "utf-8"

class GenArchivos:
    
    def __init__(self, directorio):
        self.iter = os.walk(directorio)
        self.files = []
        self.root = None

    def __iter__(self):
        return self

    def __next__(self):
        while len(self.files) == 0:
            self.root, _, self.files = self.iter.__next__()

        file = self.files.pop()
        return os.path.join(self.root, file)

def filtrar(archivo, config):
    archivo = archivo.lower()
    for dir in config["dirAFiltrar"]:
        if f"{dir}/" in archivo:
            return True
    for ext in config["extAFiltrar"]:
        if f".{ext}" in archivo:
            return True
    return False

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
    generador = GenArchivos(directorio)

    for archivo in generador:
        if filtrar(archivo, config):
            continue
        procesarArchivo(archivo, directorio)


if __name__ == "__main__":
    main(sys.argv)
