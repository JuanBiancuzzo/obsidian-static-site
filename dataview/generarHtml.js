import puppeteer from "puppeteer";
import fs from "fs";
import dataviewFunction from "./modificador.js"

const DATAVIEW_TAG_ID = "div";

async function conseguirContenido(pagina, paginaURL) {
    await pagina.goto(paginaURL, { waitUntil: "domcontentloaded" });

    const dataviewTag = await pagina.$(`#${DATAVIEW_TAG_ID}`);
    await pagina.evaluate(dataviewFunction, dataviewTag);

    let contenido = await pagina.evaluate(dv => dv.innerHTML, dataviewTag);
    console.log(contenido);
}

async function main(argv) {
    if (argv.length <= 2) {
        console.log("No se pasaron suficientes argumentos");
        return;
    }

    let query = argv[2];
    let workdir = argv[3];
    fs.read(query, "ISO-8859-1", (_, data) => {
        let [archivo, javascriptArchvo] = data.split(":");
    });

    if (argv.length <= 3) {
        let directorio = argv[1];
        pagina = `file://${directorio}/${pagina}`;
    }

    const buscador = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome-stable",
        args: ["--disable-gpu", "--disable-setuid-sandbox", "--no-sandbox", "--no-zygote"],

        headless: true,
    });

    const paginaBuscador = await buscador.newPage();

    await conseguirContenido(paginaBuscador, url);

    await buscador.close();
}

main(process.argv);
