class Dataview {
    constructor(root, metadata, current_file) {
        this.root = root;
        this.current_file = current_file;
        this.metadata = metadata;
    }

    log(texto) {
        let p = document.createElement("p");
        p.innerText = texto;
        this.root.append(p);
    }

    // Query
    current() {
        this.log("current");
    }

    pages(source) {
        this.log("pages");
    }

    pagePaths(source) {
        this.log("pagePaths");
    }


    page(path) {
        this.log("page");
    }

    // Render

    el(element, text) {
        let nuevoElemento = document.createElement(element);
        nuevoElemento.innerText = text;
        this.root.append(nuevoElemento);
    }

    header(level, text) {
        this.log("header");
    }

    paragraph(text) {
        this.log("paragraph");
    }

    span(text) {
        this.log("span");
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
        this.log("list");
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



