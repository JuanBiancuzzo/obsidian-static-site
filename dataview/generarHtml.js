import puppeteer from "puppeteer";
import fs from "fs";

const DATAVIEW_TAG_ID = "div";
const HTMLFILE = "file:///usr/src/app/dataview/index.html";

async function conseguirContenido(pagina, dataviewFunction) {
    await pagina.goto(HTMLFILE, { waitUntil: "domcontentloaded" });

    const dataviewTag = await pagina.$(`#${DATAVIEW_TAG_ID}`);
    await pagina.evaluate(dataviewFunction, dataviewTag);

    return await pagina.evaluate(dv => dv.innerHTML, dataviewTag);
}

async function importarFuncion(javascriptFile) {
    const module = await import(javascriptFile);
    return module.default;
}

async function main(argv) {
    if (argv.length <= 2) {
        console.log("No se pasaron suficientes argumentos");
        return;
    }

    let query = argv[2];
    let data = [];
    fs.read(query, "ISO-8859-1", (_, data) => {
        data.push([data.split(":")]);
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

    for (let [archivo, javascriptFile] of data) {
        let funcion = await importarFuncion(`${javascriptFile}.html`);
        let contenido = await conseguirContenido(paginaBuscador, funcion);

        fs.writeFile(`${javascriptFile}.html`, contenido, (err) => {
            if (err) throw err;
        });

        console.log(`${archivo}:${javascriptFile}`);
    }


    await buscador.close();
}

main(process.argv);
