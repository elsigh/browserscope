
{% spaceless %}
// This script is included in stats_gviz_table.html and stats_table.js
var bsResultsTable = function(id, opt_doUaDetect) {
  var doUaDetect = (typeof opt_doUaDetect != 'undefined' ?
      opt_doUaDetect : true);

  this.tableContainer_ = document.getElementById(id);
  this.container_ = this.tableContainer_.parentNode;
  this.toolsContainer_ = document.getElementById(id + '-tools');
  this.toolsDynContainer_ = document.getElementById(id + '-tools-dyn');
  this.browserFamilySelect_ = document.getElementById(id + '-v');
  this.currentPageIndex_ = 0;

  // ua detection
  if (doUaDetect &&
      !(document.getElementById(bsResultsTable.UA_DETECT_ID))) {
    var script = document.createElement('script');
    script.src = '//{{ server }}/ua?o=js';
    script.id = bsResultsTable.UA_DETECT_ID;
    this.tableContainer_.parentNode.appendChild(script);
  }

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
bsResultsTable.UA_DETECT_ID = 'bs-ua-script';

bsResultsTable.prototype.loadGvizTableApi = function() {
  var instance = this;
  google.load('visualization', '1',
        {'packages': ['table'],
          'callback': function() {
            instance.load('{{ v }}');
          }
        });
};

bsResultsTable.prototype.getDataUrl = function(family, opt_offset) {
  var offset = opt_offset || '';
  return '//{{ server }}/gviz_table_data?' +
      'category={{ category }}&' +
      'ua={{ ua_params }}&' +
      'ua_o=' + offset + '&' +
      'ua_l={{ browser_limit }}&' +
      'v=' + family + '&' +
      'o=gviz_data&' +
      'mem={{ mem }}&' +
      'f={{ f }}&' +
      'highlight={{ highlight }}&' +
      'score={{ score }}&' +
      'tqx=reqId:0';
};

bsResultsTable.prototype.handlePage = function(properties) {
  //console.log('handlePage', properties)
  var family = 3;  // Only called when v=3
  var localTableNewPage = properties['page']; // 1, -1 or 0
  var newPage = 0;

  if (localTableNewPage != 0) {
    newPage = this.currentPageIndex_ + localTableNewPage;
  }

  if (newPage == this.currentPageIndex_) {
    return;

  } else {
    this.currentPageIndex_ = newPage;
  }

  var newIndex = newPage * Number('{{ browser_limit }}');

  bsUtil.addClass(this.tableContainer_, 'rt-loading');

  this.tableContainer_.innerHTML = 'Loading more Browserscope results data ...';
  var dataUrl = this.getDataUrl(family, newIndex);
  var query = new google.visualization.Query(dataUrl,
      {'sendMethod': 'scriptInjection'});
  var instance = this;
  query.send(function(response){instance.draw_(response, family)});
};


bsResultsTable.prototype.load = function(family) {
  bsUtil.addClass(this.tableContainer_, 'rt-loading');
  this.toolsContainer_.style.display = 'none';
  this.toolsDynContainer_.innerHTML = '';
  this.builtCompareUaUi_ = false;
  this.vizTable_ = null;
  this.tableContainer_.innerHTML = 'Loading Browserscope results data ...';
  var dataUrl = this.getDataUrl(family);
  var query = new google.visualization.Query(dataUrl,
      {'sendMethod': 'scriptInjection'});
  var instance = this;
  query.send(function(response){instance.draw_(response, family)});
};


bsResultsTable.prototype.draw_ = function(response, family) {

  bsUtil.removeClass(this.tableContainer_, 'rt-loading');
  if (response.isError()) {
    alert('Sorry but there was an error getting the results data ' +
          'from Browserscope.');
    return;
  }

  if (!this.dataTable_) {
    this.vizTable_ = new google.visualization.Table(this.tableContainer_);
    this.dataTable_ = response.getDataTable();
    this.lastPageDataTable_ = this.dataTable_;

    var addListener = google.visualization.events.addListener;
    var instance = this;
    addListener(this.vizTable_, 'page', function(properties) {
      instance.handlePage(properties);
    });

    if (this.toolsContainer_.style.display != 'block') {
      this.toolsContainer_.style.display = 'block';
      this.browserFamilySelect_.onchange = function(e) {
        var browserFamilyValue = instance.browserFamilySelect_.options[
            instance.browserFamilySelect_.options.selectedIndex].value;
        instance.load(browserFamilyValue);
      };
    }

    // Bail before more interesting UI enhancements if old UA.
    if (!document.querySelectorAll) {
      return;
    }

    window.setTimeout(function() {
      instance.resultsCells_ = instance.tableContainer_.querySelectorAll(
          '.rt-row td:last-child');
      instance.drawCompareUaUi_();
      instance.drawSparseFilter_();
    }, 300);


  // Merge new data into table.
  } else {
    this.lastPageDataTable_ = response.getDataTable();
    var currentJson = JSON.parse(this.dataTable_.toJSON());
    var newJson = JSON.parse(this.lastPageDataTable_.toJSON());
    for (var i = 0, row; row = newJson['rows'][i]; i++) {
      currentJson['rows'].push(row)
    }
    this.vizTable_.clearChart();

    this.dataTable_ = new google.visualization.DataTable(currentJson);
  }

  var cssClassNames = {
    headerRow: '',
    //hoverTableRow: 'rt-row rt-row-over',
    selectedTableRow: 'rt-row rt-row-sel',
    tableRow: 'rt-row',
    frozenColumns: 1
  };

  var tableOptions = {
    {% if w %}'width': '{{ w }}',{% endif %}
    {% if h %}'height': '{{ h }}',{% endif %}
    'alternatingRowStyle': false,
    'showRowNumber': false,
    'cssClassNames': cssClassNames,
    'page': (family == '1' || family == '2' || family == '3') ?
        'event' : 'disable',
    //'pageSize': Number('{{ browser_limit }}'),
    'pagingButtonsConfiguration': 'both'
  };

  this.vizTable_.draw(this.dataTable_, tableOptions);

  // Hide the next button maybe.
  if (this.lastPageDataTable_ &&
      this.lastPageDataTable_.getNumberOfRows() <
          Number('{{ browser_limit }}')) {
    var pageEl = document.querySelector(
        '.google-visualization-table-div-page');
    if (pageEl) {
      pageEl.style.display = 'none';
    }
  }
};

bsResultsTable.prototype.buildCompareUaUi_ = function() {
  if (this.builtCompareUaUi_) {
    return;
  }
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

  this.builtCompareUaUi_ = true;
};

bsResultsTable.prototype.drawCompareUaUi_ = function() {
  var that = this;

  // Compare Link
  this.compareLink_ = document.createElement('span');
  this.compareLink_.className = 'rt-compare-link rt-link';
  this.compareLink_.innerHTML = 'Compare UAs';
  this.toolsDynContainer_.appendChild(this.compareLink_);
  this.compareLink_.onclick = function(e) {
    that.buildCompareUaUi_();
    bsUtil.addClass(that.container_, 'rt-compare');
  };

  // Compare Button
  this.compareBtn_ = document.createElement('button');
  this.compareBtn_.type = 'button';
  this.compareBtn_.appendChild(document.createTextNode('Compare'));
  this.compareBtn_.className = 'rt-compare-btn';
  this.compareBtn_.onclick = function(e) {
    bsUtil.removeClass(that.container_, 'rt-compare');
    bsUtil.addClass(that.container_, 'rt-compare-active');
    var rows = that.tableContainer_.querySelectorAll('tr');
    // force reflow sad :(
    // was necessary in Chrome 13
    for (var i = 0, row; row = rows[i]; i++) {
      row.className = row.className;
    }
  };
  this.toolsDynContainer_.appendChild(this.compareBtn_);

  // Compare Undo Link
  this.compareUndo_ = document.createElement('span');
  this.compareUndo_.className = 'rt-compare-undo rt-link';
  this.compareUndo_.innerHTML = 'Undo compare';
  this.toolsDynContainer_.appendChild(this.compareUndo_);
  this.compareUndo_.onclick = function(e) {
    var prevComparedRows = that.tableContainer_.querySelectorAll(
        'tr[data-compare-ua="1"]');
    for (var i = 0, row; row = prevComparedRows[i]; i++) {
      row.setAttribute('data-compare-ua', '0');
      row.querySelectorAll('input[type="checkbox"]')[0].checked = false;
    }
    bsUtil.removeClass(that.container_, 'rt-compare-active');
  };
};

bsResultsTable.prototype.drawSparseFilter_ = function() {
  // Add result links and set count data attr.
  for (var i = 0, cell; cell = this.resultsCells_[i]; i++) {
    var resultCount = cell.innerText || cell.textContent;
    cell.setAttribute('data-count', resultCount);
    if (resultCount > 0) {
      var uaString = cell.parentNode.getAttribute('data-ua');
      cell.innerHTML = '<a href="//{{ server }}/browse?' +
          'category={{ category }}&' +
          'ua=' + encodeURIComponent(uaString) +
          '">' + resultCount + '</a>';
    }
  }
  var that = this;
  this.filterLink_ = document.createElement('span');
  this.filterLink_.className = 'rt-filter-link rt-link';
  this.filterLink_.innerHTML = 'Sparse filter';
  this.toolsDynContainer_.appendChild(this.filterLink_);
  this.filterLink_.onclick = function(e) {
    bsUtil.addClass(that.container_, 'rt-filter');
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
    bsUtil.removeClass(that.container_, 'rt-filter');
    bsUtil.addClass(that.container_, 'rt-filter-active');

  };
  this.toolsDynContainer_.appendChild(this.filterBtn_);

  this.filterInput_ = document.createElement('input');
  this.filterInput_.className = 'rt-filter-input';
  this.filterInput_.value = '4';
  this.toolsDynContainer_.appendChild(this.filterInput_);

  this.filterUndo_ = document.createElement('span');
  this.filterUndo_.className = 'rt-filter-undo rt-link';
  this.filterUndo_.innerHTML = 'Undo filter';
  this.toolsDynContainer_.appendChild(this.filterUndo_);
  this.filterUndo_.onclick = function(e) {
    bsUtil.removeClass(that.container_, 'rt-filter-active');
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
