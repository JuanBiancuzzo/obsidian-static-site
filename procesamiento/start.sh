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

# Buildear la pagina
npx quartz build

# Mover lo creado a la carpeta de content ya que estara ahi el volumen
mv public content
cd content

# Copiamos el json de metadata
cp allFiles.json public/static
# Creamos archivo de ultima actualizacion
date +'%Y-%m-%d-%H-%M' | xargs -I {} echo '{"lastUpdate": "{}"}'  >  public/static/data.json
