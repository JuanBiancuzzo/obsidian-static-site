#!/usr/bin/bash

contenido="Contenido"
lua_file=".configuracion/init.lua"

echo "Procesando los archivos"
python3 Procesamiento/obtenerArchivos.py -d $contenido -l $lua_file | \
    tee nombre_archivos.txt | \
    parallel -k python3 Procesamiento/encoding.py -l $lua_file
