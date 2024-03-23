/*
    "where", - DONE
    "sort", - DONE
    "groupBy", - DONE
    "distinct", - DONE

    "filter", - NECESITO
    "map", - NECESITO
    "flatMap", - NECESITO
    "slice", - NECESITO
    "indexOf", - NECESITO
    "concat", - NECESITO
    "find", - NECESITO
    "findIndex", - NECESITO
    "includes", - NECESITO
    "every", - NECESITO
    "some", - NECESITO
    "first", - NECESITO
    "last", - NECESITO
    "forEach", - NECESITO
    "length", - NECESITO
    "values", - NECESITO

    "array",
    "none",
    "sortInPlace",
    "limit",
    "mutate",
    "join",
    "groupIn",
    "to",
    "into",
    "lwrap",
    "expand",
    "defaultComparator",
    "toString",
    "settings",
 */
export const dataArrayProxyHandler = {

    get: function(target, prop, receiver) {
        switch (prop) {
            case "sort": 
                throw new Error(`No hay implementacion para: ${prop}`);
                return (compareFunction) => dataArraySort(target, compareFunction);

            case "groupBy":
                throw new Error(`No hay implementacion para: ${prop}`);
                return (keyGetter) => dataArrayGroupBy(target, keyGetter);

            case "distinct":
                throw new Error(`No hay implementacion para: ${prop}`);
                return () => dataArrayDistinct(target);

            case "where":
                throw new Error(`No hay implementacion para: ${prop}`);
                return (predicate) => dataArrayWhere(target, predicate);

            case "filter": 
                throw new Error(`No hay implementacion para: ${prop}`);
                return (filterFunction) => dataArrayFilter(target, filterFunction);

            case "map": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "flatMap": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "slice": 
                throw new Error(`No hay implementacion para: ${prop}`);
                return (start = undefined, end = undefined) => dataArraySlice(target, start, end);

            case "indexOf": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "concat": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "find": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "findIndex": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "includes": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "every": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "some": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "first": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "last": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "forEach": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "length": 
                return () => target.length();

            case "values": 
                throw new Error(`No hay implementacion para: ${prop}`);

            default: return Reflect.get(...arguments);
        }
    }

};

// Sort function
function dataArraySort(array, compareFunction) {
    let newArray = [...array].sort(compareFunction);
    return new Proxy(newArray, dataArrayProxyHandler);
}

// Filter function
function dataArrayFilter(array, filterFunction) {
    let newArray = [...array].filter(filterFunction);
    return new Proxy(newArray, dataArrayProxyHandler);
}

// Slice function
function dataArraySlice(array, start, end) {
    let newArray = [...array].slice(start, end);
    return new Proxy(newArray, dataArrayProxyHandler);
}

// GroupBy function
function dataArrayGroupBy(array, keyGetter) {
    const grouped = new Map();

    array.forEach(item => {
        const key = keyGetter(item);
        const collection = grouped.get(key) || [];
        collection.push(item);
        grouped.set(key, collection);
    });

    return new Proxy(grouped, dataArrayProxyHandler);
}

// Distinct function
function dataArrayDistinct(array) {
    let newArray = Array.from(new Set(array));
    return new Proxy(newArray, dataArrayProxyHandler);
}

// Where function
function dataArrayWhere(array, predicate) {
    let newArray = array.filter(predicate);
    return new Proxy(newArray, dataArrayProxyHandler);
}

