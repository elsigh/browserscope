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

/**
 * Namespace for utility functions.
 * @type {Object}
 */
var Util = {};

/**
 * Adds CSS text to the DOM.
 * @param {string} cssText The css text to add.
 * @param {string} opt_id The id for the new stylesheet element.
 * @return {Element} cssNode the added css DOM node.
 */
Util.addCssText = function(cssText, opt_id) {
  var cssNode = document.createElement('style');
  cssNode.type = 'text/css';
  cssNode.id = opt_id ? opt_id : 'cssh-sheet-' + document.styleSheets.length;

  var headEl = document.getElementsByTagName('head')[0];
  headEl.appendChild(cssNode);

  // IE
  if (cssNode.styleSheet) {
    cssNode.styleSheet.cssText = cssText;
  // W3C
  } else {
    var cssText = document.createTextNode(cssText);
    cssNode.appendChild(cssText);
  }

  return cssNode;
};


/**
 * Preserve scope in timeouts.
 * @type {Object} scope
 * @type {Function} fn
 * @return {Function}
 */
Util.curry = function(scope, fn) {
  var scope = scope || window;
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
 * @param {IFRAMEElement} iframe
 * @return {string} The iframe's id.
 * @export
 */
Util.getIframeDocument = function(iframeId) {
  var doc;
  var iframe = window.frames[iframeId];
  if (!iframe) {
    iframe = document.getElementById(iframeId);
  }
  if (!iframe) {
    return;
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
    var container = document.createElement('strong');
    container.id = 'bs-cf-c';
    var cb = document.createElement('input');
    cb.id = 'bs-cf-enabled';
    cb.type = 'checkbox';
    var chromeFrameEnabled = goog.net.cookies.get(Util.COOKIE_CHROME_FRAME);
    cb.checked = chromeFrameEnabled == '1';
    goog.events.listen(cb, 'click', function(e) {
      var cb = e.currentTarget;
      goog.net.cookies.set(Util.COOKIE_CHROME_FRAME, cb.checked ? 1 : 0);
      if (reloadOnChange) {
        window.top.location.href = window.top.location.href;
      }
    });
    var label = document.createElement('label');
    label.setAttribute('for', cb.id);
    label.innerHTML = 'Run in Chrome Frame';

    container.appendChild(cb);
    container.appendChild(label);
    return container;
  }
};

/*****************************************/

/**
 * This is the test_driver.html runner code.
 * @constructor
 * @export
 */
Util.testDriver = function(testPage, category, categoryName, csrfToken,
    autorun, continueToNextTest) {

  /**
   * @type {string}
   */
  this.testPage = testPage;

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
   * @type {Element}
   */
  this.runTestButton = document.getElementById('bs-runtest');
  if (this.runTestButton) {
    goog.events.listen(this.runTestButton, 'click',
        goog.bind(this.runTestButtonClickHandler, this));
  }

  /**
   * @type {Element}
   */
  this.testFrame = parent.frames['bs-test-frame'];

  /**
   * @type {Array}
   */
  this.testCategories = [];

  /**
   * @type {string}
   */
  this.testResults = null;

  /**
   * @type {string}
   */
  this.uriResults = null;

  /**
   * @type {INPUTElement}
   */
  this.sendBeaconCheckbox = document.getElementById('bs-send-beacon');
};


/**
 * This is the function that all test pages will call to beacon.
 * @param {Array} testResults test1=result,test2=result, etc..
 * @param {Array} opt_urlParams Possibly a subset of testResults for
 *     sending to the results page.
 * @export
 */
Util.testDriver.prototype.sendScore = function(testResults,
    opt_continueParams) {
  var continueParams = opt_continueParams || null;
  this.testResults = testResults;
  this.uriResults = this.category + '_results=' +
      (continueParams ?
          escape(continueParams.join(',')) :
          escape(testResults.join(',')));

  var data = 'category=' + this.category + '&results=' +
      testResults.join(',') + '&csrf_token=' + this.csrfToken +
      '&js_ua=' + escape(goog.userAgent.getUserAgentString());

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
    this.runTestButton.innerHTML = 'Done! Compare your results »';
    this.runTestButton.target = '_top';
    this.runTestButton.href = '/?' + this.uriResults;
    var resultsDisplay = continueParams ?
          continueParams.join(',') :
          testResults.join(',');
    var scoreNode = document.createElement('div');
    var thanks = this.sendBeaconCheckbox.checked ?
        'Thanks for contributing! ' : '';
    scoreNode.appendChild(document.createTextNode(
        thanks + 'Your results: ' + resultsDisplay));
    scoreNode.style.margin = '.7em 0 0 1em';
    this.runTestButton.parentNode.appendChild(scoreNode);
  }

  // Update the test frame to scroll to the top where the score is.
  this.testFrame.scrollTo(0, 0);
};


/**
 * @param {goog.events.Event} e
 */
Util.testDriver.prototype.onBeaconCompleteAutorun = function(e) {
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
Util.testDriver.prototype.runTestButtonClickHandler = function(e) {
  this.runTestButton.className = 'bs-btn-disabled';
  this.runTestButton.onclick = '';
  this.runTestButton.innerHTML = this.categoryName + ' Tests Running...';
  document.getElementById('bs-send-beacon-label').style.display = 'none';
  // Is there a Chrome Frame checkbox?
  var chromFrameCheckbox = document.getElementById('bs-cf-c');
  if (chromFrameCheckbox) {
    chromFrameCheckbox.style.display = 'none';
  }
  this.runTest();
};


/**
 * Loads the test page into the frame.
 * @export
 */
Util.testDriver.prototype.runTest = function() {
  var rand = Math.floor(Math.random() * 10000000);
  var categoryTestUrl = this.testPage + '?r=' + rand;
  this.testFrame.location.href = categoryTestUrl;
};
