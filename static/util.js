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

goog.require('goog.events');
goog.require('goog.net.XhrIo');
goog.require('goog.net.cookies');
goog.require('goog.ui.TableSorter');
goog.require('goog.ui.Tooltip');
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
 * @return {string} The value of the param or an empty string.
 * @export
 */
Util.getParam = function(param, opt_win) {
  var win = opt_win || window;
  param = param.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]');
  var regexString = '[\\?&]' + param + '=([^&#]*)';
  var regex = new RegExp(regexString);
  var results = regex.exec(win.location.href);
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
 * @param {Array.<Object>} categories An array of category objs.
 * @param {string} realUaString The actual user agent string.
 * @param {string} resultsUriParams category_results=foo,bar etc..
 * @constructor
 */
Util.ResultTablesController = function(category, categories, realUaString,
    resultsUriParams) {
  this.category = category;
  this.categories = categories;
  this.realUaString = realUaString;
  this.browserFamily = 'top';
  this.resultsUriParams = resultsUriParams;
  // If we have results in the resultUriParams, scroll to them.
  if (this.resultsUriParams.indexOf('_results') !== -1) {
    window.location.hash = '#rt-' + this.category + '-cur-ua';
  }

  this.tables = {};
  this.xhrLoading = false;
  this.decorate();
  this.setCategory(category);
};

Util.ResultTablesController.prototype.decorate = function() {
  var categoriesList = goog.dom.createElement('ul');
  categoriesList.id = 'bs-results-cats';
  categoriesList.className = 'bs-compact';

  for (var category in this.categories) {
    var containerEl = this.categories[category]['container'];

    var h3 = containerEl.getElementsByTagName('h3')[0];
    goog.dom.removeNode(h3);

    var link = goog.dom.createElement('a');
    link.href = '/?category=' + category + '&' + this.resultsUriParams;
    link.category = category;
    link.appendChild(goog.dom.createTextNode(
        this.categories[category]['name']));
    this.categories[category]['link'] = link;
    goog.events.listen(link, 'click', this.changeCategoryClickHandler, false,
        this);

    var li = goog.dom.createElement('li');
    li.appendChild(link);

    if (category != this.category) {
      containerEl.innerHTML = '';
      containerEl.style.display = 'none';
    }
    categoriesList.appendChild(li);
  }
  var results = goog.dom.$('bs-results');
  var resultsByCat = goog.dom.$('bs-results-bycat');
  results.insertBefore(categoriesList, resultsByCat);
};

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

Util.ResultTablesController.prototype.setCategory = function(category) {
  if (this.category) {
    this.categories[this.category]['container'].style.display = 'none';
    this.categories[this.category]['link'].parentNode.className = '';
  }

  this.category = category;
  this.categories[this.category]['link'].parentNode.className = 'bs-sel';

  // This would be the initial set.
  if (!goog.object.containsKey(this.tables, this.category) &&
      this.categories[this.category]['container'].innerHTML != '') {
    this.tables[this.category + '-' + this.browserFamily] =
        new Util.ResultTable(this, this.category);
    this.categories[this.category]['container'].style.display = '';
  // XHR if we need to.
  } else if (this.categories[this.category]['container'].innerHTML == '') {
    this.xhrCategoryResults();
  } else {
    this.categories[this.category]['container'].style.display = '';
  }
};

Util.ResultTablesController.prototype.xhrCategoryResults = function() {
  this.xhrLoading = true;

  var container = this.categories[this.category]['container'];
  container.style.display = '';
  container.className = 'rt-loading';
  container.innerHTML = 'Loading the ' +
      this.categories[this.category]['name'] +
      ' Results ...';

  // Strip off the ua= part if not custom
  var additionalUriParams = this.resultsUriParams;
  if (this.browserFamily != 'custom') {
    additionalUriParams = additionalUriParams.replace(/&?ua=[^&]+/, '');
  }

  this.url = '/?category=' + this.category +
      '&o=xhr&v=' + this.browserFamily + '&' + additionalUriParams;
  goog.net.XhrIo.send(this.url, goog.bind(this.loadStatsTableCallback, this),
      'get', null, null, 15000); // 15000 = 15 second timeout
};

