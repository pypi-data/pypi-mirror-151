
try {
    new Function("import('/reactfiles/frontend/main-122e34bf.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main-122e34bf.js';
    el.type = 'module';
    document.body.appendChild(el);
}
