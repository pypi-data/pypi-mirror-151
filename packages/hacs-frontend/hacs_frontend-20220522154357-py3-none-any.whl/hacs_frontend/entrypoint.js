
try {
  new Function("import('/hacsfiles/frontend/main-e2f8045a.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-e2f8045a.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  