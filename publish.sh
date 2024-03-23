#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "No se paso ningun valor de version"
    exit -1
fi

version="$1"

first_flag=""
second_flag=""

if [ "$2" ]; then
    first_flag="$2"
fi

if [ "$3" ]; then
    first_flag="$3"
fi

cd preprocesamiento
if [[ $(git status --porcelain) ]] || [ "$first_flag" = "-pre" ] || ["$second_flag" = "-pre"]; then
    echo "Hay cambios en el preprocesamiento recompilando"
    # bash publish.sh "$version"
fi

cd ../procesamiento
if [[ $(git status --porcelain) ]] || [ "$first_flag" = "-pre" ] || ["$second_flag" = "-pre"]; then
    echo "Hay cambios en el procesamiento recompilando"
    #bash publish.sh "$version"
fi

cd ..
