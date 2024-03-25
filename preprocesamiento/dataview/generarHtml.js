import puppeteer from "puppeteer";
import fs from "fs";

const DATAVIEW_TAG_ID = "div";
const HTMLFILE = "file:///usr/src/app/dataview/index.html";

async function conseguirContenido(pagina, javascriptFile, metadata) {
    await pagina.goto(HTMLFILE, { waitUntil: "domcontentloaded" });

    // Cargando los archivos
    await pagina.addScriptTag({ path: './dataview.js' });
    await pagina.addScriptTag({ path: './dataArray.js' });
    await pagina.addScriptTag({ path: `${javascriptFile}.js` });

    // Wait for dataview.js to be fully loaded
    await pagina.waitForFunction(() => typeof dataArrayProxyHandler !== 'undefined');
    await pagina.waitForFunction(() => typeof dataviewCall !== 'undefined');
    await pagina.waitForFunction(() => typeof Dataview !== 'undefined');

    await pagina.evaluate((id, metadata) => {
        const root = document.getElementById(id);
        dataviewCall(root, new Proxy(metadata, dataArrayProxyHandler));
    }, DATAVIEW_TAG_ID, metadata);

    // Retrieve the content of the dataview element
    return await pagina.$eval(`#${DATAVIEW_TAG_ID}`, dv => dv.innerHTML);
}

async function main(argv) {
    if (argv.length <= 3) {
        console.log("No se pasaron suficientes argumentos");
        return;
    }

    let data = fs.readFileSync(argv[2]).toString();
    data = data.split("\n");

    let metadata = fs.readFileSync(argv[3]);
    metadata = JSON.parse(metadata).files;

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

        let contenido = await conseguirContenido(paginaBuscador, javascriptFile, metadata);

        fs.writeFileSync(`${javascriptFile}.html`, contenido);

        console.log(`${archivo}:${javascriptFile}`);
    }

    await buscador.close();
}

main(process.argv);
