(function() {
  var el = document.createElement('div');
  el.id = 'bs-ua';
  el.innerHTML = 'UA Parser thinks you are using ' +
     '<strong>{{ current_ua.prettyUA }}</strong>' +
     '&nbsp;&nbsp;<a ' +
       'href="http://code.google.com/p/ua-parser/issues/entry?template=' +
       'UA%20Parsing%20Is%20Incorrect&comment={{ current_ua.prettyUA }} is ' +
       'not correct for {{ current_ua_string }}"' +
       'target="_blank">No?</a>';
  var script = document.getElementById('bs-ua-script');
  if (!script) {
    var scripts = document.getElementsByTagName('script');
    script = scripts[scripts.length - 1];
  }
  script.parentNode.insertBefore(el, script);
})();