Util.ResultTablesController.prototype.loadStatsTableCallback = function(e) {
  var container = this.categories[this.category]['container'];
  var xhrio = e.target;
  if (xhrio.isSuccess()) {
    container.className = '';
    var html = xhrio.getResponseText();
    container.innerHTML = html;
    this.tables[this.category] = new Util.ResultTable(this, this.category);

  } else {
    container.className = 'rt-err';
    container.innerHTML =
        '<div>Crud. We encountered a problem on our server.</div>' +
        '<div>We are aware of the issue, and apologize.</div>';
    var link = goog.dom.createElement('a');
    link.category = this.category;
    goog.events.listen(link, 'click', this.xhrCategoryResults, false,
        this);
    link.href = this.url;
    link.innerHTML = 'Feel free to try again.';
    container.appendChild(link);
  }
  this.xhrLoading = false;
};

/**
 * @param {Util.ResultTablesController} controller
 * @param {string} category
 * @constructor
 */
Util.ResultTable = function(controller, category) {
  this.controller = controller;
  this.category = category;
  this.categoryObj = this.controller.categories[this.category];

  /**
   * @type {Element}
   */
  this.table = goog.dom.$('rt-' + this.category + '-t');

  this.browserFamilySelect = goog.dom.$('rt-' + this.category +
      '-v');
  this.init();
};

Util.ResultTable.prototype.init = function() {
  this.setUpBrowserFamilyForm();
  this.setUpSortableTable();
  this.fixRealUaStringInResults();
  this.initTooltips();
  this.initCompareUas();
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
    labelClone.appendChild(uaNameCell);

    cell.appendChild(labelClone);
  }

  // If we didn't add any compare checkboxes just stop now.
  if (this.compareCbs.length == 0) {
    return;
  }

  this.compareUasBtn = document.createElement('button');
  this.compareUasBtn.disabled = true;
  this.compareUasBtn.innerHTML = 'Compare UAs';
  goog.events.listen(this.compareUasBtn, 'click', this.compareUas, false, this);

  var tFoot = this.table.createTFoot();
  var tFootRow = tFoot.insertRow();
  var tFootCell = tFootRow.insertCell();
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
  var compareUasUrl = '/?category=' + this.category + '&' +
      'v=custom&' +
      'ua=' + encodeURIComponent(this.uasToCompare.join(','));
  window.location.href = compareUasUrl;
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
  // hide submit
  goog.dom.$('rt-' + this.category + '-v-s').style.display =
      'none';
  goog.events.listen(this.browserFamilySelect, 'click',
      this.browserFamilyClickHandler, false, this);
  goog.events.listen(this.browserFamilySelect, 'change',
      this.browserFamilyChangeHandler, false, this);

  // ensures a refresh doesn't make the select look wrongly selected.
  goog.dom.$('rt-' + this.category + '-v-f').reset();
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
  var yourResultsRow = goog.dom.$('rt-' + this.category + '-ua-s-r');
  if (yourResultsRow) {
    yourResultsRow.style.display = 'none';
  }
};
Util.ResultTable.prototype.fixRealUaStringInResults = function() {
  var resultUa = goog.dom.$('rt-' + this.category + '-cur-ua');
  if (this.controller.realUaString && resultUa) {
    resultUa.innerHTML = this.controller.realUaString;
  }
};
Util.ResultTable.prototype.getBrowserFamilyValue = function() {
  var browserFamilyValue;
  if (this.browserFamilySelect) {
    browserFamilyValue = this.browserFamilySelect.options[
        this.browserFamilySelect.options.selectedIndex].value;
  }
  return browserFamilyValue;
};
Util.ResultTable.prototype.browserFamilyChangeHandler = function(e) {
  this.browserFamily = this.getBrowserFamilyValue();
  this.controller.browserFamily = this.browserFamily;

  // fix the download links
  var downloadsContainer = goog.dom.$('rt-dl-' + this.category);
  if (downloadsContainer) {
    var downloadLinks = downloadsContainer.getElementsByTagName('a');
    for (var i = 0, downloadLink; downloadLink = downloadLinks[i]; i++) {
      var href = downloadLink.href;
      href = href.replace(/v=[^&]+/, 'v=' + this.browserFamily);
      // Strip off the ua parts if they switch from a custom to a known v.
      if (this.browserFamily != 'custom') {
        href = href.replace(/&?ua=[^&]+/, '')
      }
      downloadLink.href = href;
    }
  }
  this.controller.xhrCategoryResults();
  e.stopPropagation();
};
Util.ResultTable.prototype.browserFamilyClickHandler = function(e) {
  // Prevents table cells from sorting just on click.
  e.stopPropagation();
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
