#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "No se paso ningun valor de version"
    exit -1
fi

version="$1"

sudo docker build -t obsidian-static-site-$version .

sudo docker tag obsidian-static-site-$version juanbiancuzzo/obsidian-static-site:$version
sudo docker push juanbiancuzzo/obsidian-static-site:$version

sudo docker tag obsidian-static-site-$version juanbiancuzzo/obsidian-static-site:latest
sudo docker push juanbiancuzzo/obsidian-static-site:latest
