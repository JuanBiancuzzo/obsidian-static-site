import sys
import os

PREFIX_DATAVIEW = "dataview"

def main(argv):
    if len(argv) <= 1:
        print("No se ingreso argumentos")
        return -1

    nombreArchivo, htmlResultado = argv[1].split(":")

    print(f"Procesando dataview: {nombreArchivo}")

    contador = int(htmlResultado.split("_")[-1])
    id = f"{PREFIX_DATAVIEW}-{contador}"
    patron = f"<script {id}>"

    nombreTemp = "/".join(nombreArchivo.split("/")[-1])
    nombreTemp += f"/temp"

    archivo = open(nombreArchivo, "r", encoding = "ISO-8859-1")
    temp = open(nombreTemp, "w", encoding = "ISO-8859-1")

    encontrado = False

    for linea in archivo.readlines():
        if not encontrado and patron in linea:
            encontrado = True

            html = open(f"{htmlResultado}.html", "r", encoding = "utf-8")

            for lineaHtml in html.readlines():
                temp.write(lineaHtml)

            html.close()
        else:
            temp.write(linea)
     
    archivo.close()
    temp.close()

    os.replace(nombreTemp, nombreArchivo)

if __name__ == "__main__":
    main(sys.argv)



