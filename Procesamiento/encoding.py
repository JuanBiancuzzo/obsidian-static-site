import sys
import os
import argparse

ENCODING = "utf-8"

def procesarArchivo(nombreArchivo, encodingInicial): 
    nombreTemp = "/".join(nombreArchivo.split("/")[:-1]) + "/temp"
    with open(nombreArchivo, "r", encoding = encodingInicial) as archivo:
        with open(nombreTemp, "w", encoding = ENCODING) as archivoDecodeficado:
            for linea in archivo.readlines():
                linea = linea.encode(encodingInicial).decode(ENCODING)
                archivoDecodeficado.write(linea)

    os.replace(nombreTemp, nombreArchivo)

def main(archivo, directorio, path_lua):

    procesarArchivo(archivo, ENCODING)

def obtenerParametros():
    parser = argparse.ArgumentParser(
        prog = "Cambiar encoding",
        description = "Transforma el archivo de un encoding dado a utf-8"
    )

    parser.add_argument(
        "-l",
        "--path-lua",
        default = "init.lua",
        dest = "luapath",
        help = "Path al archivo de lua"
    )

    return parser.parse_args()

if __name__ == "__main__":
    parametros = obtenerParametros()

    try: 
        for linea in sys.stdin.readlines():
            archivo, directorio = linea.replace("\n", "").split(";")
            main(arhcivo, directorio, parametros.luapath)
            print(f"{archivo}:{directorio}")

    except KeyboardInterrupt:
        sys.stdout.flush()
