(function(window) {
    {{ js_ua_override|safe }}

    /**
     * Thanks JD Dalton, this hasKey routine is copied from
     * https://github.com/bestiejs/waldo/blob/master/waldo.js#L153-195
     * Checks if an object has the specified key as a direct property.
     * @private
     * @param {Object} object The object to check.
     * @param {String} key The key to check for.
     * @returns {Boolean} Returns `true` if key is a direct property,
     * else `false`.
     */
    function hasKey() {
      // lazy define for modern browsers
      if (isFunction(hasOwnProperty)) {
        hasKey = function(object, key) {
          return hasOwnProperty.call(Object(object), key);
        };
      }
      // or for Safari 2
      else if ({}.__proto__ == Object.prototype) {
        hasKey = function(object, key) {
          var result;
          object = Object(object);
          object.__proto__ = [object.__proto__, object.__proto__ =
              null, result = key in object][0];
          return result;
        };
      }
      // or for others (not as accurate)
      else {
        hasKey = function(object, key) {
          object = Object(object);
          var parent = (object.constructor || Object).prototype;
          return key in object && !(key in parent &&
              object[key] === parent[key]);
        };
      }
      // or for an Opera < 10.53 bug, found by Garrett Smith, that occurs with
      // window objects and not the global `this`
      if (window.window == window && !hasKey(window.window, 'Object')) {
        var __hasKey = hasKey;
        hasKey = function(object, key) {
          return object == window
            ? key in object && object[key] !== {}[key]
            : __hasKey(object, key);
        };
      }
      return hasKey.apply(null, arguments);
    }
    var hasOwnProperty = {}.hasOwnProperty;
    var toString = {}.toString;
    function isFunction(value) {
      return toString.call(value) == '[object Function]';
    }


    /**
     * Browserscope-specific code.
     */
    var test_key = '{{ test_key }}';
    var csrf_token = '{{ csrf_token }}';
    if (!{{ test_results_var }}) {
      alert('window.{{ test_results_var }} is empty, so no Browserscope ' +
            'data beacon will happen.');
      return;
    }
    var results = [];
    for (var key in {{ test_results_var }}) {
      if (!hasKey({{ test_results_var }}, key)) {
        continue;
      }
      var val = {{ test_results_var }}[key];
      results.push(key + '=' + val);
    }
    if (!results.length) {
      alert('{{ test_results_var }} is empty, so no Browserscope ' +
            'data beacon will happen.');
      return;
    }

    var iframe = document.createElement('iframe');
    iframe.setAttribute('width', '0');
    iframe.setAttribute('height', '0');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('name', 'browserscope-{{ epoch }}');
    iframe.id = 'browserscope-{{ epoch }}';
    iframe.src = 'about:blank';
    document.body.appendChild(iframe);
    iframe = document.all ?
        document.all['browserscope-{{ epoch }}'].contentWindow :
        window.frames['browserscope-{{ epoch }}'];
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
    for (var key in inputs) {
      if (!hasKey(inputs, key)) {
        continue;
      }
      var input = iframeDoc.createElement('input');
      input.type = 'hidden';
      input.name = key;
      input.value = inputs[key];
      form.appendChild(input);
    }

    // JS UA overrides
    // Needed to detect IE 9 preview.
    var jsUa = uap.getJsUaOverrides();
    if (jsUa) {
      for (var key in jsUa) {
        if (!hasKey(jsUa, key)) {
          continue;
        }
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
})(this);
