#!/bin/bash

app_path="/usr/src/app"
content_path="$app_path/content"
config_path="$content_path/.configuracion"

# Moviendo archivos de configuración si existen
if ls $config_path > /dev/null 2>&1; then
    echo "Hay carpeta de configuracion configuracion"

    config="quartz.config.ts"
    layout="quartz.layout.ts"

    if find "$config_path/$config" > /dev/null 2>&1 ; then
        echo "Hay configuracion"
        cp "$config_path/$config" $config > /dev/null 2>&1 
    else
        echo "No hay una configuracion especial, usando default"
    fi

    if find "$config_path/$layout" > /dev/null 2>&1; then
        echo "Hay layout"
        cp "$config_path/$layout" $layout > /dev/null 2>&1
    else
        echo "No hay una layout especial, usando default"
    fi
fi

# Cambiando el readme a el index si este no existe
index="$content_path/index.md"   
if ! find "$index" > /dev/null 2>&1 ; then
    echo "Modificando README a el index"
    touch "$index"  

    for readme in "README" "readme" "Readme" "ReadMe"
    do
        if find "$content_path/$readme.md" > /dev/null 2>&1; then

            echo -e "---\ntitle: $readme\n---" > "$index"  
            cat "$content_path/$readme.md" >>"$index"  

            rm "$content_path/$readme.md" 

            break
        fi
    done
fi

# Procesar ecuaciones matematicas para que aparezcan bien
/bin/python3 "$app_path/procesar_math.py" "$content_path"

# Reemplazar latex y tikz por svg 
mkdir "$content_path/img"
cd "$content_path/img"

/bin/python3 "$app_path/reemplazar_latex.py" "$content_path" \
    | xargs -I {} /bin/bash "$app_path/latex2svg.sh" {}

cd "$app_path"

# Generar metadata de archivos
echo "Generando metadata de archivos"
/bin/python3 "$app_path/metadata_archivos.py" "$content_path" "$app_path/dataview/allFiles.json"

mkdir "$content_path/dataview"
cp "$app_path/dataview/allFiles.json" "$content_path/dataview/allFiles.json"

# Reemplazar en los archivo
/bin/python3 "$app_path/reemplazar_dataview.py" "$content_path" "$app_path/dataview" > "$app_path/dataview/query.txt"

/bin/node "$app_path/dataview/generarHtml.js" "$app_path/dataview/query.txt" "$app_path/dataview/allFiles.json" \
    | xargs -I {} /bin/python3 "$app_path/reemplazar_por_html.py" {}

# Buildear la pagina
npx quartz build

# Mover lo creado a la carpeta de content ya que estara ahi el volumen
mv public content
