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
/bin/python3 "$app_path/reemplazar_latex.py" "$content_path" > "$content_path/img/imagenes_procesar.txt"

cd "$content_path/img"

while IFS= read -r conjunto; do

    archivo=$(echo "$conjunto" | cut -d':' -f1)
    imagen=$(echo "$conjunto" | cut -d':' -f2)

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

done < "$content_path/img/imagenes_procesar.txt"

rm "$content_path/img/imagenes_procesar.txt"
cd "$app_path"

# Reemplazar dataviewjs por su correspondiente codigo javascript
mkdir "$content_path/scripts"

# Mover dataview.js a public para ser usada
mv "$app_path/dataview.js" "$content_path/scripts/dataview.js"

# Reemplazar en los archivo
/bin/python3 "$app_path/reemplazar_dataview.py" "$content_path"

# Buildear la pagina
npx quartz build


# Mover lo creado a la carpeta de content ya que estara ahi el volumen
mv public content
