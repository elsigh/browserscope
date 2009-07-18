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
ReflowTimer.REFLOW_REST_TIME = 100;


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
ReflowTimer.TEST_MULTIPLE_REFLOW_CSSTEXT = 'font-size: 20px !important; ' +
    'line-height: 10px !important;' +
    'padding-left: 10px !important;' +
    'margin-top: 7px; !important';


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
 */
ReflowTimer.prototype.normalizeTimesToTest = 'testDisplay';


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
  this.containerStyle_.visibility = '';
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

var a, goog = goog || {};
goog.global = this;
goog.DEBUG = true;
goog.LOCALE = "en_US";
goog.evalWorksForGlobals_ = null;
goog.provide = function(name$30) {
  goog.exportPath_(name$30)
};
goog.exportPath_ = function(name$31, opt_object, opt_objectToExportTo) {
  var parts = name$31.split("."), cur = opt_objectToExportTo || goog.global;
  !(parts[0] in cur) && cur.execScript && cur.execScript("var " + parts[0]);
  for(var part;parts.length && (part = parts.shift());)if(!parts.length && goog.isDef(opt_object))cur[part] = opt_object;
  else cur = cur[part] ? cur[part] : (cur[part] = {})
};
goog.getObjectByName = function(name$32, opt_obj) {
  for(var parts$1 = name$32.split("."), cur$1 = opt_obj || goog.global, part$1;part$1 = parts$1.shift();)if(cur$1[part$1])cur$1 = cur$1[part$1];
  else return null;
  return cur$1
};
goog.globalize = function(obj$2, opt_global) {
  var global = opt_global || goog.global;
  for(var x$35 in obj$2)global[x$35] = obj$2[x$35]
};
goog.addDependency = function() {
};
goog.require = function() {
};
goog.useStrictRequires = false;
goog.basePath = "";
goog.nullFunction = function() {
};
goog.identityFunction = function() {
  return arguments[0]
};
goog.abstractMethod = function() {
  throw Error("unimplemented abstract method");
};
goog.addSingletonGetter = function(ctor) {
  ctor.getInstance = function() {
    return ctor.instance_ || (ctor.instance_ = new ctor)
  }
};
goog.typeOf = function(value$8) {
  var s$1 = typeof value$8;
  if(s$1 == "object")if(value$8) {
    if(value$8 instanceof Array || !(value$8 instanceof Object) && Object.prototype.toString.call(value$8) == "[object Array]" || typeof value$8.length == "number" && typeof value$8.splice != "undefined" && typeof value$8.propertyIsEnumerable != "undefined" && !value$8.propertyIsEnumerable("splice"))return"array";
    if(!(value$8 instanceof Object) && (Object.prototype.toString.call(value$8) == "[object Function]" || typeof value$8.call != "undefined" && typeof value$8.propertyIsEnumerable != "undefined" && !value$8.propertyIsEnumerable("call")))return"function"
  }else return"null";
  else if(s$1 == "function" && typeof value$8.call == "undefined")return"object";
  return s$1
};
goog.propertyIsEnumerableCustom_ = function(object, propName) {
  if(propName in object)for(var key$3 in object)if(key$3 == propName && Object.prototype.hasOwnProperty.call(object, propName))return true;
  return false
};
goog.propertyIsEnumerable_ = function(object$1, propName$1) {
  return object$1 instanceof Object ? Object.prototype.propertyIsEnumerable.call(object$1, propName$1) : goog.propertyIsEnumerableCustom_(object$1, propName$1)
};
goog.isDef = function(val) {
  return val !== undefined
};
goog.isNull = function(val$1) {
  return val$1 === null
};
goog.isDefAndNotNull = function(val$2) {
  return val$2 != null
};
goog.isArray = function(val$3) {
  return goog.typeOf(val$3) == "array"
};
goog.isArrayLike = function(val$4) {
  var type$8 = goog.typeOf(val$4);
  return type$8 == "array" || type$8 == "object" && typeof val$4.length == "number"
};
goog.isDateLike = function(val$5) {
  return goog.isObject(val$5) && typeof val$5.getFullYear == "function"
};
goog.isString = function(val$6) {
  return typeof val$6 == "string"
};
goog.isBoolean = function(val$7) {
  return typeof val$7 == "boolean"
};
goog.isNumber = function(val$8) {
  return typeof val$8 == "number"
};
goog.isFunction = function(val$9) {
  return goog.typeOf(val$9) == "function"
};
goog.isObject = function(val$10) {
  var type$9 = goog.typeOf(val$10);
  return type$9 == "object" || type$9 == "array" || type$9 == "function"
};
goog.getHashCode = function(obj$3) {
  if(obj$3.hasOwnProperty && obj$3.hasOwnProperty(goog.HASH_CODE_PROPERTY_))return obj$3[goog.HASH_CODE_PROPERTY_];
  obj$3[goog.HASH_CODE_PROPERTY_] || (obj$3[goog.HASH_CODE_PROPERTY_] = ++goog.hashCodeCounter_);
  return obj$3[goog.HASH_CODE_PROPERTY_]
};
goog.removeHashCode = function(obj$4) {
  "removeAttribute" in obj$4 && obj$4.removeAttribute(goog.HASH_CODE_PROPERTY_);
  try {
    delete obj$4[goog.HASH_CODE_PROPERTY_]
  }catch(ex) {
  }
};
goog.HASH_CODE_PROPERTY_ = "closure_hashCode_" + Math.floor(Math.random() * 2147483648).toString(36);
goog.hashCodeCounter_ = 0;
goog.cloneObject = function(proto) {
  var type$10 = goog.typeOf(proto);
  if(type$10 == "object" || type$10 == "array") {
    if(proto.clone)return proto.clone.call(proto);
    var clone = type$10 == "array" ? [] : {};
    for(var key$4 in proto)clone[key$4] = goog.cloneObject(proto[key$4]);
    return clone
  }return proto
};
goog.bind = function(fn, selfObj) {
  var boundArgs = fn.boundArgs_;
  if(arguments.length > 2) {
    var args = Array.prototype.slice.call(arguments, 2);
    boundArgs && args.unshift.apply(args, boundArgs);
    boundArgs = args
  }selfObj = fn.boundSelf_ || selfObj;
  fn = fn.boundFn_ || fn;
  var newfn, context = selfObj || goog.global;
  newfn = boundArgs ? function() {
    var args$1 = Array.prototype.slice.call(arguments);
    args$1.unshift.apply(args$1, boundArgs);
    return fn.apply(context, args$1)
  } : function() {
    return fn.apply(context, arguments)
  };
  newfn.boundArgs_ = boundArgs;
  newfn.boundSelf_ = selfObj;
  newfn.boundFn_ = fn;
  return newfn
};
goog.partial = function(fn$1) {
  var args$2 = Array.prototype.slice.call(arguments, 1);
  args$2.unshift(fn$1, null);
  return goog.bind.apply(null, args$2)
};
goog.mixin = function(target$12, source) {
  for(var x$36 in source)target$12[x$36] = source[x$36]
};
goog.now = Date.now || function() {
  return(new Date).getTime()
};
goog.globalEval = function(script$1) {
  if(goog.global.execScript)goog.global.execScript(script$1, "JavaScript");
  else if(goog.global.eval) {
    if(goog.evalWorksForGlobals_ == null) {
      goog.global.eval("var _et_ = 1;");
      if(typeof goog.global._et_ != "undefined") {
        delete goog.global._et_;
        goog.evalWorksForGlobals_ = true
      }else goog.evalWorksForGlobals_ = false
    }if(goog.evalWorksForGlobals_)goog.global.eval(script$1);
    else {
      var doc$3 = goog.global.document, scriptElt = doc$3.createElement("script");
      scriptElt.type = "text/javascript";
      scriptElt.defer = false;
      scriptElt.appendChild(doc$3.createTextNode(script$1));
      doc$3.body.appendChild(scriptElt);
      doc$3.body.removeChild(scriptElt)
    }
  }else throw Error("goog.globalEval not available");
};
goog.declareType = function() {
};
goog.typedef = true;
goog.getCssName = function(className$1, opt_modifier) {
  var cssName = className$1 + (opt_modifier ? "-" + opt_modifier : "");
  return goog.cssNameMapping_ && cssName in goog.cssNameMapping_ ? goog.cssNameMapping_[cssName] : cssName
};
goog.setCssNameMapping = function(mapping) {
  goog.cssNameMapping_ = mapping
};
goog.getMsg = function(str$6, opt_values) {
  var values = opt_values || {};
  for(var key$5 in values)str$6 = str$6.replace(new RegExp("\\{\\$" + key$5 + "\\}", "gi"), values[key$5]);
  return str$6
};
goog.exportSymbol = function(publicPath, object$2, opt_objectToExportTo$1) {
  goog.exportPath_(publicPath, object$2, opt_objectToExportTo$1)
};
goog.exportProperty = function(object$3, publicName, symbol) {
  object$3[publicName] = symbol
};
goog.inherits = function(childCtor, parentCtor) {
  function tempCtor() {
  }
  tempCtor.prototype = parentCtor.prototype;
  childCtor.superClass_ = parentCtor.prototype;
  childCtor.prototype = new tempCtor
};
goog.MODIFY_FUNCTION_PROTOTYPES = true;
if(goog.MODIFY_FUNCTION_PROTOTYPES) {
  Function.prototype.bind = function(selfObj$1) {
    if(arguments.length > 1) {
      var args$3 = Array.prototype.slice.call(arguments, 1);
      args$3.unshift(this, selfObj$1);
      return goog.bind.apply(null, args$3)
    }else return goog.bind(this, selfObj$1)
  };
  Function.prototype.partial = function() {
    var args$4 = Array.prototype.slice.call(arguments);
    args$4.unshift(this, null);
    return goog.bind.apply(null, args$4)
  };
  Function.prototype.inherits = function(parentCtor$1) {
    goog.inherits(this, parentCtor$1)
  };
  Function.prototype.mixin = function(source$1) {
    goog.mixin(this.prototype, source$1)
  }
};goog.array = {};
goog.array.ArrayLike = goog.typedef;
goog.array.peek = function(array) {
  return array[array.length - 1]
};
goog.array.indexOf = function(arr$7, obj$5, opt_fromIndex$4) {
  if(arr$7.indexOf)return arr$7.indexOf(obj$5, opt_fromIndex$4);
  if(Array.indexOf)return Array.indexOf(arr$7, obj$5, opt_fromIndex$4);
  for(var i$3 = opt_fromIndex$4 == null ? 0 : opt_fromIndex$4 < 0 ? Math.max(0, arr$7.length + opt_fromIndex$4) : opt_fromIndex$4;i$3 < arr$7.length;i$3++)if(i$3 in arr$7 && arr$7[i$3] === obj$5)return i$3;
  return-1
};
goog.array.lastIndexOf = function(arr$8, obj$6, opt_fromIndex$5) {
  var fromIndex$1 = opt_fromIndex$5 == null ? arr$8.length - 1 : opt_fromIndex$5;
  if(arr$8.lastIndexOf)return arr$8.lastIndexOf(obj$6, fromIndex$1);
  if(Array.lastIndexOf)return Array.lastIndexOf(arr$8, obj$6, fromIndex$1);
  if(fromIndex$1 < 0)fromIndex$1 = Math.max(0, arr$8.length + fromIndex$1);
  for(var i$4 = fromIndex$1;i$4 >= 0;i$4--)if(i$4 in arr$8 && arr$8[i$4] === obj$6)return i$4;
  return-1
};
goog.array.forEach = function(arr$9, f, opt_obj$1) {
  if(arr$9.forEach)arr$9.forEach(f, opt_obj$1);
  else if(Array.forEach)Array.forEach(arr$9, f, opt_obj$1);
  else for(var l$1 = arr$9.length, arr2 = goog.isString(arr$9) ? arr$9.split("") : arr$9, i$5 = 0;i$5 < l$1;i$5++)i$5 in arr2 && f.call(opt_obj$1, arr2[i$5], i$5, arr$9)
};
goog.array.forEachRight = function(arr$10, f$1, opt_obj$2) {
  for(var l$2 = arr$10.length, arr2$1 = goog.isString(arr$10) ? arr$10.split("") : arr$10, i$6 = l$2 - 1;i$6 >= 0;--i$6)i$6 in arr2$1 && f$1.call(opt_obj$2, arr2$1[i$6], i$6, arr$10)
};
goog.array.filter = function(arr$11, f$2, opt_obj$3) {
  if(arr$11.filter)return arr$11.filter(f$2, opt_obj$3);
  if(Array.filter)return Array.filter(arr$11, f$2, opt_obj$3);
  for(var l$3 = arr$11.length, res = [], resLength = 0, arr2$2 = goog.isString(arr$11) ? arr$11.split("") : arr$11, i$7 = 0;i$7 < l$3;i$7++)if(i$7 in arr2$2) {
    var val$11 = arr2$2[i$7];
    if(f$2.call(opt_obj$3, val$11, i$7, arr$11))res[resLength++] = val$11
  }return res
};
goog.array.map = function(arr$12, f$3, opt_obj$4) {
  if(arr$12.map)return arr$12.map(f$3, opt_obj$4);
  if(Array.map)return Array.map(arr$12, f$3, opt_obj$4);
  for(var l$4 = arr$12.length, res$1 = [], resLength$1 = 0, arr2$3 = goog.isString(arr$12) ? arr$12.split("") : arr$12, i$8 = 0;i$8 < l$4;i$8++)if(i$8 in arr2$3)res$1[resLength$1++] = f$3.call(opt_obj$4, arr2$3[i$8], i$8, arr$12);
  return res$1
};
goog.array.reduce = function(arr$13, f$4, val$12, opt_obj$5) {
  if(arr$13.reduce)return opt_obj$5 ? arr$13.reduce(goog.bind(f$4, opt_obj$5), val$12) : arr$13.reduce(f$4, val$12);
  var rval = val$12;
  goog.array.forEach(arr$13, function(val$13, index$32) {
    rval = f$4.call(opt_obj$5, rval, val$13, index$32, arr$13)
  });
  return rval
};
goog.array.reduceRight = function(arr$14, f$5, val$14, opt_obj$6) {
  if(arr$14.reduceRight)return opt_obj$6 ? arr$14.reduceRight(goog.bind(f$5, opt_obj$6), val$14) : arr$14.reduceRight(f$5, val$14);
  var rval$1 = val$14;
  goog.array.forEachRight(arr$14, function(val$15, index$33) {
    rval$1 = f$5.call(opt_obj$6, rval$1, val$15, index$33, arr$14)
  });
  return rval$1
};
goog.array.some = function(arr$15, f$6, opt_obj$7) {
  if(arr$15.some)return arr$15.some(f$6, opt_obj$7);
  if(Array.some)return Array.some(arr$15, f$6, opt_obj$7);
  for(var l$5 = arr$15.length, arr2$4 = goog.isString(arr$15) ? arr$15.split("") : arr$15, i$9 = 0;i$9 < l$5;i$9++)if(i$9 in arr2$4 && f$6.call(opt_obj$7, arr2$4[i$9], i$9, arr$15))return true;
  return false
};
goog.array.every = function(arr$16, f$7, opt_obj$8) {
  if(arr$16.every)return arr$16.every(f$7, opt_obj$8);
  if(Array.every)return Array.every(arr$16, f$7, opt_obj$8);
  for(var l$6 = arr$16.length, arr2$5 = goog.isString(arr$16) ? arr$16.split("") : arr$16, i$10 = 0;i$10 < l$6;i$10++)if(i$10 in arr2$5 && !f$7.call(opt_obj$8, arr2$5[i$10], i$10, arr$16))return false;
  return true
};
goog.array.find = function(arr$17, f$8, opt_obj$9) {
  var i$11 = goog.array.findIndex(arr$17, f$8, opt_obj$9);
  return i$11 < 0 ? null : goog.isString(arr$17) ? arr$17.charAt(i$11) : arr$17[i$11]
};
goog.array.findIndex = function(arr$18, f$9, opt_obj$10) {
  for(var l$7 = arr$18.length, arr2$6 = goog.isString(arr$18) ? arr$18.split("") : arr$18, i$12 = 0;i$12 < l$7;i$12++)if(i$12 in arr2$6 && f$9.call(opt_obj$10, arr2$6[i$12], i$12, arr$18))return i$12;
  return-1
};
goog.array.findRight = function(arr$19, f$10, opt_obj$11) {
  var i$13 = goog.array.findIndexRight(arr$19, f$10, opt_obj$11);
  return i$13 < 0 ? null : goog.isString(arr$19) ? arr$19.charAt(i$13) : arr$19[i$13]
};
goog.array.findIndexRight = function(arr$20, f$11, opt_obj$12) {
  for(var l$8 = arr$20.length, arr2$7 = goog.isString(arr$20) ? arr$20.split("") : arr$20, i$14 = l$8 - 1;i$14 >= 0;i$14--)if(i$14 in arr2$7 && f$11.call(opt_obj$12, arr2$7[i$14], i$14, arr$20))return i$14;
  return-1
};
goog.array.contains = function(arr$21, obj$7) {
  if(arr$21.contains)return arr$21.contains(obj$7);
  return goog.array.indexOf(arr$21, obj$7) > -1
};
goog.array.isEmpty = function(arr$22) {
  return arr$22.length == 0
};
goog.array.clear = function(arr$23) {
  if(!goog.isArray(arr$23))for(var i$15 = arr$23.length - 1;i$15 >= 0;i$15--)delete arr$23[i$15];
  arr$23.length = 0
};
goog.array.insert = function(arr$24, obj$8) {
  goog.array.contains(arr$24, obj$8) || arr$24.push(obj$8)
};
goog.array.insertAt = function(arr$25, obj$9, opt_i) {
  goog.array.splice(arr$25, opt_i, 0, obj$9)
};
goog.array.insertArrayAt = function(arr$26, elementsToAdd, opt_i$1) {
  goog.partial(goog.array.splice, arr$26, opt_i$1, 0).apply(null, elementsToAdd)
};
goog.array.insertBefore = function(arr$27, obj$10, opt_obj2) {
  var i$16;
  arguments.length == 2 || (i$16 = goog.array.indexOf(arr$27, opt_obj2)) == -1 ? arr$27.push(obj$10) : goog.array.insertAt(arr$27, obj$10, i$16)
};
goog.array.remove = function(arr$28, obj$11) {
  var i$17 = goog.array.indexOf(arr$28, obj$11), rv;
  if(rv = i$17 != -1)goog.array.removeAt(arr$28, i$17);
  return rv
};
goog.array.removeAt = function(arr$29, i$18) {
  return Array.prototype.splice.call(arr$29, i$18, 1).length == 1
};
goog.array.removeIf = function(arr$30, f$12, opt_obj$13) {
  var i$19 = goog.array.findIndex(arr$30, f$12, opt_obj$13);
  if(i$19 >= 0) {
    goog.array.removeAt(arr$30, i$19);
    return true
  }return false
};
goog.array.clone = function(arr$31) {
  if(goog.isArray(arr$31))return arr$31.concat();
  else {
    for(var rv$1 = [], i$20 = 0, len = arr$31.length;i$20 < len;i$20++)rv$1[i$20] = arr$31[i$20];
    return rv$1
  }
};
goog.array.toArray = function(object$4) {
  if(goog.isArray(object$4))return object$4.concat();
  return goog.array.clone(object$4)
};
goog.array.extend = function(arr1) {
  for(var i$21 = 1;i$21 < arguments.length;i$21++) {
    var arr2$8 = arguments[i$21];
    if(goog.isArrayLike(arr2$8)) {
      arr2$8 = goog.array.toArray(arr2$8);
      arr1.push.apply(arr1, arr2$8)
    }else arr1.push(arr2$8)
  }
};
goog.array.splice = function(arr$32) {
  return Array.prototype.splice.apply(arr$32, goog.array.slice(arguments, 1))
};
goog.array.slice = function(arr$33, start$1, opt_end$2) {
  return arguments.length <= 2 ? Array.prototype.slice.call(arr$33, start$1) : Array.prototype.slice.call(arr$33, start$1, opt_end$2)
};
goog.array.removeDuplicates = function(arr$34, opt_rv) {
  for(var rv$2 = opt_rv || arr$34, seen = {}, cursorInsert = 0, cursorRead = 0;cursorRead < arr$34.length;) {
    var current = arr$34[cursorRead++], hc = goog.isObject(current) ? goog.getHashCode(current) : current;
    if(!(hc in seen)) {
      seen[hc] = true;
      rv$2[cursorInsert++] = current
    }
  }rv$2.length = cursorInsert
};
goog.array.binarySearch = function(arr$35, target$13, opt_compareFn) {
  for(var left$1 = 0, right$1 = arr$35.length - 1, compareFn = opt_compareFn || goog.array.defaultCompare;left$1 <= right$1;) {
    var mid = left$1 + right$1 >> 1, compareResult = compareFn(target$13, arr$35[mid]);
    if(compareResult > 0)left$1 = mid + 1;
    else if(compareResult < 0)right$1 = mid - 1;
    else return mid
  }return-(left$1 + 1)
};
goog.array.sort = function(arr$36, opt_compareFn$1) {
  Array.prototype.sort.call(arr$36, opt_compareFn$1 || goog.array.defaultCompare)
};
goog.array.stableSort = function(arr$37, opt_compareFn$2) {
  for(var i$22 = 0;i$22 < arr$37.length;i$22++)arr$37[i$22] = {index:i$22, value:arr$37[i$22]};
  var valueCompareFn = opt_compareFn$2 || goog.array.defaultCompare;
  function stableCompareFn(obj1, obj2) {
    return valueCompareFn(obj1.value, obj2.value) || obj1.index - obj2.index
  }
  goog.array.sort(arr$37, stableCompareFn);
  for(i$22 = 0;i$22 < arr$37.length;i$22++)arr$37[i$22] = arr$37[i$22].value
};
goog.array.sortObjectsByKey = function(arr$38, key$6, opt_compareFn$3) {
  var compare = opt_compareFn$3 || goog.array.defaultCompare;
  goog.array.sort(arr$38, function(a, b) {
    return compare(a[key$6], b[key$6])
  })
};
goog.array.compare = function(arr1$1, arr2$9, opt_compareFn$4) {
  if(!goog.isArrayLike(arr1$1) || !goog.isArrayLike(arr2$9) || arr1$1.length != arr2$9.length)return false;
  for(var l$9 = arr1$1.length, compareFn$1 = opt_compareFn$4 || goog.array.defaultCompareEquality, i$23 = 0;i$23 < l$9;i$23++)if(!compareFn$1.call(null, arr1$1[i$23], arr2$9[i$23]))return false;
  return true
};
goog.array.defaultCompare = function(a$1, b$1) {
  return a$1 > b$1 ? 1 : a$1 < b$1 ? -1 : 0
};
goog.array.defaultCompareEquality = function(a$2, b$2) {
  return a$2 === b$2
};
goog.array.binaryInsert = function(array$1, value$9, opt_compareFn$5) {
  var index$35 = goog.array.binarySearch(array$1, value$9, opt_compareFn$5);
  if(index$35 < 0) {
    goog.array.insertAt(array$1, value$9, -(index$35 + 1));
    return true
  }return false
};
goog.array.binaryRemove = function(array$2, value$10, opt_compareFn$6) {
  var index$36 = goog.array.binarySearch(array$2, value$10, opt_compareFn$6);
  return index$36 >= 0 ? goog.array.removeAt(array$2, index$36) : false
};
goog.array.bucket = function(array$3, sorter) {
  for(var buckets = {}, i$24 = 0;i$24 < array$3.length;i$24++) {
    var value$11 = array$3[i$24], key$7 = sorter(value$11, i$24, array$3);
    if(goog.isDef(key$7))(buckets[key$7] || (buckets[key$7] = [])).push(value$11)
  }return buckets
};
goog.array.repeat = function(value$12, n) {
  for(var array$4 = [], i$25 = 0;i$25 < n;i$25++)array$4[i$25] = value$12;
  return array$4
};
goog.array.flatten = function() {
  for(var result = [], i$26 = 0;i$26 < arguments.length;i$26++) {
    var element$3 = arguments[i$26];
    goog.isArray(element$3) ? result.push.apply(result, goog.array.flatten.apply(null, element$3)) : result.push(element$3)
  }return result
};goog.math = {};
goog.math.Coordinate = function(opt_x, opt_y) {
  this.x = goog.isDef(opt_x) ? opt_x : 0;
  this.y = goog.isDef(opt_y) ? opt_y : 0
};
goog.math.Coordinate.prototype.clone = function() {
  return new goog.math.Coordinate(this.x, this.y)
};
if(goog.DEBUG)goog.math.Coordinate.prototype.toString = function() {
  return"(" + this.x + ", " + this.y + ")"
};
goog.math.Coordinate.equals = function(a$3, b$3) {
  if(a$3 == b$3)return true;
  if(!a$3 || !b$3)return false;
  return a$3.x == b$3.x && a$3.y == b$3.y
};
goog.math.Coordinate.distance = function(a$4, b$4) {
  var dx$4 = a$4.x - b$4.x, dy$4 = a$4.y - b$4.y;
  return Math.sqrt(dx$4 * dx$4 + dy$4 * dy$4)
};
goog.math.Coordinate.squaredDistance = function(a$5, b$5) {
  var dx$5 = a$5.x - b$5.x, dy$5 = a$5.y - b$5.y;
  return dx$5 * dx$5 + dy$5 * dy$5
};
goog.math.Coordinate.difference = function(a$6, b$6) {
  return new goog.math.Coordinate(a$6.x - b$6.x, a$6.y - b$6.y)
};
goog.math.Coordinate.sum = function(a$7, b$7) {
  return new goog.math.Coordinate(a$7.x + b$7.x, a$7.y + b$7.y)
};goog.math.Size = function(width, height) {
  this.width = width;
  this.height = height
};
goog.math.Size.equals = function(a$8, b$8) {
  if(a$8 == b$8)return true;
  if(!a$8 || !b$8)return false;
  return a$8.width == b$8.width && a$8.height == b$8.height
};
goog.math.Size.prototype.clone = function() {
  return new goog.math.Size(this.width, this.height)
};
if(goog.DEBUG)goog.math.Size.prototype.toString = function() {
  return"(" + this.width + " x " + this.height + ")"
};
goog.math.Size.prototype.area = function() {
  return this.width * this.height
};
goog.math.Size.prototype.isEmpty = function() {
  return!this.area()
};
goog.math.Size.prototype.floor = function() {
  this.width = Math.floor(this.width);
  this.height = Math.floor(this.height);
  return this
};goog.object = {};
goog.object.forEach = function(obj$12, f$13, opt_obj$14) {
  for(var key$8 in obj$12)f$13.call(opt_obj$14, obj$12[key$8], key$8, obj$12)
};
goog.object.filter = function(obj$13, f$14, opt_obj$15) {
  var res$2 = {};
  for(var key$9 in obj$13)if(f$14.call(opt_obj$15, obj$13[key$9], key$9, obj$13))res$2[key$9] = obj$13[key$9];
  return res$2
};
goog.object.map = function(obj$14, f$15, opt_obj$16) {
  var res$3 = {};
  for(var key$10 in obj$14)res$3[key$10] = f$15.call(opt_obj$16, obj$14[key$10], key$10, obj$14);
  return res$3
};
goog.object.some = function(obj$15, f$16, opt_obj$17) {
  for(var key$11 in obj$15)if(f$16.call(opt_obj$17, obj$15[key$11], key$11, obj$15))return true;
  return false
};
goog.object.every = function(obj$16, f$17, opt_obj$18) {
  for(var key$12 in obj$16)if(!f$17.call(opt_obj$18, obj$16[key$12], key$12, obj$16))return false;
  return true
};
goog.object.getCount = function(obj$17) {
  var rv$3 = 0;
  for(var key$13 in obj$17)rv$3++;
  return rv$3
};
goog.object.getAnyKey = function(obj$18) {
  for(var key$14 in obj$18)return key$14
};
goog.object.getAnyValue = function(obj$19) {
  for(var key$15 in obj$19)return obj$19[key$15]
};
goog.object.contains = function(obj$20, val$16) {
  return goog.object.containsValue(obj$20, val$16)
};
goog.object.getValues = function(obj$21) {
  var res$4 = [], i$27 = 0;
  for(var key$16 in obj$21)res$4[i$27++] = obj$21[key$16];
  return res$4
};
goog.object.getKeys = function(obj$22) {
  var res$5 = [], i$28 = 0;
  for(var key$17 in obj$22)res$5[i$28++] = key$17;
  return res$5
};
goog.object.containsKey = function(obj$23, key$18) {
  return key$18 in obj$23
};
goog.object.containsValue = function(obj$24, val$17) {
  for(var key$19 in obj$24)if(obj$24[key$19] == val$17)return true;
  return false
};
goog.object.findKey = function(obj$25, f$18, opt_this) {
  for(var key$20 in obj$25)if(f$18.call(opt_this, obj$25[key$20], key$20, obj$25))return key$20;
  return undefined
};
goog.object.findValue = function(obj$26, f$19, opt_this$1) {
  var key$21 = goog.object.findKey(obj$26, f$19, opt_this$1);
  return key$21 && obj$26[key$21]
};
goog.object.isEmpty = function(obj$27) {
  for(var key$22 in obj$27)return false;
  return true
};
goog.object.clear = function(obj$28) {
  for(var keys = goog.object.getKeys(obj$28), i$29 = keys.length - 1;i$29 >= 0;i$29--)goog.object.remove(obj$28, keys[i$29])
};
goog.object.remove = function(obj$29, key$23) {
  var rv$4;
  if(rv$4 = key$23 in obj$29)delete obj$29[key$23];
  return rv$4
};
goog.object.add = function(obj$30, key$24, val$18) {
  if(key$24 in obj$30)throw Error('The object already contains the key "' + key$24 + '"');goog.object.set(obj$30, key$24, val$18)
};
goog.object.get = function(obj$31, key$25, opt_val) {
  if(key$25 in obj$31)return obj$31[key$25];
  return opt_val
};
goog.object.set = function(obj$32, key$26, value$13) {
  obj$32[key$26] = value$13
};
goog.object.setIfUndefined = function(obj$33, key$27, value$14) {
  return key$27 in obj$33 ? obj$33[key$27] : (obj$33[key$27] = value$14)
};
goog.object.clone = function(obj$34) {
  var res$6 = {};
  for(var key$28 in obj$34)res$6[key$28] = obj$34[key$28];
  return res$6
};
goog.object.transpose = function(obj$35) {
  var transposed = {};
  for(var key$29 in obj$35)transposed[obj$35[key$29]] = key$29;
  return transposed
};
goog.object.PROTOTYPE_FIELDS_ = ["constructor", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "toLocaleString", "toString", "valueOf"];
goog.object.extend = function(target$16) {
  for(var key$30, source$2, i$30 = 1;i$30 < arguments.length;i$30++) {
    source$2 = arguments[i$30];
    for(key$30 in source$2)target$16[key$30] = source$2[key$30];
    for(var j$1 = 0;j$1 < goog.object.PROTOTYPE_FIELDS_.length;j$1++) {
      key$30 = goog.object.PROTOTYPE_FIELDS_[j$1];
      if(Object.prototype.hasOwnProperty.call(source$2, key$30))target$16[key$30] = source$2[key$30]
    }
  }
};
goog.object.create = function() {
  var argLength = arguments.length;
  if(argLength == 1 && goog.isArray(arguments[0]))return goog.object.create.apply(null, arguments[0]);
  if(argLength % 2)throw Error("Uneven number of arguments");for(var rv$5 = {}, i$31 = 0;i$31 < argLength;i$31 += 2)rv$5[arguments[i$31]] = arguments[i$31 + 1];
  return rv$5
};
goog.object.createSet = function() {
  var argLength$1 = arguments.length;
  if(argLength$1 == 1 && goog.isArray(arguments[0]))return goog.object.createSet.apply(null, arguments[0]);
  for(var rv$6 = {}, i$32 = 0;i$32 < argLength$1;i$32++)rv$6[arguments[i$32]] = true;
  return rv$6
};goog.string = {};
goog.string.Unicode = {NBSP:"\u00a0"};
goog.string.startsWith = function(str$7, prefix$2) {
  return str$7.indexOf(prefix$2) == 0
};
goog.string.endsWith = function(str$8, suffix) {
  var l$10 = str$8.length - suffix.length;
  return l$10 >= 0 && str$8.lastIndexOf(suffix, l$10) == l$10
};
goog.string.caseInsensitiveStartsWith = function(str$9, prefix$3) {
  return goog.string.caseInsensitiveCompare(prefix$3, str$9.substr(0, prefix$3.length)) == 0
};
goog.string.caseInsensitiveEndsWith = function(str$10, suffix$1) {
  return goog.string.caseInsensitiveCompare(suffix$1, str$10.substr(str$10.length - suffix$1.length, suffix$1.length)) == 0
};
goog.string.subs = function(str$11) {
  for(var i$33 = 1;i$33 < arguments.length;i$33++) {
    var replacement = String(arguments[i$33]).replace(/\$/g, "$$$$");
    str$11 = str$11.replace(/\%s/, replacement)
  }return str$11
};
goog.string.collapseWhitespace = function(str$12) {
  return str$12.replace(/[\s\xa0]+/g, " ").replace(/^\s+|\s+$/g, "")
};
goog.string.isEmpty = function(str$13) {
  return/^[\s\xa0]*$/.test(str$13)
};
goog.string.isEmptySafe = function(str$14) {
  return goog.string.isEmpty(goog.string.makeSafe(str$14))
};
goog.string.isBreakingWhitespace = function(str$15) {
  return!/[^\t\n\r ]/.test(str$15)
};
goog.string.isAlpha = function(str$16) {
  return!/[^a-zA-Z]/.test(str$16)
};
goog.string.isNumeric = function(str$17) {
  return!/[^0-9]/.test(str$17)
};
goog.string.isAlphaNumeric = function(str$18) {
  return!/[^a-zA-Z0-9]/.test(str$18)
};
goog.string.isSpace = function(ch) {
  return ch == " "
};
goog.string.isUnicodeChar = function(ch$1) {
  return ch$1.length == 1 && ch$1 >= " " && ch$1 <= "~" || ch$1 >= "\u0080" && ch$1 <= "\ufffd"
};
goog.string.stripNewlines = function(str$19) {
  return str$19.replace(/(\r\n|\r|\n)+/g, " ")
};
goog.string.canonicalizeNewlines = function(str$20) {
  return str$20.replace(/(\r\n|\r|\n)/g, "\n")
};
goog.string.normalizeWhitespace = function(str$21) {
  return str$21.replace(/\xa0|\s/g, " ")
};
goog.string.normalizeSpaces = function(str$22) {
  return str$22.replace(/\xa0|[ \t]+/g, " ")
};
goog.string.trim = function(str$23) {
  return str$23.replace(/^[\s\xa0]+|[\s\xa0]+$/g, "")
};
goog.string.trimLeft = function(str$24) {
  return str$24.replace(/^[\s\xa0]+/, "")
};
goog.string.trimRight = function(str$25) {
  return str$25.replace(/[\s\xa0]+$/, "")
};
goog.string.caseInsensitiveCompare = function(str1, str2) {
  var test1 = String(str1).toLowerCase(), test2 = String(str2).toLowerCase();
  return test1 < test2 ? -1 : test1 == test2 ? 0 : 1
};
goog.string.numerateCompareRegExp_ = /(\.\d+)|(\d+)|(\D+)/g;
goog.string.numerateCompare = function(str1$1, str2$1) {
  if(str1$1 == str2$1)return 0;
  if(!str1$1)return-1;
  if(!str2$1)return 1;
  for(var tokens1 = str1$1.toLowerCase().match(goog.string.numerateCompareRegExp_), tokens2 = str2$1.toLowerCase().match(goog.string.numerateCompareRegExp_), count$3 = Math.min(tokens1.length, tokens2.length), i$34 = 0;i$34 < count$3;i$34++) {
    var a$9 = tokens1[i$34], b$9 = tokens2[i$34];
    if(a$9 != b$9) {
      var num1 = parseInt(a$9, 10);
      if(!isNaN(num1)) {
        var num2 = parseInt(b$9, 10);
        if(!isNaN(num2) && num1 - num2)return num1 - num2
      }return a$9 < b$9 ? -1 : 1
    }
  }if(tokens1.length != tokens2.length)return tokens1.length - tokens2.length;
  return str1$1 < str2$1 ? -1 : 1
};
goog.string.encodeUriRegExp_ = /^[a-zA-Z0-9\-_.!~*'()]*$/;
goog.string.urlEncode = function(str$26) {
  str$26 = String(str$26);
  if(!goog.string.encodeUriRegExp_.test(str$26))return encodeURIComponent(str$26);
  return str$26
};
goog.string.urlDecode = function(str$27) {
  return decodeURIComponent(str$27.replace(/\+/g, " "))
};
goog.string.newLineToBr = function(str$28, opt_xml) {
  return str$28.replace(/(\r\n|\r|\n)/g, opt_xml ? "<br />" : "<br>")
};
goog.string.htmlEscape = function(str$29, opt_isLikelyToContainHtmlChars) {
  if(opt_isLikelyToContainHtmlChars)return str$29.replace(goog.string.amperRe_, "&amp;").replace(goog.string.ltRe_, "&lt;").replace(goog.string.gtRe_, "&gt;").replace(goog.string.quotRe_, "&quot;");
  else {
    if(!goog.string.allRe_.test(str$29))return str$29;
    if(str$29.indexOf("&") != -1)str$29 = str$29.replace(goog.string.amperRe_, "&amp;");
    if(str$29.indexOf("<") != -1)str$29 = str$29.replace(goog.string.ltRe_, "&lt;");
    if(str$29.indexOf(">") != -1)str$29 = str$29.replace(goog.string.gtRe_, "&gt;");
    if(str$29.indexOf('"') != -1)str$29 = str$29.replace(goog.string.quotRe_, "&quot;");
    return str$29
  }
};
goog.string.amperRe_ = /&/g;
goog.string.ltRe_ = /</g;
goog.string.gtRe_ = />/g;
goog.string.quotRe_ = /\"/g;
goog.string.allRe_ = /[&<>\"]/;
goog.string.unescapeEntities = function(str$30) {
  if(goog.string.contains(str$30, "&"))return"document" in goog.global && !goog.string.contains(str$30, "<") ? goog.string.unescapeEntitiesUsingDom_(str$30) : goog.string.unescapePureXmlEntities_(str$30);
  return str$30
};
goog.string.unescapeEntitiesUsingDom_ = function(str$31) {
  var el$1 = goog.global.document.createElement("a");
  el$1.innerHTML = str$31;
  el$1[goog.string.NORMALIZE_FN_] && el$1[goog.string.NORMALIZE_FN_]();
  str$31 = el$1.firstChild.nodeValue;
  el$1.innerHTML = "";
  return str$31
};
goog.string.unescapePureXmlEntities_ = function(str$32) {
  return str$32.replace(/&([^;]+);/g, function(s$4, entity) {
    switch(entity) {
      case "amp":
        return"&";
      case "lt":
        return"<";
      case "gt":
        return">";
      case "quot":
        return'"';
      default:
        if(entity.charAt(0) == "#") {
          var n$1 = Number("0" + entity.substr(1));
          if(!isNaN(n$1))return String.fromCharCode(n$1)
        }return s$4
    }
  })
};
goog.string.NORMALIZE_FN_ = "normalize";
goog.string.whitespaceEscape = function(str$33, opt_xml$1) {
  return goog.string.newLineToBr(str$33.replace(/  /g, " &#160;"), opt_xml$1)
};
goog.string.stripQuotes = function(str$34, quoteChars) {
  for(var length$1 = quoteChars.length, i$35 = 0;i$35 < length$1;i$35++) {
    var quoteChar = length$1 == 1 ? quoteChars : quoteChars.charAt(i$35);
    if(str$34.charAt(0) == quoteChar && str$34.charAt(str$34.length - 1) == quoteChar)return str$34.substring(1, str$34.length - 1)
  }return str$34
};
goog.string.truncate = function(str$35, chars, opt_protectEscapedCharacters) {
  if(opt_protectEscapedCharacters)str$35 = goog.string.unescapeEntities(str$35);
  if(str$35.length > chars)str$35 = str$35.substring(0, chars - 3) + "...";
  if(opt_protectEscapedCharacters)str$35 = goog.string.htmlEscape(str$35);
  return str$35
};
goog.string.truncateMiddle = function(str$36, chars$1, opt_protectEscapedCharacters$1) {
  if(opt_protectEscapedCharacters$1)str$36 = goog.string.unescapeEntities(str$36);
  if(str$36.length > chars$1) {
    var half = Math.floor(chars$1 / 2), endPos = str$36.length - half;
    half += chars$1 % 2;
    str$36 = str$36.substring(0, half) + "..." + str$36.substring(endPos)
  }if(opt_protectEscapedCharacters$1)str$36 = goog.string.htmlEscape(str$36);
  return str$36
};
goog.string.jsEscapeCache_ = {"\u0008":"\\b", "\u000c":"\\f", "\n":"\\n", "\r":"\\r", "\t":"\\t", "\u000b":"\\x0B", '"':'\\"', "'":"\\'", "\\":"\\\\"};
goog.string.quote = function(s$5) {
  s$5 = String(s$5);
  if(s$5.quote)return s$5.quote();
  else {
    for(var sb = ['"'], i$36 = 0;i$36 < s$5.length;i$36++)sb[i$36 + 1] = goog.string.escapeChar(s$5.charAt(i$36));
    sb.push('"');
    return sb.join("")
  }
};
goog.string.escapeChar = function(c) {
  if(c in goog.string.jsEscapeCache_)return goog.string.jsEscapeCache_[c];
  var rv$7 = c, cc = c.charCodeAt(0);
  if(cc > 31 && cc < 127)rv$7 = c;
  else {
    if(cc < 256) {
      rv$7 = "\\x";
      if(cc < 16 || cc > 256)rv$7 += "0"
    }else {
      rv$7 = "\\u";
      if(cc < 4096)rv$7 += "0"
    }rv$7 += cc.toString(16).toUpperCase()
  }return goog.string.jsEscapeCache_[c] = rv$7
};
goog.string.toMap = function(s$6) {
  for(var rv$8 = {}, i$37 = 0;i$37 < s$6.length;i$37++)rv$8[s$6.charAt(i$37)] = true;
  return rv$8
};
goog.string.contains = function(s$7, ss) {
  return s$7.indexOf(ss) != -1
};
goog.string.removeAt = function(s$8, index$37, stringLength) {
  var resultStr = s$8;
  if(index$37 >= 0 && index$37 < s$8.length && stringLength > 0)resultStr = s$8.substr(0, index$37) + s$8.substr(index$37 + stringLength, s$8.length - index$37 - stringLength);
  return resultStr
};
goog.string.remove = function(s$9, ss$1) {
  var re = new RegExp(goog.string.regExpEscape(ss$1), "");
  return s$9.replace(re, "")
};
goog.string.removeAll = function(s$10, ss$2) {
  var re$1 = new RegExp(goog.string.regExpEscape(ss$2), "g");
  return s$10.replace(re$1, "")
};
goog.string.regExpEscape = function(s$11) {
  return String(s$11).replace(/([-()\[\]{}+?*.$\^|,:#<!\\])/g, "\\$1").replace(/\x08/g, "\\x08")
};
goog.string.repeat = function(string, length$2) {
  return(new Array(length$2 + 1)).join(string)
};
goog.string.padNumber = function(num$4, length$3, opt_precision$1) {
  var s$12 = goog.isDef(opt_precision$1) ? num$4.toFixed(opt_precision$1) : String(num$4), index$38 = s$12.indexOf(".");
  if(index$38 == -1)index$38 = s$12.length;
  return goog.string.repeat("0", Math.max(0, length$3 - index$38)) + s$12
};
goog.string.makeSafe = function(obj$36) {
  return obj$36 == null ? "" : String(obj$36)
};
goog.string.buildString = function() {
  return Array.prototype.join.call(arguments, "")
};
goog.string.getRandomString = function() {
  return Math.floor(Math.random() * 2147483648).toString(36) + (Math.floor(Math.random() * 2147483648) ^ (new Date).getTime()).toString(36)
};
goog.string.compareVersions = function(version1, version2) {
  for(var order = 0, v1Subs = goog.string.trim(String(version1)).split("."), v2Subs = goog.string.trim(String(version2)).split("."), subCount = Math.max(v1Subs.length, v2Subs.length), subIdx = 0;order == 0 && subIdx < subCount;subIdx++) {
    var v1Sub = v1Subs[subIdx] || "", v2Sub = v2Subs[subIdx] || "", v1CompParser = new RegExp("(\\d*)(\\D*)", "g"), v2CompParser = new RegExp("(\\d*)(\\D*)", "g");
    do {
      var v1Comp = v1CompParser.exec(v1Sub) || ["", "", ""], v2Comp = v2CompParser.exec(v2Sub) || ["", "", ""];
      if(v1Comp[0].length == 0 && v2Comp[0].length == 0)break;
      var v1CompNum = v1Comp[1].length == 0 ? 0 : parseInt(v1Comp[1], 10), v2CompNum = v2Comp[1].length == 0 ? 0 : parseInt(v2Comp[1], 10);
      order = goog.string.compareElements_(v1CompNum, v2CompNum) || goog.string.compareElements_(v1Comp[2].length == 0, v2Comp[2].length == 0) || goog.string.compareElements_(v1Comp[2], v2Comp[2])
    }while(order == 0)
  }return order
};
goog.string.compareElements_ = function(left$2, right$2) {
  if(left$2 < right$2)return-1;
  else if(left$2 > right$2)return 1;
  return 0
};
goog.string.HASHCODE_MAX_ = 4294967296;
goog.string.hashCode = function(str$37) {
  for(var result$1 = 0, i$38 = 0;i$38 < str$37.length;++i$38) {
    result$1 = 31 * result$1 + str$37.charCodeAt(i$38);
    result$1 %= goog.string.HASHCODE_MAX_
  }return result$1
};
goog.string.uniqueStringCounter_ = goog.now();
goog.string.createUniqueString = function() {
  return"goog_" + goog.string.uniqueStringCounter_++
};
goog.string.toNumber = function(str$38) {
  var num$5 = Number(str$38);
  if(num$5 == 0 && goog.string.isEmpty(str$38))return NaN;
  return num$5
};goog.userAgent = {};
goog.userAgent.ASSUME_IE = false;
goog.userAgent.ASSUME_GECKO = false;
goog.userAgent.ASSUME_CAMINO = false;
goog.userAgent.ASSUME_WEBKIT = false;
goog.userAgent.ASSUME_MOBILE_WEBKIT = false;
goog.userAgent.ASSUME_OPERA = false;
goog.userAgent.BROWSER_KNOWN_ = goog.userAgent.ASSUME_IE || goog.userAgent.ASSUME_GECKO || goog.userAgent.ASSUME_CAMINO || goog.userAgent.ASSUME_MOBILE_WEBKIT || goog.userAgent.ASSUME_WEBKIT || goog.userAgent.ASSUME_OPERA;
goog.userAgent.getUserAgentString = function() {
  return goog.global.navigator ? goog.global.navigator.userAgent : null
};
goog.userAgent.getNavigator = function() {
  return goog.global.navigator
};
goog.userAgent.init_ = function() {
  goog.userAgent.detectedOpera_ = false;
  goog.userAgent.detectedIe_ = false;
  goog.userAgent.detectedWebkit_ = false;
  goog.userAgent.detectedMobile_ = false;
  goog.userAgent.detectedGecko_ = false;
  goog.userAgent.detectedCamino_ = false;
  var ua;
  if(!goog.userAgent.BROWSER_KNOWN_ && (ua = goog.userAgent.getUserAgentString())) {
    var navigator$1 = goog.userAgent.getNavigator();
    goog.userAgent.detectedOpera_ = ua.indexOf("Opera") == 0;
    goog.userAgent.detectedIe_ = !goog.userAgent.detectedOpera_ && ua.indexOf("MSIE") != -1;
    goog.userAgent.detectedWebkit_ = !goog.userAgent.detectedOpera_ && ua.indexOf("WebKit") != -1;
    goog.userAgent.detectedMobile_ = goog.userAgent.detectedWebkit_ && ua.indexOf("Mobile") != -1;
    goog.userAgent.detectedGecko_ = !goog.userAgent.detectedOpera_ && !goog.userAgent.detectedWebkit_ && navigator$1.product == "Gecko";
    goog.userAgent.detectedCamino_ = goog.userAgent.detectedGecko_ && navigator$1.vendor == "Camino"
  }
};
goog.userAgent.BROWSER_KNOWN_ || goog.userAgent.init_();
goog.userAgent.OPERA = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_OPERA : goog.userAgent.detectedOpera_;
goog.userAgent.IE = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_IE : goog.userAgent.detectedIe_;
goog.userAgent.GECKO = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_GECKO || goog.userAgent.ASSUME_CAMINO : goog.userAgent.detectedGecko_;
goog.userAgent.CAMINO = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_CAMINO : goog.userAgent.detectedCamino_;
goog.userAgent.WEBKIT = goog.userAgent.BROWSER_KNOWN_ ? goog.userAgent.ASSUME_WEBKIT || goog.userAgent.ASSUME_MOBILE_WEBKIT : goog.userAgent.detectedWebkit_;
goog.userAgent.MOBILE = goog.userAgent.ASSUME_MOBILE_WEBKIT || goog.userAgent.detectedMobile_;
goog.userAgent.SAFARI = goog.userAgent.WEBKIT;
goog.userAgent.determinePlatform_ = function() {
  var navigator$2 = goog.userAgent.getNavigator();
  return navigator$2 && navigator$2.platform || ""
};
goog.userAgent.PLATFORM = goog.userAgent.determinePlatform_();
goog.userAgent.ASSUME_MAC = false;
goog.userAgent.ASSUME_WINDOWS = false;
goog.userAgent.ASSUME_LINUX = false;
goog.userAgent.ASSUME_X11 = false;
goog.userAgent.PLATFORM_KNOWN_ = goog.userAgent.ASSUME_MAC || goog.userAgent.ASSUME_WINDOWS || goog.userAgent.ASSUME_LINUX || goog.userAgent.ASSUME_X11;
goog.userAgent.initPlatform_ = function() {
  goog.userAgent.detectedMac_ = goog.string.contains(goog.userAgent.PLATFORM, "Mac");
  goog.userAgent.detectedWindows_ = goog.string.contains(goog.userAgent.PLATFORM, "Win");
  goog.userAgent.detectedLinux_ = goog.string.contains(goog.userAgent.PLATFORM, "Linux");
  goog.userAgent.detectedX11_ = !!goog.userAgent.getNavigator() && goog.string.contains(goog.userAgent.getNavigator().appVersion || "", "X11")
};
goog.userAgent.PLATFORM_KNOWN_ || goog.userAgent.initPlatform_();
goog.userAgent.MAC = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_MAC : goog.userAgent.detectedMac_;
goog.userAgent.WINDOWS = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_WINDOWS : goog.userAgent.detectedWindows_;
goog.userAgent.LINUX = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_LINUX : goog.userAgent.detectedLinux_;
goog.userAgent.X11 = goog.userAgent.PLATFORM_KNOWN_ ? goog.userAgent.ASSUME_X11 : goog.userAgent.detectedX11_;
goog.userAgent.determineVersion_ = function() {
  var version$6 = "", re$2;
  if(goog.userAgent.OPERA && goog.global.opera) {
    var operaVersion = goog.global.opera.version;
    version$6 = typeof operaVersion == "function" ? operaVersion() : operaVersion
  }else {
    if(goog.userAgent.GECKO)re$2 = /rv\:([^\);]+)(\)|;)/;
    else if(goog.userAgent.IE)re$2 = /MSIE\s+([^\);]+)(\)|;)/;
    else if(goog.userAgent.WEBKIT)re$2 = /WebKit\/(\S+)/;
    if(re$2) {
      var arr$39 = re$2.exec(goog.userAgent.getUserAgentString());
      version$6 = arr$39 ? arr$39[1] : ""
    }
  }return version$6
};
goog.userAgent.VERSION = goog.userAgent.determineVersion_();
goog.userAgent.compare = function(v1, v2) {
  return goog.string.compareVersions(v1, v2)
};
goog.userAgent.isVersionCache_ = {};
goog.userAgent.isVersion = function(version$7) {
  return goog.userAgent.isVersionCache_[version$7] || (goog.userAgent.isVersionCache_[version$7] = goog.string.compareVersions(goog.userAgent.VERSION, version$7) >= 0)
};goog.dom = {};
goog.dom.classes = {};
goog.dom.classes.set = function(element$4, className$2) {
  element$4.className = className$2
};
goog.dom.classes.get = function(element$5) {
  var className$3 = element$5.className;
  return className$3 && typeof className$3.split == "function" ? className$3.split(" ") : []
};
goog.dom.classes.add = function(element$6) {
  var classes = goog.dom.classes.get(element$6), args$5 = goog.array.slice(arguments, 1), b$10 = goog.dom.classes.add_(classes, args$5);
  element$6.className = classes.join(" ");
  return b$10
};
goog.dom.classes.remove = function(element$7) {
  var classes$1 = goog.dom.classes.get(element$7), args$6 = goog.array.slice(arguments, 1), b$11 = goog.dom.classes.remove_(classes$1, args$6);
  element$7.className = classes$1.join(" ");
  return b$11
};
goog.dom.classes.add_ = function(classes$2, args$7) {
  for(var rv$9 = 0, i$39 = 0;i$39 < args$7.length;i$39++)if(!goog.array.contains(classes$2, args$7[i$39])) {
    classes$2.push(args$7[i$39]);
    rv$9++
  }return rv$9 == args$7.length
};
goog.dom.classes.remove_ = function(classes$3, args$8) {
  for(var rv$10 = 0, i$40 = 0;i$40 < classes$3.length;i$40++)if(goog.array.contains(args$8, classes$3[i$40])) {
    goog.array.splice(classes$3, i$40--, 1);
    rv$10++
  }return rv$10 == args$8.length
};
goog.dom.classes.swap = function(element$8, fromClass, toClass) {
  for(var classes$4 = goog.dom.classes.get(element$8), removed = false, i$41 = 0;i$41 < classes$4.length;i$41++)if(classes$4[i$41] == fromClass) {
    goog.array.splice(classes$4, i$41--, 1);
    removed = true
  }if(removed) {
    classes$4.push(toClass);
    element$8.className = classes$4.join(" ")
  }return removed
};
goog.dom.classes.addRemove = function(element$9, classesToRemove, classesToAdd) {
  var classes$5 = goog.dom.classes.get(element$9);
  if(goog.isString(classesToRemove))goog.array.remove(classes$5, classesToRemove);
  else goog.isArray(classesToRemove) && goog.dom.classes.remove_(classes$5, classesToRemove);
  if(goog.isString(classesToAdd) && !goog.array.contains(classes$5, classesToAdd))classes$5.push(classesToAdd);
  else goog.isArray(classesToAdd) && goog.dom.classes.add_(classes$5, classesToAdd);
  element$9.className = classes$5.join(" ")
};
goog.dom.classes.has = function(element$10, className$4) {
  return goog.array.contains(goog.dom.classes.get(element$10), className$4)
};
goog.dom.classes.enable = function(element$11, className$5, enabled) {
  enabled ? goog.dom.classes.add(element$11, className$5) : goog.dom.classes.remove(element$11, className$5)
};
goog.dom.classes.toggle = function(element$12, className$6) {
  var add = !goog.dom.classes.has(element$12, className$6);
  goog.dom.classes.enable(element$12, className$6, add);
  return add
};goog.dom.TagName = {A:"A", ABBR:"ABBR", ACRONYM:"ACRONYM", ADDRESS:"ADDRESS", APPLET:"APPLET", AREA:"AREA", B:"B", BASE:"BASE", BASEFONT:"BASEFONT", BDO:"BDO", BIG:"BIG", BLOCKQUOTE:"BLOCKQUOTE", BODY:"BODY", BR:"BR", BUTTON:"BUTTON", CAPTION:"CAPTION", CENTER:"CENTER", CITE:"CITE", CODE:"CODE", COL:"COL", COLGROUP:"COLGROUP", DD:"DD", DEL:"DEL", DFN:"DFN", DIR:"DIR", DIV:"DIV", DL:"DL", DT:"DT", EM:"EM", FIELDSET:"FIELDSET", FONT:"FONT", FORM:"FORM", FRAME:"FRAME", FRAMESET:"FRAMESET", H1:"H1", 
H2:"H2", H3:"H3", H4:"H4", H5:"H5", H6:"H6", HEAD:"HEAD", HR:"HR", HTML:"HTML", I:"I", IFRAME:"IFRAME", IMG:"IMG", INPUT:"INPUT", INS:"INS", ISINDEX:"ISINDEX", KBD:"KBD", LABEL:"LABEL", LEGEND:"LEGEND", LI:"LI", LINK:"LINK", MAP:"MAP", MENU:"MENU", META:"META", NOFRAMES:"NOFRAMES", NOSCRIPT:"NOSCRIPT", OBJECT:"OBJECT", OL:"OL", OPTGROUP:"OPTGROUP", OPTION:"OPTION", P:"P", PARAM:"PARAM", PRE:"PRE", Q:"Q", S:"S", SAMP:"SAMP", SCRIPT:"SCRIPT", SELECT:"SELECT", SMALL:"SMALL", SPAN:"SPAN", STRIKE:"STRIKE", 
STRONG:"STRONG", STYLE:"STYLE", SUB:"SUB", SUP:"SUP", TABLE:"TABLE", TBODY:"TBODY", TD:"TD", TEXTAREA:"TEXTAREA", TFOOT:"TFOOT", TH:"TH", THEAD:"THEAD", TITLE:"TITLE", TR:"TR", TT:"TT", U:"U", UL:"UL", VAR:"VAR"};goog.dom.ASSUME_QUIRKS_MODE = false;
goog.dom.ASSUME_STANDARDS_MODE = false;
goog.dom.COMPAT_MODE_KNOWN_ = goog.dom.ASSUME_QUIRKS_MODE || goog.dom.ASSUME_STANDARDS_MODE;
goog.dom.NodeType = {ELEMENT:1, ATTRIBUTE:2, TEXT:3, CDATA_SECTION:4, ENTITY_REFERENCE:5, ENTITY:6, PROCESSING_INSTRUCTION:7, COMMENT:8, DOCUMENT:9, DOCUMENT_TYPE:10, DOCUMENT_FRAGMENT:11, NOTATION:12};
goog.dom.getDomHelper = function(opt_element) {
  return opt_element ? new goog.dom.DomHelper(goog.dom.getOwnerDocument(opt_element)) : goog.dom.defaultDomHelper_ || (goog.dom.defaultDomHelper_ = new goog.dom.DomHelper)
};
goog.dom.getDocument = function() {
  return document
};
goog.dom.getElement = function(element$13) {
  return goog.isString(element$13) ? document.getElementById(element$13) : element$13
};
goog.dom.$ = goog.dom.getElement;
goog.dom.getElementsByTagNameAndClass = function(opt_tag, opt_class, opt_el) {
  return goog.dom.getElementsByTagNameAndClass_(document, opt_tag, opt_class, opt_el)
};
goog.dom.getElementsByTagNameAndClass_ = function(doc$4, opt_tag$1, opt_class$1, opt_el$1) {
  var parent = opt_el$1 || doc$4, tagName$1 = opt_tag$1 && opt_tag$1 != "*" ? opt_tag$1.toLowerCase() : "";
  if(parent.querySelectorAll && (tagName$1 || opt_class$1) && (!goog.userAgent.WEBKIT || goog.dom.isCss1CompatMode_(doc$4) || goog.userAgent.isVersion("528")))return parent.querySelectorAll(tagName$1 + (opt_class$1 ? "." + opt_class$1 : ""));
  if(opt_class$1 && parent.getElementsByClassName) {
    var els = parent.getElementsByClassName(opt_class$1);
    if(tagName$1) {
      for(var arrayLike = {}, len$1 = 0, i$42 = 0, el$2;el$2 = els[i$42];i$42++)if(tagName$1 == el$2.nodeName.toLowerCase())arrayLike[len$1++] = el$2;
      arrayLike.length = len$1;
      return arrayLike
    }else return els
  }els = parent.getElementsByTagName(tagName$1 || "*");
  if(opt_class$1) {
    arrayLike = {};
    for(i$42 = len$1 = 0;el$2 = els[i$42];i$42++) {
      var className$7 = el$2.className;
      if(typeof className$7.split == "function" && goog.array.contains(className$7.split(" "), opt_class$1))arrayLike[len$1++] = el$2
    }arrayLike.length = len$1;
    return arrayLike
  }else return els
};
goog.dom.$$ = goog.dom.getElementsByTagNameAndClass;
goog.dom.setProperties = function(element$14, properties) {
  goog.object.forEach(properties, function(val$19, key$31) {
    if(key$31 == "style")element$14.style.cssText = val$19;
    else if(key$31 == "class")element$14.className = val$19;
    else if(key$31 == "for")element$14.htmlFor = val$19;
    else if(key$31 in goog.dom.DIRECT_ATTRIBUTE_MAP_)element$14.setAttribute(goog.dom.DIRECT_ATTRIBUTE_MAP_[key$31], val$19);
    else element$14[key$31] = val$19
  })
};
goog.dom.DIRECT_ATTRIBUTE_MAP_ = {cellpadding:"cellPadding", cellspacing:"cellSpacing", colspan:"colSpan", rowspan:"rowSpan", valign:"vAlign", height:"height", width:"width", usemap:"useMap", frameborder:"frameBorder", type:"type"};
goog.dom.getViewportSize = function(opt_window) {
  return goog.dom.getViewportSize_(opt_window || window)
};
goog.dom.getViewportSize_ = function(win) {
  var doc$5 = win.document;
  if(goog.userAgent.WEBKIT && !goog.userAgent.isVersion("500") && !goog.userAgent.MOBILE) {
    if(typeof win.innerHeight == "undefined")win = window;
    var innerHeight = win.innerHeight, scrollHeight = win.document.documentElement.scrollHeight;
    if(win == win.top)if(scrollHeight < innerHeight)innerHeight -= 15;
    return new goog.math.Size(win.innerWidth, innerHeight)
  }var el$3 = goog.dom.isCss1CompatMode_(doc$5) && (!goog.userAgent.OPERA || goog.userAgent.OPERA && goog.userAgent.isVersion("9.50")) ? doc$5.documentElement : doc$5.body;
  return new goog.math.Size(el$3.clientWidth, el$3.clientHeight)
};
goog.dom.getDocumentHeight = function() {
  return goog.dom.getDocumentHeight_(window)
};
goog.dom.getDocumentHeight_ = function(win$1) {
  var doc$6 = win$1.document, height$1 = 0;
  if(doc$6) {
    var vh = goog.dom.getViewportSize_(win$1).height, body = doc$6.body, docEl = doc$6.documentElement;
    if(goog.dom.isCss1CompatMode_(doc$6) && docEl.scrollHeight)height$1 = docEl.scrollHeight != vh ? docEl.scrollHeight : docEl.offsetHeight;
    else {
      var sh$2 = docEl.scrollHeight, oh = docEl.offsetHeight;
      if(docEl.clientHeight != oh) {
        sh$2 = body.scrollHeight;
        oh = body.offsetHeight
      }height$1 = sh$2 > vh ? sh$2 > oh ? sh$2 : oh : sh$2 < oh ? sh$2 : oh
    }
  }return height$1
};
goog.dom.getPageScroll = function(opt_window$1) {
  return goog.dom.getDomHelper((opt_window$1 || goog.global || window).document).getDocumentScroll()
};
goog.dom.getDocumentScroll = function() {
  return goog.dom.getDocumentScroll_(document)
};
goog.dom.getDocumentScroll_ = function(doc$7) {
  var el$4 = goog.dom.getDocumentScrollElement_(doc$7);
  return new goog.math.Coordinate(el$4.scrollLeft, el$4.scrollTop)
};
goog.dom.getDocumentScrollElement = function() {
  return goog.dom.getDocumentScrollElement_(document)
};
goog.dom.getDocumentScrollElement_ = function(doc$8) {
  return!goog.userAgent.WEBKIT && goog.dom.isCss1CompatMode_(doc$8) ? doc$8.documentElement : doc$8.body
};
goog.dom.getWindow = function(opt_doc) {
  return opt_doc ? goog.dom.getWindow_(opt_doc) : window
};
goog.dom.getWindow_ = function(doc$9) {
  if(doc$9.parentWindow)return doc$9.parentWindow;
  if(goog.userAgent.WEBKIT && !goog.userAgent.isVersion("500") && !goog.userAgent.MOBILE) {
    var scriptElement = doc$9.createElement("script");
    scriptElement.innerHTML = "document.parentWindow=window";
    var parentElement = doc$9.documentElement;
    parentElement.appendChild(scriptElement);
    parentElement.removeChild(scriptElement);
    return doc$9.parentWindow
  }return doc$9.defaultView
};
goog.dom.createDom = function() {
  return goog.dom.createDom_(document, arguments)
};
goog.dom.createDom_ = function(doc$10, args$9) {
  var tagName$3 = args$9[0], attributes = args$9[1];
  if(goog.userAgent.IE && attributes && (attributes.name || attributes.type)) {
    var tagNameArr = ["<", tagName$3];
    attributes.name && tagNameArr.push(' name="', goog.string.htmlEscape(attributes.name), '"');
    if(attributes.type) {
      tagNameArr.push(' type="', goog.string.htmlEscape(attributes.type), '"');
      attributes = goog.cloneObject(attributes);
      delete attributes.type
    }tagNameArr.push(">");
    tagName$3 = tagNameArr.join("")
  }var element$15 = doc$10.createElement(tagName$3);
  if(attributes)if(goog.isString(attributes))element$15.className = attributes;
  else goog.dom.setProperties(element$15, attributes);
  if(args$9.length > 2) {
    function childHandler(child$1) {
      if(child$1)element$15.appendChild(goog.isString(child$1) ? doc$10.createTextNode(child$1) : child$1)
    }
    for(var i$43 = 2;i$43 < args$9.length;i$43++) {
      var arg$5 = args$9[i$43];
      goog.isArrayLike(arg$5) && !goog.dom.isNodeLike(arg$5) ? goog.array.forEach(goog.dom.isNodeList(arg$5) ? goog.array.clone(arg$5) : arg$5, childHandler) : childHandler(arg$5)
    }
  }return element$15
};
goog.dom.$dom = goog.dom.createDom;
goog.dom.createElement = function(name$33) {
  return document.createElement(name$33)
};
goog.dom.createTextNode = function(content) {
  return document.createTextNode(content)
};
goog.dom.htmlToDocumentFragment = function(htmlString) {
  return goog.dom.htmlToDocumentFragment_(document, htmlString)
};
goog.dom.htmlToDocumentFragment_ = function(doc$11, htmlString$1) {
  var tempDiv = doc$11.createElement("div");
  tempDiv.innerHTML = htmlString$1;
  if(tempDiv.childNodes.length == 1)return tempDiv.firstChild;
  else {
    for(var fragment = doc$11.createDocumentFragment();tempDiv.firstChild;)fragment.appendChild(tempDiv.firstChild);
    return fragment
  }
};
goog.dom.getCompatMode = function() {
  return goog.dom.isCss1CompatMode() ? "CSS1Compat" : "BackCompat"
};
goog.dom.isCss1CompatMode = function() {
  return goog.dom.isCss1CompatMode_(document)
};
goog.dom.isCss1CompatMode_ = function(doc$12) {
  if(goog.dom.COMPAT_MODE_KNOWN_)return goog.dom.ASSUME_STANDARDS_MODE;
  return doc$12.compatMode == "CSS1Compat"
};
goog.dom.canHaveChildren = function(node$1) {
  if(node$1.nodeType != goog.dom.NodeType.ELEMENT)return false;
  if("canHaveChildren" in node$1)return node$1.canHaveChildren;
  switch(node$1.tagName) {
    case goog.dom.TagName.APPLET:
    ;
    case goog.dom.TagName.AREA:
    ;
    case goog.dom.TagName.BR:
    ;
    case goog.dom.TagName.COL:
    ;
    case goog.dom.TagName.FRAME:
    ;
    case goog.dom.TagName.HR:
    ;
    case goog.dom.TagName.IMG:
    ;
    case goog.dom.TagName.INPUT:
    ;
    case goog.dom.TagName.IFRAME:
    ;
    case goog.dom.TagName.ISINDEX:
    ;
    case goog.dom.TagName.LINK:
    ;
    case goog.dom.TagName.NOFRAMES:
    ;
    case goog.dom.TagName.NOSCRIPT:
    ;
    case goog.dom.TagName.META:
    ;
    case goog.dom.TagName.OBJECT:
    ;
    case goog.dom.TagName.PARAM:
    ;
    case goog.dom.TagName.SCRIPT:
    ;
    case goog.dom.TagName.STYLE:
      return false
  }
  return true
};
goog.dom.appendChild = function(parent$1, child$2) {
  parent$1.appendChild(child$2)
};
goog.dom.removeChildren = function(node$2) {
  for(var child$3;child$3 = node$2.firstChild;)node$2.removeChild(child$3)
};
goog.dom.insertSiblingBefore = function(newNode$1, refNode$8) {
  refNode$8.parentNode && refNode$8.parentNode.insertBefore(newNode$1, refNode$8)
};
goog.dom.insertSiblingAfter = function(newNode$2, refNode$9) {
  refNode$9.parentNode && refNode$9.parentNode.insertBefore(newNode$2, refNode$9.nextSibling)
};
goog.dom.removeNode = function(node$3) {
  return node$3 && node$3.parentNode ? node$3.parentNode.removeChild(node$3) : null
};
goog.dom.replaceNode = function(newNode$3, oldNode) {
  var parent$2 = oldNode.parentNode;
  parent$2 && parent$2.replaceChild(newNode$3, oldNode)
};
goog.dom.flattenElement = function(element$16) {
  var child$4, parent$3 = element$16.parentNode;
  if(parent$3 && parent$3.nodeType != goog.dom.NodeType.DOCUMENT_FRAGMENT)if(element$16.removeNode)return element$16.removeNode(false);
  else {
    for(;child$4 = element$16.firstChild;)parent$3.insertBefore(child$4, element$16);
    return goog.dom.removeNode(element$16)
  }
};
goog.dom.getFirstElementChild = function(node$4) {
  return goog.dom.getNextElementNode_(node$4.firstChild, true)
};
goog.dom.getLastElementChild = function(node$5) {
  return goog.dom.getNextElementNode_(node$5.lastChild, false)
};
goog.dom.getNextElementSibling = function(node$6) {
  return goog.dom.getNextElementNode_(node$6.nextSibling, true)
};
goog.dom.getPreviousElementSibling = function(node$7) {
  return goog.dom.getNextElementNode_(node$7.previousSibling, false)
};
goog.dom.getNextElementNode_ = function(node$8, forward) {
  for(;node$8 && node$8.nodeType != goog.dom.NodeType.ELEMENT;)node$8 = forward ? node$8.nextSibling : node$8.previousSibling;
  return node$8
};
goog.dom.isNodeLike = function(obj$37) {
  return goog.isObject(obj$37) && obj$37.nodeType > 0
};
goog.dom.BAD_CONTAINS_WEBKIT_ = goog.userAgent.WEBKIT && goog.userAgent.compare(goog.userAgent.VERSION, "521") <= 0;
goog.dom.contains = function(parent$4, descendant) {
  if(typeof parent$4.contains != "undefined" && !goog.dom.BAD_CONTAINS_WEBKIT_ && descendant.nodeType == goog.dom.NodeType.ELEMENT)return parent$4 == descendant || parent$4.contains(descendant);
  if(typeof parent$4.compareDocumentPosition != "undefined")return parent$4 == descendant || Boolean(parent$4.compareDocumentPosition(descendant) & 16);
  for(;descendant && parent$4 != descendant;)descendant = descendant.parentNode;
  return descendant == parent$4
};
goog.dom.compareNodeOrder = function(node1, node2) {
  if(node1 == node2)return 0;
  if(node1.compareDocumentPosition)return node1.compareDocumentPosition(node2) & 2 ? 1 : -1;
  if("sourceIndex" in node1 || node1.parentNode && "sourceIndex" in node1.parentNode) {
    var isElement1 = node1.nodeType == goog.dom.NodeType.ELEMENT, isElement2 = node2.nodeType == goog.dom.NodeType.ELEMENT;
    if(isElement1 && isElement2)return node1.sourceIndex - node2.sourceIndex;
    else {
      var parent1 = node1.parentNode, parent2 = node2.parentNode;
      if(parent1 == parent2)return goog.dom.compareSiblingOrder_(node1, node2);
      if(!isElement1 && goog.dom.contains(parent1, node2))return-1 * goog.dom.compareParentsDescendantNodeIe_(node1, node2);
      if(!isElement2 && goog.dom.contains(parent2, node1))return goog.dom.compareParentsDescendantNodeIe_(node2, node1);
      return(isElement1 ? node1.sourceIndex : parent1.sourceIndex) - (isElement2 ? node2.sourceIndex : parent2.sourceIndex)
    }
  }var doc$13 = goog.dom.getOwnerDocument(node1), range1, range2;
  range1 = doc$13.createRange();
  range1.selectNode(node1);
  range1.collapse(true);
  range2 = doc$13.createRange();
  range2.selectNode(node2);
  range2.collapse(true);
  return range1.compareBoundaryPoints(goog.global.Range.START_TO_END, range2)
};
goog.dom.compareParentsDescendantNodeIe_ = function(textNode, node$9) {
  var parent$5 = textNode.parentNode;
  if(parent$5 == node$9)return-1;
  for(var sibling = node$9;sibling.parentNode != parent$5;)sibling = sibling.parentNode;
  return goog.dom.compareSiblingOrder_(sibling, textNode)
};
goog.dom.compareSiblingOrder_ = function(node1$1, node2$1) {
  for(var s$13 = node2$1;s$13 = s$13.previousSibling;)if(s$13 == node1$1)return-1;
  return 1
};
goog.dom.findCommonAncestor = function() {
  var i$44, count$4 = arguments.length;
  if(count$4) {
    if(count$4 == 1)return arguments[0]
  }else return null;
  var paths = [], minLength = Infinity;
  for(i$44 = 0;i$44 < count$4;i$44++) {
    for(var ancestors = [], node$10 = arguments[i$44];node$10;) {
      ancestors.unshift(node$10);
      node$10 = node$10.parentNode
    }paths.push(ancestors);
    minLength = Math.min(minLength, ancestors.length)
  }var output = null;
  for(i$44 = 0;i$44 < minLength;i$44++) {
    for(var first = paths[0][i$44], j$2 = 1;j$2 < count$4;j$2++)if(first != paths[j$2][i$44])return output;
    output = first
  }return output
};
goog.dom.getOwnerDocument = function(node$11) {
  return node$11.nodeType == goog.dom.NodeType.DOCUMENT ? node$11 : node$11.ownerDocument || node$11.document
};
goog.dom.getFrameContentDocument = function(frame) {
  var doc$14;
  return doc$14 = goog.userAgent.WEBKIT ? frame.document || frame.contentWindow.document : frame.contentDocument || frame.contentWindow.document
};
goog.dom.getFrameContentWindow = function(frame$1) {
  return frame$1.contentWindow || goog.dom.getWindow_(goog.dom.getFrameContentDocument(frame$1))
};
goog.dom.setTextContent = function(element$17, text$5) {
  if("textContent" in element$17)element$17.textContent = text$5;
  else if(element$17.firstChild && element$17.firstChild.nodeType == goog.dom.NodeType.TEXT) {
    for(;element$17.lastChild != element$17.firstChild;)element$17.removeChild(element$17.lastChild);
    element$17.firstChild.data = text$5
  }else {
    goog.dom.removeChildren(element$17);
    var doc$15 = goog.dom.getOwnerDocument(element$17);
    element$17.appendChild(doc$15.createTextNode(text$5))
  }
};
goog.dom.getOuterHtml = function(element$18) {
  if("outerHTML" in element$18)return element$18.outerHTML;
  else {
    var div = goog.dom.getOwnerDocument(element$18).createElement("div");
    div.appendChild(element$18.cloneNode(true));
    return div.innerHTML
  }
};
goog.dom.findNode = function(root, p) {
  var rv$11 = [];
  return goog.dom.findNodes_(root, p, rv$11, true) ? rv$11[0] : undefined
};
goog.dom.findNodes = function(root$1, p$1) {
  var rv$12 = [];
  goog.dom.findNodes_(root$1, p$1, rv$12, false);
  return rv$12
};
goog.dom.findNodes_ = function(root$2, p$2, rv$13, findOne) {
  if(root$2 != null)for(var i$45 = 0, child$5;child$5 = root$2.childNodes[i$45];i$45++) {
    if(p$2(child$5)) {
      rv$13.push(child$5);
      if(findOne)return true
    }if(goog.dom.findNodes_(child$5, p$2, rv$13, findOne))return true
  }return false
};
goog.dom.TAGS_TO_IGNORE_ = {SCRIPT:1, STYLE:1, HEAD:1, IFRAME:1, OBJECT:1};
goog.dom.PREDEFINED_TAG_VALUES_ = {IMG:" ", BR:"\n"};
goog.dom.isFocusableTabIndex = function(element$19) {
  var attrNode = element$19.getAttributeNode("tabindex");
  if(attrNode && attrNode.specified) {
    var index$39 = element$19.tabIndex;
    return goog.isNumber(index$39) && index$39 >= 0
  }return false
};
goog.dom.setFocusableTabIndex = function(element$20, enable) {
  if(enable)element$20.tabIndex = 0;
  else element$20.removeAttribute("tabIndex")
};
goog.dom.getTextContent = function(node$12) {
  var textContent;
  if(goog.userAgent.IE && "innerText" in node$12)textContent = goog.string.canonicalizeNewlines(node$12.innerText);
  else {
    var buf = [];
    goog.dom.getTextContent_(node$12, buf, true);
    textContent = buf.join("")
  }textContent = textContent.replace(/\xAD/g, "");
  textContent = textContent.replace(/ +/g, " ");
  if(textContent != " ")textContent = textContent.replace(/^\s*/, "");
  return textContent
};
goog.dom.getRawTextContent = function(node$13) {
  var buf$1 = [];
  goog.dom.getTextContent_(node$13, buf$1, false);
  return buf$1.join("")
};
goog.dom.getTextContent_ = function(node$14, buf$2, normalizeWhitespace) {
  if(!(node$14.nodeName in goog.dom.TAGS_TO_IGNORE_))if(node$14.nodeType == goog.dom.NodeType.TEXT)normalizeWhitespace ? buf$2.push(String(node$14.nodeValue).replace(/(\r\n|\r|\n)/g, "")) : buf$2.push(node$14.nodeValue);
  else if(node$14.nodeName in goog.dom.PREDEFINED_TAG_VALUES_)buf$2.push(goog.dom.PREDEFINED_TAG_VALUES_[node$14.nodeName]);
  else for(var child$6 = node$14.firstChild;child$6;) {
    goog.dom.getTextContent_(child$6, buf$2, normalizeWhitespace);
    child$6 = child$6.nextSibling
  }
};
goog.dom.getNodeTextLength = function(node$15) {
  return goog.dom.getTextContent(node$15).length
};
goog.dom.getNodeTextOffset = function(node$16, opt_offsetParent) {
  for(var root$3 = opt_offsetParent || goog.dom.getOwnerDocument(node$16).body, buf$3 = [];node$16 && node$16 != root$3;) {
    for(var cur$2 = node$16;cur$2 = cur$2.previousSibling;)buf$3.unshift(goog.dom.getTextContent(cur$2));
    node$16 = node$16.parentNode
  }return goog.string.trimLeft(buf$3.join("")).replace(/ +/g, " ").length
};
goog.dom.getNodeAtOffset = function(parent$6, offset$9, opt_result$2) {
  for(var stack = [parent$6], pos = 0, cur$3;stack.length > 0 && pos < offset$9;) {
    cur$3 = stack.pop();
    if(!(cur$3.nodeName in goog.dom.TAGS_TO_IGNORE_))if(cur$3.nodeType == goog.dom.NodeType.TEXT) {
      var text$6 = cur$3.nodeValue.replace(/(\r\n|\r|\n)/g, "").replace(/ +/g, " ");
      pos += text$6.length
    }else if(cur$3.nodeName in goog.dom.PREDEFINED_TAG_VALUES_)pos += goog.dom.PREDEFINED_TAG_VALUES_[cur$3.nodeName].length;
    else for(var i$46 = cur$3.childNodes.length - 1;i$46 >= 0;i$46--)stack.push(cur$3.childNodes[i$46])
  }if(goog.isObject(opt_result$2)) {
    opt_result$2.remainder = cur$3 ? cur$3.nodeValue.length + offset$9 - pos - 1 : 0;
    opt_result$2.node = cur$3
  }return cur$3
};
goog.dom.isNodeList = function(val$20) {
  if(val$20 && typeof val$20.length == "number")if(goog.isObject(val$20))return typeof val$20.item == "function" || typeof val$20.item == "string";
  else if(goog.isFunction(val$20))return typeof val$20.item == "function";
  return false
};
goog.dom.getAncestorByTagNameAndClass = function(element$21, opt_tag$2, opt_class$2) {
  return goog.dom.getAncestor(element$21, function(node$17) {
    return(!opt_tag$2 || node$17.nodeName == opt_tag$2) && (!opt_class$2 || goog.dom.classes.has(node$17, opt_class$2))
  }, true)
};
goog.dom.getAncestor = function(element$22, matcher, opt_includeNode, opt_maxSearchSteps) {
  if(!opt_includeNode)element$22 = element$22.parentNode;
  for(var ignoreSearchSteps = opt_maxSearchSteps == null, steps = 0;element$22 && (ignoreSearchSteps || steps <= opt_maxSearchSteps);) {
    if(matcher(element$22))return element$22;
    element$22 = element$22.parentNode;
    steps++
  }return null
};
goog.dom.DomHelper = function(opt_document) {
  this.document_ = opt_document || goog.global.document || document
};
a = goog.dom.DomHelper.prototype;
a.getDomHelper = goog.dom.getDomHelper;
a.getDocument = function() {
  return this.document_
};
a.getElement = function(element$23) {
  return goog.isString(element$23) ? this.document_.getElementById(element$23) : element$23
};
a.$ = goog.dom.DomHelper.prototype.getElement;
a.getElementsByTagNameAndClass = function(opt_tag$3, opt_class$3, opt_el$2) {
  return goog.dom.getElementsByTagNameAndClass_(this.document_, opt_tag$3, opt_class$3, opt_el$2)
};
a.$$ = goog.dom.DomHelper.prototype.getElementsByTagNameAndClass;
a.setProperties = goog.dom.setProperties;
a.getViewportSize = function(opt_window$2) {
  return goog.dom.getViewportSize(opt_window$2 || this.getWindow())
};
a.getDocumentHeight = function() {
  return goog.dom.getDocumentHeight_(this.getWindow())
};
a.createDom = function() {
  return goog.dom.createDom_(this.document_, arguments)
};
a.$dom = goog.dom.DomHelper.prototype.createDom;
a.createElement = function(name$34) {
  return this.document_.createElement(name$34)
};
a.createTextNode = function(content$1) {
  return this.document_.createTextNode(content$1)
};
a.htmlToDocumentFragment = function(htmlString$2) {
  return goog.dom.htmlToDocumentFragment_(this.document_, htmlString$2)
};
a.getCompatMode = function() {
  return this.isCss1CompatMode() ? "CSS1Compat" : "BackCompat"
};
a.isCss1CompatMode = function() {
  return goog.dom.isCss1CompatMode_(this.document_)
};
a.getWindow = function() {
  return goog.dom.getWindow_(this.document_)
};
a.getDocumentScrollElement = function() {
  return goog.dom.getDocumentScrollElement_(this.document_)
};
a.getDocumentScroll = function() {
  return goog.dom.getDocumentScroll_(this.document_)
};
a.appendChild = goog.dom.appendChild;
a.removeChildren = goog.dom.removeChildren;
a.insertSiblingBefore = goog.dom.insertSiblingBefore;
a.insertSiblingAfter = goog.dom.insertSiblingAfter;
a.removeNode = goog.dom.removeNode;
a.replaceNode = goog.dom.replaceNode;
a.flattenElement = goog.dom.flattenElement;
a.getFirstElementChild = goog.dom.getFirstElementChild;
a.getLastElementChild = goog.dom.getLastElementChild;
a.getNextElementSibling = goog.dom.getNextElementSibling;
a.getPreviousElementSibling = goog.dom.getPreviousElementSibling;
a.isNodeLike = goog.dom.isNodeLike;
a.contains = goog.dom.contains;
a.getOwnerDocument = goog.dom.getOwnerDocument;
a.getFrameContentDocument = goog.dom.getFrameContentDocument;
a.getFrameContentWindow = goog.dom.getFrameContentWindow;
a.setTextContent = goog.dom.setTextContent;
a.findNode = goog.dom.findNode;
a.findNodes = goog.dom.findNodes;
a.getTextContent = goog.dom.getTextContent;
a.getNodeTextLength = goog.dom.getNodeTextLength;
a.getNodeTextOffset = goog.dom.getNodeTextOffset;
a.getAncestorByTagNameAndClass = goog.dom.getAncestorByTagNameAndClass;
a.getAncestor = goog.dom.getAncestor;goog.cssom = {};
goog.cssom.getAllCssText = function(opt_styleSheet) {
  return goog.cssom.getAllCss_(opt_styleSheet || document.styleSheets, true)
};
goog.cssom.getAllCssStyleRules = function(opt_styleSheet$1) {
  return goog.cssom.getAllCss_(opt_styleSheet$1 || document.styleSheets, false)
};
goog.cssom.getCssRulesFromStyleSheet = function(styleSheet$2) {
  var cssRuleList = null;
  try {
    cssRuleList = styleSheet$2.rules || styleSheet$2.cssRules
  }catch(e) {
    if(e.code == 15)throw e;
  }return cssRuleList
};
goog.cssom.getAllCssStyleSheets = function(opt_styleSheet$2, opt_includeDisabled) {
  var styleSheetsOutput = [], styleSheet$3 = opt_styleSheet$2 || document.styleSheets, includeDisabled = goog.isDef(opt_includeDisabled) ? opt_includeDisabled : false;
  if(styleSheet$3.imports && styleSheet$3.imports.length)for(var i$47 = 0, n$2 = styleSheet$3.imports.length;i$47 < n$2;i$47++)goog.array.extend(styleSheetsOutput, goog.cssom.getAllCssStyleSheets(styleSheet$3.imports[i$47]));
  else if(styleSheet$3.length) {
    i$47 = 0;
    for(n$2 = styleSheet$3.length;i$47 < n$2;i$47++)goog.array.extend(styleSheetsOutput, goog.cssom.getAllCssStyleSheets(styleSheet$3[i$47]))
  }else {
    var cssRuleList$1 = goog.cssom.getCssRulesFromStyleSheet(styleSheet$3);
    if(cssRuleList$1 && cssRuleList$1.length) {
      i$47 = 0;
      n$2 = cssRuleList$1.length;
      for(var cssRule;i$47 < n$2;i$47++) {
        cssRule = cssRuleList$1[i$47];
        cssRule.styleSheet && goog.array.extend(styleSheetsOutput, goog.cssom.getAllCssStyleSheets(cssRule.styleSheet))
      }
    }
  }if((styleSheet$3.type || styleSheet$3.rules) && (!styleSheet$3.disabled || includeDisabled))styleSheetsOutput.push(styleSheet$3);
  return styleSheetsOutput
};
goog.cssom.getCssTextFromCssRule = function(cssRule$1) {
  var cssText = "";
  if(cssRule$1.cssText)cssText = cssRule$1.cssText;
  else if(cssRule$1.style && cssRule$1.style.cssText && cssRule$1.selectorText) {
    var styleCssText = cssRule$1.style.cssText.replace(/\s*-goog-parent-stylesheet:\s*\[object\];?\s*/gi, "").replace(/\s*-goog-rule-index:\s*[\d]+;?\s*/gi, "");
    cssText = cssRule$1.selectorText + " { " + styleCssText + " }"
  }return cssText
};
goog.cssom.getCssRuleIndexInParentStyleSheet = function(cssRule$2, opt_parentStyleSheet) {
  if(cssRule$2.style["-goog-rule-index"])return cssRule$2.style["-goog-rule-index"];
  var parentStyleSheet = opt_parentStyleSheet || goog.cssom.getParentStyleSheet(cssRule$2);
  if(!parentStyleSheet)throw Error("Cannot find a parentStyleSheet.");var cssRuleList$2 = goog.cssom.getCssRulesFromStyleSheet(parentStyleSheet);
  if(cssRuleList$2 && cssRuleList$2.length)for(var i$48 = 0, n$3 = cssRuleList$2.length, thisCssRule;i$48 < n$3;i$48++) {
    thisCssRule = cssRuleList$2[i$48];
    if(thisCssRule == cssRule$2)return i$48
  }return-1
};
goog.cssom.getParentStyleSheet = function(cssRule$3) {
  return cssRule$3.parentStyleSheet || cssRule$3.style["-goog-parent-stylesheet"]
};
goog.cssom.replaceCssRule = function(cssRule$4, cssText$1, opt_parentStyleSheet$1, opt_index$2) {
  var parentStyleSheet$1 = opt_parentStyleSheet$1 || goog.cssom.getParentStyleSheet(cssRule$4);
  if(parentStyleSheet$1) {
    var index$40 = opt_index$2 >= 0 ? opt_index$2 : goog.cssom.getCssRuleIndexInParentStyleSheet(cssRule$4, parentStyleSheet$1);
    if(index$40) {
      goog.cssom.removeCssRule(parentStyleSheet$1, index$40);
      goog.cssom.addCssRule(parentStyleSheet$1, cssText$1, index$40)
    }else throw Error("Cannot proceed without the index of the cssRule.");
  }else throw Error("Cannot proceed without the parentStyleSheet.");
};
goog.cssom.addCssRule = function(cssStyleSheet, cssText$2, opt_index$3) {
  var index$41 = opt_index$3;
  if(index$41 < 0 || index$41 == undefined)index$41 = (cssStyleSheet.rules || cssStyleSheet.cssRules).length;
  if(cssStyleSheet.insertRule)cssStyleSheet.insertRule(cssText$2, index$41);
  else {
    var matches = /^([^\{]+)\{([^\{]+)\}/.exec(cssText$2);
    if(matches.length == 3)cssStyleSheet.addRule(matches[1], matches[2], index$41);
    else throw Error("Your CSSRule appears to be ill-formatted.");
  }
};
goog.cssom.removeCssRule = function(cssStyleSheet$1, index$42) {
  cssStyleSheet$1.deleteRule ? cssStyleSheet$1.deleteRule(index$42) : cssStyleSheet$1.removeRule(index$42)
};
goog.cssom.addCssText = function(cssText$3, opt_domHelper) {
  var document$2 = opt_domHelper ? opt_domHelper.getDocument() : goog.dom.getDocument(), cssNode = document$2.createElement("style");
  cssNode.type = "text/css";
  document$2.getElementsByTagName("head")[0].appendChild(cssNode);
  if(cssNode.styleSheet)cssNode.styleSheet.cssText = cssText$3;
  else {
    cssText$3 = document$2.createTextNode(cssText$3);
    cssNode.appendChild(cssText$3)
  }return cssNode
};
goog.cssom.getFileNameFromStyleSheet = function(styleSheet$4) {
  var href = styleSheet$4.href;
  if(!href)return null;
  return/([^\/\?]+)[^\/]*$/.exec(href)[1]
};
goog.cssom.getAllCss_ = function(styleSheet$5, isTextOutput) {
  for(var cssOut = [], styleSheets = goog.cssom.getAllCssStyleSheets(styleSheet$5), i$49 = 0;styleSheet$5 = styleSheets[i$49];i$49++) {
    var cssRuleList$3 = goog.cssom.getCssRulesFromStyleSheet(styleSheet$5);
    if(cssRuleList$3 && cssRuleList$3.length) {
      if(!isTextOutput)var ruleIndex = 0;
      for(var j$3 = 0, n$4 = cssRuleList$3.length, cssRule$5;j$3 < n$4;j$3++) {
        cssRule$5 = cssRuleList$3[j$3];
        if(isTextOutput && !cssRule$5.href) {
          var res$7 = goog.cssom.getCssTextFromCssRule(cssRule$5);
          cssOut.push(res$7)
        }else if(!cssRule$5.href) {
          cssRule$5.parentStyleSheet || (cssRule$5.style["-goog-parent-stylesheet"] = styleSheet$5);
          cssRule$5.style["-goog-rule-index"] = ruleIndex;
          cssOut.push(cssRule$5)
        }isTextOutput || ruleIndex++
      }
    }
  }return isTextOutput ? cssOut.join(" ") : cssOut
};
// Copyright 2008-9 Google Inc.  All Rights Reserved.

/**
 * @fileoverview An interactive form of reflow_timer.js
 * @author elsigh@google.com (Lindsey Simon)
 *
 * TODO(elsigh): allow targeting by element.
 * TODO(elsigh): show results about dom depth and * elements.
 */

(function(){

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
  style.fontSize = 'inherit';
  style.fontFamily = 'inherit';
  style.color = 'inherit';
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
  style.color = '#111';
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
