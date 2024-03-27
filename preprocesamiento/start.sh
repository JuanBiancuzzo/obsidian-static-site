#!/bin/bash

app_path="/usr/src/app"
content_path="$app_path/content"

# Pasar todos los archivos a utf8
/bin/python3 "$app_path/transformar_a_utf8.py" "$content_path"

# Procesar ecuaciones matematicas para que aparezcan bien
/bin/python3 "$app_path/procesar_math.py" "$content_path"

# Reemplazar latex y tikz por svg 
mkdir "$content_path/img"
cd "$content_path/img"

/bin/python3 "$app_path/reemplazar_latex.py" "$content_path" \
    | xargs -I {} /bin/bash "$app_path/latex2svg.sh" {} \
    | /bin/python3 "$app_path/reemplazar_por_svg.py"

cd "$app_path"
rm -rf "$content_path/img"

# Reemplazar dataview
cd "$app_path/dataview"

# Generar metadata de archivos
echo "Generando metadata de archivos"
/bin/python3 "$app_path/metadata_archivos.py" "$content_path" "allFiles.json"

# Reemplazar en los archivo
/bin/python3 "$app_path/reemplazar_dataview.py" "$content_path" "$app_path/dataview" > "query.txt"

/bin/node --experimental-modules "generarHtml.js" "query.txt" "allFiles.json" \
    | xargs -I {} /bin/python3 "$app_path/reemplazar_por_html.py" {}

cd "$app_path"
