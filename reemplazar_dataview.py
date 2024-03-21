import sys
import os

PATRON_INICIAL = "```dataviewjs"
PATRON_FINAL = "```"
PREFIX_DATAVIEW = "dataview"
CLASS = "dataview"
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

def obtenerDirectorioRelativo(nombreArchivo):
    if len(nombreArchivo.split("/")) <= 2:
        return "."

    return "/".join(
        map(
            lambda _: "..",
            nombreArchivo.split("/")[:-2]
        )
    )

def crearScript(index, id, script, nombreArchivo, directorio, outputdir):
    nombreScript = f"{outputdir}/dataviewScriptFile{index}_{id}"
    archivojs = open(f"{nombreScript}.js", "w", encoding = ENCODING)

    archivojs.write(f"export default async function dataviewFunc{id}(root, metadata) " + "{\n")

    dataviewjs = open(f"{outputdir}/dataview.js", "r", encoding = ENCODING)

    for linea in dataviewjs.readlines():
        archivojs.write(f"\t{linea}")
    archivojs.write("\n\n")

    dataviewjs.close()


    archivojs.write("\ttry{")
    nombreArchivoRelativo = nombreArchivo.replace(directorio, '')
    archivojs.write(f"\n\tconst dv = new Dataview(root, metadata, '{nombreArchivoRelativo}');\n")

    for linea in script:
        archivojs.write(f"\t{linea}")

    archivojs.write("\t} catch (error) {\n")

    archivojs.write("\tlet h5 = document.createElement('h5');\n")
    archivojs.write("\th5.innerText = 'Hubo un error';\n")
    archivojs.write("\troot.append(h5);\n")

    archivojs.write("\tlet p = document.createElement('p');\n")
    archivojs.write("\tp.innerText = `${error}`;\n")
    archivojs.write("\troot.append(p);\n")

    archivojs.write("}\n}\n")
    archivojs.close()

    print(f"{nombreArchivo}:{nombreScript}")

def procesarArchivo(index, nombreArchivo, directorio, outputdir):
    nombreTemp = f"{directorio}/temp.txt"
    nombreArchivoRelativo = nombreArchivo.replace(directorio, '')

    patronEncontrado = False

    archivo = open(nombreArchivo, "r", encoding = ENCODING)
    temp = open(nombreTemp, "w", encoding = ENCODING)

    script = []
    contador = 0
    for linea in archivo.readlines():
        if not patronEncontrado:
            if PATRON_INICIAL in linea:
                patronEncontrado = True
                indexPatron = linea.index(PATRON_INICIAL)
                
                temp.write(linea[:indexPatron])
                script.append(linea[indexPatron + len(PATRON_INICIAL):])

            else:
                temp.write(linea)

            continue
        else:
            if PATRON_FINAL in linea:
                patronEncontrado = False
                indexPatron = linea.index(PATRON_FINAL)

                script.append(linea[:indexPatron])
                crearScript(index, contador, script, nombreArchivo, directorio, outputdir)
                script = []

                id = f"{PREFIX_DATAVIEW}-{contador}"

                temp.write(f"\n\n<div class='dataview'>\n")
                temp.write(f"\n\n<script {id}>\n\n")
                temp.write(f"\n</div>\n")
                temp.write(linea[indexPatron + len(PATRON_FINAL):])

                contador += 1

            else:
                script.append(linea)

    archivo.close()
    temp.close()

    if contador > 0:
        os.replace(nombreTemp, nombreArchivo)
    else:
        os.remove(nombreTemp)


def main(argv):
    if len(argv) <= 2:
        print("No se paso un directorio a buscar")
        return -1

    config = {
        "dirAFiltrar": ["git", "github", ".configuracion"],
        "extAFiltrar": ["png", "jpg", "svg"],
    }

    directorio = argv[1]
    outputdir = argv[2]
    generador = GenArchivos(directorio)

    for index, archivo in enumerate(generador):
        if filtrar(archivo, config):
            continue
        procesarArchivo(index, archivo, directorio, outputdir)

if __name__ == "__main__":
    main(sys.argv)

