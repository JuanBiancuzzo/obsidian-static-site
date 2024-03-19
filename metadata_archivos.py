import sys
import os
import json

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

def procesarArchivo(index, nombreArchivo, directorio):
    return {
        "index": index,
        "nombre": nombreArchivo.replace(directorio, ""),
    }


def main(argv):
    if len(argv) <= 1:
        print("No se paso un directorio a buscar")
        return -1

    if len(argv) <= 2:
        print("No se nombre del archivo con la metadata")
        return -1

    config = {
        "dirAFiltrar": ["git", "github", ".configuracion"],
        "extAFiltrar": ["png", "jpg", "svg"],
    }

    directorio = argv[1]
    allFiles = argv[2]
    generador = GenArchivos(directorio)

    metadata = {
        'files': [],
    }

    for index, archivo in enumerate(generador):
        if filtrar(archivo, config):
            continue

        metadataArchivo = procesarArchivo(index, archivo, directorio)
        metadata["files"].append(metadataArchivo)

    with open(allFiles, "w", encoding = "ISO-8859-1") as metadataFile:
        json.dump(metadata, metadataFile, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv)

