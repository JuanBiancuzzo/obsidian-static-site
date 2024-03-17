import puppeteer from "puppeteer";

async function conseguirContenido(paginaURL) {
    const buscador = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome-stable",
        args: ["--disable-gpu", "--disable-setuid-sandbox", "--no-sandbox", "--no-zygote"],
        headless: true,
    });

    const pagina = await buscador.newPage();
    await pagina.goto(paginaURL);

    let contenido = await pagina.content();

    console.log(contenido);

    await buscador.close();
}


async function main(argv) {
    if (argv.length <= 2) {
        console.log("No se pasaron suficientes argumentos");
        return;
    }

    argv = argv.slice(2);
    let pagina = argv[0];
    await conseguirContenido(pagina);
}

main(process.argv);


