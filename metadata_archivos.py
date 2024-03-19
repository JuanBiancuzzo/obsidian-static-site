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

def procesarArchivo(nombreArchivo, outgoingLinks):
    # Todos la metadata del archivo como keys en el diccionario
    # tags: [] -> lista de tags de la pagina
    # file: 
    #   * cday -> ctime pero sin contar los milisegundos, segundos, minutos ni horas
    #   * ctime -> which refers to the last time some metadata related to the file was changed.
    #   * etags -> tags
    #   * ext -> "md"
    #   * folder -> absoluta
    #   * frontmatter -> repetir lo mismo que antes, metadata y tags
    #   * inlinks
    #   * link
    #       * display -> nombre
    #       * embed -> True / False
    #       * path
    #       * subpath
    #       * type -> file
    #   * mday -> mtime pero sin contar los milisegundos, segundos, minutos ni horas
    #   * mtime -> which is the last time a file’s contents were modified.
    #   * name
    #   * outlinks -> lo generamos como una lista vacia inialmente
    #       * display -> nombre
    #       * embed -> True / False
    #       * path
    #       * subpath
    #       * type -> file
    #   * path -> folder + name + . + ext
    #   * size
    #   * tags -> las mismas q etags (la tag es #nombre)
    #   * tasks 
    return {
        "nombre": nombreArchivo.replace(directorio, ""),
    }

def encontrarArchivo(metadata):
    pass

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

    metadata = {
        'files': [],
    }

    outgoingLinks = {}

    generador = GenArchivos(directorio)
    for archivo in generador:
        if filtrar(archivo, config):
            continue

        archivo = archivo.replace(directorio, "")

        metadataArchivo = procesarArchivo(archivo, outgoingLinks)
        metadata["files"].append(metadataArchivo)

    generador = GenArchivos(directorio)
    for archivo in generador:
        if filtrar(archivo, config):
            continue

        archivo = archivo.replace(directorio, "")
        if not archivo in outgoingLinks:
            continue

        pos = encontrarArchivo(metadata)
        if pos < 0:
            continue
        
        metadata["files"][pos]["file"]["outlinks"].append(outgoingLinks[archivo])


    with open(allFiles, "w", encoding = "ISO-8859-1") as metadataFile:
        json.dump(metadata, metadataFile, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv)

