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
     '<strong>' + reconciledUa + '</strong>';
  var script = document.getElementById('bs-ua-script');
  if (!script) {
    var scripts = document.getElementsByTagName('script');
    script = scripts[scripts.length - 1];
  }
  script.parentNode.insertBefore(el, script);
})();
