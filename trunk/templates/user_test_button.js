(function() {

  // Adds the CSS to the DOM.
  var cssNode = document.createElement('link');
  cssNode.rel = 'stylesheet';
  cssNode.type = 'text/css';
  cssNode.href = 'http://{{ server }}/static/button.css';
  var headEl = document.getElementsByTagName('head')[0];
  headEl.appendChild(cssNode);

  var runTestEl = document.createElement('div');
  runTestEl.id = 'bs-run';

  runTestButton = document.createElement('button');
  runTestButton.className = 'bs-btn';
  runTestButton.innerHTML = '{{ btn_text|escapejs }}';
  runTestButton.onclick = {{ fn }};
  runTestEl.appendChild(runTestButton);

  var sendToBrowserscopeLabel = document.createElement('label');
  sendToBrowserscopeLabel.setAttribute('for', 'bs-send');

  sendToBrowserscopeCheckbox = document.createElement('input');
  sendToBrowserscopeCheckbox.id = 'bs-send';
  sendToBrowserscopeCheckbox.type = 'checkbox';
  sendToBrowserscopeCheckbox.checked = true; // defaults to yes

  sendToBrowserscopeLabel.appendChild(sendToBrowserscopeCheckbox);
  sendToBrowserscopeLabel.appendChild(document.createTextNode(
      ' {{ cb_text|escapejs }}'));

  runTestEl.appendChild(sendToBrowserscopeLabel);

  var scripts = document.getElementsByTagName('script');
  var lastScript = scripts[scripts.length - 1];
  lastScript.parentNode.insertBefore(runTestEl, lastScript);

})();

