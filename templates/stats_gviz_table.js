{% spaceless %}
// This script is included in stats_gviz_table.html and stats_table.js

var bsResultsTable = function(id) {

  this.tableContainer_ = document.getElementById(id);

  // ua detection
  var script = document.createElement('script');
  script.src = '//{{ server }}/ua?o=js';
  script.id = 'bs-ua-script';
  this.tableContainer_.parentNode.appendChild(script);

  // jsapi - load it only once
  if (!document.getElementById(bsResultsTable.JSAPI_ID)) {
    script = document.createElement('script');
    script.id = bsResultsTable.JSAPI_ID;
    var instance = this;
    var scriptLoaded = false;

    // script onload for IE
    script.onreadystatechange = function() {
      if (!scriptLoaded &&
          (this.readyState == 'loaded' || this.readyState == 'complete')) {
        scriptLoaded = true;
        instance.loadGvizTableApi();
      }
    };

    // script.onload
    script.onload = function() {
      instance.loadGvizTableApi();
    };

    script.src = '//www.google.com/jsapi';
    this.tableContainer_.parentNode.insertBefore(script, this.tableContainer_);
  } else {
    this.load();
  }

};

bsResultsTable.JSAPI_ID = 'bs-jsapi';


bsResultsTable.prototype.loadGvizTableApi = function() {
  var instance = this;
  google.load('visualization', '1',
        {'packages': ['table'],
          'callback': function() {
            instance.load();
          }
        });
};


bsResultsTable.prototype.load = function() {
  bsUtil.addClass(this.tableContainer_, 'rt-loading');
  this.tableContainer_.innerHTML = 'Loading Browserscope results data ...';
  var dataUrl = '//{{ server }}/gviz_table_data?' +
      'category={{ category }}&' +
      'ua={{ ua_params }}&' +
      'v={{ v }}&' +
      'o=gviz_data&' +
      'mem={{ mem }}&' +
      'f={{ f }}&' +
      'highlight={{ highlight }}&' +
      'score={{ score }}&' +
      'tqx=reqId:0';
  var query = new google.visualization.Query(dataUrl,
      {'sendMethod': 'scriptInjection'});
  var instance = this;
  query.send(function(response){instance.draw_(response)});
};

bsResultsTable.prototype.draw_ = function(response) {
  if (response.isError()) {
    alert('Sorry but there was an error getting the results data ' +
          'from Browserscope.');
  }
  bsUtil.removeClass(this.tableContainer_, 'rt-loading');
  var dataTable = new google.visualization.Table(this.tableContainer_);
  var data = response.getDataTable();
  var cssClassNames = {
    headerRow: '',
    hoverTableRow: 'rt-row rt-row-over',
    selectedTableRow: 'rt-row rt-row-sel',
    tableRow: 'rt-row',
    frozenColumns: 1
  };
  dataTable.draw(data, {
    {% if w %}'width': '{{ w }}',{% endif %}
    {% if h %}'height': '{{ h }}',{% endif %}
    'alternatingRowStyle': false,
    'cssClassNames': cssClassNames
  });

  // Bail before more interesting UI enhancements if old UA.
  if (!document.querySelectorAll) {
    return;
  }

  var that = this;
  window.setTimeout(function() {
    that.resultsCells_ = that.tableContainer_.querySelectorAll(
        '.rt-row td:last-child');
    that.drawCompareUaUi_();
    that.drawSparseFilter_();
  }, 200);
};

