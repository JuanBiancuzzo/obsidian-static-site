import puppeteer from "puppeteer";
import fs from "fs";

import { dataArrayProxyHandler } from "./dataArray";

const DATAVIEW_TAG_ID = "div";
const HTMLFILE = "file:///usr/src/app/dataview/index.html";

async function conseguirContenido(pagina, dataviewFunction, metadata) {
    await pagina.goto(HTMLFILE, { waitUntil: "domcontentloaded" });

    // Ejecutar el código custom en el DOM
    const dataviewTag = await pagina.$(`#${DATAVIEW_TAG_ID}`);
    await pagina.evaluate(dataviewFunction, dataviewTag, metadata);

    // Obtener el html de lo ejecutado
    return await pagina.evaluate(dv => dv.innerHTML, dataviewTag);
}

// Obtiene el default de un path a un archivo js pasado por parametro
async function importarFuncion(javascriptFile) {
    const module = await import(javascriptFile);
    return module.default;
}

async function main(argv) {
    if (argv.length <= 3) {
        console.log("No se pasaron suficientes argumentos");
        return;
    }

    let data = fs.readFileSync(argv[2]).toString();
    data = data.split("\n");

    let metadata = fs.readFileSync(argv[3]);
    metadata = new Proxy(JSON.parse(metadata).files, dataArrayProxyHandler);

    const buscador = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome-stable",
        args: ["--disable-gpu", "--disable-setuid-sandbox", "--no-sandbox", "--no-zygote"],

        headless: true,
    });

    const paginaBuscador = await buscador.newPage();

    for (let linea of data) {
        let lineaSplit = linea.split(":");

        let archivo = lineaSplit[0];
        let javascriptFile = lineaSplit[1];

        if (!archivo || !javascriptFile)
            continue;

        let funcion = await importarFuncion(`${javascriptFile}.js`);
        let contenido = await conseguirContenido(paginaBuscador, funcion, metadata);

        fs.writeFileSync(`${javascriptFile}.html`, contenido);

        console.log(`${archivo}:${javascriptFile}`);
    }

    await buscador.close();
}

main(process.argv);
