
// This script is included in stats_gviz_table.html and stats_table.js


var tableContainer = document.getElementById('bs-rt-{{ category }}');

// Store a reference to the initialize function in this closure on the DOM
// node for the results table for external use, i.e. in JSPerf.
tableContainer.refresh = initialize;

// ua
var script = document.createElement('script');
script.src = '//{{ server }}/ua?o=js';
script.id = 'bs-ua-script';
tableContainer.parentNode.appendChild(script);

// jsapi
script = document.createElement('script');
script.src = '//www.google.com/jsapi';
script.onload = function() {
  google.load('visualization', '1',
    {'packages': ['table'], 'callback': initialize});
}
tableContainer.parentNode.insertBefore(script, tableContainer);

function initialize() {
  tableContainer.innerHTML = 'Loading Browserscope results data ...';
  tableContainer.className = 'rt-loading';
  var dataUrl = '//{{ server }}/gviz_table_data?' +
      'category={{ category }}&' +
      'ua={{ ua_params }}&' +
      'v={{ v }}&' +
      'o=gviz_data&' +
      'highlight={{ highlight }}&' +
      'score={{ score }}&' +
      'tqx=reqId:0';
  var query = new google.visualization.Query(dataUrl,
      {'sendMethod': 'scriptInjection'});
  query.send(draw);
}

function draw(response) {
  if (response.isError()) {
    alert('Sorry but there was an error getting the results data ' +
          'from Browserscope.');
  }
  tableContainer.className = ''; // remove loading.
  var dataTable = new google.visualization.Table(tableContainer);
  var data = response.getDataTable();
  var cssClassNames = {
    headerRow: '',
    hoverTableRow: '',
    selectedTableRow: '',
    tableRow: 'rt-row',
    frozenColumns: 1
  };
  dataTable.draw(data, {
    {% if w %}'width': '{{ w }}',{% endif %}
    {% if h %}'height': '{{ h }}',{% endif %}
    'alternatingRowStyle': false,
    'cssClassNames': cssClassNames
  });
}

