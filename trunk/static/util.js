/*
 * Copyright 2009 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * @fileoverview Shared javascript.
 * @author elsigh@google.com (Lindsey Simon)
 */


goog.provide('Util');
goog.provide('Util.ResultTablesController');
goog.provide('Util.ResultTable');
goog.provide('Util.TestDriver');

goog.require('goog.dom');
goog.require('goog.events');
goog.require('goog.net.XhrIo');
goog.require('goog.net.cookies');
goog.require('goog.ui.TableSorter');
goog.require('goog.ui.Tooltip');
goog.require('goog.uri.utils');
goog.require('goog.userAgent');


/**
 * Adds CSS text to the DOM.
 * @param {string} cssText The css text to add.
 * @param {string} opt_id The id for the new stylesheet element.
 * @return {Element} cssNode the added css DOM node.
 */
Util.addCssText = function(cssText, opt_id) {
  var cssNode = goog.dom.createElement('style');
  cssNode.type = 'text/css';
  cssNode.id = opt_id ? opt_id : 'cssh-sheet-' + document.styleSheets.length;

  var headEl = document.getElementsByTagName('head')[0];
  headEl.appendChild(cssNode);

  // IE
  if (cssNode.styleSheet) {
    cssNode.styleSheet.cssText = cssText;
  // W3C
  } else {
    cssText = goog.dom.createTextNode(cssText);
    cssNode.appendChild(cssText);
  }

  return cssNode;
};


/**
 * Preserve scope in timeouts.
 * @param {Object} scope
 * @param {Function} fn
 * @return {Function}
 */
Util.curry = function(scope, fn) {
  scope = scope || window;
  var args = [];
  for (var i = 2, len = arguments.length; i < len; ++i) {
    args.push(arguments[i]);
  };
  return function() {
    fn.apply(scope, args);
  };
};


/**
 * @return {boolean} true if IE, false otherwise.
 */
Util.isInternetExplorer = function() {
   return /msie/i.test(navigator.userAgent) &&
       !/opera/i.test(navigator.userAgent);
};


/**
 * Read url param value from href.
 * @param {string} param The param to look for.
 * @param {boolean} opt_win Use top instead of the current window.
 * @param {boolean} opt_url Use url instead of location.href.
 * @return {string} The value of the param or an empty string.
 * @export
 */
Util.getParam = function(param, opt_win, opt_url) {
  var win = opt_win || window;
  var url = opt_url || win.location.href
  param = param.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]');
  var regexString = '[\\?&]' + param + '=([^&#]*)';
  var regex = new RegExp(regexString);
  var results = regex.exec(url);
  if (results == null) {
    return '';
  } else {
    return results[1];
  }
};


/**
 * @param {string} iframeId
 * @return {?string} The iframe's id.
 * @export
 */
Util.getIframeDocument = function(iframeId) {
  var doc;
  var iframe = window.frames[iframeId];
  if (!iframe) {
    iframe = goog.dom.$(iframeId);
  }
  if (!iframe) {
    return null;
  }
  if (iframe.contentDocument) {
    // For NS6
    doc = iframe.contentDocument;
  } else if (iframe.contentWindow) {
    // For IE5.5 and IE6
    doc = iframe.contentWindow.document;
  } else if (iframe.document) {
    // For IE5
    doc = iframe.document;
  }
  return doc;
};

/**
 * @type {string}
 */
Util.COOKIE_CHROME_FRAME = 'browserscope-chromeframe-enabled';


/**
 * @return {Element} container with the checkbox.
 * @export
 */
Util.createChromeFrameCheckbox = function(serverUaString, opt_reloadOnChange) {
  var reloadOnChange = opt_reloadOnChange || false;
  var ua = goog.userAgent.getUserAgentString();
  if (serverUaString.indexOf('chromeframe') != -1) {
    var container = goog.dom.createElement('strong');
    container.id = 'bs-cf-c';
    var cb = goog.dom.createElement('input');
    cb.id = 'bs-cf-enabled';
    cb.type = 'checkbox';
    var chromeFrameEnabled = goog.net.cookies.get(Util.COOKIE_CHROME_FRAME);
    cb.checked = chromeFrameEnabled == '1';
    goog.events.listen(cb, 'click', function(e) {
      var cb = e.currentTarget;
      goog.net.cookies.set(Util.COOKIE_CHROME_FRAME, cb.checked ? '1' : '0');
      if (reloadOnChange) {
        window.top.location.href = window.top.location.href;
      }
    });
    var label = goog.dom.createElement('label');
    label.setAttribute('for', cb.id);
    label.innerHTML = 'Run in Chrome Frame';

    container.appendChild(cb);
    container.appendChild(label);
    return container;
  }
};


