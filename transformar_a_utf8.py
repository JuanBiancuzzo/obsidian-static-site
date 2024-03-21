import sys
import os

ENCODING_INICIAL = "ISO-8859-1"
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

def procesarArchivo(nombreArchivo): 
    nombreTemp = "/".join(nombreArchivo.split("/")[:-1]) + "/temp"
    with open(nombreArchivo, "r", encoding = ENCODING_INICIAL) as archivo:
        with open(nombreTemp, "w", encoding = ENCODING) as archivoDecodeficado:
            for linea in archivo.readlines():
                linea = linea.decode(ENCODING_INICIAL).encode(ENCODING)
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

    generador = GenArchivos(directorio)
    for archivo in generador:
        if filtrar(archivo, config):
            continue
        procesarArchivo(archivo)

if __name__ == "__main__":
    main(sys.argv)

