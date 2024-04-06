#!/bin/bash

app_path="/usr/src/app"
content_path="$app_path/content"
archivos_directorio="$app_path/archivos.txt"
encoding_inicial="ISO-8859-1"

# Pasar todos los archivos a utf8
echo "Transformando los archivos de $encoding_inicial a UTF8"
/bin/python3 "$app_path/transformar_a_utf8.py" "$content_path" "$encoding_inicial" > "$archivos_directorio"

# Procesar ecuaciones matematicas para que aparezcan bien
cat "$archivos_directorio" | /bin/python3 "$app_path/procesar_math.py"

# Reemplazar latex y tikz por svg 
mkdir "$content_path/img"
cd "$content_path/img"

cat "$archivos_directorio" \
    | /bin/python3 "$app_path/reemplazar_latex.py" \
    | xargs -I {} /bin/bash "$app_path/latex2svg.sh" {}

cd "$app_path"

# Reemplazar dataview
cd "$app_path/dataview"

# Generar metadata de archivos
echo "Generando metadata de archivos"
/bin/python3 "$app_path/metadata_archivos.py" "$content_path" "allFiles.json"
cp "allFiles.json" "$content_path"

# Reemplazar en los archivo
/bin/python3 "$app_path/reemplazar_dataview.py" "$content_path" "$app_path/dataview" > "query.txt"

/bin/node --experimental-modules "generarHtml.js" "query.txt" "allFiles.json" \
    | xargs -I {} /bin/python3 "$app_path/reemplazar_por_html.py" {}

cd "$app_path"
