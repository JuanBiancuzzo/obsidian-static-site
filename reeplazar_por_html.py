import os
import sys

def main(argv):
    if len(argv) <= 1:
        print("No se ingreso argumentos")
        return -1

    archivoACambiar, archivoResultado = argv[1].split(":")

    print(f"Archivo: {archivoACambiar}")
    print(f"Html: {archivoResultado}")

if __name__ == "__main__":
    main(sys.argv)



