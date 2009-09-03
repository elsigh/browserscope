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
 * @param {string} param The param to look for
 * @return {string} The value of the param or an empty string.
 */
Util.getParam = function(param) {
  param = param.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]');
  var regexString = '[\\?&]' + param + '=([^&#]*)';
  var regex = new RegExp(regexString);
  var results = regex.exec(window.location.href);
  if (results == null) {
    return '';
  } else {
    return results[1];
  }
};


/**
 * @param {IFRAMEElement} iframe
 * @reutrn {string} The iframe's id.
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
 * Makes it so that links in iframes load in a new tab/window.
 * @param {IFRAMEElement} iframe
 */
Util.fixIframeLinks = function(iframe) {
  var doc = Util.getIframeDocument(iframe);
  var links = doc.getElementsByTagName('a');
  for (var i = 0, link; link = links[i]; i++) {
    link.onclick = function(e) {
      this.target = '_blank';
    }
  }
};

/**
 * @type {Object} doc A document object.
 */
Util.getDocumentHeight = function(doc) {
  return Math.max(
    Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight),
    Math.max(doc.body.offsetHeight, doc.documentElement.offsetHeight),
    Math.max(doc.body.clientHeight, doc.documentElement.clientHeight)
  );
}
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
 *
 * @fileoverview Shared javascript for sending beacons and blocking so
 * that we know the beacon has completed.
 * @author elsigh@google.com (Lindsey Simon)
 */

/**
 * Adds a SCRIPT element to the DOM and monitors for existence of a completion
 * variable named BEACON_COMPLETE.
 * @param {string} uriParams URI params for the script element.
 * @param {Object} opt_doc Document object.
 * @param {string} opt_id DOM id for the script element.
 * @constructor
 */
var Beacon = function(uriParams, opt_doc, opt_id) {

  var id = opt_id || Beacon.DEFAULT_ID;

  /**
   * @type {Object}
   */
  this.doc_ = opt_doc || document;

  /**
   * @type {HTMLHeadElement}
   * @private
   */
  this.head_ = this.doc_.getElementsByTagName('head')[0];

  /**
   * @type {HTMLScriptElement}
   * @private
   */
  this.script_ = this.doc_.createElement('script');
  this.script_.type = 'text/javascript';
  this.script_.id = id;

  var src = Beacon.SERVER + '/beacon?' + uriParams + '&callback=1' +
      Beacon.ADDTL_PARAMS;
  this.script_.src = src;

  /**
   * @type {Function}
   */
  this.checkCompleteCurry_ = Util.curry(this, this.checkComplete_);
};


/**
 * @type {number}
 * @private
 */
Beacon.completeInt_ = null;


/**
 * @type {number}
 * @private
 */
Beacon.COMPLETE_CHECK_SPEED = 50;


/**
 * @type {string}
 * @private
 */
Beacon.DEFAULT_ID = 'beacon';


/**
 * Can be used by implementations done to make requests to a
 * server on another domain.
 * @type {string}
 */
Beacon.SERVER = '';


/**
 * Can be used by implementations.
 * @type {string}
 */
Beacon.ADDTL_PARAMS = '';


/**
 * Sends a JSONP request and begins a timer to check that it has
 * completed.
 */
Beacon.prototype.send = function() {
  //console.log('sending with src: ', this.script_.src);
  this.head_.appendChild(this.script_);
  this.checkComplete_();
};


/**
 * Checks to see if the JSONP request has finished by looking for
 * a magic variable BEACON_COMPLETE.
 * @private
 */
Beacon.prototype.checkComplete_ = function() {
  if (typeof BEACON_COMPLETE != 'undefined') {
    window.clearTimeout(this.completeInt_);
    this.onComplete();
  } else {
    this.completeInt_ = window.setTimeout(
        this.checkCompleteCurry_, Beacon.COMPLETE_CHECK_SPEED);
  }
};


/**
 * To be made use of as desired by implementations.
 */
Beacon.prototype.onComplete = function() {};

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
*/
/**
 * @fileoverview The reflow timer attempts to time the speed of re-flowing a web
 * page. This means selector matching + rendering tree construction +
 * reflow and position/geometry recalculations.
 * Requires util.js and beacon.js
 * @author elsigh@google.com (Lindsey Simon)
 */

/**
 * The reflow timer class.
 * @param {boolean} opt_sendResultsToServer If true, send the results to our
 *     App Engine server for datastore-age.
 * @param {HTMLElement} opt_container The container element to manipulate.
 * @param {number} opt_passes The number of times to run the test for computing
 *     a median reflow time.
 * @constructor
 */
var ReflowTimer = function(sendResultsToServer, opt_container, opt_passes) {

  /**
   * @type {boolean}
   * @private
   */
  this.shouldSendResultsToServer_ = sendResultsToServer;

  /**
   * @type {number}
   * @private
   */
  this.passes_ = opt_passes || 3;

  /**
   * @type {HTMLDocumentElement}
   * @private
   */
  this.doc_ = window.document;

  /**
   * @type {HTMLBodyElement}
   * @private
   */
  this.body_ = this.doc_.body;

  /**
   * This is the element we tweak display none on to measure the reflow time.
   * Interesting to note here:
   * Setting document.body.style.display = 'none' in IE appears not to
   * actually cause the entire body to disappear, for instance buttons
   * remain laid out on the page but with their text removed. Bizarro.
   * @type {DocumentElement|BodyElement}
   * @private
   */
   this.containerEl_ = opt_container ? opt_container :
       (Util.isInternetExplorer() ?
        this.doc_.documentElement : this.body_);

  /**
   * @type {Object}
   */
  this.containerStyle_ = this.containerEl_.style;

  /**
   * @type {Array}
   * @private
   */
  this.times_ = [];

  /**
   * @type {Array}
   * @private
   */
  this.reflowTimes_ = [];

  /**
   * @type {Array}
   * @private
   */
  this.medianReflowTimes_ = [];

  /**
   * @type {Array}
   * @private
   */
  this.normalizedTimes_ = [];

  /**
   * @type {Function}
   */
  this.testCurry_ = Util.curry(this, this.test_);

  /**
   * @type {Function}
   */
  this.testContinueCurry_ = Util.curry(this, this.testContinue_);

  /**
   * Start with the first test.
   * @type {number}
   */
  this.currentTestIndex_ = 0;

  /**
   * @type {Object}
   */
  this.results = {};

  /**
   * @type {Array.<string>}
   */
  this.resultsParams = [];
};

