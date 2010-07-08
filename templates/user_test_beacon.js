(function() {
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
    form.action = 'http://{{ server }}/beacon';
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

    iframeDoc.body.appendChild(form);
    form.submit();

    {% if callback %}
      window.setTimeout({{ callback }}, 50);
    {% endif %}
})();
