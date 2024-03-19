import sys
import os

def main(argv):
    if len(argv) <= 1:
        print("No se ingreso argumentos")
        return -1

    resultado = argv[1].split(":")
    print(resultado)
    return
    archivoACambiar = resultado[0]
    archivoResultado = resultado[1]

    print(f"Archivo: {archivoACambiar}")
    print(f"Html: {archivoResultado}.html")

if __name__ == "__main__":
    main(sys.argv)



