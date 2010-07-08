(function() {
  var el = document.createElement('div');
  el.id = 'bs-ua';
  el.innerHTML = 'Browserscope thinks you are using ' +
     '<strong>{{ current_ua.pretty }}</strong> ' +
     '<a ' +
       'href="http://code.google.com/p/browserscope/issues/entry?template=' +
       'UA%20Parsing%20Is%20Incorrect&comment={{ current_ua.pretty }} is ' +
       'not {{ current_ua_string }}"' +
       'target="_blank">No?</a>';
  var scripts = document.getElementsByTagName('script');
  var lastScript = scripts[scripts.length - 1];
  lastScript.parentNode.insertBefore(el, lastScript);
})();
