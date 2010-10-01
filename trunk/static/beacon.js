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

