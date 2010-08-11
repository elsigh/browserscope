(function() {
    var getJsUaOverrides = function() {
      var jsUa, jsFamilyName, jsV1, jsV2, jsV3;
      var isIE = navigator.userAgent.indexOf('MSIE') != -1;
      if (isIE && typeof document.documentMode != 'undefined') {
        if (window.external == null) {
            jsFamilyName = 'IE Platform Preview';
            jsV1 = '9';
            jsV2 = '0';
          // Based on the code at
          // http://ie.microsoft.com/testdrive/HTML5/DOMCapabilities/demo.js
          if (Object.getPrototypeOf(document.createElement('div')) ==
              HTMLDivElement.prototype) {
            jsV3 = '4';
          } else if (typeof Array.prototype.indexOf != 'undefined') {
            jsV3 = '3';
          } else if (typeof document.getElementsByClassName != 'undefined') {
            jsV3 = '2';
          } else {
            jsV3 = '1';
          }
        }
        else if (document.documentMode == 9) {
          if (window.navigator.appMinorVersion.indexOf("beta") > -1) {
            jsFamilyName = 'IE Beta';
            jsV1 = '9';
            jsV2 = '0';
            jsV3 = 'beta';
          }
        }
      }
      if (jsFamilyName) {
        // Keys match the params that our server expects.
        jsUa = {
          'js_user_agent_family': jsFamilyName,
          'js_user_agent_v1': jsV1,
          'js_user_agent_v2': jsV2,
          'js_user_agent_v3': jsV3
        };
      }

      return jsUa;
    };

    var test_key = '{{ test_key }}';
    var csrf_token = '{{ csrf_token }}';
    if (!_bTestResults) {
      alert('var _bTestResults is empty, so no Browserscope ' +
            'data beacon will happen.');
      return;
    }
    var results = [];
    for (var key in _bTestResults) {
      var val = _bTestResults[key];
      results.push(key + '=' + val);
    }
    if (!results.length) {
      alert('var _bTestResults is empty, so no Browserscope ' +
            'data beacon will happen.');
      return;
    }

    var iframe = document.createElement('iframe');
    iframe.setAttribute('width', '0');
    iframe.setAttribute('height', '0');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('name', 'browserscope');
    iframe.id = 'browserscope';
    iframe.src = 'about:blank';
    document.body.appendChild(iframe);
    iframe = document.all ? document.all.browserscope.contentWindow :
        window.frames.browserscope;
    var iframeDoc = iframe.document;
    iframeDoc.open();
    iframeDoc.writeln('<html><body></body></html>');
    iframeDoc.close();

    var form = iframeDoc.createElement('form');
    form.action = 'http://{{ server }}/beacon/{{ test_key }}';
    form.method = 'post';
    var inputs = {
      'test_key': test_key,
      'csrf_token': csrf_token,
      'category': 'usertest_{{ test_key }}',
      'results': results.join(','){% if sandboxid %},
      'sandboxid': '{{ sandboxid }}'{% endif %}
    };
    for (key in inputs) {
      var input = iframeDoc.createElement('input');
      input.type = 'hidden';
      input.name = key;
      input.value = inputs[key];
      form.appendChild(input);
    }

    // JS UA overrides
    // Needed to detect IE 9 preview.
    var jsUa = getJsUaOverrides();
    if (jsUa) {
      for (var key in jsUa) {
        var input = iframeDoc.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = jsUa[key];
        form.appendChild(input);
      }
    }

    iframeDoc.body.appendChild(form);
    form.submit();

    {% if callback %}
      window.setTimeout({{ callback }}, 50);
    {% endif %}
})();