bsResultsTable.prototype.drawCompareUaUi_ = function() {
  var that = this;

  var uaCells = this.tableContainer_.querySelectorAll(
      'tr.rt-row > td:first-child');
  var cbClone = document.createElement('input');
  cbClone.type = 'checkbox';
  cbClone.className = 'rt-compare-cb';
  var cbClick = function(e) {
    var row = this.parentNode.parentNode;
    row.setAttribute('data-compare-ua', this.checked ? '1' : '0');
  };
  for (var i = 0, uaCell; uaCell = uaCells[i]; i++) {
    var uaString = uaCell.innerText || uaCell.textContent;
    uaCell.parentNode.setAttribute('data-ua', uaString);
    var cb = cbClone.cloneNode(true);
    cb.id = 'rt-compare-cb-' + i;
    cb.onclick = cbClick;
    uaCell.innerHTML = '';
    uaCell.appendChild(cb);
    var uaLabel = document.createElement('label');
    uaLabel.setAttribute('for', cb.id);
    uaLabel.appendChild(document.createTextNode(uaString));
    uaCell.appendChild(uaLabel);
  }

  // Compare Button
  this.compareBtn_ = document.createElement('button');
  this.compareBtn_.type = 'button';
  this.compareBtn_.appendChild(document.createTextNode('Compare'));
  this.compareBtn_.className = 'rt-compare-btn';
  this.compareBtn_.onclick = function(e) {
    bsUtil.addClass(that.tableContainer_, 'rt-compare-active');
    bsUtil.removeClass(that.tableContainer_, 'rt-compare');
  };
  this.tableContainer_.appendChild(this.compareBtn_);

  // Compare Undo Link
  this.compareUndo_ = document.createElement('span');
  this.compareUndo_.className = 'rt-compare-undo rt-link';
  this.compareUndo_.innerHTML = 'Undo compare';
  this.tableContainer_.appendChild(this.compareUndo_);
  this.compareUndo_.onclick = function(e) {
    var prevComparedRows = that.tableContainer_.querySelectorAll(
        'tr[data-compare-ua="1"]');
    for (var i = 0, row; row = prevComparedRows[i]; i++) {
      row.setAttribute('data-compare-ua', '0');
    }
    bsUtil.removeClass(that.tableContainer_, 'rt-compare-active');
  };

  // Compare Link
  this.compareLink_ = document.createElement('span');
  this.compareLink_.className = 'rt-compare-link rt-link';
  this.compareLink_.innerHTML = 'Compare UAs';
  this.tableContainer_.appendChild(this.compareLink_);
  this.compareLink_.onclick = function(e) {
    bsUtil.addClass(that.tableContainer_, 'rt-compare');
  };
};

bsResultsTable.prototype.drawSparseFilter_ = function() {
  // Add result links and set count data attr.
  for (var i = 0, cell; cell = this.resultsCells_[i]; i++) {
    var resultCount = cell.innerText || cell.textContent;
    cell.setAttribute('data-count', resultCount);
    var uaString = cell.parentNode.getAttribute('data-ua');
    cell.innerHTML = '<a href="//{{ server }}/browse?' +
        'category={{ category }}&' +
        'ua=' + encodeURIComponent(uaString) +
        '">' + resultCount + '</a>';
  }
  var that = this;
  this.filterLink_ = document.createElement('span');
  this.filterLink_.className = 'rt-filter-link rt-link';
  this.filterLink_.innerHTML = 'Sparse filter';
  this.tableContainer_.appendChild(this.filterLink_);
  this.filterLink_.onclick = function(e) {
    bsUtil.addClass(that.tableContainer_, 'rt-filter');
  };

  this.filterBtn_ = document.createElement('button');
  this.filterBtn_.type = 'button';
  this.filterBtn_.appendChild(document.createTextNode('Hide < '));
  this.filterBtn_.className = 'rt-filter-btn';
  this.filterBtn_.onclick = function() {
    var sparseValue = Number(that.filterInput_.value);
    for (var i = 0, cell; cell = that.resultsCells_[i]; i++) {
      var resultCount = Number(cell.getAttribute('data-count'));
      cell.parentNode.setAttribute('data-filter',
          resultCount < sparseValue ? '1' : '0');
    }
    bsUtil.removeClass(that.tableContainer_, 'rt-filter');
    bsUtil.addClass(that.tableContainer_, 'rt-filter-active');

  };
  this.tableContainer_.appendChild(this.filterBtn_);

  this.filterInput_ = document.createElement('input');
  this.filterInput_.className = 'rt-filter-input';
  this.filterInput_.value = '4';
  this.tableContainer_.appendChild(this.filterInput_);

  this.filterUndo_ = document.createElement('span');
  this.filterUndo_.className = 'rt-filter-undo rt-link';
  this.filterUndo_.innerHTML = 'Undo filter';
  this.tableContainer_.appendChild(this.filterUndo_);
  this.filterUndo_.onclick = function(e) {
    bsUtil.removeClass(that.tableContainer_, 'rt-filter-active');
  };

};

var bsUtil = {};
bsUtil.hasClass = function(el, className) {
  return el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
};
bsUtil.addClass = function(el, className) {
  if (!bsUtil.hasClass(el, className)) {
    el.className += ' ' + className;
  }
};
bsUtil.removeClass = function(el, className) {
  if (bsUtil.hasClass(el, className)) {
    var regExp = new RegExp('(\\s|^)' + className + '(\\s|$)');
    el.className = el.className.replace(regExp, ' ');
  }
};
{% endspaceless %}