/**
 * Used for the bookmarklet's link back to the homepage.
 * @type {string}
 */
ReflowTimer.SERVER = 'ua-profiler.appspot.com';

/**
 * @type {number}
 */
ReflowTimer.REFLOW_REST_TIME = 250;


/**
 * @type {string}
 */
ReflowTimer.TEST_BODY_ATTR = 'bogusattribute';


/**
 * @type {string}
 */
ReflowTimer.TEST_BODY_ATTR_VAL = 'bogusvalue';


/**
 * @type {string}
 */
ReflowTimer.TEST_CLASS_NAME = 'rt-test-classname';


/**
 * @type {string}
 */
ReflowTimer.TEST_MULTIPLE_REFLOW_CSSTEXT = 'font-size: 20px; ' +
    'line-height: 10px;' +
    'padding-left: 10px;' +
    'margin-top: 7px;';


/**
 * @type {string}
 */
ReflowTimer.TEST_PADDING_LEFT_LONGHAND_CSSTEXT = 'padding: 0 0 0 4px;';


/**
 * @type {string}
 */
ReflowTimer.TEST_PADDING_LEFT_SHORTHAND_CSSTEXT = 'padding-left: 4px;';


/**
 * These are the enabled tests.
 * @type {Array.<string>}
 */
ReflowTimer.prototype.tests = [
  'testDisplay',
  'testVisibility',
  'testNonMatchingClass',
  'testFourClassReflows',
  'testFourScriptReflows',
  'testTwoScriptReflows',
  'testPaddingPx',
  'testPaddingLeftPx',
  'testFontSizeEm',
  'testWidthPercent',
  'testBackground',
  'testOverflowHidden',
  'testGetOffsetHeight'
];


/**
 * And these are the rest of the ones we've tried.
 * @type {Array.<string>}
 */
ReflowTimer.prototype.unusedTests = [
  'testSelectorMatchTime', // only works in FF this way
  'testLineHeight', // Same as testFontSize
  'testWidthPx', // Same as testWidthEm
  'testFontSizePx', // Same as testFontSizeEm
  'testOverflowVisible', // Seems uninteresting
  'testMarginPx', // Same as testPaddingPx
  'testPaddingLeftLonghandScript',
  'testPaddingLeftLonghandClass',
  'testPaddingLeftShorthandClass'
];


/**
 * Normalize values when sent to the server based on the following
 * test's score, using it as a golden test of 1x reflow.
 * @type {text|boolean}
 * @deprecated
 */
ReflowTimer.prototype.normalizeTimesToTest = false;


/**
 * @type {string}
 * @private
 */
ReflowTimer.prototype.currentTestName_ = null;


/**
 * @type {boolean}
 * @private
 */
ReflowTimer.prototype.recordPaintEvents_ = false;


/**
 * @type {Array}
 * @private
 */
ReflowTimer.prototype.paintEvents_ = [];


/**
 * @type {Array|string}
 * @private
 */
ReflowTimer.prototype.originalValue_ = null;


/**
 * @type {boolean}
 * @private
 */
ReflowTimer.prototype.showFeedbackDuringTests_ = true;


/**
 * @type {HTMLElement}
 * @private
 */
ReflowTimer.prototype.testFeedbackEl_ = null;


/**
 * Calculates the median value rounded to the nearest int for an array of
 * numbers.
 * @type {Array.<number>} array The array of numbers.
 * @return {number}
 */
ReflowTimer.getMedian = function(array) {
  array.sort(function(a, b) {
    var result = a - b;
    return result == 0 ? 0 : result / Math.abs(result);
  });
  var halfLen = array.length / 2;
  var index = array.length == 2 ? 0 : Math.floor(halfLen);
  var median;
  if (array.length == 1) {
    median = array[0];
  }
  else if (index == halfLen || index == 0) {
    median = (array[index + 1] + array[index]) / 2;
  } else {
    median = array[index];
  }
  return median.toFixed(0);
};


/**
 * @param {Element} el
 * @param {string} style to get
 * @return {string} computedStyle
 */
ReflowTimer.prototype.getComputedStyle = function(el, style) {
  var computedStyle = null;
  if (this.doc_.defaultView && this.doc_.defaultView.getComputedStyle) {
    var computedStyleObj =
        this.doc_.defaultView.getComputedStyle(el, '');
    var computedStyle = computedStyleObj[style];
  }
  return computedStyle;
};


/******************************
 * CLASS METHODS
 ******************************/


/**
 * Flush any style, rendering tree construction, and layout operations/queues.
 * This was a recommendation by David Baron at Mozilla. Thanks David!
 */
ReflowTimer.prototype.flushRenderQueue_ = function() {
  var offsetHeight = this.body_.offsetHeight;
};

/**
 * Only flushes style computations.
 */
