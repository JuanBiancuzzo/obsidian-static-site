import os
import argparse

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

def filtrar_json(archivo, config):
    archivo = archivo.lower()
    for dir in config["dirAFiltrar"]:
        if f"{dir}/" in archivo:
            return True
    for ext in config["extAFiltrar"]:
        if f".{ext}" in archivo:
            return True
    return False

class Parametros:
    def __init__(self, directorio, path_lua):
        self.directorio = directorio
        self.filtro = lambda _: True

    @classmethod
    def obtener_filtro_json(filtro_json):
        return None

    @classmethod
    def obtener_filtro_lua(filtro_lua):
        return None

def obtener_parametros():
    parser = argparse.ArgumentParser(
        prog = "Generar Archivos",
        description = "Devuelve por stdin todos los archivos en un directorio posiblemente filtrados"
    )

    parser.add_argument(
        "-d",
        "--directorio",
        default = ".",
        dest = "directorio",
        help = "Directorio donde obtener los archivos"
    )
    parser.add_argument(
        "-l",
        "--arc-lua",
        default = "init.lua",
        dest = "filtro",
        help = "Path al archivo de lua con la forma de filtrar"
    )

    args = parser.parse_args()
    return Parametros(args.directorio, args.filtro)

def main(parametros):
    generador = GenArchivos(parametros.directorio)

    for archivo in generador:
        if parametros.filtro(archivo):
            print(f"{archivo};{parametros.directorio}")

if __name__ == "__main__":
    parametros = obtener_parametros()
    main(parametros)