/**
 * @param {string} httpUserAgent A full user agent string - HTTP_USER_AGENT
 * @param {string} userAgentPretty A parsed Family v1.v2.v3 string
 */
Util.reconcileClientServerUaPretty = function(httpUserAgent, userAgentPretty) {
  var ua = goog.userAgent.getUserAgentString();
  var reconciledUa = userAgentPretty;
  // Chrome Frame detection, i.e. server side UA string and client
  // are in mismatch.
  // @see http://code.google.com/p/chromium/issues/detail?id=22997
  if (httpUserAgent.indexOf('chromeframe') != -1 &&
      ua.indexOf('chromeframe') == -1) {
    reconciledUa = 'Chrome Frame (' + userAgentPretty + ')';
  }
  return reconciledUa;
};

Util.alphaCaseInsensitiveCompare = function(a, b) {
  // turns 9/10 into 9
  if (a.match(/\//) && b.match(/\//)) {
    a = a.replace(/\/.*/, '');
    b = b.replace(/\/.*/, '');
    return goog.ui.TableSorter.numericSort(a, b);
  } else {
    a = a.toLowerCase();
    b = b.toLowerCase();
    return a > b ? 1 : a < b ? -1 : 0;
  }
};

/*****************************************/



/**
 * @param {string} category The current category.
 * @param {string} browserFamily The current browserFamily.
 * @param {string} realUaString The actual user agent string.
 * @param {string} uaUriParams ua=foo,bar etc..
 * @param {string} resultsUriParams category_results=foo,bar etc..
 * @constructor
 */
Util.ResultTablesController = function(category, browserFamily,
    output, realUaString, uaUriParams, resultsUriParams) {

  /**
   * @type {string}
   */
  this.category = category;

  /**
   * @type {string}
   */
  this.browserFamily = browserFamily;

  /**
   * @type {string}
   */
  this.output = output == 'html' ? 'xhr': output;

  /**
   * @type {string}
   */
  this.realUaString = realUaString;

  /**
   * @type {string}
   */
  this.uaUriParams = uaUriParams;

  /**
   * @type {string}
   */
  this.resultsUriParams = resultsUriParams;

  // If we have results in the resultUriParams, scroll to them.
  if (this.resultsUriParams.indexOf('_results') !== -1) {
    window.location.hash = '#rt-' + this.category + '-cur-ua';
  }

  /**
   * @type {Element}
   */
  this.el = goog.dom.$('bs-results');

  /**
   * @type {Element}
   */
  this.resultsEl = goog.dom.$dom('div', {'className': 'bs-results-bycat'});


  /**
   * @type {Object}
   */
  this.categoryLinks = {};

  /**
   * @type {Object}
   */
  this.categoryNames = {};

  /**
   * @type {Object}
   */
  this.tables = {};

  /**
   * @type {Object}
   */
  this.resultTables = {};

  /**
   * @type {boolean}
   */
  this.xhrLoading = false;

  /**
   * @type {Array.<string>}
   */
  this.extraBrowserFamilyOpts = [];

  /**
   * @type {Element}
   */
  this.browserFamilySelect = null;

  /**
   * @type {Element}
   */
  this.outputToggle = null;

  // Initialize.
  this.resetUrl();
  this.decorate();
  this.updateExtraBrowserFamilyOpts();
};

Util.ResultTablesController.prototype.decorate = function() {
  var categoriesList = goog.dom.createElement('ul');
  categoriesList.id = 'bs-results-cats';
  categoriesList.className = 'bs-compact';

  var originalResults = goog.dom.$('bs-results-bycat');
  var containerEls = originalResults.getElementsByTagName('li');

  var initialCategoryEl;
  var aClone = goog.dom.createElement('a');
  var liClone = goog.dom.createElement('li');
  for (var i = 0, containerEl; containerEl = containerEls[i]; i++) {

    var category = containerEl.id.replace('-results', '');
    var h3 = containerEl.getElementsByTagName('h3')[0];
    var categoryName = goog.dom.getTextContent(h3);
    this.categoryNames[category] = categoryName;
    goog.dom.removeNode(h3);

    var link = aClone.cloneNode(true);
    link.href = goog.uri.utils.setParam(this.url, 'category', category);
    link.category = category;
    link.appendChild(goog.dom.createTextNode(categoryName));
    this.categoryLinks[category] = link;
    goog.events.listen(link, 'click', this.changeCategoryClickHandler, false,
        this);

    var li = liClone.cloneNode(true);
    li.appendChild(link);
    categoriesList.appendChild(li);

    // Get set up for the chosen category table.
    if (category == this.category) {
      var resultTableContainer = goog.dom.$$('div', 'rt', containerEl)[0];
      goog.style.showElement(resultTableContainer, false);
      this.tables[this.url] = resultTableContainer;
      this.categoryLinks[category].parentNode.className = 'bs-sel';
    }
  }
  goog.dom.removeNode(originalResults);
  this.el.appendChild(categoriesList);
  this.el.appendChild(this.resultsEl);

  // Inits the first ResultTable.
  this.resultsEl.appendChild(resultTableContainer);

  // Ensures a refresh doesn't make the form select look wrongly selected.
  goog.dom.$$('form', null, resultTableContainer)[0].reset();

  var select = goog.dom.$$('select', null, resultTableContainer)[0];
  this.browserFamilySelect = goog.dom.removeNode(select);
  goog.events.listen(this.browserFamilySelect, 'click',
      this.browserFamilyClickHandler, false, this);
  goog.events.listen(this.browserFamilySelect, 'change',
      this.browserFamilyChangeHandler, false, this);

  this.outputToggleXhr = goog.dom.$dom('span',
      {'className': 'bs-o-xhr bs-o-sel', 'tabIndex': 0});
  this.outputToggleGviz = goog.dom.$dom('span',
      {'className': 'bs-o-gviz', 'tabIndex': 0});
  this.outputToggles = [this.outputToggleXhr, this.outputToggleGviz];
  this.outputToggle = goog.dom.$dom('span', {'className': 'bs-o'});
  goog.events.listen(this.outputToggle, 'click',
      this.outputToggleClickHandler, false, this);
  this.outputToggle.appendChild(this.outputToggleXhr);
  this.outputToggle.appendChild(this.outputToggleGviz);

  this.resultTables[this.url] =
      new Util.ResultTable(this, resultTableContainer);
  goog.style.showElement(resultTableContainer, true);
};

/**
 * @param {goog.events.Event} e
 */
Util.ResultTablesController.prototype.outputToggleClickHandler = function(e) {
  var el = e.target;
  var newOutput = el.className.replace('bs-o-', '');
  if (newOutput == this.output) {
    return;
  }
  this.output = newOutput;
  this.resetUrl();
  this.updateTableDisplay();
  e.stopPropagation();
};

/**
 * @return {string} browserFamilyValue
 */
Util.ResultTablesController.prototype.getBrowserFamilyValue = function() {
  var browserFamilyValue;
  if (this.browserFamilySelect) {
    browserFamilyValue = this.browserFamilySelect.options[
        this.browserFamilySelect.options.selectedIndex].value;
  }
  return browserFamilyValue;
};

/**
 * @param {goog.events.Event} e
 */
Util.ResultTablesController.prototype.browserFamilyChangeHandler = function(e) {

  var browserFamily = this.getBrowserFamilyValue();

  // Pluck and fix uaUriParams from the browserFamily option value string.
  if (goog.uri.utils.hasParam(browserFamily, 'ua')) {
    this.uaUriParams = goog.uri.utils.getParamValue(browserFamily, 'ua');
    browserFamily = goog.uri.utils.removeParam(browserFamily, 'ua');
  } else {
    this.uaUriParams = null;
  }

  // always reset output to xhr here.
  this.output = 'xhr';

  this.setBrowserFamily(browserFamily);

  // Prevents table from sorting when changing the select.
  e.stopPropagation();
};

/**
 * Prevents table from sorting just on click.
 * @param {goog.events.Event} e
 */
Util.ResultTablesController.prototype.browserFamilyClickHandler = function(e) {
  e.stopPropagation();
};


/**
 * @param {goog.events.Event} e
 */
Util.ResultTablesController.prototype.changeCategoryClickHandler = function(e) {
  var link = e.currentTarget;
  // this is some anchor with .category
  if (this.xhrLoading || this.category == link.category) {
    e.preventDefault();
    return;
  }
  this.setCategory(link.category);
  e.preventDefault();
};

/**
 * @param {string} category
 */
Util.ResultTablesController.prototype.setCategory = function(category) {
  if (this.category) {
    this.categoryLinks[this.category].parentNode.className = '';
    goog.style.showElement(this.tables[this.url], false);
  }

  this.category = category;
  this.categoryLinks[this.category].parentNode.className = 'bs-sel';
  this.resetUrl();
  this.updateTableDisplay();
};


/**
 * @param {string} browserFamily
 */
Util.ResultTablesController.prototype.setBrowserFamily = function(
    browserFamily) {
  this.browserFamily = browserFamily;
  this.resetUrl();
  this.updateTableDisplay();
};

Util.ResultTablesController.prototype.resetUrl = function() {
  var url = Util.ResultTablesController.generateUrl(this.category,
      this.output, this.browserFamily, this.uaUriParams, this.resultsUriParams);
  this.url = url;
};

Util.ResultTablesController.prototype.hideTables = function() {
  goog.object.forEach(this.tables, function(el, url, obj) {
      if (goog.style.isElementShown(el)) {
        goog.style.showElement(el, false);
      }
  });
};

Util.ResultTablesController.prototype.updateTableDisplay = function() {
  this.hideTables();

  for (var i = 0, el; el = this.outputToggles[i]; i++) {
    if (goog.dom.classes.has(el, 'bs-o-' + this.output)) {
      goog.dom.classes.add(el, 'bs-o-sel');
    } else {
      goog.dom.classes.remove(el, 'bs-o-sel');
    }
  }

  if (!goog.object.containsKey(this.tables, this.url)) {
    if (this.output == 'xhr') {
      this.xhrCategoryResults();
    } else if (this.output == 'gviz') {
      this.tables[this.url] = goog.dom.$dom('div',
          {'className': 'rt'},
          goog.dom.$dom('div', {'className': 'rt-b-f'}),
          goog.dom.$dom('div', {'className': 'rt-gviz'}));
      this.resultsEl.appendChild(this.tables[this.url]);
      this.setLoading(true);
      this.resultTables[this.url] = new Util.ResultTable(this,
          this.tables[this.url]);
    }
  } else {
    goog.style.showElement(this.tables[this.url], true);
    this.resultTables[this.url].setUpBrowserFamilyForm();
  }
};

/**
 * @param {boolean} isLoading
 */
Util.ResultTablesController.prototype.setLoading = function(isLoading) {
  this.xhrLoading = isLoading;
  if (this.xhrLoading) {
    if (!this.tables[this.url]) {
      var textContent = 'Loading the ' +
          this.categoryNames[this.category] +
          ' Results ...';
      this.tables[this.url] = goog.dom.$dom('div',
          null, textContent);
      this.resultsEl.appendChild(this.tables[this.url]);
    }
    goog.dom.classes.add(this.tables[this.url], 'rt-loading');
  } else {
    goog.dom.classes.remove(this.tables[this.url], 'rt-loading');
  }
};

Util.ResultTablesController.prototype.xhrCategoryResults = function() {
  this.setLoading(true);
  goog.net.XhrIo.send(this.url, goog.bind(this.loadStatsTableCallback, this),
      'get', null, null, 15000); // 15000 = 15 second timeout
};

Util.ResultTablesController.prototype.loadStatsTableCallback = function(e) {
  var xhrio = e.target;
  this.setLoading(false);
  if (xhrio.isSuccess()) {
    var html = xhrio.getResponseText();
    this.tables[this.url].innerHTML = html;
    this.resultTables[this.url] =
        new Util.ResultTable(this, this.tables[this.url]);

  } else {
    this.tables[this.url].className = 'rt-err';
    this.tables[this.url].innerHTML =
        '<div>Crud. We encountered a problem on our server.</div>' +
        '<div>We are aware of the issue, and apologize.</div>';
    var link = goog.dom.createElement('a');
    link.category = this.category;
    goog.events.listen(link, 'click', this.xhrCategoryResults, false,
        this);
    link.href = this.url;
    link.innerHTML = 'Feel free to try again.';
    this.tables[this.url].appendChild(link);
  }
};

/**
 * @param {string} opt_category
 * @param {string} opt_browserFamily
 * @param {string} opt_uaUriParams
 */
Util.ResultTablesController.prototype.generateBrowserFamilyTableKey = function(
    opt_browserFamily, opt_uaUriParams) {
  var browserFamily = goog.isDef(opt_browserFamily) ? opt_browserFamily :
      this.browserFamily;
  var uaUriParams = goog.isDef(opt_uaUriParams) ? opt_uaUriParams :
      this.uaUriParams;
  var key = '';
  if (browserFamily && uaUriParams) {
    key = browserFamily + '&ua=' + uaUriParams;
  }
  return key;
};

/**
 * @param {string} browserFamily
 * @param {Array.<string>} uasToCompare
 */
Util.ResultTablesController.prototype.updateExtraBrowserFamilyOpts =
    function() {
  var key = this.generateBrowserFamilyTableKey();
  if (key && !goog.array.contains(this.extraBrowserFamilyOpts, key)) {
    this.extraBrowserFamilyOpts.push(key);
    var opts = this.browserFamilySelect.options;
    var len = this.browserFamilySelect.length
    var optionText;

    // Need to look for the ua=foo* first
    if (key.indexOf('*') !== -1) {
      optionText = goog.uri.utils.getParamValue(key, 'ua');
    } else if (goog.uri.utils.hasParam(key, 'ua')) {
      optionText = 'Compare';
    } else {
      optionText = 'Custom';
    }
    opts[len] = new Option(optionText, key);
    this.browserFamilySelect.selectedIndex = -1;
    opts[len].selected = true;
  }
};


/**
 * @param {Util.ResultTablesController} controller
 * @param {string} category
 * @param {Element} tableEl
 * @constructor
 */
Util.ResultTable = function(controller, el) {

  /**
   * @type {Util.ResultTablesController}
   */
  this.controller = controller;

  var tables = goog.dom.$$('table', 'rt-t', el);
  var gvizLines = goog.dom.$$('div', 'rt-gviz', el);

  if (tables.length) {
    this.table = tables[0];
  } else if (gvizLines.length) {
    this.gvizLineEl = gvizLines[0];
  }

  /**
   * @type {Element}
   */
  this.formContainer = goog.dom.$$('div', 'rt-b-f', el)[0];
  this.formContainer.innerHTML = '';

  this.init();
};

/**
 * @type {Element}
 */
Util.ResultTable.prototype.table = null;

/**
 * @type {Element}
 */
Util.ResultTable.prototype.gvizLineEl = null;

Util.ResultTable.prototype.init = function() {
  this.setUpBrowserFamilyForm();
  if (this.table) {
    this.setUpSortableTable();
    this.fixRealUaStringInResults();
    this.initTooltips();
    this.initCompareUas();
    this.initUaStarLinks();
  } else if (this.gvizLineEl) {
    this.initGvizLine();
  }
};

Util.ResultTable.prototype.initGvizLine = function() {
  google.load('visualization', '1',
      {'packages': ['linechart'],
       'callback': goog.bind(this.initGvizLineReady, this)});
};

Util.ResultTable.prototype.initGvizLineReady = function() {
  url = goog.uri.utils.setParam(this.controller.url, 'o', 'gviz_data');
  url = goog.uri.utils.appendParam(url, 'tqx',
      'reqId:' + Math.floor(Math.random() * 100000));
  //url = 'http://elsigh.latest.ua-profiler.appspot.com' + url;
  var query = new google.visualization.Query(url);
  query.send(goog.bind(this.initGvizQueryResponse, this));
};

Util.ResultTable.prototype.initGvizQueryResponse = function(response) {
  this.gvizLoaded = true;
  if (response.isError()) {
    alert('Error in query: ' + response.getMessage() + ' ' +
        response.getDetailedMessage());
    return;
  }

  this.controller.setLoading(false);
  goog.style.showElement(this.formContainer, true);

  var data = response.getDataTable();

  var chart = new google.visualization.LineChart(this.gvizLineEl);
  //var chart = new google.visualization.ColumnChart(this.gvizLineEl);
  chart.draw(data, {
    'height': 400,
    'min': 0,
    'max': 10,
    'axisFontSize': 10,
    'smoothLine': true,
    'legend': 'none'
  });
};

Util.ResultTable.prototype.initUaStarLinks = function() {
  var links = goog.dom.$$('a', 'bs-ua-star', this.table);
  for (var i = 0, el; el = links[i]; i++) {
    goog.events.listen(el, 'click', this.compareUaStarClickHandler, false,
        this);
  }
};

/**
 * @param {goog.events.Event} e
 */
Util.ResultTable.prototype.compareUaStarClickHandler = function(e) {
  var uaStar = goog.uri.utils.getParamValue(e.currentTarget.href, 'ua');
  this.controller.uaUriParams = uaStar;
  this.controller.updateExtraBrowserFamilyOpts();
  this.controller.resetUrl();
  this.controller.updateTableDisplay();
  e.preventDefault();
};

Util.ResultTable.prototype.initCompareUas = function() {
  /**
   * @type {Array.<HTMLInputElement>}
   */
  this.compareCbs = [];

  /**
   * @type {Array.<string>}
   */
  this.uasToCompare = [];

  if (!this.table) {
    return;
  }

  var rows = this.table.rows;
  var cbNode = document.createElement('input');
  cbNode.type = 'checkbox';
  var labelNode = document.createElement('label');

  var cells = goog.dom.$$('td', 'rt-ua', this.table);
  for (var i = 0, cell; cell = cells[i]; i++) {
    var uaNameCellList = goog.dom.$$('span', 'bs-ua-n', cell);
    if (!uaNameCellList.length == 1) {
      continue;
    }
    var uaNameCell = uaNameCellList[0];
    var uaName = uaNameCell.innerHTML;
    var cbClone = cbNode.cloneNode(false);
    this.compareCbs.push(cbClone);
    cbClone.id = 'rt-ua-cb-' + i;
    cbClone.value = goog.dom.getTextContent(uaNameCell);
    goog.events.listen(cbClone, 'click', this.cbClick, false, this);

    var labelClone = labelNode.cloneNode(false);
    labelClone.setAttribute('for', cbClone.id);
    labelClone.appendChild(cbClone);
    cell.insertBefore(labelClone, uaNameCell);
    labelClone.appendChild(uaNameCell);
  }

  // If we didn't add any compare checkboxes just stop now.
  if (this.compareCbs.length == 0) {
    return;
  }

  this.compareUasBtn = document.createElement('button');
  this.compareUasBtn.disabled = true;
  this.compareUasBtn.innerHTML = 'Compare Browsers';
  goog.events.listen(this.compareUasBtn, 'click', this.compareUas, false, this);

  var tFoot = this.table.createTFoot();
  var tFootRow = tFoot.insertRow(0);
  var tFootCell = tFootRow.insertCell(0);
  tFootCell.setAttribute('colspan', rows[0].cells.length);
  tFootCell.appendChild(this.compareUasBtn);
};

/**
 * @param {goog.events.Event} e Browser click event.
 */
Util.ResultTable.prototype.cbClick = function(e) {
  var cb = e.currentTarget;
  if (cb.checked) {
    goog.array.insert(this.uasToCompare, cb.value);
  } else {
    goog.array.remove(this.uasToCompare, cb.value);
  }
  if (this.compareUasBtn.disabled && this.uasToCompare.length > 0) {
    this.compareUasBtn.disabled = false;
  } else if (this.uasToCompare.length == 0) {
    this.compareUasBtn.disabled = true;
  }
};

/**
 * @param {goog.events.Event} e Browser click event.
 */
Util.ResultTable.prototype.compareUas = function(e) {
  this.controller.uaUriParams = this.uasToCompare.join(',');
  this.controller.updateExtraBrowserFamilyOpts();
  this.controller.resetUrl();
  this.controller.updateTableDisplay();
};

Util.ResultTable.prototype.initTooltips = function() {
  if (!this.table) { return; }
  var thead = this.table.getElementsByTagName('thead')[0];
  var ths = thead.getElementsByTagName('th');
  for (var i = 0, th; th = ths[i]; i++) {
    if (th.title && th.title != '') {
      var tt = new goog.ui.Tooltip(th);
      tt.setHtml(th.title);
      th.setAttribute('title', '');
    }
  }
};

Util.ResultTable.prototype.setUpBrowserFamilyForm = function() {
  this.formContainer.appendChild(this.controller.browserFamilySelect);
  this.formContainer.appendChild(this.controller.outputToggle);
  if (this.controller.uaUriParams &&
    this.controller.uaUriParams.indexOf('*') !== -1) {
    goog.style.showElement(this.controller.outputToggle, true);
    if (this.controller.output == 'gviz' && !this.gvizLoaded) {
      goog.style.showElement(this.formContainer, false);
    }
  } else {
    goog.style.showElement(this.controller.outputToggle, false);
    goog.style.showElement(this.controller.browserFamilySelect, true);
  }
};

Util.ResultTable.prototype.setUpSortableTable = function() {
  if (!this.table) { return; }
  // we know # tests should be numeric sort
  var thead = this.table.getElementsByTagName('thead')[0];
  var ths = thead.getElementsByTagName('th');
  var numTestsIndex = ths.length - 1;

  var tableSorter = new goog.ui.TableSorter();
  tableSorter.setDefaultSortFunction(Util.alphaCaseInsensitiveCompare);
  tableSorter.setSortFunction(numTestsIndex,
      goog.ui.TableSorter.numericSort);
  tableSorter.decorate(this.table);
  goog.events.listen(tableSorter, goog.ui.TableSorter.EventType.SORT,
      this.onTableSort, false, this);
};
Util.ResultTable.prototype.onTableSort = function(e) {
  var yourResultsRow = goog.dom.$('tr', 'rt-ua-s-r', this.table);
  if (yourResultsRow && yourResultsRow.length) {
    goog.style.showElement(yourResultsRow[0], false);
  }
};
Util.ResultTable.prototype.fixRealUaStringInResults = function() {
  var resultUa = goog.dom.$$('span', 'rt-cur-ua', this.table);
  if (this.controller.realUaString && resultUa.length) {
    resultUa[0].innerHTML = this.controller.realUaString;
  }
};


/**
 * Static function for generating the results table URL.
 * @param {string} category
 * @param {string} output xhr or gviz
 * @param {string} opt_versionLevel
 * @param {string} opt_ua
 * @param {string} opt_results
 * @return {string} url
 */
Util.ResultTablesController.generateUrl = function(category, output,
    opt_versionLevel, opt_ua, opt_results, opt_output) {
  var url = '/';
  url = goog.uri.utils.appendParam(url, 'category', category);
  url = goog.uri.utils.appendParam(url, 'o', output);

  if (opt_versionLevel) {
    url = goog.uri.utils.appendParam(url, 'v', opt_versionLevel);
  }
  if (opt_ua) {
    url = goog.uri.utils.appendParam(url, 'ua', opt_ua);
    // reset to v=3 if ua*
    if (opt_ua.indexOf('*') != -1) {
      url = goog.uri.utils.setParam(url, 'v', '3');
    }
  }
  if (opt_results) {
    url += '&' + opt_results.replace('&', '');
  }


  return url;
};


/*****************************************/

/**
 * This is the test_driver.html runner code.
 * @param {string} testPage
 * @param {Object} windowParent
 * @param {string} category
 * @param {string} categoryName
 * @param {string} csrfToken
 * @param {boolean} autorun
 * @param {boolean} continueToNextTest
 * @param {string} testUrl
 * @constructor
 */
Util.TestDriver = function(testPage, windowParent, category, categoryName,
    csrfToken, autorun, continueToNextTest, testUrl) {

  /**
   * @type {string}
   */
  this.testPage = testPage;

  /**
   * @type {Object}
   * @private
   */
  this.windowParent_ = windowParent;

  /**
   * @type {string}
   */
  this.category = category;

  /**
   * @type {string}
   */
  this.categoryName = categoryName;

  /**
   * @type {string}
   */
  this.csrfToken = csrfToken;

  /**
   * @type {boolean}
   */
  this.autorun = autorun == '1';

  /**
   * @type {boolean}
   */
  this.continueToNextTest = (continueToNextTest != '' &&
      continueToNextTest != 'None');

  /**
   * @type {string}
   */
  this.testUrl = testUrl;

  /**
   * @type {Function}
   */
  this.runTestButtonClickHandlerBound =
      goog.bind(this.runTestButtonClickHandler, this)

  /**
   * @type {Element}
   */
  this.runTestButton = goog.dom.$('bs-runtest');
  if (this.runTestButton) {
    goog.events.listen(this.runTestButton, 'click',
        this.runTestButtonClickHandlerBound);
  }

  /**
   * @type {Element}
   */
  this.testFrame = this.windowParent_.frames['bs-test-frame'];

  /**
   * @type {Array}
   */
  this.testCategories = [];

  /**
   * @type {Array}
   */
  this.testResults = null;

  /**
   * @type {Element}
   */
  this.sendBeaconCheckbox = goog.dom.$('bs-send-beacon');
};

/**
 * @type {?string}
 */
Util.TestDriver.prototype.uriResults = null;

/**
 * @param {string} category
 */
Util.TestDriver.prototype.addCategory = function(category) {
  this.testCategories.push(category);
};

/**
 * This is the function that all test pages will call to beacon.
 * @param {Array} testResults test1=result,test2=result, etc..
 * @param {Array} opt_continueParams Possibly a subset of testResults for
 *     sending to the results page.
 */
Util.TestDriver.prototype.sendScore = function(testResults,
    opt_continueParams) {

  // Support for abart's syntax
  if (typeof(testResults[0]) == 'object') {
    var reFormattedResults = [];
    for (var i = 0, test; test = testResults[i]; i++) {
      reFormattedResults.push(test['test'] + '=' +
          (test['result'] === true ? '1' : 0));
    }
    testResults = reFormattedResults
  }
  var continueParams = opt_continueParams || null;
  this.testResults = testResults;
  this.uriResults = this.category + '_results=' +
      (continueParams ?
          escape(continueParams.join(',')) :
          escape(testResults.join(',')));

  var uaString = goog.userAgent.getUserAgentString() || '';
  var data = 'category=' + this.category + '&results=' +
      testResults.join(',') + '&csrf_token=' + this.csrfToken +
      '&js_ua=' + escape(uaString);

  // Autorun always shares your score.
  if (this.autorun) {
    goog.net.XhrIo.send('/beacon',
        goog.bind(this.onBeaconCompleteAutorun, this),
        'post', data);
  } else {
    if (this.sendBeaconCheckbox.checked) {
      goog.net.XhrIo.send('/beacon', null, 'post', data);
    }
    this.runTestButton.className = 'bs-btn';
    var checkmarkUtf8 = '✓';
    this.runTestButton.innerHTML = checkmarkUtf8 + 'Done! Compare your ' +
        this.categoryName + ' Test results »';
    this.runTestButton.continueUrl = '/?' + this.uriResults;
    goog.events.listen(this.runTestButton, 'click', function(e) {
      var btn = e.target;
      var continueUrl = btn.continueUrl;
      window.top.location.href = continueUrl;
    });

    /*
    var resultsDisplay = continueParams ?
          continueParams.join(',') :
          testResults.join(',<wbr>');
    var scoreNode = goog.dom.createElement('div');
    var thanks = this.sendBeaconCheckbox.checked ?
        'Thanks for contributing! ' : '';
    scoreNode.innerHTML = thanks + 'Your results: ' + resultsDisplay;
    scoreNode.style.margin = '.7em 0 0 1em';
    this.runTestButton.parentNode.appendChild(scoreNode);
    */
  }

  // Update the test frame to scroll to the top where the score is.
  this.testFrame.scrollTo(0, 0);
};


/**
 * @param {goog.events.Event} e
 */
Util.TestDriver.prototype.onBeaconCompleteAutorun = function(e) {
  var len = this.testCategories.length;
  var nextUrl;
  if (this.continueToNextTest) {
    var nextTest;
    for (var i = 0, n = len; i < n; i++) {
      if (this.testCategories[i] == this.category) {
        // last test?
        if (i == len - 1) {
          nextTest = '/?';
        } else {
          nextTest = '/' + this.testCategories[i + 1] +
              '/test?autorun=1&continue=1';
        }
      }
    }
    nextUrl = nextTest + '&' + this.uriResults;

    // now add on previous test scores
    for (var i = 0, n = len; i < n; i++) {
      var category = this.testCategories[i];
      var results = Util.getParam(category + '_results',
          window.top);
      if (results) {
        nextUrl += '&' + category + '_results=' + results;
      }
    }
    window.top.location.href = nextUrl;
  } else {
    //console.log('autorun but no continue');
  }
};


/**
 * @param {goog.events.Event} e
 */
Util.TestDriver.prototype.runTestButtonClickHandler = function(e) {
  this.runTestButton.className = 'bs-btn-disabled';
  goog.events.unlisten(this.runTestButton, 'click',
      this.runTestButtonClickHandlerBound);
  this.runTestButton.innerHTML = this.categoryName + ' Tests Running...';
  goog.dom.$('bs-send-beacon-label').style.display = 'none';
  // Is there a Chrome Frame checkbox?
  var chromFrameCheckbox = goog.dom.$('bs-cf-c');
  if (chromFrameCheckbox) {
    chromFrameCheckbox.style.display = 'none';
  }
  this.runTest();
};


/**
 * Loads the test page into the frame.
 * @export
 */
Util.TestDriver.prototype.runTest = function() {
  // i.e. run just one test.
  if (this.testUrl != '') {
    this.sendBeaconCheckbox.style.display = 'none';
    this.runTestButton.style.display = 'none';
    goog.dom.$('bs-send-beacon-label').style.display = 'none';
    this.testFrame.location.href = this.testUrl;
  } else {
    var rand = Math.floor(Math.random() * 10000000);
    var categoryTestUrl = this.testPage + '?category=' + this.category + '&r=' + rand;
    this.testFrame.location.href = categoryTestUrl;
  }
};

/**
 * EXPORTS
 */
goog.exportSymbol('Util.createChromeFrameCheckbox',
    Util.createChromeFrameCheckbox);
goog.exportSymbol('Util.reconcileClientServerUaPretty',
    Util.reconcileClientServerUaPretty);
goog.exportSymbol('Util.getParam', Util.getParam);
goog.exportSymbol('Util.ResultTablesController', Util.ResultTablesController);
goog.exportSymbol('Util.TestDriver', Util.TestDriver);
goog.exportSymbol('Util.TestDriver.prototype.addCategory',
    Util.TestDriver.prototype.addCategory);
goog.exportSymbol('Util.TestDriver.prototype.runTest',
    Util.TestDriver.prototype.runTest);
goog.exportSymbol('Util.TestDriver.prototype.sendScore',
    Util.TestDriver.prototype.sendScore);