ReflowTimer.prototype.flushStyleComputation_ = function() {
  this.getComputedStyle(this.doc_.body, 'color');
};

/**
 * Public function to begin the test routine.
 */
ReflowTimer.prototype.run = function() {

  // Cresultslear these from prior runs.
  this.results = {};
  this.resultsParams = []

  // Gets rid of prior test elements in the DOM.
  var previousElementIds = ['rt-content', 'rt-results',
      'rt-feedback', 'rt-css', Beacon.DEFAULT_ID];
  for (var i = 0, id; id = previousElementIds[i]; i++) {
    var el = document.getElementById(id);
    if (el) {
      el.parentNode.removeChild(el);
    }
  }

  // Adds the CSS for our class name test.
  if (!document.getElementById(ReflowTimer.TEST_CLASS_NAME)) {
    var cssText = '.' + ReflowTimer.TEST_CLASS_NAME + ' { ' +
        ReflowTimer.TEST_MULTIPLE_REFLOW_CSSTEXT + ' }';
    Util.addCssText(cssText, ReflowTimer.TEST_CLASS_NAME);
  }

  // css longhand test needs this.
  if (!document.getElementById(ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-longhand')) {
    var cssText = '.' + ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-longhand  { ' +
        ReflowTimer.TEST_PADDING_LEFT_LONGHAND_CSSTEXT + ' }';
    Util.addCssText(cssText, ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-longhand');
  }
  // css shorthand test needs this.
  if (!document.getElementById(ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-shorthand')) {
    var cssText = '.' + ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-shorthand  { ' +
        ReflowTimer.TEST_PADDING_LEFT_SHORTHAND_CSSTEXT + ' }';
    Util.addCssText(cssText, ReflowTimer.TEST_CLASS_NAME +
        '-padding-left-shorthand');
  }

  // If possible listen for and record paint events.
  if (window.addEventListener && this.recordPaintEvents_) {
    var thisInstance = this;
    window.addEventListener('MozAfterPaint', function(e) {
        thisInstance.logPaintEvents_(e); }, false);
  }

  // Set up an element to show what test we're on.
  if (this.showFeedbackDuringTests_) {
    this.testFeedbackEl_ = document.createElement('div');
    this.testFeedbackEl_.id = 'rt-feedback';
    var style = this.testFeedbackEl_.style;
    style.position = 'absolute';
    style.fontSize = '13px';
    style.textAlign = 'center';
    style.background = '#eee';
    style.border = '1px solid #333';
    if (style.setProperty) {
      style.setProperty('-moz-border-radius-bottom', '4px', '');
      style.setProperty('-webkit-border-radius-bottom', '4px', '');
    }
    style.borderTop = '0';
    style.padding = '4px 20px';
    style.top = '0px';
    style.left = '40%';
    style.width = '22em';
    style.color = '#333';
    style.zIndex = '999';

    this.testFeedbackEl_.innerHTML = 'Beginning the Reflow tests...';
    this.body_.appendChild(this.testFeedbackEl_);
  }

  this.testStart_();
};


/**
 * Starts the test routine.
 * @private
 */
ReflowTimer.prototype.testStart_ = function() {

  this.currentTestName_ = this.tests[this.currentTestIndex_];

  if (!this.reflowTimes_[this.currentTestName_]) {
    this.reflowTimes_[this.currentTestName_] = [];
  }

  // If there's a setup function for the current test, run that first.
  if (this[this.currentTestName_ + 'SetUp']) {
    this[this.currentTestName_ + 'SetUp']();
  }

  if (this.testFeedbackEl_) {
    var feedback = 'Test '  + (this.currentTestIndex_ + 1) + ' of ' +
        this.tests.length + ' - ' +
        this.currentTestName_.replace('test', '') +
        ' - pass ' +
        (this.reflowTimes_[this.currentTestName_].length + 1) +
        ' of ' + this.passes_;
    this.testFeedbackEl_.innerHTML = feedback;
  }

  // Let the browser rest a little bit between tests.
  window.setTimeout(this.testCurry_, ReflowTimer.REFLOW_REST_TIME);
};


/**
 * Test routine.
 * @private
 */
ReflowTimer.prototype.test_ = function() {

  // Ensure the render queue is clean before starting the timer.
  this.flushRenderQueue_();

  // For testing selector match time we'll want to call a different
  // "flush" function.
  this.flushBetween_ = this.currentTestName_ == 'testSelectorMatchTime' ?
      this.flushStyleComputation_ : this.flushRenderQueue_;

  var time1 = new Date().getTime();

  // Run the current test.
  this[this.currentTestName_]();

  // Now flush the render queue again, ensuring that our last change
  // gets pushed all the way through.
  this.flushBetween_();

  var time2 = new Date().getTime();

  var reflowTime = time2 - time1;
  this.reflowTimes_[this.currentTestName_].push(reflowTime);

  window.setTimeout(this.testContinueCurry_, ReflowTimer.REFLOW_REST_TIME);
};


ReflowTimer.prototype.testContinue_ = function() {
  // If there's a teardown function for the current test, run that now.
  if (this[this.currentTestName_ + 'TearDown']) {
    this[this.currentTestName_ + 'TearDown']();
  }
  this.flushRenderQueue_();

  // Do another pass of this test?
  if (this.reflowTimes_[this.currentTestName_].length != this.passes_) {
    this.testStart_();

  // On to the next test.
  } else if (this.currentTestIndex_ != this.tests.length - 1) {
    this.currentTestIndex_ += 1;
    this.testStart_();

  // All done with everything.
  } else {
    this.testsComplete_();
  }
};


/**
 * Completes the test routine.
 * @private
 */
ReflowTimer.prototype.testsComplete_ = function() {

  // Cleans up paint event listener before possibly rendering anything.
  if (window.addEventListener && this.recordPaintEvents_) {
    var thisInstance = this;
    window.removeEventListener('MozAfterPaint', function(e) {
        thisInstance.logPaintEvents_(e);}, false);
  }

  // Get all the median test times.
  for (var i = 0, test; test = this.tests[i]; i++) {
    this.medianReflowTimes_[test] =
        ReflowTimer.getMedian(this.reflowTimes_[test]);
  }

  // Normalized times.
  if (this.normalizeTimesToTest) {
    var benchmark = this.medianReflowTimes_[this.normalizeTimesToTest];
    for (var i = 0, test; test = this.tests[i]; i++) {
      var percentage = Math.round(
          (this.medianReflowTimes_[test]/benchmark) * 100);
      this.normalizedTimes_[test] = percentage;
    }
  }

  // Results.
  for (var i = 0, test; test = this.tests[i]; i++) {
    var result = this.normalizeTimesToTest ?
                 this.normalizedTimes_[test] :
                 this.medianReflowTimes_[test]
    this.resultsParams.push(test + '=' + result);
    this.results[test] = result;
  }

  // Inserts a result el into the doc for selenium-rc to block on.
  var el = document.createElement('input');
  el.type = 'hidden';
  el.id = 'rt-results';
  el.value = this.resultsParams.join(',');
  this.body_.appendChild(el, this.body_.firstChild);

  if (this.testFeedbackEl_) {
    this.testFeedbackEl_.innerHTML = 'All done with the reflow tests!';
  }

  // Send and or render on page.
  if (this.shouldSendResultsToServer_) {
    if (this.testFeedbackEl_) {
      this.testFeedbackEl_.innerHTML +=
          '<br>Sending your results to be saved...';
    }
    this.sendResultsToServer_();
  }

  this.onTestsComplete(this.results);
};


/**
 * Provides a function for subclasses/functional uses to implement.
 * @param {array.<string>} results The results array where test=result.
 */
ReflowTimer.prototype.onTestsComplete = function(results) {};


/******************************
 * Various Reflow Tests
 ******************************/

ReflowTimer.prototype.testDisplaySetUp = function() {
  this.containerStyle_.display = 'none';
};
ReflowTimer.prototype.testDisplay = function() {
  this.containerStyle_.display = '';
};


ReflowTimer.prototype.testVisibilitySetUp = function() {
  this.containerStyle_.visibility = 'hidden';
};
ReflowTimer.prototype.testVisibility = function() {
  this.containerStyle_.visibility = 'visible';
};


ReflowTimer.prototype.testOverflowHiddenSetUp = function() {
  this.originalValue_ = this.containerStyle_.overflow;
};
ReflowTimer.prototype.testOverflowHidden = function() {
  this.containerStyle_.overflow = 'hidden';
};
ReflowTimer.prototype.testOverflowHiddenTearDown = function() {
  this.containerStyle_.overflow = this.originalValue_;
};


ReflowTimer.prototype.testOverflowAutoSetUp = function() {
  this.originalValue_ = this.containerStyle_.overflow;
};
ReflowTimer.prototype.testOverflowAuto = function() {
  this.containerStyle_.overflow = 'auto';
};
ReflowTimer.prototype.testOverflowAutoTearDown = function() {
  this.containerStyle_.overflow = this.originalValue_;
};


ReflowTimer.prototype.testOverflowVisibleSetUp = function() {
  this.originalValue_ = this.containerStyle_.overflow;
};
ReflowTimer.prototype.testOverflowVisible = function() {
  this.containerStyle_.overflow = 'visible';
};
ReflowTimer.prototype.testOverflowVisibleTearDown = function() {
  this.containerStyle_.overflow = this.originalValue_;
};


ReflowTimer.prototype.testMarginPxSetUp = function() {
  this.originalValue_ = this.containerStyle_.margin;
};
ReflowTimer.prototype.testMarginPx = function() {
  this.containerStyle_.margin = '20px';
};
ReflowTimer.prototype.testMarginPxTearDown = function() {
  this.containerStyle_.margin = this.originalValue_;
};


ReflowTimer.prototype.testPaddingPxSetUp = function() {
  this.originalValue_ = this.containerStyle_.padding;
};
ReflowTimer.prototype.testPaddingPx = function() {
  this.containerStyle_.padding = '20px';
};
ReflowTimer.prototype.testPaddingPxTearDown = function() {
  this.containerStyle_.padding = this.originalValue_;
};


ReflowTimer.prototype.testPaddingEmSetUp = function() {
  this.originalValue_ = this.containerStyle_.padding;
};
ReflowTimer.prototype.testPaddingEm = function() {
  this.containerStyle_.padding = '4em';
};
ReflowTimer.prototype.testPaddingEmTearDown = function() {
  this.containerStyle_.padding = this.originalValue_;
};


ReflowTimer.prototype.testPaddingLeftPxSetUp = function() {
  this.originalValue_ = this.containerStyle_.paddingLeft;
};
ReflowTimer.prototype.testPaddingLeftPx = function() {
  this.containerStyle_.paddingLeft = '20px';
};
ReflowTimer.prototype.testPaddingLeftPxTearDown = function() {
  this.containerStyle_.paddingLeft = this.originalValue_;
};


ReflowTimer.prototype.testPaddingLeftLonghandScriptSetUp = function() {
  this.originalValue_ = this.containerStyle_.padding;
};
ReflowTimer.prototype.testPaddingLeftLonghandScript = function() {
  this.containerStyle_.padding = '0 0 0 20px';
};
ReflowTimer.prototype.testPaddingLeftLonghandScriptTearDown = function() {
  this.containerStyle_.padding = this.originalValue_;
};


ReflowTimer.prototype.testPaddingLeftLonghandClassSetUp = function() {
  this.originalValue_ = this.containerEl_.className;
};
ReflowTimer.prototype.testPaddingLeftLonghandClass = function() {
  this.containerEl_.className = ReflowTimer.TEST_CLASS_NAME +
      '-padding-left-longhand';
};
ReflowTimer.prototype.testPaddingLeftLonghandClassTearDown = function() {
  this.containerEl_.className = this.originalValue_;
};


ReflowTimer.prototype.testPaddingLeftShorthandClassSetUp = function() {
  this.originalValue_ = this.containerEl_.className;
};
ReflowTimer.prototype.testPaddingLeftShorthandClass = function() {
  this.containerEl_.className = ReflowTimer.TEST_CLASS_NAME +
      '-padding-left-shorthand';
};
ReflowTimer.prototype.testPaddingLeftShorthandClassTearDown = function() {
  this.containerEl_.className = this.originalValue_;
};


ReflowTimer.prototype.testWidthPxSetUp = function() {
  this.originalValue_ = this.containerStyle_.width;
};
ReflowTimer.prototype.testWidthPx = function() {
  this.containerStyle_.width = '500px';
};
ReflowTimer.prototype.testWidthPxTearDown = function() {
  this.containerStyle_.width = this.originalValue_;
};


ReflowTimer.prototype.testLineHeightSetUp = function() {
  this.originalValue_ = this.containerStyle_.lineHeight;
};
ReflowTimer.prototype.testLineHeight = function() {
  this.containerStyle_.lineHeight = '2';
};
ReflowTimer.prototype.testLineHeightTearDown = function() {
  this.containerStyle_.lineHeight = this.originalValue_;
};


ReflowTimer.prototype.testFontSizePxSetUp = function() {
  this.originalValue_ = this.containerStyle_.fontSize;
};
ReflowTimer.prototype.testFontSizePx = function() {
  this.containerStyle_.fontSize = '20px';
};
ReflowTimer.prototype.testFontSizePxTearDown = function() {
  this.containerStyle_.fontSize = this.originalValue_;
};


ReflowTimer.prototype.testFontSizeEmSetUp = function() {
  this.originalValue_ = this.containerStyle_.fontSize;
};
ReflowTimer.prototype.testFontSizeEm = function() {
  this.containerStyle_.fontSize = '2em';
};
ReflowTimer.prototype.testFontSizeEmTearDown = function() {
  this.containerStyle_.fontSize = this.originalValue_;
};


ReflowTimer.prototype.testWidthPercentSetUp = function() {
  this.originalValue_ = this.containerStyle_.width;
};
ReflowTimer.prototype.testWidthPercent = function() {
  this.containerStyle_.width = '50%';
};
ReflowTimer.prototype.testWidthPercentTearDown = function() {
  this.containerStyle_.width = this.originalValue_;
};


ReflowTimer.prototype.testNonMatchingClassSetUp = function() {
  this.originalValue_ = this.containerEl_.className;
};
ReflowTimer.prototype.testNonMatchingClass = function() {
  this.containerEl_.className = ReflowTimer.TEST_CLASS_NAME + '-nomatch';
};
ReflowTimer.prototype.testNonMatchingClassTearDown = function() {
  this.containerEl_.className = this.originalValue_;
};


ReflowTimer.prototype.testFourClassReflowsSetUp = function() {
  this.originalValue_ = this.containerEl_.className;
};
ReflowTimer.prototype.testFourClassReflows = function() {
  this.containerEl_.className = ReflowTimer.TEST_CLASS_NAME;
};
ReflowTimer.prototype.testFourClassReflowsTearDown = function() {
  this.containerEl_.className = this.originalValue_;
};


ReflowTimer.prototype.testFourScriptReflowsSetUp = function() {
  this.originalValue_ = [];
  this.originalValue_[0] = this.containerStyle_.fontSize;
  this.originalValue_[1] = this.containerStyle_.lineHeight;
  this.originalValue_[2] = this.containerStyle_.paddingLeft;
  this.originalValue_[3] = this.containerStyle_.marginTop;
};
ReflowTimer.prototype.testFourScriptReflows = function() {
  this.containerStyle_.fontSize = '20px';
  this.containerStyle_.lineHeight = '10px';
  this.containerStyle_.paddingLeft = '10px';
  this.containerStyle_.marginTop = '7px';
};
ReflowTimer.prototype.testFourScriptReflowsTearDown = function() {
  this.containerStyle_.fontSize = this.originalValue_[0];
  this.containerStyle_.lineHeight = this.originalValue_[1];
  this.containerStyle_.paddingLeft = this.originalValue_[2];
  this.containerStyle_.marginTop = this.originalValue_[3];
};


ReflowTimer.prototype.testTwoScriptReflowsSetUp = function() {
  this.originalValue_ = [];
  this.originalValue_[0] = this.containerStyle_.fontSize;
  this.originalValue_[1] = this.containerStyle_.paddingLeft;
};
ReflowTimer.prototype.testTwoScriptReflows = function() {
  this.containerStyle_.fontSize = '20px';
  this.containerStyle_.paddingLeft = '10px';
};
ReflowTimer.prototype.testTwoScriptReflowsTearDown = function() {
  this.containerStyle_.fontSize = this.originalValue_[0];
  this.containerStyle_.paddingLeft = this.originalValue_[1];
};


ReflowTimer.prototype.testBackgroundSetUp = function() {
  this.originalValue_ = this.containerStyle_.background;
};
ReflowTimer.prototype.testBackground = function() {
  this.containerStyle_.background = '#f0f0f0';
};
ReflowTimer.prototype.testBackgroundTearDown = function() {
  this.containerStyle_.background = this.originalValue_;
};


ReflowTimer.prototype.testGetOffsetHeight = function() {};


/**
 * Tests the time to perform selector matching.
 * This may be Mozilla specific based on how they optimize.
 * David explained that by making a rule that couldn't match ever but yet gets
 * activated by setting a body attribute, we can guage the time to perform
 * selector matching without reflow.
 * @private
 */
ReflowTimer.prototype.testSelectorMatchTimeSetUp = function() {
  if (!document.getElementById('rt-css-selectors')) {
    var cssText = 'body[' + ReflowTimer.TEST_BODY_ATTR + '=' +
        ReflowTimer.TEST_BODY_ATTR_VAL + '] html {color:pink}';
    Util.addCssText(cssText, 'rt-css-selectors');
  }
};
ReflowTimer.prototype.testSelectorMatchTime = function() {
  this.body_.setAttribute(ReflowTimer.TEST_BODY_ATTR,
      ReflowTimer.TEST_BODY_ATTR_VAL);
};
ReflowTimer.prototype.testSelectorMatchTimeTearDown = function() {
  this.body_.setAttribute(ReflowTimer.TEST_BODY_ATTR, '');
};


/**
 * @see http://ejohn.org/blog/browser-paint-events/
 */
ReflowTimer.prototype.logPaintEvents_ = function(e) {
  var log = {
      'time': new Date().getTime(),
      'clientRects': e.clientRects,
      'boundingClientRect': e.boundingClientRect};
  this.paintEvents_.push(log);
};


/**
 * Sends the reflow time to our server.
 * @private
 */
ReflowTimer.prototype.sendResultsToServer_ = function() {

  var uriParams = 'category=reflow' + '&results=' +
      this.resultsParams.join(',');

  // Add on params to the beacon.
  var paramsEl = document.getElementById('rt-params');
  if (paramsEl) {
    uriParams += '&params=' + paramsEl.value;

  // store the entire window.location.href as a param
  } else {
    uriParams += '&params=' + encodeURI(window.location.href);
  }

  // Gets our csrf_token from the page.
  var csrfTokenEl = document.getElementById('csrf_token');
  if (csrfTokenEl) {
    var csrfToken = csrfTokenEl.value;
    uriParams += '&csrf_token=' + csrfToken;
  }

  /**
   * @type {Beacon}
   */
  this.beacon_ = new Beacon(uriParams);
  this.beacon_.onComplete = Util.curry(this, this.onBeaconComplete_);
  this.beacon_.send();
};


/**
 * Private beacon complete method, which fires the public onBeaconComplete
 * method.
 * @private
 */
ReflowTimer.prototype.onBeaconComplete_ = function() {
  if (this.testFeedbackEl_) {
    this.testFeedbackEl_.innerHTML = 'Your results were saved.';
  }
  this.onBeaconComplete();
};


/**
 * Provides a function for subclasses/functional uses to implement.
 */
ReflowTimer.prototype.onBeaconComplete = function() {};

var e=false,l=Object,m="push",n="length",o="propertyIsEnumerable",r="indexOf",s="imports",t="call",u=this,v=function(a){var c=typeof a;if(c=="object")if(a){if(a instanceof Array||!(a instanceof l)&&l.prototype.toString[t](a)=="[object Array]"||typeof a[n]=="number"&&typeof a.splice!="undefined"&&typeof a[o]!="undefined"&&!a[o]("splice"))return"array";if(!(a instanceof l)&&(l.prototype.toString[t](a)=="[object Function]"||typeof a[t]!="undefined"&&typeof a[o]!="undefined"&&!a[o]("call")))return"function"}else return"null";
else if(c=="function"&&typeof a[t]=="undefined")return"object";return c};Math.floor(Math.random()*2147483648).toString(36);var w=function(a){for(var c=1;c<arguments[n];c++){var b=arguments[c],d,i=v(b);if(d=i=="array"||i=="object"&&typeof b[n]=="number"){if(v(b)=="array")b=b.concat();else if(v(b)=="array")b=b.concat();else{for(var g=[],f=0,h=b[n];f<h;f++)g[f]=b[f];b=g}a[m].apply(a,b)}else a[m](b)}};var x=function(a){return a.replace(/^[\s\xa0]+|[\s\xa0]+$/g,"")},y=function(a,c){return a[r](c)!=-1},A=function(a,c){for(var b=0,d=x(String(a)).split("."),i=x(String(c)).split("."),g=Math.max(d[n],i[n]),f=0;b==0&&f<g;f++){var h=d[f]||"",j=i[f]||"",E=new RegExp("(\\d*)(\\D*)","g"),k=new RegExp("(\\d*)(\\D*)","g");do{var p=E.exec(h)||["","",""],q=k.exec(j)||["","",""];if(p[0][n]==0&&q[0][n]==0)break;var R=p[1][n]==0?0:parseInt(p[1],10),S=q[1][n]==0?0:parseInt(q[1],10);b=z(R,S)||z(p[2][n]==0,q[2][n]==
0)||z(p[2],q[2])}while(b==0)}return b},z=function(a,c){if(a<c)return-1;else if(a>c)return 1;return 0};(Date.now||function(){return(new Date).getTime()})();var B,C,D,F,G,H,I,J,K,L,M=function(){return u.navigator?u.navigator.userAgent:null},N=function(){return u.navigator};(function(){H=G=F=D=C=B=e;var a;if(a=M()){var c=N();B=a[r]("Opera")==0;C=!B&&a[r]("MSIE")!=-1;F=(D=!B&&a[r]("WebKit")!=-1)&&a[r]("Mobile")!=-1;H=(G=!B&&!D&&c.product=="Gecko")&&c.vendor=="Camino"}})();var O=B,P=C,Q=G,T=D,U=function(){var a=N();return a&&a.platform||""}();(function(){I=y(U,"Mac");J=y(U,"Win");K=y(U,"Linux");L=!!N()&&y(N().appVersion||"","X11")})();
var aa=function(){var a="",c;if(O&&u.opera){var b=u.opera.version;a=typeof b=="function"?b():b}else{if(Q)c=/rv\:([^\);]+)(\)|;)/;else if(P)c=/MSIE\s+([^\);]+)(\)|;)/;else if(T)c=/WebKit\/(\S+)/;if(c){var d=c.exec(M());a=d?d[1]:""}}return a}();T&&A(aa,"521");var V=function(a){var c=null;try{c=a.rules||a.cssRules}catch(b){if(b.code==15)throw b;}return c},W=function(a,c){var b=[],d=a||document.styleSheets,i=c!==undefined?c:e;if(d[s]&&d[s][n])for(var g=0,f=d[s][n];g<f;g++)w(b,W(d[s][g]));else if(d[n]){g=0;for(f=d[n];g<f;g++)w(b,W(d[g]))}else{var h=V(d);if(h&&h[n]){g=0;f=h[n];for(var j;g<f;g++){j=h[g];j.styleSheet&&w(b,W(j.styleSheet))}}}if((d.type||d.rules)&&(!d.disabled||i))b[m](d);return b};{var X=function(a){for(var c,b=a||document.styleSheets,d=[],i=W(b),g=0;b=i[g];g++){var f=V(b);if(f&&f[n])for(var h=0,j=0,E=f[n],k;j<E;j++){k=f[j];if(!k.href){k.parentStyleSheet||(k.style["-goog-parent-stylesheet"]=b);k.style["-goog-rule-index"]=h;d[m](k)}h++}}return c=d},Y="goog.cssom.getAllCssStyleRules".split("."),Z=u;!(Y[0]in Z)&&Z.execScript&&Z.execScript("var "+Y[0]);for(var $;Y[n]&&($=Y.shift());)if(!Y[n]&&X!==undefined)Z[$]=X;else Z=Z[$]?Z[$]:(Z[$]={})};
// Copyright 2008-9 Google Inc.  All Rights Reserved.

/**
 * @fileoverview An interactive form of reflow_timer.js
 * @author elsigh@google.com (Lindsey Simon)
 *
 * TODO(elsigh): allow targeting by element.
 * TODO(elsigh): show results about dom depth and * elements.
 */

(function(){

  var FONT_SIZE = '13px';
  var FONT_FAMILY = 'Arial, sans';
  var COLOR = '#111';

  // TODO(elsigh): Also remove event listeners to prevent memory leakage.
  var dispose = function() {
    var previousRunEl = document.getElementById('rt-alltests');
    if (previousRunEl) {
      previousRunEl.parentNode.removeChild(previousRunEl);
    }
    var feedbackEl = document.getElementById('rt-feedback');
    if (feedbackEl) {
      feedbackEl.parentNode.removeChild(feedbackEl);
    }
  };
  dispose();

  var allTests = ReflowTimer.prototype.tests;
  //for (var i = 0, test; test = ReflowTimer.prototype.unusedTests[i]; i++) {
  //  allTests.push(test);
  //}
  //allTests.sort();

  var divEl = document.createElement('div');
  var spanEl = document.createElement('span');
  spanEl.style.marginLeft = '4px';

  var buttonEl = document.createElement('button');
  var style = buttonEl.style;
  style.textAlign = 'left';
  style.width = '12em';
  style.padding = '0';
  style.margin = '0';
  style.fontSize = FONT_SIZE;
  style.fontFamily = FONT_FAMILY;
  style.color = COLOR;
  style.background = 'none';

  var container = divEl.cloneNode(false);
  var style = container.style;
  style.position = 'absolute';
  style.left = '20px';
  style.top = '20px';
  style.border = '3px solid #444';
  style.padding = '5px 5px 15px 15px';
  style.background = '#eee';
  style.width = '22em';
  style.font = '13px normal Arial, sans';
  style.lineHeight = '1.3';
  style.color = COLOR;
  style.textAlign = 'left';
  style.zIndex = '999';
  if (style.setProperty) {
    style.setProperty('-moz-border-radius', '10px', '');
    style.setProperty('-moz-box-shadow', '5px 5px 5px #ccc', '');
    style.setProperty('-webkit-border-radius', '10px', '');
    style.setProperty('-webkit-box-shadow', '5px 5px 5px #ccc', '');
  }
  container.id = 'rt-alltests';
  var header = divEl.cloneNode(false);
  var anchor = document.createElement('a');
  style = anchor.style;
  style.fontSize = '14px';
  style.fontWeight = 'bold';
  style.textDecoration = 'none';
  style.color = '#333';
  anchor.appendChild(document.createTextNode('Reflow Timer'));
  anchor.target = '_blank';
  anchor.href = 'http://www.browserscope.org/reflow/';
  header.appendChild(anchor);
  container.appendChild(header);

  var close = divEl.cloneNode(false);
  close.appendChild(document.createTextNode('close'));
  style = close.style;
  style.position = 'absolute';
  style.fontSize = '9px';
  style.top = '5px';
  style.right = '5px';
  style.cursor = 'pointer';
  style.color = '#777';
  container.appendChild(close);
  close.onclick = dispose;

  var listItem = document.createElement('li');
  style = listItem.style;
  style.padding = '0';
  style.height = 'auto';
  style.width = 'auto';
  style.background = 'none';
  style.border = 'none';
  style.margin = '2px 0';
  style.cssFloat = 'none';
  style.styleFloat = 'none';
  style.display = 'list-item';


  // Stats
  var numElements = document.getElementsByTagName('*').length;
  try {
    var rules = goog.cssom.getAllCssStyleRules();
    var numCss = rules.length;
  } catch(e) {
    var numCss = 'Exception...';
  }
  var ul = document.createElement('ul');
  var style = ul.style;
  style.listStyle = 'none';
  style.padding = '0 0 0 1em';
  style.margin = '.2em 0 0 0';

  var li = listItem.cloneNode(false);
  li.appendChild(document.createTextNode('# Elements: ' + numElements));
  ul.appendChild(li);

  var li = listItem.cloneNode(false);
  li.appendChild(document.createTextNode('# CSS rules: ' + numCss));
  ul.appendChild(li);

  // TODO(elsigh): this would be cool!
  //var li = listItem.cloneNode(false);
  //li.appendChild(document.createTextNode('Avg Depth: X (min x, max x)'));
  //ul.appendChild(li);

  var li = listItem.cloneNode(false);
  var reflowElLabel = document.createElement('label');
  reflowElLabel.setAttribute('for', 'bs-el-id');
  reflowElLabel.appendChild(document.createTextNode('ID:'));
  reflowElLabel.style.display = 'inline';
  li.appendChild(reflowElLabel);
  var reflowElInput = document.createElement('input');
  reflowElInput.id = reflowElLabel.getAttribute('for');
  reflowElInput.type = 'text';
  reflowElInput.size = '18';
  if (window.location.href.match('/reflow/test')) {
    reflowElInput.value = 'g-content';
  }
  li.appendChild(reflowElInput);
  ul.appendChild(li);

  container.appendChild(ul);

  // Runs the ReflowTimer
  var buttonClickHandler = function(e) {
    var thisButton = this;
    var span = thisButton.nextSibling;
    span.innerHTML = '';
    span.appendChild(document.createTextNode('runnin..'));

    // Does the user want to run the test on a particular el?
    var reflowElId = reflowElInput.value;
    var reflowEl;
    if (reflowElId) {
      reflowEl = document.getElementById(reflowElId);
    }

    thisButton.disabled = true;
    thisButton.rt = new ReflowTimer(false, reflowEl);
    thisButton.rt.normalizeTimesToTest = false;
    thisButton.rt.tests = [thisButton.test];
    thisButton.rt.onTestsComplete = function(medianReflowTimes) {
      thisButton.disabled = false;
      var time = medianReflowTimes[this.tests[0]];
      span.innerHTML = '';
      span.appendChild(document.createTextNode(time + ' ms.'));
      if (runningAllTests) {
        var nextButton = document.getElementById('rt-btn-' +
            thisButton.nextIndex);
        if (nextButton) {
          nextButton.onclick();
        } else {
          // all done
          runningAllTests = false;
        }
      }
    };
    thisButton.rt.run();
  };

  var buttonContainer = divEl.cloneNode(false);
  buttonContainer.style.margin = '5px 0 8px 0';

  var stopRunningAllTests = function() {
    runningAllTests = false;
    runAllTestsButton.innerHTML = '';
    runAllTestsButton.appendChild(document.createTextNode('run all tests'));
    runAllTestsButton.onclick = runAllTests;
    for (var i = 0, button; button = buttonEls[i]; i++) {
      button.disabled = false;
      if (button.rt) {
        button.rt.onTestsComplete = function() {};
      }
    }
  };

  var runningAllTests = false;

  // Run all button.
  var runAllTests = function() {
    runningAllTests = true;
    clearResults();
    runAllTestsButton.innerHTML = '';
    runAllTestsButton.appendChild(document.createTextNode('stop'));
    runAllTestsButton.onclick = stopRunningAllTests;
    for (var i = 0, button; button = buttonEls[i]; i++) {
      button.disabled = true;
    }
    buttonEls[0].onclick();
  };
  var runAllTestsButton = buttonEl.cloneNode(false);
  runAllTestsButton.appendChild(document.createTextNode('run all tests'));
  runAllTestsButton.style.width = '8em';
  runAllTestsButton.onclick = runAllTests;
  buttonContainer.appendChild(runAllTestsButton);

  // Clear results button.
  var clearResults = function() {
    for (var i = 0, span; span = resultEls[i]; i++) {
      span.innerHTML = '';
    }
  };
  var button = buttonEl.cloneNode(false);
  button.appendChild(document.createTextNode('clear'));
  button.style.width = '4em';
  button.style.cssFloat = 'right';
  button.style.styleFloat = 'right';
  button.onclick = clearResults;
  buttonContainer.appendChild(button);

  container.appendChild(buttonContainer);

  var resultEls = [];
  var buttonEls = [];
  for (var i = 0, test; test = allTests[i]; i++) {
    var buttonContainer = divEl.cloneNode(false);
    buttonContainer.style.marginTop = '5px';

    var button = buttonEl.cloneNode(false);
    button.appendChild(document.createTextNode(test.replace('test', '')));
    button.id = 'rt-btn-' + i;
    button.nextIndex = i + 1;
    button.test = test;
    button.onclick = buttonClickHandler;
    buttonEls.push(button);

    var span = spanEl.cloneNode(false);
    span.style.fontWeight = 'bold';
    resultEls.push(span);

    buttonContainer.appendChild(button);
    buttonContainer.appendChild(span);
    container.appendChild(buttonContainer);
  }
  document.body.appendChild(container);

})();
