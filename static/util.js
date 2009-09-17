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
 * @param {string} param The param to look for.
 * @param {boolean} opt_win Use top instead of the current window.
 * @return {string} The value of the param or an empty string.
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
