
// This script is included in stats_gviz_table.html and stats_table.js

var bsResultsTable = function(id) {

  this.tableContainer_ = document.getElementById(id);

  // ua
  var script = document.createElement('script');
  script.src = '//{{ server }}/ua?o=js';
  script.id = 'bs-ua-script';
  this.tableContainer_.parentNode.appendChild(script);

  // jsapi - load it only once
  if (!document.getElementById(bsResultsTable.JSAPI_ID)) {
    script = document.createElement('script');
    script.id = bsResultsTable.JSAPI_ID;
    script.src = '//www.google.com/jsapi';
    var instance = this;
    script.onload = function() {
      google.load('visualization', '1',
        {'packages': ['table'],
          'callback': function() {
            instance.load();
          }
        })
    };
    this.tableContainer_.parentNode.insertBefore(script, this.tableContainer_);
  } else {
    this.load();
  }

};

bsResultsTable.JSAPI_ID = 'bs-jsapi';

bsResultsTable.prototype.load = function() {
  this.tableContainer_.className = 'rt-loading';
  this.tableContainer_.innerHTML = 'Loading Browserscope results data ...';
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
  var instance = this;
  query.send(function(response){instance.draw_(response)});
}

bsResultsTable.prototype.draw_ = function(response) {
  if (response.isError()) {
    alert('Sorry but there was an error getting the results data ' +
          'from Browserscope.');
  }
  this.tableContainer_.className = ''; // remove loading.
  var dataTable = new google.visualization.Table(this.tableContainer_);
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

