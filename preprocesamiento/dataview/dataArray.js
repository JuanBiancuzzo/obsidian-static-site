/*
    "where", - DONE
    "sort", - DONE
    "groupBy", - DONE
    "distinct", - DONE
    "filter", - DONE
    "map", - DONE

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
const dataArrayProxyHandler = {

    get: function(target, prop, receiver) {
        switch (prop) {
            case "sort": 
                return (compareFunction) => dataArraySort(target, compareFunction);

            case "groupBy":
                throw new Error(`No hay implementacion para: ${prop}`);
                return (keyGetter) => dataArrayGroupBy(target, keyGetter);

            case "distinct":
                return () => dataArrayDistinct(target);

            case "where":
                return (predicate) => dataArrayWhere(target, predicate);

            case "filter": 
                throw new Error(`No hay implementacion para: ${prop}`);
                return (filterFunction) => dataArrayFilter(target, filterFunction);

            case "map": 
                return (mapFunction) => dataArrayMap(target, mapFunction);

            case "flatMap": 
                throw new Error(`No hay implementacion para: ${prop}`);

            case "slice": 
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
    return [...array].sort(compareFunction);
}

// Filter function
function dataArrayFilter(array, filterFunction) {
    return [...array].filter(filterFunction);
}

// Map function
function dataArrayMap(array, mapFunction) {
    return [...array].map(mapFunction);
}

// Slice function
function dataArraySlice(array, start, end) {
    return [...array].slice(start, end);
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

    return grouped;
}

// Distinct function
function dataArrayDistinct(array) {
    return Array.from(new Set(array));
}

// Where function
function dataArrayWhere(array, predicate) {
    return array.filter(predicate);
}

