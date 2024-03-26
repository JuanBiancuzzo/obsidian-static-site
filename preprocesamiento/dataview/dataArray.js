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

class DataArray {
    constructor(array) {
        this.array = array;
    }
    // Sort function
    sort(elementToValue, dir = 'asc') {
        let compareFunction;
        if (dir == 'desc') {
            compareFunction = function (a, b) {
                return elementToValue(b) - elementToValue(a);
            }
        } else {
            compareFunction = function (a, b) {
                return elementToValue(a) - elementToValue(b);
            }
        }
        return new DataArray(this.array.slice().sort(compareFunction));
    }

    // Filter function
    filter(filterFunction) {
        return new DataArray(this.array.filter(filterFunction));
    }

    // Map function
    flatMap(flatMapFunction) {
        return new DataArray(this.array.flatMap(flatMapFunction));
    }

    // Map function
    map(mapFunction) {
        return new DataArray(this.array.map(mapFunction));
    }

    // Slice function
    slice(start = undefined, end = undefined) {
        return new DataArray(this.array.slice(start, end));
    }

    // GroupBy function
    groupBy(keyGetter) {
        const grouped = new Map();

        this.array.slice().forEach(item => {
            const key = keyGetter(item);
            const collection = grouped.get(key) || [];
            collection.push(item);
            grouped.set(key, collection);
        });

        // values = [ { keys: "key", rows: [...] }, ... ]
        return new DataArray(Array.from(grouped).map(([key, value]) => {
            return {
                key: key,
                rows: new DataArray(value),
            };
        }));
    }

    // Distinct function
    distinct() {
        return new DataArray(Array.from(new Set(this.array)));
    }

    // Where function
    where(predicate) {
        return new Dataview(this.array.where(predicate));
    }
}

DataArray.prototype.get = function(index) {
  return this.array[index];
};

DataArray.prototype[Symbol.iterator] = function() {
    let index = -1;
    let data = this.array;

    return {
        next: () => ({ value: data[++index], done: !(index in data) })
    };
}

DataArray.prototype.length = function() {
    return this.array.length;
}
