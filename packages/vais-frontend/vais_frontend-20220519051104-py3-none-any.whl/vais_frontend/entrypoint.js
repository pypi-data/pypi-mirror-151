
try {
  new Function("import('/vaisfiles/frontend/main-e088bb19.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/vaisfiles/frontend/main-e088bb19.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  