class Dataview {
    constructor(root, metadata, current_file) {
        this.root = root;
        this.current_file = current_file;
        this.metadata = metadata.files;
    }

    log(texto) {
        let p = document.createElement("p");
        p.innerText = texto;
        this.root.append(p);
    }

    // Query
    current() {
        page(this.current_file);
    }

    pages(source = undefined) {
        let resultado = this.metadata.slice();
        if (!source)
            return resultado;

        // Agregar los casos con los parentesis
        let comandos = source.split(" ")
            .map(cmd => cmd.trim());

        

        return resultado;
    }

    pagePaths(source = undefined) {
        return this.pages(source).map(archivo => archivo.file.path);
    }


    page(path) {
        let resultados = this.pages().filter(archivo => {
            let archivoPath = archivo.file.path;
            let archivoPathSinExt = `${archivo.file.folder}/${archivo.file.name}`;
            return path == archivoPath || path == archivoPathSinExt;
        });

        return resultados.length > 0 ? resultados[0] : undefined;
    }

    closestFile(nameOrPath) {
        return this.pages().filter(archivo => archivo.file.path.includes(nameOrPath))[0];
    }

    slitearLinks(string) {
        let resultado = [];
        let inicioEncontrado = false;
        let index;

        while (true) {
            index = (inicioEncontrado) ? string.indexOf("]]") + 2 : string.indexOf("[[");
            if (index < 0) {
                resultado.push(string);
                break;
            }

            inicioEncontrado = !inicioEncontrado;
            resultado.push(string.slice(0, index));
            string = string.slice(index);
        }
        return resultado;
    }

    crearLink(string) {
        string = string.slice(2, string.length - 2);
        let [nombre, nombreSustituto] = [string, string];
        let archivo = this.closestFile(nombre);

        let link = document.createElement("a");
        link.setAttribute("data-slug", archivo.file.path);
        link.classList.add("internal");

        if (nombre.includes("|")) {
            [nombre, nombreSustituto] = nombre.split("|");
            link.classList.add("alias");
        }

        link.innerText = nombreSustituto;
        return link;
    }

    // Por ahora unicamente links internos
    parsearTexto(texto) {
        return slitearLinks(texto).map(subtexto => {
            if (subtexto.includes("[[") && subtexto.includes("]]"))
                return crearLink(subtexto);
            return subtexto;
        });
    }

    // Render
    el(element, text, opt = undefined) {
        let nuevoElemento = document.createElement(element);
        if (opt) {
            for (let [key, value] of opt) {
                link.setAttribute(key, value);
            }
        }

        let textoParseado = parsearTexto(text);
        for (let texto of textoParseado) {
            nuevoElemento.append(texto);
        }

        this.root.append(nuevoElemento);
    }

    header(level, text) {
        this.el(`h${level}`, text);
    }

    paragraph(text) {
        this.el("p", text);
    }

    span(text) {
        this.el("span", text);
    }

    execute(source) {
        this.log("executeJs");
    }

    executeJs(source) {
        this.log("executeJs");
    }

    view(path, input) {
        this.log("view");
    }

    // Dataviews
    list(lista) {
        let ul = document.createElement("ul");

        for (let elemento of lista) {
            let li = document.createElement("li");
            li.append(this.elementoParseado("span", elemento));
            ul.append(li);
        }

        this.root.append(ul);
    }

    taskList(tasks, groupByFile) {
        this.log("taskList");
    }

    table(headers, elements) {
        this.log("table");
    }

    // Markdown Dataviews

    markdownTable(headers, values) {
        this.log("markdownTable");
    }

    markdownList(values) {
        this.log("markdownList");
    }

    markdownTaskList(tasks) {
        this.log("markdownTaskList");
    }

    // Utility
    
    array(value) {
        this.log("array");
    }
    
    isArray(value) {
        this.log("isArray");
    }
    
    fileLink(path, [embed = undefined], [display_name = undefined]) {
        this.log("fileLink");
    }
    
    sectionLink(path, section, [embed = undefined], [display = undefined]) {
        this.log("sectionLink");
    }
    
    blockLink(path, blockId, [embed = undefined], [display = undefined]) {
        this.log("blockLink");
    }
    
    date(text) {
        this.log("date");
    }
    
    duration(text) {
        this.log("duration");
    }
    
    compare(a, b) {
        this.log("compare");
    }
    
    equal(a, b) {
        this.log("equal");
    }
    
    clone(value) {
        this.log("clone");
    }
    
    parse(value) {
        this.log("parse");
    }

    // Query evaluation

    query(source, [file, settings]) {
        this.log("query");
    }
    
    tryQuery(source, [file, settings]) {
        this.log("tryQuery");
    }
    
    queryMarkdown(source, [file], [settings]) {
        this.log("queryMarkdown");
    }
    
    tryQueryMarkdown(source, [file], [settings]) {
        this.log("tryQueryMarkdown");
    }
    
    tryEvaluate(expression, [context]) {
        this.log("tryEvaluate");
    }
    
    evaluate(expression, [context]) {
        this.log("evaluate");
    }
}



