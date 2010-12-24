(function() {
  {{ js_ua_override|safe }}
  var jsUa = uap.getJsUaOverrides();
  var reconciledUa = '{{ current_ua.pretty }}';
  if (jsUa) {
    reconciledUa = jsUa['js_user_agent_family'] + ' ' +
        jsUa['js_user_agent_v1'] + '.' +
        jsUa['js_user_agent_v2'] + '.' + jsUa['js_user_agent_v3'];
    reconciledUa = reconciledUa.replace('0.0', '0');
  }
  var el = document.createElement('div');
  el.id = 'bs-ua';
  el.innerHTML = 'Browserscope thinks you are using ' +
     '<strong>' + reconciledUa + '</strong>' +
     '&nbsp;&nbsp;<a ' +
       'href="http://code.google.com/p/ua-parser/issues/entry?template=' +
       'UA%20Parsing%20Is%20Incorrect&comment=' + reconciledUa + ' is ' +
       'not correct for {{ current_ua_string }}"' +
       'target="_blank">No?</a>';
  var script = document.getElementById('bs-ua-script');
  if (!script) {
    var scripts = document.getElementsByTagName('script');
    script = scripts[scripts.length - 1];
  }
  script.parentNode.insertBefore(el, script);
})();
