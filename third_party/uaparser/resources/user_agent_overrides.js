/*
 * Copyright 2010 Google Inc.
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

// Namespace.
var uap = {};

/**
 * Performs additional client side user agent detection for overriding
 * the server-side UA detection.
 * @return {?Array.<string>}
 */
uap.getJsUaOverrides = function() {
  var jsUa, jsFamilyName, jsV1, jsV2, jsV3;
  var uaString = navigator.userAgent;
  var isIE = uaString.indexOf('MSIE') != -1;
  var compatVersion;
  if (isIE && typeof document.documentMode != 'undefined') {
    var matches = /MSIE (\d+)\.(\d+)/.exec(uaString); // MSIE x.x;
    var tridentVersion = /Trident\/(\d+)/.exec(uaString);
    // Idea courtesy of JD Dalton.
    // see https://github.com/mathiasbynens/benchmark.js/blob/master/benchmark.js
    var MAGIC_IE_NUM = 4;
    if (!window.external) {
        jsFamilyName = 'IE Platform Preview';
        jsV1 = matches[1];
        jsV2 = '0';
        jsV3 = ''

      var tempDiv = document.createElement('div');

      // Based on the code at
      // http://ie.microsoft.com/testdrive/Graphics/Transform2D/animation.js
      if (jsV1 == '9') {
        if (typeof tempDiv.style['msTransform'] != 'undefined') {
          jsV3 = '6';
        }
        // Based on the code at
        // http://ie.microsoft.com/testdrive/HTML5/DOMCapabilities/demo.js
        else if (Object.getPrototypeOf(tempDiv) == HTMLDivElement.prototype) {
          jsV3 = '4';
        } else if (typeof Array.prototype.indexOf != 'undefined') {
          jsV3 = '3';
        } else if (typeof document.getElementsByClassName != 'undefined') {
          jsV3 = '2';
        } else {
          jsV3 = '1';
        }
      }

    // IE 9 Beta
    } else if (document.documentMode == 9 &&
               window.navigator.appMinorVersion.indexOf('beta') > -1) {
        jsFamilyName = 'IE Beta';
        jsV1 = '9';
        jsV2 = '0';
        jsV3 = 'beta';

    // Masquerading Document modes
    } else if (tridentVersion &&
               (compatVersion = Number(tridentVersion[1]) + MAGIC_IE_NUM,
                compatVersion != document.documentMode)) {
      jsFamilyName = 'IE ' + compatVersion + ' in Compatibility Mode';
      jsV1 = document.documentMode;
      jsV2 = matches[2];
      jsV3 = '0';
    }
  }

  // Keys match the params that our server expects.
  if (jsFamilyName) {
    jsUa = {
      'js_user_agent_family': jsFamilyName,
      'js_user_agent_v1': jsV1,
      'js_user_agent_v2': jsV2,
      'js_user_agent_v3': jsV3
    };
  }

  return jsUa;
};
