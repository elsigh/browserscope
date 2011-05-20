(function() {
    {{ js_ua_override|safe }}

    var test_key = '{{ test_key }}';
    var csrf_token = '{{ csrf_token }}';
    if (!{{ test_results_var }}) {
      alert('window.{{ test_results_var }} is empty, so no Browserscope ' +
            'data beacon will happen.');
      return;
    }
    var results = [];
    for (var key in {{ test_results_var }}) {
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
    for (key in inputs) {
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
