import sys
import os

def main(argv):
    if len(argv) <= 2:
        print("No se paso el archivo o la imagen")
        return -1

    nombreArchivo = argv[1]
    nombreImagen =  argv[2]

    directorio =  "/".join(nombreImagen.split("/")[:-2])
    nombreTemp = f"{directorio}/temp.txt"
    
    archivo = open(nombreArchivo, "r", encoding = "utf-8")
    temp = open(nombreTemp, "w", encoding = "utf-8")

    nombreImagenReducido = "/".join(nombreImagen.split("/")[-2:])
    patron = f"![[{nombreImagenReducido}.svg]]"

    for linea in archivo.readlines():
        if not patron in linea:
            temp.write(linea)
            continue

        with open(f"{nombreImagen}.svg", "r", encoding = "utf-8") as imagen:
            temp.write('\n\n<div class="tikz_svg">\n\n')
            for svgLinea in imagen.readlines():
                temp.write(svgLinea)
            temp.write('\n\n</div>\n\n')

    archivo.close()
    temp.close()

    os.replace(nombreTemp, nombreArchivo)



if __name__ == "__main__":
    main(sys.argv)
