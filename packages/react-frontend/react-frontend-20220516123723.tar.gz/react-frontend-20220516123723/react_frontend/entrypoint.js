
try {
    new Function("import('/reactfiles/frontend/main-ac83c92b.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main-ac83c92b.js';
    el.type = 'module';
    document.body.appendChild(el);
}
