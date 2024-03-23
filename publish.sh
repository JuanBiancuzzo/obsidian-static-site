#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "No se paso ningun valor de version"
    exit -1
fi

version="$1"

first_flag=""
second_flag=""

preflag="-pre"
proflag="-pro"

if [ "$2" ]; then
    first_flag="$2"
fi

if [ "$3" ]; then
    second_flag="$3"
fi

if [ "$first_flag" = "$preflag" ] || [ "$second_flag" = "$preflag" ]; then
    cd preprocesamiento

    echo "Hay cambios en el preprocesamiento recompilando"
    bash publish.sh "$version"

    cd ..
else
    echo "No hay cambios en el preprocesamiento recompilando"
fi



if [ "$first_flag" = "$proflag" ] || [ "$second_flag" = "$proflag" ]; then
    cd procesamiento

    echo "Hay cambios en el procesamiento recompilando"
    bash publish.sh "$version"

    cd ..
else
    echo "No hay cambios en el procesamiento recompilando"
fi

