#!/bin/bash

archivo=$(echo "$1" | cut -d':' -f1)
imagen=$(echo "$1" | cut -d':' -f2)

echo "Procesando imagen: $imagen"

# Crear pdf
pdflatex "$imagen.tex" > /dev/null

# Transformar pdf en svg
if ! pdf2svg "$imagen.pdf" "$imagen.svg"; then
    echo "Hubo un error en la imagen: $imagen"
    continue
fi

# Eliminar archivos exceso
for extension in "aux" "log" "pdf" "tex" 
do 
    rm "$imagen.$extension" > /dev/null 2>&1
done
