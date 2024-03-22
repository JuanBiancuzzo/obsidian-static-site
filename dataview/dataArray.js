
export const dataArrayProxyHandler = {

  get: function(target, prop, receiver) {
    if (prop === 'sort')
        return (compareFunction) => dataArraySort(target, compareFunction);

    if (prop === 'groupBy') 
        return (keyGetter) => dataArrayGroupBy(target, keyGetter);

    if (prop === 'distinct')
        return () => dataArrayDistinct(target);

    if (prop === 'where') 
        return (predicate) => dataArrayWhere(target, predicate);
    
    return Reflect.get(...arguments);
  }

};

// Sort function
function dataArraySort(array, compareFunction) {
  return [...array].sort(compareFunction);
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

