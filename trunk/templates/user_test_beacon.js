(function() {
    var test_key = '{{ test_key }}';
    var csrf_token = '{{ csrf_token }}';
    var callback = '{{ callback }}';
    var script = document.createElement('script');
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
    var url = 'http://{{ server }}/beacon?category=usertest_{{ test_key }}&' +
        'csrf_token=' + csrf_token + '&' +
        'callback=' + callback + '&' +
        'results=' + results.join(',');
    script.src = url;
    script.setAttribute('async', 'true');
    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length - 1];
    lastScript.parentNode.insertBefore(script, lastScript);
})();
