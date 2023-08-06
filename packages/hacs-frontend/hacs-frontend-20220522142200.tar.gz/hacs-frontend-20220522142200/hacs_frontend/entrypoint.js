
try {
  new Function("import('/hacsfiles/frontend/main-7b19d938.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-7b19d938.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  