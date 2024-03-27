import sys
import time

PREFIX_TIKZ = "tikz"
ENCODING = "utf-8"

def main(linea):
    nombreArchivo, svgResultado = linea.split(":")

    print(f"Procesando tikz: {nombreArchivo}")

    contador = int(svgResultado.split("_")[-1])
    id = f"{PREFIX_TIKZ}-{contador}"
    patron = f"<tikz {id}>"

    nombreTemp = "/".join(nombreArchivo.split("/")[:-1])
    nombreTemp += "/temp"

    archivo = open(nombreArchivo, "r", encoding = ENCODING)
    temp = open(nombreTemp, "w", encoding = ENCODING)

    encontrado = False

    for linea in archivo.readlines():
        if not encontrado and patron in linea:
            encontrado = True

            html = open(f"{svgResultado}.svg", "r", encoding = ENCODING)

            for lineaHtml in html.readlines():
                temp.write(lineaHtml)

            html.close()
        else:
            temp.write(linea)
     
    archivo.close()
    temp.close()

    os.replace(nombreTemp, nombreArchivo)

if __name__ == "__main__":
    try:
        for linea in sys.stdin:
            main(linea)
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass




