(function(){

  // Adds the CSS to the DOM.
  var cssNode = document.createElement('link');
  cssNode.rel = 'stylesheet';
  cssNode.type = 'text/css';
  cssNode.href = 'http://{{ server }}/static/results_table.css';
  var headEl = document.getElementsByTagName('head')[0];
  headEl.appendChild(cssNode);

  var resultsTable = document.createElement('div');
  resultsTable.className = 'bs-results-usertest';
  resultsTable.innerHTML = '{% filter escapejs %}{% spaceless %}
  {% if message %}
    <p class="d-msg">{{ message }}</p>
  {% endif %}
  <div id="bs-results" class="bs-usertest">
    <ul id="bs-results-bycat" class="bs-results-bycat bs-compact">
      <li id="usertest_{{ test.key }}-results">
        <h3>
        <a href="http://{{ server }}/user/tests/table/{{ test.key }}"
          >{{ test.name }}</a>
        </h3>
        {% if test.description %}
          <p>{{ test.description }}</p>
        {% endif %}
        {{ stats_table|safe }}
      </li>
    </ul>
  </div>{% endspaceless %}{% endfilter %}';

  // Adds the table HTML to the DOM.
  var scripts = document.getElementsByTagName('script');
  var lastScript = scripts[scripts.length - 1];
  lastScript.parentNode.insertBefore(resultsTable, lastScript);

})();


