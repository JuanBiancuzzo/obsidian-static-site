#!/bin/bash

app_path="/usr/src/app"

if [ -z "$1" ]; then
    echo "No se paso ningun valor de version"
    exit -1
fi

archivo=$(echo "$1" | cut -d':' -f1)
nombreScript=$(echo "$1" | cut -d':' -f2)

mkdir temp
cp "index.html" "./temp/"
cp "generarHtml.js" "./temp/"
cp "$nombreScript.js" "./temp/modificador.js"
cat "dataview.js" >> "./temp/modificador.js"
cd temp

/bin/node "generarHtml.js" "index.html" "$app_path/dataview/temp" \
    > "$nombreScript.html"

rm *
cd ..
rmdir temp

echo "$archivo:$nombreScript.html"

