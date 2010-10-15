/**
 * Copyright 2009 Google Inc. All Rights Reserved.
 * License: http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview Puppet: a web-application testing framework.
 * @author stse@google.com
 */

/**
 * Namespace of Puppet.
 *
 * @type {Object}
 */
var puppet = {};


/**
 * Gets a matched string.
 *
 * @param {RegExp} re a regular expression.
 * @param {string} str a string to be matched.
 * @param {string|number} opt_value the default value.
 * @return {string} the first match (or false, if not matched).
 */
puppet.str = function(re, str, opt_value) {
  var match = re.exec(str);
  return match ? match[1] : opt_value;
};


/**
 * The version of Firefox.
 *
 * Note that beta versions of Firefox are called 'Minefield' or
 * 'Shiretoko', not 'Firefox'; hence checking for Gecko version in
 * addition. Must match 'Gecko\/[0-9]*', not 'Gecko\/[^ ]*', because
 * Webkit-based browsers contains 'Gecko like'.
 *
 * Ref: http://www.zytrax.com/tech/web/browser_ids.htm
 *
 * E.g. 3.0.1 for Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US;
 * rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1
 *
 * or, 2.0.0.16 for Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US;
 * rv:1.8.1.16) Gecko/20080716 Firefox/2.0.0.16
 *
 * or, Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:2.0a1pre)
 * Gecko/2008032902 Minefield/4.0a1pre.
 *
 * or, Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1a2)
 * Gecko/20080829071937 Shiretoko/3.1a2.
 *
 * @type {string?}
 */
puppet.firefox = puppet.str(/\bFirefox\/([0-9.]*)/, navigator.userAgent) ||
    puppet.str(/\bGecko\/([0-9.]*)/, navigator.userAgent);


/**
 * Version of Microsoft Internet Explorer.
 *
 * E.g. 7.0 for Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;
 * Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)
 *
 * or, 6.0 for Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;
 * GoogleT5; .NET CLR 1.1.4322; .NET CLR 2.0.50727)
 *
 * @type {string?}
 */
puppet.explorer = puppet.str(/\bMSIE ([0-9.]*)/, navigator.userAgent);


/**
 * Version of Webkit.
 *
 * E.g. 525.13 for Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)
 * AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13
 *
 * or, 525.13 for Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)
 * AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29
 * Safari/525.13
 *
 * @type {string?}
 */
puppet.webkit = puppet.str(/\bAppleWebKit\/([0-9.]*)/, navigator.userAgent);


/**
 * Version of Safari.
 *
 * E.g. 525.13 for Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)
 * AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13
 *
 * @type {string?}
 */
puppet.safari = puppet.str(/\bVersion\/([0-9.]*) Safari/, navigator.userAgent);


/**
 * Version of Chrome.
 *
 * or, 525.13 for Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)
 * AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29
 * Safari/525.13
 *
 * @type {string?}
 */
puppet.chrome = puppet.str(/\bChrome\/([0-9.]*)/, navigator.userAgent);


if (!puppet.firefox && !puppet.explorer && !puppet.webkit) {
  alert('Unsupported browser: ' + navigator.userAgent);
}


/**
 * Check if running on Windows.
 *
 * @type {boolean}
 */
puppet.windows = /Win/.test(navigator.platform);


/**
 * Check if running on Linux.
 *
 * @type {boolean}
 */
puppet.linux = /Linux/.test(navigator.platform);


/**
 * Check if running on Mac OS.
 *
 * @type {boolean}
 */
puppet.mac = /Mac/.test(navigator.platform);


/**
 * Check if running on iPhone
 *
 * @type {boolean}
 */
puppet.iphone = /iPhone/.test(navigator.userAgent);


/**
 * If the content is in an iframe.
 *
 * @private
 * @type {Element?}
 */
puppet.iframe_ = true;


/**
 * Iframe for the content document being tested.
 *
 * @private
 * @type {Element?}
 */
puppet.content_ = null;


/**
 * Div for the log of testing.
 *
 * @private
 * @type {Element?}
 */
puppet.log_ = null;


/**
 * Buffered HTML content of puppet.log_.
 *
 * Necessary for displaying errors at loading time. See
 * puppet/inline.html.
 *
 * @private
 * @type {string}
 */
puppet.html_ = '';


/**
 * Iframe for the control thread of testing; useful for Firebug's
 * debugger in Firefox.
 *
 * Not necessary for other browsers without Firebug's debugger,
 * sometimes even harmful. For example, in Safari, calling
 * XMLHttpRequest from the iframe's thread throws an permission
 * error. See puppet/request.html.
 *
 * @private
 * @type {Element?}
 */
puppet.control_ = null;


/**
 * If execution is ready for the next command.
 *
 * @private
 * @type {boolean}
 */
puppet.ready_ = false;


/**
 * If execution is in batch mode (not interactive).
 *
 * @private
 * @type {boolean}
 */
puppet.batch_ = true;


/**
 * The number of commands that have been queued via run().
 *
 * @private
 * @type {number}
 */
puppet.queued_ = 0;


/**
 * Command queue.
 *
 * @private
 * @type {Array}
 */
puppet.commands_ = [];


/**
 * Starting time.
 *
 * @private
 * @type {Date}
 */
puppet.start_ = new Date;


/**
 * If to show the clock time and the elapsed seconds at each command.
 *
 * @private
 * @type {boolean}
 */
puppet.clock_ = !!/[?&]clock\b/.exec(location.search);


/**
 * If to use Firebug lite; see http://getfirebug.com/lite.html.
 *
 * @private
 * @type {boolean}
 */
puppet.firebug_ = !!/[?&]firebug\b/.exec(location.search);


/**
 * If to show the evaluated string of the caller.
 *
 * @private
 * @type {boolean}
 */
puppet.call_ = !!/[?&]call\b/.exec(location.search);


/**
 * If to show the evaluated string of the caller only via window.dump().
 *
 * @private
 * @type {boolean}
 */
puppet.callx_ = !!/[?&]callx\b/.exec(location.search);


/**
 * If puppet should automatically start on load.
 *
 * @private
 * @type {boolean}
 */
puppet.nostart_ = !!/[?&]nostart\b/.exec(location.search);


/**
 * The number of seconds to delay between commands.
 *
 * @private
 * @type {number}
 */
puppet.delay_ = Number(puppet.str(/[?&]delay=([0-9.]+)/,
    location.search, 0));


/**
 * The number of seconds to flash/highlight the element in
 * action.
 *
 * Use ?flash=0 to disable flashing.
 *
 * @private
 * @type {number}
 */
puppet.flash_ = Number(puppet.str(/[?&]flash=([0-9.]+)/,
    location.search, 0.5));


/**
 * The number of seconds to before the whole test times out.
 *
 * @type {number}
 */
puppet.timeout = Number(puppet.str(/[?&]time=([0-9.]+)/,
    location.search, 20));


/**
 * The height of the content iframe.
 *
 * For example, 65% or 100pt.
 *
 * Use ?height=100% or the shortcut ?full for fullscreen demo.
 *
 * @private
 * @type {string}
 */
puppet.height_ = puppet.str(/[?&]height=([^?&]+)/, location.search, '65%');

if (/[?&]full\b/.exec(location.search)) puppet.height_ = '100%';


/**
 * If to step through and stop for debugging.
 *
 * @private
 * @type {boolean}
 */
puppet.step_ = !!/[?&]step\b/.exec(location.search);


/**
 * The i-th numbers of run() commands to pause, separated by comma.
 *
 * E.g. ?cmd=3,6 to pause at the 3rd and the 6th commands.
 *
 * @private
 * @type {Array.<string>}
 */
puppet.command_ = puppet.str(/[?&]cmd=([^?&]+)\b/,
    location.search, '').split(',');


/**
 * The i-th numbers of soure code lines to pause, separated by comma. Only
 * supported in Firefox.
 *
 * E.g. ?line=3,6 to pause at the 3rd and the 6th lines.
 *
 * @private
 * @type {Array.<string>}
 */
puppet.line_ = puppet.str(/[?&]line=([^?&]+)\b/,
    location.search, '').split(',');

// Function split() returns [''] for the empty split, hence the array
// always contains at least one element.
if (!puppet.firefox && Number(puppet.line_[0])) {
  alert('Param ?line is not supported for this browser; use ?cmd instead.');
}


/**
 * If the test is run via the multi-test runner puppet/run.html.
 *
 * @private
 * @type {boolean}
 */
puppet.multirun_ = !!/[?&]time=0/.test(location.search);


/**
 * The number of remaining commands to step through.
 *
 * @private
 * @type {number}
 */
puppet.steps_ = 1;


/**
 * Confirm dialog answer queue.
 *
 * @private
 * @type {Array}
 */
puppet.confirms_ = [];


/**
 * Prompt dialog answer queue.
 *
 * @private
 * @type {Array}
 */
puppet.prompts_ = [];


/**
 * Alert dialog counter.
 *
 * @private
 * @type {number}
 */
puppet.alerts_ = 0;


/**
 * Initialization hooks for the 'onload' handler during the first
 * load of the page.
 *
 * @type {Array.<Function>}
 */
puppet.oninit = [];


/**
 * Finalization hooks.
 *
 * @type {Array.<Function>}
 */
puppet.ondone = [];


/**
 * The URL in the last call of window.open.
 *
 * Puppet cannot control or check elements in new windows opened by
 * the test applications via window.open(). Mock window.open() and
 * save the URL such that the test can load the URL manually.
 *
 * @type {string}
 */
puppet.url = '';


/**
 * If the server domain is outside google.com or do not server /maps/,
 * or explicitly with ?domain in URL.
 *
 * @type {boolean}
 */
puppet.domain = location.pathname.indexOf('/api/') >= 0 && (
    !!/[?&]domain\b/.exec(location.search) ||
    location.hostname.indexOf('.google.com') == -1 ||
    location.pathname.indexOf('/maps/') == -1);


//-- Browser commands.

/**
 * Loads a new document and waits until the document is fully loaded.
 *
 * Do not load documents more than once per test, regardless of using
 * load/login/logout. Loading documents and initializing take
 * significant amount of time; tests with long running time will time
 * out in slower machines, a slower xpath library for IE, Forge
 * backends, or Selenium farm. Divide your tests into minimal units so
 * that they can run in parallel. In general, a test should not run
 * more than 10 seconds in your local Firefox 3 on Linux.
 *
 * @param {string} url URL of the document.
 */
function load(url) {
  var url2 = puppet.searchParams(url);
  puppet.echo('-- loading: ' + url2,
      '-- loading: ' + '<a href=' + url2 + ' target=_blank>' + url2 + '</a>');
  // An onload handler for puppet.content_, which turns puppet.ready_
  // true when loaded, is already installed in puppet.init().
  puppet.ready_ = false;

  // NOTE(stse): must use 'location.replace(url2)' instead of
  // 'location.href = url2' or 'src = url2' to force firebug to load the
  // document even when firebug's debugger is active.
  // See 'Reloading Breakpoint' in puppet/debugger.html.
  if (puppet.firefox) puppet.window().location.href = url2;
  else puppet.content_.src = url2;
}


/**
 * Reloads the current page and waits until the document is fully loaded.
 */
function reload() {
  load(puppet.window().location.href);
}


/**
 * Focuses to an element.
 *
 * @param {string} path XPath of the target element.
 */
function focus(path) {
  puppet.element(path).focus();
}


/**
 * Blurs from an element.
 *
 * @param {string} path XPath of the target element.
 */
function blur(path) {
  puppet.element(path).blur();
}


/**
 * Goes to the link of an 'A' element.
 *
 * The path must be relative such that the proxy is still used.
 *
 * @param {string} path XPath of the target element.
 */
function go(path) {
  // Using absolute URLs with http:// protocol prefix leads the test
  // page to go to a different domain (except when the domain happens
  // to be the same), violating the browser's cross-domain restriction
  // for security. Always use relative URLs.
  var domain = location.protocol + '//' + location.host;

  // An onload handler for puppet.content_, which turns puppet.ready_
  // true when loaded, is already installed in puppet.init().
  // puppet.ready_ = false;

  var href = puppet.element(path).href;
  assert(href.indexOf(domain) == 0 || !/:\/\//.test(href),
      'using absolute path violates cross-domain restriction:\n  ' + href);
  puppet.window().location.href = href;
}


/**
 * Inputs a value to a text field element.
 *
 * @param {string} path XPath of the target element.
 * @param {string} value string.
 */
function input(path, value) {
  puppet.element(path).value = value;
  puppet.change(puppet.elem(path));
}


/**
 * Types a string, or presses a key or key sequence to an element.
 *
 * If the element is not listening to keyboard events, use 'input'
 * instead of 'type'. The former is preferred because it is more
 * robust to UI changes and browser compatibility.
 *
 * The second parameter can be:
 * 1. A string like 'abc'.
 *    run(type, map.input, 'abc'): Type 'abc'.
 *
 * 2. A number: key code of pressed key. Set char code as 0 by default.
 *    run(type, map.input, 40): Press down key(key code: 40).
 *
 * 3. An array: key sequence. Each element can be a key code, or a char.
 *    run(type, map.input, 40): Press down key.
 *    run(type, map.input, [40, 38]): Press down key, then up key(key code: 38).
 *    run(type, map.input, ['a', 38, 'B']. First press 'a', then down key, and
 *       finally 'B'.
 *
 * Use only key code when necessary.
 *
 * @param {string} path XPath of the target element.
 * @param {string|number|Array} value Typed string, or pressed key or key
 *     sequence.
 */
function type(path, value) {
  var elem = puppet.element(path);
  var keyCodes = [];
  var charCodes = [];

  if (typeof value == 'string') {
    var upper = value.toUpperCase();
    for (var i = 0; i < value.length; i++) {
      keyCodes.push(upper.charCodeAt(i));
      charCodes.push(value.charCodeAt(i));
    }
  } else if (typeof value == 'number') {
    keyCodes.push(value);
    charCodes.push(0);
  } else if (value instanceof Array) {
    for (var i = 0; i < value.length; i++) {
      if (typeof value[i] == 'number') {
        keyCodes.push(value[i]);
        charCodes.push(0);
      } else if (typeof value[i] == 'string') {
        // Use the first char, if multiple chars is provided,
        // e.g. ['bc', 40] is equals to ['b', 40].
        keyCodes.push(value[i].toUpperCase().charCodeAt(0));
        charCodes.push(value[i].charCodeAt(0));
      }
    }
  }

  for (var i = 0; i < keyCodes.length; i++) {
    puppet.key_(path, 'keydown', keyCodes[i], 0);
    puppet.key_(path, 'keypress', keyCodes[i], charCodes[i]);
    puppet.key_(path, 'keyup', keyCodes[i], 0);

    // TODO(stse): Firefox also triggers an 'input' event.

    // Ignore non-printable ASCII character simply, to make sure the input
    // box won't change when type ASCII control keys like '\t', '\n'.
    // However, there are inconsistent though rare cases with backspace where
    // type(map.input, 'ab\b') becomes 'a' in firefox but 'ab' in IE.
    var c = String.fromCharCode(charCodes[i]);
    if (!puppet.firefox && elem.tagName == 'INPUT' &&
        (c >= ' ' && c <= '~' || c > '\x7F')) {
      // Assume that the cursor is at the end of the input.
      elem.value += c;
    }
  }
}


/**
 * Fires a mouse event to an element at the x and y coordinates.
 *
 * No action if the element is null (to make it easier to trigger
 * multiple mouse events in sequence).
 *
 * @param {string} path XPath of the target element.
 * @param {string} type event type.
 * @param {number?} opt_x The x coordinate in the client space.
 * @param {number?} opt_y The y coordinate of the client space.
 * @param {number?} opt_button The mouse button.
 */
function mouse(path, type, opt_x, opt_y, opt_button) {
  var elem = puppet.elem(path);
  if (!elem) return;

  var x = opt_x || 0;
  var y = opt_y || 0;
  var button = opt_button || 0;
  if (puppet.firefox || puppet.webkit) {
    var event = puppet.window().document.createEvent('MouseEvents');
    // screenX=0 and screenY=0 are ignored
    event.initMouseEvent(
        type, true, true, puppet.window(), 1, 0, 0, x, y,
        false, false, false, false, button, null);
    elem.dispatchEvent(event);
  } else {  // Assume puppet.explorer.
    var event = document.createEventObject();
    event.clientX = x;
    event.clientY = y;
    event.button = button;
    elem.fireEvent('on' + type, event);
  }
}


/**
 * Clicks an element at the x and y coordinates.
 *
 * For GWT (Google Web Toolkit), use mouse(path, 'click') instead
 * because the href of its buttons should not be followed.
 *
 * @param {string} path XPath of the target element.
 * @param {number} opt_x The x coordinate in the client space.
 * @param {number} opt_y The y coordinate of the client space.
 */
function click(path, opt_x, opt_y) {
  assert(puppet.elem(path), 'missing element');
  mouse(path, 'mousedown', opt_x, opt_y);
  mouse(path, 'mouseup', opt_x, opt_y);
  mouse(path, 'click', opt_x, opt_y);

  var elem = puppet.elem(path);
  if (!elem) return;  // Gone after actions by mouse() above.

  if (elem.tagName == 'INPUT' && puppet.explorer) elem.click();
  else if (elem.tagName == 'LABEL' && puppet.explorer) elem.click();
  else if (elem.tagName == 'A' && !elem.onclick) {
    // Skip 'go' if there are maps-specific click handlers.
    if (elem.__e_ && elem.__e_.click || elem.getAttribute('xonclick') ||
        elem.getAttribute('jsaction')) return;

    // Follow the 'href' link via go() only if there are no direct
    // handlers. This behavior is different from interactively
    // clicking on the element: 1. there can be handlers in a
    // containing element, and, 2. the handler may return 'false', in
    // which case the link is still followed. There is no easy, robust
    // way to implement the exact behavior; a test can simply call
    // go() instead of click(), if that's the desired action.
    go(path);
  }
}


/**
 * Drags an element.
 *
 * @param {string} path XPath of the target element.
 * @param {number} dx increment in x coordinate.
 * @param {number} dy increment in y coordinate.
 */
function drag(path, dx, dy) {
  var x = puppet.left(puppet.elem(path));
  var y = puppet.top(puppet.elem(path));
  mouse(path, 'mousedown', x, y);
  mouse(path, 'mousemove', x + dx, y + dy);
  mouse(path, 'mouseup', x + dx, y + dy);
}


/**
 * Fires a mutation event.
 *
 * @param {string} path XPath of the target element.
 * @param {string} type event type.
 */
function mutation(path, type) {
  if (puppet.firefox) {
    var event = document.createEvent('MutationEvents');
    event.initMutationEvent(type, true, true, null, null, null, null, null);
    puppet.element(path).dispatchEvent(event);
  } else assert(false, 'unsupported');
}


/**
 * Selects a value from a pull down menu.
 *
 * @param {string} path XPath of the target element.
 * @param {string} value value to be selected.
 */
function select(path, value) {
  var elem = puppet.element(path);
  elem.value = value;
  puppet.change(elem);
}


/**
 * Toggles a checkbox.
 *
 * @param {string} path XPath of the target element.
 * @param {string} opt_value Forced value.
 */
function toggle(path, opt_value) {
  var elem = puppet.element(path);
  var value = typeof opt_value == 'undefined' ? !elem.checked : opt_value;
  elem.checked = value;
  puppet.change(elem);
}


/**
 * Fires a change event.
 *
 * @param {string} elem The target element.
 */
puppet.change = function(elem) {
  if (puppet.firefox || puppet.webkit) {
    var event = document.createEvent('HTMLEvents');
    event.initEvent('change', true, true);
    elem.dispatchEvent(event);
  } else {
    var event = document.createEventObject();
    elem.fireEvent('onchange', event);
  }
};


/**
 * Waits until an element is present, shown and has the property value.
 *
 * See puppet.shown for the definitions of visibility.
 *
 * @param {string} path XPath of the target element.
 * @param {string} opt_key key of the property.
 * @param {string} opt_value value of the property.
 * @return {boolean} If the wait is over.
 */
function find(path, opt_key, opt_value) {
  return wait(puppet.check_, path, opt_key, opt_value);
}


/**
 * Waits until the number of elements has the expected count.
 *
 * @param {string} path XPath of the target elements.
 * @param {number} expected number of elements expected to match.
 * @return {boolean} If the wait is over.
 */
function count(path, expected) {
  return wait(function() {
    return puppet.elems(path).length == expected;
  });
}


/**
 * Waits until an element is present and shown.
 *
 * See puppet.shown for the definitions of visibility.
 *
 * @param {string} path XPath of the target element.
 */
function shown(path) {
  wait(function() {
    var elem = puppet.elem(path);
    return !!elem && puppet.shown(elem);
  });
}


/**
 * Waits until an element is present and visible.
 *
 * See puppet.shown for the definitions of visibility.
 *
 * @param {string} path XPath of the target element.
 */
function visible(path) {
  wait(function() {
    var elem = puppet.elem(path);
    return !!elem && puppet.visible(elem);
  });
}


/**
 * Checks if an element is present, shown and has the property value.
 *
 * See puppet.shown for definitions of visibility.
 *
 * TODO(stse): rename to 'present' (symmetric to 'absent').
 *
 * @param {string} path XPath of the target element.
 * @param {string} opt_key key of the property.
 * @param {string} opt_value value of the property.
 */
function check(path, opt_key, opt_value) {
  // HACK(stse): Maps API also defines 'window.check', which is in
  // conflict with Puppet; verify by loading API tests in debug mode.
  if (typeof path != 'string') return;
  assert(puppet.check_(path, opt_key, opt_value), 'missing element');
}


/**
 * Checks if an element has the effective property value.
 *
 * @param {string} path XPath of the target element.
 * @param {string} key key of the property.
 * @param {string} value value of the property.
 */
function effective(path, key, value) {
  assertEq(puppet.effective(puppet.element(path), key), value,
      'effective value');
}


/**
 * Waits until an element is undefined or not shown or does not have
 * the property value.
 *
 * See puppet.shown for definitions of visibility.
 *
 * If an action such as click() is used to trigger the disappearing of
 * an element (to be verified by this function), some definite
 * condition such as the change of other element must be checked first
 * before checking with absent(), to ensure that click() is finished
 * before checking with absent(). Otherwise, the change made by
 * click() may not be in effect when absent() is called. However, the
 * sequence of checking the presence of an element, clicking, and then
 * checking the absence of the same element is fine.
 *
 * For example, this is a bad test:
 *
 *   1. run(load, '/maps?q=ny');
 *   2. run(click, map.mapshop.launcher);
 *   3. run(absent, map.panel + text('New York'));
 *
 * because the element text('New York') may have yet appeared at Step
 * 2, hence Step 3 passes trivially. Change it to
 *
 *   1. run(load, '/maps?q=ny');
 *   2. run(find, map.panel + text('New York'));
 *   3. run(click, map.mapshop.launcher);
 *   4. run(absent, map.panel + text('New York'));
 *
 * or
 *
 *   1. run(load, '/maps?q=ny');
 *   2. run(click, map.mapshop.launcher);
 *   3. run(find, map.mapshop.panel);
 *   4. run(absent, map.panel + text('New York'));
 *
 * @param {string} path XPath of the target element.
 * @param {string} opt_key key of the property.
 * @param {string} opt_value value of the property.
 * @return {boolean} If the wait is over.
 */
function absent(path, opt_key, opt_value) {
  return wait(function() { return !puppet.check_(path, opt_key, opt_value); });
}


/**
 * Waits until an element has a given style.
 *
 * Use background(foo, value) instead of have(foo, 'backgroundColor',
 * value) in order to support flashing of the element in action; see
 * puppet.flash().
 *
 * NOTE(rdub): Browser inconsistencies can require the same effective property
 * to be measured in different ways depending on the browser. For example, a
 * centered background image is registered as having backgroundPosition
 * '50% 50%' in FF3 and Safari, '' in FF2, and both backgroundPositionX:
 * 'center' and backgroundPositionY: '50%' in IE.
 *
 * @param {string} path XPath of the target element.
 * @param {string} key key of the style.
 * @param {string} value value of the style.
 * @return {boolean} If the wait is over.
 */
function have(path, key, value) {
  return wait(function() {
    var elem = puppet.elem(path);
    return elem && puppet.match(value, puppet.style(elem)[key]); });
}


/**
 * Waits until an element has a given background color.
 *
 * See puppet.flash().
 *
 * @param {string} path XPath of the target element.
 * @param {string} value value of the style.
 * @return {boolean} If the wait is over.
 */
function background(path, value) {
  return wait(function() {
    var elem = puppet.elem(path);
    if (!elem) return false;
    if ('puppetColor_' in elem) return puppet.match(value, elem.puppetColor_);
    else puppet.match(value, puppet.style(elem).backgroundColor);
  });
}


/**
 * Waits until an element has a given attribute.
 *
 * @param {string} path XPath of the target element.
 * @param {string} key key of the style.
 * @param {string} value value of the style.
 * @return {boolean} If the wait is over.
 */
function attribute(path, key, value) {
  return wait(function() {
    var elem = puppet.elem(path);
    if (key == 'class' && puppet.explorer) key = 'className';
    return elem && puppet.match(value, elem.getAttribute(key)); });
}


/**
 * Waits until an element has a given property.
 *
 * @param {string} path XPath of the target element.
 * @param {string} key key of the style.
 * @param {string} value value of the style.
 * @return {boolean} If the wait is over.
 */
function property(path, key, value) {
  return wait(function() {
    var elem = puppet.elem(path);
    return elem && puppet.match(value, elem[key]); });
}


/**
 * Outputs the HTML content of an element for debug.
 *
 * @param {string} path XPath of the target element.
 */
function output(path) {
  puppet.echo(puppet.element(path).innerHTML);
}


/**
 * Stops and skips the rest of testing commands.
 *
 * Useful for controling the flow of tests such as marking manual test
 * cases for broken tests, or for tests that require certain browsers
 * or servers.
 */
function stop() {
  if (/[?&]nostop\b/.test(location.search)) {
    puppet.echo('stop() is skipped due to ?nostop in URL.');
    return;
  }

  puppet.echo('-- use ?nostop in URL to override.', '-- use <a href=' +
    puppet.add_(document.location.href, 'nostop') +
    '>?nostop</a> in URL to override.');
  puppet.commands_ = [];
}


/**
 * Waits until the function with the arguments is satisfied.
 *
 * @param {Object} func The function.
 * @param {*} var_args Variable-length arguments.
 * @return {boolean} If the wait is over.
 * @see puppet.eval_().
 */
function wait(func, var_args) {
  assertEq('function', typeof func, 'wrong type');
  var args = puppet.copy_(arguments);
  puppet.ready_ = puppet.eval_.apply(null, args);
  if (!puppet.ready_) {
    // Wait for network and js evaluation.
    puppet.setTimeout_(function() {
      wait.apply(null, args);  // arguments of wait()
    }, 200);
  }
  return puppet.ready_;
}


/**
 * Waits until the function with the arguments is NOT satisfied.
 *
 * @param {Object} func The function.
 * @param {*} var_args Variable-length arguments.
 * @return {boolean} If the wait is over.
 * @see puppet.eval_().
 */
function waitNot(func, var_args) {
  // Same as wait() but negating the result of puppet.eval_.
  assertEq('function', typeof func, 'wrong type');
  var args = puppet.copy_(arguments);
  puppet.ready_ = !puppet.eval_.apply(null, args);
  if (!puppet.ready_) {
    // Wait for network and js evaluation.
    puppet.setTimeout_(function() {
      waitNot.apply(null, args);  // arguments of waitNot()
    }, 200);
  }
  return puppet.ready_;
}


/**
 * Makes a new, identified element as the content being tested.
 *
 * This function replaces the content iframe. Call via run(), and do
 * not call load(), go(), submit() afterwards.
 *
 * @param {string} id identifier of the new 'div'.
 * @return {Element} The new 'div'.
 */
function make(id) {
  assert(puppet.ready_, 'use inside run()');
  puppet.iframe_ = false;
  var div = puppet.document().createElement('div');
  div.id = id;
  div.style.width = '100%';
  div.style.height = puppet.height_;
  puppet.document().body.replaceChild(div, puppet.content_);
  // Since the iframe puppet.content_ is replaced, do initializations here.
  puppet.setDialog_();
  puppet.ready_ = true;
  return div;
}


/**
 * Queues to run a command asynchronously.
 *
 * The function run(command, arg1, arg2, ...) queues the command and
 * its arguments and executes command(arg1, arg2, ...) only when the
 * commands queued earlier are executed. If the command is a string,
 * the function eval() is used to execute the command; if it is a
 * function, its method apply is called with arg1, arg2, ...; or, if
 * it is an array, run() is recursively called on each element of the
 * array with the same arguments arg1, arg2, .... For example,
 * run([find, click], map.submit); is the same as run(find,
 * map.submit); run(click, map.submit);.
 *
 * The order of command execution are guaranteed; when all batch
 * commands are finished, a passed (or failed or timed out) message is
 * printed to the browser's standard output using window.dump() (see
 * below on how to enable window.dump). When close is passed as an URL
 * parameter, window.close() is called when the test is done to close
 * the browser, which is useful for testing in batch mode with Blaze
 * and Forge.
 *
 * Call run() with no arguments to end a test if there are no commands
 * to queue.
 *
 * This function also inserts pause() based on ?cmd or ?line.
 *
 * @param {*} var_args function and its arguments.
 */
function run(var_args) {
  // If there are no arguments, use a command of the empty array as a
  // placeholder because puppet.start checks if queueing of commands
  // is done by waiting for the length of puppet.commands_  > 0.
  var command = arguments.length == 0 ? [[]] : puppet.copy_(arguments);

  var caller = puppet.caller_();
  if (caller) command.caller_ = 'line ' + caller.line + ': ' + caller.code;

  // Insert pause() based on ?cmd or ?line. Do not use
  // puppet.commands_.length to check against ?cmd because the added
  // pause() commands change the numbers of commands in the queue
  // puppet.commands_.
  if (caller && puppet.member_(String(caller.line), puppet.line_) ||
      puppet.member_(String(puppet.queued_), puppet.command_)) {
    var command2 = [pause];
    command2.caller_ = ': pause() from URL ?cmd or ?line';
    puppet.commands_.push(command2);
  }

  puppet.commands_.push(command);
  puppet.queued_++;
}


/**
 * Runs a command if the predicate is satisfied.
 *
 * @param {Object} pred The predicate that takes no arguments.
 * @param {*} var_args The command as it would be passed to run.
 * @see puppet.eval_().
 * @see puppet.execute().
 */
function when(pred, var_args) {
  if (puppet.eval_(pred)) puppet.execute(puppet.copy_(arguments, 1));
}


/**
 * Asserts a predicate.
 *
 * Stops testing and throws an exception if the predicate is not
 * satisfied.
 *
 * @param {Object} pred The predicate that takes no arguments.
 * @param {string} opt_comment Comment on the predicate.
 * @param {boolean} opt_nothrow No error throwing.
 * @see puppet.eval_().
 */
function assert(pred, opt_comment, opt_nothrow) {
  var value = puppet.eval_(pred);
  if (!value) {
    // No stack trace for non-Fireox; use manual echo instead.
    if (!puppet.firefox) {
      puppet.echo('assert: ' + value + ': ' + (opt_comment || pred));
    }
    puppet.ready_ = false;
    var stack = puppet.stack_();
    puppet.done_(stack);
    if (!opt_nothrow) throw stack;
  }
}


/**
 * Asserts equality.
 *
 * This simple function should not be inlined so that the stack trace
 * shows the arguments during debugging.
 *
 * @param {Object} x Any object.
 * @param {Object} y Any object.
 * @param {string} opt_comment Comment on the equality.
 */
function assertEq(x, y, opt_comment) {
  if (x != y) puppet.echo('Expected: ' + x + '\nActual:   ' + y);
  assert(x == y, opt_comment);
}


/**
 * Asserts inequality.
 *
 * This simple function should not be inlined so that the stack trace
 * shows the arguments during debugging.
 *
 * @param {Object} x Any object.
 * @param {Object} y Any object.
 * @param {string} opt_comment Comment on the inequality.
 */
function assertNotEq(x, y, opt_comment) {
  if (x == y) puppet.echo('Same: ' + x);
  assert(x != y, opt_comment);
}


/**
 * Asserts floating-point equality with tolerance.
 *
 * This simple function should not be inlined so that the stack trace
 * shows the arguments during debugging.
 *
 * @param {Number} x A numerical value.
 * @param {Number} y A numerical value.
 * @param {Number} tolerance A numerical value.
 * @param {string} opt_comment Comment on the inequality.
 */
function assertClose(x, y, tolerance, opt_comment) {
  var close = Math.abs(x - y) < tolerance;
  if (!close) puppet.echo(
      'Difference: |' + x + ' - ' + y + '| = ' + Math.abs(x - y) + '\n' +
      'Tolerance:   ' + tolerance);
  assert(close, opt_comment);
}


/**
 * Submits a form.
 *
 * @param {string} html HTML of the form.
 */
puppet.submit = function(html) {
  // An onload handler for puppet.content_, which turns puppet.ready_
  // true when loaded, is already installed in puppet.init().
  puppet.ready_ = false;
  puppet.document().body.innerHTML = html;
  puppet.document().getElementsByTagName('form')[0].submit();
};


/**
 * Sleeps.
 *
 * This command is for experimenting testing; never rely on sleeping
 * for synchronization such as completion of asynchronous network
 * downloads or javascript initializations.
 *
 * @param {number} sec second to sleep.
 */
function sleep_(sec) {
  if (/[?&]nosleep\b/.test(location.search)) {
    puppet.echo('sleep_() is skipped due to ?nosleep in URL.');
    return;
  } else if (puppet.step_) {
    puppet.echo('sleep_() is skipped due to stepping.');
    return;
  }

  puppet.echo('-- sleeping ' + sec +
      ' seconds; use ?nosleep in URL to override.',
      '-- sleeping ' + sec + ' seconds; use <a href=' +
      puppet.add_(document.location.href, 'nosleep') +
      '>?nosleep</a> in URL to override.');
  var elapsed = 0;
  wait(function() {
    elapsed += 100;
    return elapsed >= sec * 1000; });
}


/**
 * Sleeps for flaky tests (for temporary use).
 */
function sleep__() {
  sleep_(3);
}


//-- XPath predicates.

/**
 * Make a XPath predicate function.
 *
 * The default value of opt_path for these functions is //*, which in
 * XPath means any node in the subtree. These convenience functions
 * make string quoting and composing XPath predicates easy. For
 * example, map.panel + text('New York, NY')) in the test submit.html
 * above is evaluated to be 'id("panel")//*[text() = "New York, NY"]'.
 *
 * @param {string} prefix prefix of the predicate string.
 * @param {string} suffix suffix of the predicate string.
 * @return {function(string, string=):string} a function that takes the
 *     value of the predicate and an optional path and returns a XPath
 *     predicate as a string; the default value of the path is '//*'.
 */
puppet.pred = function(prefix, suffix) {
  return function(value, opt_path) {
    var path = typeof opt_path == 'undefined' ? '//*' : opt_path;
    return path + prefix + puppet.quote_(value) + suffix;
  };
};


/**
 * Make a quoted XPath value.
 *
 * E.g.,
 *
 *   foo       becomes  "foo"
 *   foo'bar   becomes  "foo'bar"
 *   foo"bar   becomes  'foo"bar'
 *   foo"bar'  becomes  concat("foo", '"', "bar'")
 *
 * @private
 * @param {string} x Input.
 * @return {string} Quoted value.
 */
puppet.quote_ = function(x) {
  var y = String(x);
  if (y.indexOf('"') >= 0 && y.indexOf('\'') >= 0) {  // contains both quotes
    return 'concat("' + y.split('"').join('", \'"\', "') + '")';
  } else if (y.indexOf('"') >= 0) {  // contains only double quotes
    return '\'' + y + '\'';
  } else return '"' + y + '"';  // contains only single quotes
};


/**
 * XPath namespaces.
 *
 * @type {Object}
 */
puppet.namespace = { svg: 'http://www.w3.org/2000/svg' };


/**
 * XPath namespace resolver.
 *
 * @private
 * @param {string} prefix The prefix.
 * @return {string} The namespace.
 */
puppet.resolver_ = function(prefix) {
  return puppet.namespace[prefix] || null;
};


/**
 * XPath predicate for the 'class' attribute.
 *
 * Note that 'class' is a reserved keyword.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var xclass = puppet.pred('[@class = ', ']');


/**
 * XPath predicate for the containment with the 'style' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred

 */
var style = puppet.pred('[contains(@style, ', ')]');


/**
 * XPath predicate for the containment with the 'class' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred

 */
var subclass = puppet.pred('[contains(@class, ', ')]');


/**
 * XPath predicate for the 'href' attribute.
 *
 * TODO(stse): always use subhref instead of href.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred

 */
var href = puppet.pred('[@href = ', ']');


/**
 * XPath predicate for the containment with the 'href' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred

 */
var subhref = puppet.pred('[contains(@href, ', ')]');


/**
 * Optimized XPath predicate for the 'id' attribute for unique
 * identifiers.
 *
 * 'id' should uniquely identify an element, hence the usual prefix
 * path such as //* is not a parameter. It returns expressions of the
 * form 'id("foo")' For performance, do not use expression such as
 * '//*[@id = "foo"]' unless the identifier is not unique, in which case
 * the function idx() below can be used.
 *
 * @param {string} value Attribute value.
 * @return {string} XPath predicate.
 */
function id(value) {
  return 'id("' + value + '")';
}


/**
 * XPath predicate for the 'id' attribute for non-unique identifiers.
 *
 * Useful for combining XPath expressions such as id('foo') +
 * idx('bar') = id('foo')//*[@id = "bar"], as well as for other XPath
 * features such as //*[@id = "bar"][2] for selecting the second
 * match.
 *
 * See the discussion at id(). Also, note that //*[id("foo")] is
 * different from '//*[@id = "foo"]'; the latter should be used
 * instead.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var idx = puppet.pred('[@id = ', ']');


/**
 * XPath predicate for the containment with the 'id' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var subid = puppet.pred('[contains(@id, ', ')]');


/**
 * XPath predicate for the 'name' attribute.
 *
 * Note that 'window.name' is predefined. In WebKit, window.name is
 * special and cannot even be reassigned.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var xname = puppet.pred('[@name = ', ']');


/**
 * XPath predicate for the containment with the 'src' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var src = puppet.pred('[contains(@src, ', ')]');


/**
 * XPath predicate for the containment with the 'text' function.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var subtext = puppet.pred('[contains(text(), ', ')]');


/**
 * XPath predicate for the 'text' function.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var text = puppet.pred('[text() = ', ']');


/**
 * XPath predicate for the 'title' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var title = puppet.pred('[@title = ', ']');


/**
 * XPath predicate for the 'value' attribute.
 *
 * @type {function(string, string=):string}
 * @see puppet.pred
 */
var value = puppet.pred('[@value = ', ']');


/**
 * XPath predicate for containment with an arbitrary attribute.
 *
 * @param {string} key Key of the attribute.
 * @param {string} value Value of the attribute.
 * @param {string} opt_path XPath to search under, relative to current path.
 * @return {string} XPath.
 */
function contains(key, value, opt_path) {
  // TODO(rdub): for some reason the JS compiler complains about
  // chaining the two function calls together here, but doesn't mind
  // it in the next function (equals). Figure out why.
  var pred = puppet.pred('[contains(' + key + ', ', ')]');
  return pred(value, opt_path);
}


/**
 * XPath predicate for an arbitrary attribute.
 *
 * @param {string} key Key of the attribute.
 * @param {string} value Value of the attribute.
 * @param {string} opt_path XPath to search under, relative to current path.
 * @return {string} XPath.
 */
function equals(key, value, opt_path) {
  return puppet.pred('[' + key + ' = ', ']')(value, opt_path);
}


//-- Control flow.

/**
 * If command execution is paused.
 *
 * @private
 * @type {boolean}
 */
puppet.paused_ = false;


/**
 * The hash search string for synchronizing two tests in two.html.
 *
 * @private
 * @type {number}
 */
puppet.hash_ = 0;


/**
 * Starts execution of commands.
 */
puppet.start = function() {
  // Must copy and store the hash value, instead of modifying the hash
  // value, because there is no locking between the test and two.html
  // and both can modify at the same time.
  var hash = location.hash.substr(1) || 0;
  puppet.steps_ += hash - puppet.hash_;
  puppet.hash_ = hash;

  var next = puppet.ready_ && puppet.queued_ > 0 && puppet.batch_;
  var step = !puppet.step_ || puppet.steps_ > 0;
  if (!puppet.paused_ && next && !step) {
    puppet.paused_ = true;
    puppet.echo("Paused; click 'continue' (press c) " +
        "or 'step' (press s/S) to resume.");
  }

  // The execution order of onload handlers on different documents is
  // not guaranteed: The onload handler in this file on the document
  // of the control iframe may be executed before the onload handler
  // in the test file on the main document; that is, this function may
  // be called before any command has been queued. Hence the checking
  // of puppet.queued_; otherwise, a test can pass trivially.
  if (next && step) {
    puppet.paused_ = false;
    puppet.steps_--;
    try {
      puppet.execute(puppet.commands_.shift());
    } catch (e) {
      if (!document) return;  // see puppet.done_()
/*
      var stack = puppet.trim_(e.stack || '');
      var message = 'Error: ' + (e.message || e) + stack;
      puppet.done_(message);
      throw e;  // Rethrow the same exception.
*/
      puppet.done_('');
    }
  // Wait for network and js evaluation.
  } else puppet.setTimeout_(puppet.start, 200);
};


/**
 * Execute a command.
 *
 * If the command is a string, use eval(); if it is a function, use
 * Function.apply with arguments; or, if it is an array, recursively
 * call puppet.execute() with each element inside the array.
 *
 * @param {Array} command command to be executed.
 */
puppet.execute = function(command) {

  if (command) {
    var func = command.shift();
    assertNotEq('undefined', typeof func, 'undefined function');
    var args = command;
    if (typeof func == 'string') {
      puppet.echo('- ' + func);
      puppet.eval_(func);
    } else if (func && func instanceof Array) {
      for (var i = func.length - 1; i >= 0; i--) {
        var command2 = puppet.copy_(args);
        command2.unshift(func[i]);
        // Append #i, showing the index of the compound command.
        command2.caller_ = command.caller_ ? command.caller_ + ' #' + i : '';
        puppet.commands_.unshift(command2);
      }
    } else if (func instanceof Function) {
      var caller = command.caller_ || '';
      if (caller == '' || puppet.call_) {
        if (puppet.call_) caller += '\n';
        caller += ': ' + puppet.str_(func) + '(' + puppet.str_(args) + ')';
      }
      var time = puppet.clock_ ? ' #' + puppet.time_() : '';
      puppet.echo(caller + time);
      if (!puppet.call_ && puppet.callx_) {
        puppet.dump(': ' + puppet.str_(func) + '(' + puppet.str_(args) + ')');
      }
      func.apply(null, args);
    } else assert(false, 'bad type: ' + func + ': ' + typeof func);

    // Execute next command.
    puppet.setTimeout_(puppet.start, puppet.delay_ * 1000);

  } else {
    // NOTE(stse): use the timer in the main frame (instead of calling
    // done() directly or use the timer in the control frame) so that
    // firebug will block the time out during debugger's breakpoint to
    // allow more puppet commands from run().
    window.setTimeout(function() { puppet.done_(); }, 0);

    // Wait for user to add new commands via run(), unless the this
    // test is run via the multi-test runner in which case no new
    // commands should be taken.
    //
    // Note that:
    // 1. To use debugger breakpoints in Firebug, puppet.start() must
    //   be continuously called below because new commands can be
    //   added via stepping through run() commands.
    // 2. To conserve thread resources in IE when using multi-test
    //   runner, puppet.start() must _not_ be called after a test is
    //   done to avoid busy-waiting when a test window is not properly
    //   closed.
    if (!puppet.multirun_) {
      puppet.setTimeout_(puppet.start, 200);
    }
  }
};


/**
 * Last message from puppet.done() for the callback puppet.free().
 *
 * @type {string|undefined}.
 */
puppet.doneMessage_;


/**
 * Finalization function to finish testing.
 *
 * To be overriden for customization.
 *
 * @param {Function} func The default finalization function.
 */
puppet.done = function(func) {
  func();
};


/**
 * Finishes execution of commands.
 *
 * @param {string} opt_message A summary message to be displayed as
 * the test has failed.
 * @private
 */
puppet.done_ = function(opt_message) {
  if (!puppet.batch_) return;
  puppet.batch_ = false;
  puppet.doneMessage_ = opt_message;
  for (var i = 0; i < puppet.ondone.length; i++) puppet.ondone[i]();
  puppet.done(puppet.done2_);
};


/**
 * Helper to finish execution of commands.
 *
 * @private
 */
puppet.done2_ = function() {
  var passed = typeof puppet.doneMessage_ == 'undefined';
  var result = passed ? 'passed' : 'failed';

  // Avoid multiple errors from puppet.doneMessage_ and checking puppet.dialog_.
  if (passed) puppet.dialog_();

  if (puppet.doneMessage_) puppet.echo(puppet.doneMessage_);
  var color = passed ? 'palegreen' : 'pink';
  puppet.status_(result, color);

  // The current window may already be closed by the multi-test runner
  // puppet/run.html via puppet.status_. The object 'document',
  // not 'window', becomes undefined after window.close() is called.
  // Continuing the rest of the function will generate errors such as
  // 'puppet' is undefined or native component exceptions when calling
  // window.close() again.
  if (!document) return;

  // For Selenium farm.
  var elem = document.createElement('div');
  // Do not use 'result' as the DOM identifier: the identifier is
  // already used by 'Error console' in Safari. The append operation
  // itself succeeds but any subsequent Javascript evaluation in
  // 'Error console' will return 'undefined'.
  // Do not use innerHTML as getText() of a hidden element is deprecated in
  // Selenium.
  // FIXME(meghnasharma): set attribute on /html instead.
  elem.id = 'puppet.result';
  elem.setAttribute('result', result);
  elem.style.display = 'none';
  if (document.body) document.body.appendChild(elem);

  // Must call puppet.close_() via a timer so that DOM updates due to
  // puppet.status_() are finished before saving a screenshot via XHR
  // with puppet.save_().
  window.setTimeout(function() { puppet.close_(result); }, 0);
};


/**
 * Saves a screenshot and closes window.
 *
 * @private
 * @param {string} result 'passed' or 'failed'.
 */
puppet.close_ = function(result) {
  if (result == 'failed') puppet.save_();
  if (/[?&]close=0\b/.test(location.search)) return;
  var close_pass = /[?&]close=pass\b/.test(location.search);
  var close_all = /[?&](close$|close[^=])/.test(location.search);
  if (close_all || close_pass && result == 'passed') self.close();
};


/**
 * Clears a cookie.
 *
 * For example, puppet.clear('SID=; domain=google.com; path=/').
 *
 * @param {string} cookie Cookie specification.
 */
puppet.clear = function(cookie) {
  // IE does not support 'max-age'.
  var expires = '; expires=' + new Date(0).toGMTString();
  document.cookie = cookie + '; max-age=0' + expires;
};


//-- Utilities.


/**
 * Defines recursive objects.
 *
 * For example,
 *
 *   puppet.define({ x: 1 }, function(me) { return { y: me.x + 2 };})
 *
 * gives { x: 1, y: 3 }
 *
 * @param {Object} x An initial object.
 * @param {*} var_args Variable-length arguments: initialization
 *   functions that take the base object and returns an extended object.
 * @return {Object} The recursively defined object.
 */
puppet.define = function(x, var_args) {
  for (var i = 1; i < arguments.length; i++) {
    var y = arguments[i](x);
    for (var key in y) x[key] = y[key];
  }
  return x;
};


/**
 * Suppresses prompt/confirm/alert dialog boxes, and sets the next
 * predefined response.
 *
 * Puppet checks at the end of the test if all dialogs have been
 * displayed; see puppet.dialog_().
 *
 * @param {string|boolean|null} response Return value of the dialog box.
 * @param {string} opt_content Expected dialog content.
 */
function dialog(response, opt_content) {
  if (typeof response == 'string') {
    puppet.prompts_.push(response);
  } else if (typeof response == 'boolean') {
    puppet.confirms_.push(response);
  } else {
    puppet.alerts_++;
  }
}


/**
 * The property name of the text content or the inner text of an
 * element.
 *
 * @type {string}
 */
puppet.text = (puppet.firefox || puppet.webkit) ? 'textContent' : 'innerText';


/**
 * Gets the text content or the inner text of an element.
 *
 * @param {string} path XPath of the target element.
 * @return {string} Text content.
 */
puppet.get = function(path) {
  return puppet.elem(path)[puppet.text];
};


/**
 * Gets the specified attribute of an element.
 *
 * @param {string} path XPath of the target element.
 * @param {string} attr The desired attribute name.
 * @return {string} Attribute value.
 */
puppet.attr = function(path, attr) {
  return puppet.elem(path).getAttribute(attr);
};


/**
 * Checks if all dialogs have been displayed unless ?dialog is in the
 * URL.
 *
 * @private
 */
puppet.dialog_ = function() {
  if (/[?&]dialog\b/.exec(location.search)) return;
  assertEq(0, puppet.prompts_.length,
      'Some prompt dialogs did not display: ' + puppet.str_(puppet.prompts_));
  assertEq(0, puppet.confirms_.length,
      'Some confirm dialogs did not display: ' + puppet.str_(puppet.confirms_));
  assertEq(0, puppet.alerts_,
      'Some alert dialogs did not display: ' + puppet.alerts_);
};


/**
 * Adds search parametrers to URL, separated either by ? or &.
 *
 * @private
 * @param {string} url The base URL.
 * @param {string} params The additional search parametrers.
 * @return {string} URL appended with the search parameters.
 */
puppet.add_ = function(url, params) {
  return url + (url.indexOf('?') > 0 ? '&' : '?') + params;
};


/**
 * Echos a debug string to the commonad log and Firebug console.
 *
 * It also echos in the standard output of the Unix terminal for
 * Firefox if window.dump is enabled in about:config.
 *
 * @param {string} x anything.
 * @param {string} opt_html Input x in HTML.
 */
puppet.echo = function(x, opt_html) {
  var str = String(x);
  var html = opt_html ||
      str.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  puppet.dump(str);
  // Preserve \n for the IE's output from the Selenium farm.
  // Do not use extra newlines for Firefox 2.
  // Do not use <br> for non-IE for getElementById('log2')[puppet.text].
  var newline = puppet.explorer ? '\n<br>' : '\n';
  puppet.html_ += html.replace(/\n/g, newline) + newline;
  if (puppet.log_) puppet.log_.innerHTML = puppet.html_;
  // Must use 'window.console', not just 'console', for Firebug 1.3+.
  if (window.console) window.console.log(str);
};


/**
 * Echos in the standard output of the Unix terminal for Firefox if
 * window.dump is enabled in about:config.
 *
 * @param {string} x anything.
 */
puppet.dump = function(x) {
  if (window.dump) window.dump(x + '\n');
};


/**
 * Gets search parameters from the test URL (the main page as in
 * document.location) to the load URL (the new page to be loaded
 * inside the test iframe).
 *
 * Currently, 'deb', 'e', 'expid', and 'hl' are passed.
 *
 * @param {string} url The load URL.
 * @return {string} The URL with additional search parameters.
 */
puppet.searchParams = function(url) {
  var params = [
    'deb',  // debug level
    'e',  // labrat experiment
    'expid',  // labrat experiment id
    'hl'  // human language
  ];
  var url2 = url;
  for (var i = 0; i < params.length; i++) {
    var regexp = RegExp('[?&]' + params[i] + '=([^?&]+)');
    var value = puppet.str(regexp, location.search);
    // HACK(stse): e.g. use ?deb=j2slow for both ?deb=j2 and ?deb=slow.
    if (value && params[i] == 'deb' && /[^?]deb=slow\b/.test(url)) {
      url2 = puppet.add_(url2, params[i] + '=' + value + 'slow');
      url2 = url2.replace(/[^?]deb=slow\b/, '');
    } else if (value) {
      url2 = puppet.add_(url2, params[i] + '=' + value);
    }
  }
  return url2;
};


/**
 * Shorthand for puppet.echo.
 *
 * Use the shorthand only for interactive debugging, but not in the test.
 *
 * @type {Function}.
 */
var o = puppet.echo;


/**
 * Gets the effective style of an element.
 *
 * @param {Element} elem the target element.
 * @return {Object} style mapping.
 */
puppet.style = function(elem) {
  if (!elem) return {};
  var value = puppet.explorer ?
      elem.currentStyle :
      puppet.window().getComputedStyle(elem, null);
  return value == 'inherit' ? puppet.style(elem.parentNode) : value;
};


/**
 * Returns normalized opacity of an element.
 *
 * @param {string} path XPath of target element.
 * @return {number} Numerical opacity value in range [0-1].
 */
puppet.opacity = function(path) {
  return puppet.explorer ?
      Number(puppet.str(/\(opacity=([0-9]+)\)/,
      puppet.elem(path).style.filter)) / 100 :
      Number(puppet.style(puppet.elem(path))['opacity']);
};


/**
 * Matches value with a string.
 *
 * If the pattern is a string, use '==='; or, if it is a regular
 * expression, use RegExp.test().
 *
 * @param {string|RegExp} pattern pattern.
 * @param {string} value value.
 * @return {boolean} if matching.
 */
puppet.match = function(pattern, value) {
  return pattern instanceof RegExp ?
      pattern.test(value) :
      pattern === value;
};


/**
 * Gets the content document being tested.
 *
 * @return {Element} content document.
 */
puppet.document = function() {
  return puppet.window().document;
};


/**
 * Gets the content window being tested.
 *
 * @return {Element} content window.
 */
puppet.window = function() {
  return puppet.iframe_ ?
    (puppet.content_ ? puppet.content_.contentWindow : null) :
    window;
};


/**
 * Converts anything to string with showing functions by names not
 * definitions and showing strings with enclosing quotes.
 *
 * @private
 * @param {Function|Array|string|Object} x anything.
 * @return {string} representation.
 */
puppet.str_ = function(x) {
  if (x instanceof Function) {
    if (x.name) return x.name;  // if not anonymous functions
    if (x._name) return x._name;  // if manually named functions (see main.js)

    var str = String(x);
    var name2 = puppet.str(/^function ([a-zA-Z_]+)\(/, str);
    if (name2) return name2;  // named functions in IE

    // Webkit does not take 'g' (global replacement) as the third argument.
    var code = str.replace(/\n/g, '')  // make it one-line
        .replace(/    /g, ' ');  // delete indentation (4 spaces in firefox)

    // Use ellipse ... for long functions.
    return code.length < 50 ? code : code.substr(0, 50) + ' ...}';

  } else if (x && x instanceof Array) {
    var str = '';  // join via puppet.str_() with commas
    for (var i = 0; i < x.length - 1; i++) str += puppet.str_(x[i]) + ', ';
    if (x.length > 0) str += puppet.str_(x[x.length - 1]);
    return str;

  } else if (typeof x == 'string') {
    return '\'' + x + '\'';
  } else return String(x);
};


/**
 * Copies an array from a starting index.
 *
 * @private
 * @param {Array} x array.
 * @param {number} opt_from Starting index; default is 0.
 * @return {Array} copy.
 */
puppet.copy_ = function(x, opt_from){
  var from = opt_from || 0;
  var y = [];
  for (var i = 0; i < x.length - from; i++) y[i] = x[from + i];
  return y;
};


/**
 * Gets the current stack trace.
 *
 * To test: try { throw new Error(); } catch (e) { alert(e.stack) }
 *
 * @private
 * @param {boolean} opt_notrim Do not trim url prefix.
 * @return {string} stack trace.
 */
puppet.stack_ = function(opt_notrim) {
  if (puppet.firefox) {
    try {
      throw new Error();
    } catch (e) {
      var stack = e.stack
          .replace(/.*\n.*\n/, '')  // delete trace of puppet.stack_()
          .replace(/@:0/g, '');  // delete junk line info
      return opt_notrim ? stack : puppet.trim_(stack);
    }
  } else return '';  // IE and Webkit does not support stack trace.
};


/**
 * If an element is a member of an array.
 *
 * Using === for equality test so that 0 is not a member of [''].
 *
 * @private
 * @param {*} x Element.
 * @param {Array} s Array.
 * @return {boolean} If member.
 */
puppet.member_ = function(x, s) {
  for (var i = 0; i < s.length; i++)
    if (s[i] === x) return true;
  return false;
};


/**
 * Gets the caller's source code.
 *
 * @private
 * @return {Object|undefined}
 *   {number} line Line number.
 *   {string} code Source code.
 */
puppet.caller_ = function() {
  // IE and Safari do not export stack traces or line numbers in 'Error'.
  if (!puppet.firefox) return;

  var lines = puppet.stack_(true).split('\n');
  // The last stack frames, minus trash trailing whitelines in stack trace.
  var whitelines = /^2/.test(puppet.firefox) ? 3 : 2;
  var info;
  for (var l = lines.length-1; l >= 0; l--) {
    if (lines[l].match("@")) {
      info = lines[l].split('@')[1];
      break;
    }
  }

  var url = info.substr(0, info.lastIndexOf(':'))
  // Line number and array index are off by one.
  var index = Number(info.substr(info.lastIndexOf(':') + 1) - 1);
  var source = puppet.source_(url);

  // In Firefox, 'index' is the last line of the multiple lines of
  // the source; print all previous lines until the line without
  // indentation of more than three or more spaces. Never use tabs.
  //
  // TODO(stse): print the whole html and highlight the current
  // line, making the context of preceding line or proceeding lines
  // clear.
  var code = '';

  // function() {...} is a special case where its first line is reported.
  for (var i = index + 1; i < source.length; ++i) {
    if (!/^   /.test(source[i])) break;
    code += source[i].replace(/^ */, '') + ' ';
  }
  for (; index >= 0; --index) {
    if (!source[index]) continue;
    code = source[index].replace(/^ */, '') + ' ' + code;
    if (!/^   /.test(source[index])) break;
  }
  return { line: index + 1, code: code };
};


/**
 * Evaluates a predicate.
 *
 * If the type of the predicate is a function, then the predicate will
 * be called with no arguments and its return value will be used;
 * otherwise, the value is the predicate evaluated in the Boolean context
 * using double-negation '!!'.
 *
 * @private
 * @param {Object} pred Predicate.
 * @param {*} var_args Variable-length arguments.
 * @return {boolean} If satisfied.
 */
puppet.eval_ = function(pred, var_args) {
  var args = puppet.copy_(arguments, 1);
  return pred instanceof Function ? pred.apply(null, args) : pred;
};


/**
 * Gets the elapsed seconds since the loading of the document.
 *
 * @private
 * @return {string} the elapsed seconds.
 */
puppet.time_ = function() {
  function pad(x) { return ('' + x).length < 2 ? '0' + x : '' + x; }
  var now = new Date;
  var hour = pad(now.getHours());
  var min = pad(now.getMinutes());
  var sec = pad(now.getSeconds());
  var elapsed = (now - puppet.start_) / 1000.0;
  return hour + ':' + min + ':' + sec + ' (' + elapsed + 's)';
};


/**
 * Sends a string to the standard output via /echoz of the proxy if
 * ?send is in the URL parameter.
 *
 * @private
 * @param {string} x anything.
 */
puppet.send_ = function(x) {
  if (!/[?&]send\b/.test(location.search)) return;
  puppet.request('/echoz', 'POST', x);
};


/**
 * Hook to save the status or the screenshot of failed tests.
 *
 * To be overriden for customization.
 *
 * @private
 */
puppet.save_ = function() {};


/**
 * Updates the status of the test.
 *
 * @private
 * @param {string} result 'passed' or 'failed'.
 * @param {string?} color background color.
 */
puppet.status_ = function(result, color) {
  // Display timestamps for the message status of the multitest runner.
  var message2 = result + ' #' + puppet.time_();
  puppet.echo('== ' + message2);

  if (puppet.log_) puppet.log_.style.backgroundColor = color;
  puppet.send_(puppet.name() + ': ' + message2);

  // The function self.opener.runner.status() is accessible only if the
  // current page is opened by puppet/run.html. In particular,
  // Selenium runner (via Selenium farm) defines self.opener but not
  // self.opener.runner nor self.opener.runner.status(). Verify with
  // with running the test in Selenium farm.
  var access = false;
  try {
    // Check for the presence of self.opener.runner to avoid js
    // errors, if possible, in Firebug with break-on-all-errors turned
    // on. Other than this way of accessing the variable in a
    // try-catch block, there is no other way to check if
    // runner.status is accessible due to security restriction.
    if (self.opener && self.opener.runner) {
      access = self.opener.runner.status;
    }
  } catch (e) {}
  // The function self.opener.runner.status() is called outside the
  // try-catch statement above so that actual errors during invocation
  // will not be thrown away.
  if (access) {
    self.opener.runner.status(
        location.pathname, message2, color, !puppet.multirun_);
  }
};


/**
 * Loads and evaluates a Javascript file synchronously in the same domain.
 *
 * The loading is synchronous for simplifying the order of
 * initializations.
 *
 * See puppet.call() for asynchronous loading in possiblly a different
 * domain.
 *
 * @param {string} path The source of the Javascript file in the same
 * domain.
 */
puppet.load = function(path) {
  // Browser quirks:
  // - window.execScript(content) also works for but only for IE.
  // - window.eval(content) also works for but only for Firefox.
  // - eval(content) does not work because evaluation happens in local
  //   scope.
  // - script.appendChild(document.createTextNode(content)) also works
  //   for Firefox and Webkit, but not IE.
  puppet.dump('== loading: ' + path);
  var script = document.createElement('script');
  script.text = puppet.request(path);
  // Do not use 'head' or 'body' elements, which may not exist yet.
  document.documentElement.firstChild.appendChild(script);
};


/**
 * Loads and evaluates a Javascript file asynchronously in possibly a
 * different domain.
 *
 * The loading is necessarily asynchronous because of the use of
 * <script> tags; especially in IE, the order of execution is not
 * guaranteed.
 *
 * See puppet.load() for synchronous loading in the same domain.
 *
 * IE caches dynamic scripts (even when its cahce policy is set to
 * 'Never'). Setting the HTTP server response header 'Expires' to a
 * specific date in the past solves the problem. See Puppet Allocation
 * server for example. None of the following
 * headers works:
 *
 *  - Cache-Control: no-cache, must-revalidate
 *  - Last-Modified: Mon, 1 Jan 1900 00:00:00 GMT
 *  - Pragma: no-cache
 *  - Expires: 0 or -1
 *
 * 'Expires: 0 or -1' works if the re-querying is a few seconds apart;
 * see puppet/alloc.html for calling puppet.calls() consecutively.
 *
 * Appending a unique junk query string to URL also works but is
 * inelegant.
 *
 * @param {string} url The source of the Javascript file in possibly a
 * different domain.
 */
puppet.call = function(url) {
  puppet.echo('-- calling: ' + url,
      '-- calling: ' + '<a href=' + url + ' target=_blank>' + url + '</a>');
  var script = document.createElement('script');
  script.src = url;
  // Do not use 'head' or 'body' elements, which may not exist yet.
  document.documentElement.firstChild.appendChild(script);
};


/**
 * Makes a GET/POST request via XMLHttpRequest.
 *
 * @param {string} url The target URL.
 * @param {string} opt_type The request type, either 'GET' (default) or 'POST'.
 * @param {string} opt_body The request body.
 * @return {string?} The content if the return code is HTTP 200.
 */
puppet.request = function(url, opt_type, opt_body) {
  var request = window.XMLHttpRequest ?
      new XMLHttpRequest() :
      new ActiveXObject('Microsoft.XMLHTTP');
  request.open(opt_type || 'GET', url, false);

  // IE6 erroneously returns HTTP 200 Found for cached HTTP 404
  // Not-found requests. Neither setting 'Pragma=no-cache' or
  // 'Cache-Control=no-cache' fixes the problem.
  if (/^6/.test(puppet.explorer)) {
    request.setRequestHeader('If-Modified-Since', 0);
  }

  request.send(opt_body || null);
  return ((url.substr(0, 5) == 'file:' && request.status == 0) ||
      request.status == 200) ? request.responseText : null;
};


/**
 * Gets source code.
 *
 * TODO(stse): Use .toSource() (supported in Firefox only).
 * Ref: https://developer.mozilla.org/en/Core_JavaScript_1.5_Reference/\
 * Global_Objects/Object/toSource.
 *
 * @private
 * @param {string} url The target URL.
 * @return {string} The code.
 */
puppet.source_ = function(url) {
  // FIXME(stse): return continuation lines based on indentation.
  var lines = puppet.source_cache_[url];
  if (!lines) {
    lines = puppet.request(url).split('\n');
    puppet.source_cache_[url] = lines;
  }
  return lines;
};


/**
 * Cache for puppet.source_.
 *
 * @private
 * @type {Object} Mapping of URL string to lines of source code.
 */
puppet.source_cache_ = {};


/**
 * If an element is shown and has the property value.
 *
 * See puppet.shown for definitions of visibility.
 *
 * @private
 * @param {string} path XPath of the target element.
 * @param {string} opt_key key of the property.
 * @param {string} opt_value value of the property.
 * @return {boolean} If shown and has the property value.
 */
puppet.check_ = function(path, opt_key, opt_value) {
  // Arguments opt_key and opt_value must be both absent, or both
  // present.
  var key_defined = typeof opt_key == 'undefined';
  var value_defined = typeof opt_value == 'undefined';
  assert(key_defined == value_defined, 'missing argument');
  var elem = puppet.elem(path);
  return !!elem && puppet.shown(elem) &&
      (!opt_key || typeof opt_value == 'undefined' ||
      puppet.match(opt_value, elem[opt_key]));
};


//-- DOM Utilities.

/**
 * Gets an element by id.
 *
 * @param {string} id a unique identifier.
 * @return {Element} the target element.
 */
puppet.id = function(id) {
  return puppet.document().getElementById(id);
};


/**
 * Gets a node by XPath.
 *
 * This function handles xpath expressions across iframes by requiring
 * explicit '/content' annotations and evaluating trailing paths in the
 * the iframe's document. For example, 'foo/content/bar' will get the
 * iframe element 'foo', then get the element 'bar' inside the
 * document of 'foo'.
 *
 * Do not use /iframe as /iframe itself is a valid xpath expression
 * (the child 'iframe' element).
 *
 * @param {string} path a XPath predicate.
 * @param {Window} opt_win The document window.
 * @return {Element} the target element.
 */
puppet.node = function(path, opt_win) {
  assertEq('string', typeof path, 'invalid xpath type: ' + path);
  var win = opt_win || puppet.window();
  var exp = path;
  if (path.indexOf('/content') >= 0) {
    var index1 = path.indexOf('/content');
    var index2 = index1 + '/content'.length;
    if (index2 < path.length) {
      win = puppet.element(path.substr(0, index1)).contentWindow;
      exp = path.substr(index2);
    }
  }

  // Calling install() on demand for new documents from commands like
  // load() or click(), or for documents inside iframes from extended
  // xpath expressions with '/content'.
  if (!win.document.evaluate) window.install(win);
  assert(!!win.document.evaluate, 'missing xpath library');

  // 0 = XPathResult.ANY_TYPE
  return win.document.evaluate(exp, win.document, puppet.resolver_, 0, null);
};


/**
 * Flashes/highlight the element in action.
 *
 * The highlight may not be cleared properly if the element is copied
 * during highlight such as during infowindow resizing.
 *
 * @param {Element} elem The target element.
 */
puppet.flash = function(elem) {
  // Guard against re-entrance before the original color is restored;
  // otherwise subsequent calls of puppet.flash on the same element
  // will get the highlight color (red) if the flash is not yet
  // over.
  //
  // Use a separate variable elem.puppetFlashing_ instead of checking
  // elem.puppetColor_ as its value may be undefined or the empty
  // string. For some unknown reason, 'delete elem.puppetColor_' does
  // not work in IE inside the function below for resetting.
  //
  // Verify with a test that accesses the same element twice and
  // with a long flash delay, say ?flash=5.
  if (!puppet.batch_ || puppet.flash_ == 0 || elem.puppetFlashing_) return;
  // We check this because, e.g., the root element does not have a style.
  if (!elem || !elem.style) return;
  var color = elem.style.backgroundColor;
  elem.puppetColor_ = puppet.style(elem).backgroundColor; // for background()
  elem.puppetFlashing_ = true;
  elem.style.backgroundColor = 'red';  // highlight
  window.setTimeout(function() {
    // In IE, resetting the element after a new document is loaded
    // causes 'Permission denied' exception. Ignore the exception.
    try {
       // Restore the toplevel property 'backgroundColor' (which possibly
       // is undefined or the empty string), not the computed color
       // 'elem.puppetColor_'.
       elem.style.backgroundColor = color;
       elem.puppetFlashing_ = false;
    } catch (e) {}
  }, puppet.flash_ * 1000);
};


/**
 * Gets the first element by an XPath expression.
 *
 * @param {string} path a XPath predicate.
 * @return {Element} the target element.
 */
puppet.elem = function(path) {
  var elem = puppet.node(path).iterateNext();
  if (elem) puppet.flash(elem);
  return elem;
};


/**
 * Shorthand for puppet.elem.
 *
 * Use the shorthand only for interactive debugging, but not in the test.
 *
 * @type {Function}.
 */
var e = puppet.elem;


/**
 * Gets an element by XPath and aborts if null.
 *
 * @param {string} path a XPath predicate.
 * @return {Element} the target element.
 */
puppet.element = function(path) {
  var x = puppet.elem(path);
  assert(x !== null, 'missing element');
  return x;
};


/**
 * Gets all elements by an XPath expression.
 *
 * @param {string} path a XPath predicate.
 * @return {Array} the target element.
 */
puppet.elems = function(path) {
  var node = puppet.node(path);
  var list = [];
  while (true) {
    var x = node.iterateNext();

    // Firefox/Safari uses 'null' while xpath.js (for IE) uses
    // 'undefined' to indicate the end of iteration.
    if (!x) break;

    list.push(x);
  }
  return list;
};


/**
 * Gets the count of all elements by XPath.
 *
 * @param {string} path a XPath predicate.
 * @return {Element} the target element.
 */
puppet.count = function(path) {
  return puppet.node('count(' + path + ')').numberValue;
};


/**
 * Dispatches a keyboard event to an element.
 *
 * No action if the element is null (to make it easier to trigger
 * multiple mouse events in sequence).
 *
 * @private
 * @param {string} path XPath of the target element.
 * @param {string} type event type.
 * @param {number} key_code key code.
 * @param {number} char_code character code.
 * @see http://unixpapa.com/js/key.html.
 */
puppet.key_ = function(path, type, key_code, char_code) {
  var elem = puppet.elem(path);
  if (!elem) return;

  if (puppet.firefox) {
    var event = document.createEvent('KeyboardEvent');
    event.initKeyEvent(type, true, true, window,
        false, false, false, false, key_code, char_code);
    elem.dispatchEvent(event);
  } else if (puppet.webkit) {
    var event = document.createEvent('Events');  // not 'UIEvents'
    event.initEvent(type, true, true, window, 1);  // not initUIEvent()
    event.charCode = char_code;
    event.keyCode = key_code;
    elem.dispatchEvent(event);
  } else {  // Assume puppet.explorer.
    var event = document.createEventObject();
    event.keyCode = key_code;
    // IE does not support charCode.
    elem.fireEvent('on' + type, event);
  }
};


/**
 * Gets the effective offset from the left of an element.
 *
 * @param {Element} elem the target element.
 * @return {number} offset.
 */
puppet.left = function(elem) {
  return elem ? elem.offsetLeft + puppet.left(elem.offsetParent) : 0;
};


/**
 * Gets the effective offset from the top of an element.
 *
 * @param {Element} elem the target element.
 * @return {number} offset.
 */
puppet.top = function(elem) {
  return elem ? elem.offsetTop + puppet.top(elem.offsetParent) : 0;
};


/**
 * Gets the effective property of an element.
 *
 * @param {Element} elem element.
 * @param {string} key key of the property.
 * @return {Object?} the effective value, or null if not found.
 */
puppet.effective = function(elem, key) {
  if (!elem) return null;
  return elem[key] ? elem[key] : puppet.effective(elem.parentNode, key);
};


/**
 * Resize the content iframe window to a given width.
 *
 * @param {string} width width of the window (e.g. 800px or 100%).
 */
puppet.resizeWidth = function(width) {
  puppet.content_.width = width;
};


/**
 * Gets the pixel size of the content iframe.
 *
 * @return {number} The pixel size of the content iframe.
 */
puppet.width = function() {
  return puppet.content_.offsetWidth;
};


/**
 * Resize the content iframe window to a given height.
 *
 * @param {string} height height of the window (e.g. 800px or 100%).
 */
puppet.resizeHeight = function(height) {
  puppet.content_.height = height;
};


/**
 * If an element is effectively shown, according to its
 * inherited visibility/display style or its input field's type.
 *
 * Definitions of visibility: An element is visible if the visibility
 * property of its effective style is not hidden and if the element is
 * not a hidden input field (see puppet.visible). An element is
 * displayed if the display property of its effective style is not
 * none and its parent node is also displayed (see
 * puppet.displayed). An element is shown if it is visible and
 * displayed (see puppet.shown).
 *
 * Note that the infowindow or the markers of the map's viewport may
 * be visible but not displayed when the browser window is small. Use
 * visible, not shown, in your tests for those cases.
 *
 * @param {Element} elem Element.
 * @return {boolean} If effectively shown.
 */
puppet.shown = function(elem) {
  return puppet.visible(elem) && puppet.displayed(elem);
};


/**
 * If an element is effectively visible, according to its
 * inherited visibility style or its input field's type.
 *
 * See puppet.shown for definitions of visibility.
 *
 * @param {Element} elem Element.
 * @return {boolean} If effectively visible.
 */
puppet.visible = function(elem) {
  return puppet.style(elem).visibility != 'hidden' && (
      elem.tagName.toLowerCase() != 'input' ||
      elem.type.toLowerCase() != 'hidden');
};


/**
 * If an element is effectively displayed.
 *
 * See puppet.shown for definitions of visibility.
 *
 * @param {Element} elem element.
 * @return {boolean} if effectively displayed.
 */
puppet.displayed = function(elem) {
  if (!elem || !elem.style) return true;
  return puppet.style(elem).display != 'none' &&
      puppet.displayed(elem.parentNode);
};


/**
 * Adds an event listener for 'load'.
 *
 * Must use addEventListener('load', ...) instead of setting
 * 'window.onload' for firebug's debugger to work properly.
 *
 * See 'Simple Breakpoint' in puppet/debugger.html.
 *
 * @private
 * @param {Element} elem element to be listened on.
 * @param {Function} func event handler.
 */
puppet.addOnLoad_ = function(elem, func) {
  puppet.firefox || puppet.webkit ?
      elem.addEventListener('load', func, false) :
      elem.attachEvent('onload', func);
};


/**
 * Project-specific menu.
 *
 * @type {Array}
 */
puppet.menu = [];


/**
 * Sets timeout with the control iframe or the main window.
 *
 * @private
 * @param {Function} func Callback function.
 * @param {number} seconds Number of seconds to wait for.
 * @return {number} Timer id.
 */
puppet.setTimeout_ = function(func, seconds) {
  var win = puppet.control_ ? puppet.control_.contentWindow : window;
  return win.setTimeout(func, seconds);
};


/**
 * Sets responses of dialog boxes unless ?dialog is in the URL.
 *
 * @private
 */
puppet.setDialog_ = function() {
  if (/[?&]dialog\b/.exec(location.search)) return;

  // There are no other way to access window.{confirm,prompt,alert} if
  // there is only one window.
  if (puppet.window() == window) return;

  puppet.window().confirm = function(x) {
    if (!puppet.batch_) return window.confirm(x);
    assert(puppet.confirms_.length > 0,
        'Unexpected confirmation dialog box; use dialog().');
    return puppet.confirms_.shift();
  };
  puppet.window().prompt = function(x) {
    if (!puppet.batch_) return window.prompt(x);
    assert(puppet.prompts_.length > 0,
        'Unexpected prompt dialog box; use dialog().');
    return puppet.prompts_.shift();
  };
  puppet.window().alert = function(x) {
    if (!puppet.batch_) return window.alert(x);
    assert(puppet.alerts_ > 0,
        'Unexpected alert dialog box; use dialog().');
    puppet.alerts_--;
  };
  puppet.window().print = function() {};  // disable printing
};


/**
 * Steps through a number of commands if the test is running, or
 * restart the test if the test has finished.
 *
 * @param {number} count The number of steps.
 */
puppet.step = function(count) {
  // If the test is under progress (puppet.batch_) and not waiting for
  // some condition (puppet.ready_), then switch to stepping mode and
  // keep the URL. This allows switching to stepping mode in the
  // middle of a test without restarting the whole test.
  if (puppet.batch_ && puppet.ready_) {
    puppet.step_ = true;
    puppet.steps_ = count;
  } else if (!puppet.step_) {
    location.href = puppet.add_(location.href.replace(/[?&]+step/, ''), 'step');
  }
};


/**
 * Pauses the test for interactive stepping.
 */
function pause() {
  puppet.step_ = true;
}


/**
 * Resets to no stepping nor delay.
 */
puppet.reset = function() {
  location.href = location.href
      .replace(/[?&]+step/, '')
      .replace(/[?&]+cmd/, '')
      .replace(/[?&]+line/, '')
      .replace(/[?&]+delay=[0-9]+/, '');
};


/**
 * Loads Firebug lite.
 */
puppet.firebug = function() {
  if (window.firebug) return;
  var script = document.createElement('script');
  // TODO(stse): Check http://getfirebug.com/releases/lite for the
  // latest version.
  script.setAttribute('src',
      'http://getfirebug.com/releases/lite/1.2/firebug-lite-compressed.js');
  document.body.appendChild(script);

  // Firebug lite requires the 'head' and the 'body' elements, which
  // are inserted above, if missing.
  (function() {
    if (window.firebug && window.firebug.init) window.firebug.init();
    else window.setTimeout(arguments.callee); })();
};


/**
 * Converts an array of links to HTML menu.
 *
 * @private
 * @param {Array} links Menu links.
 * @return {string} Menu in html.
 */
puppet.menu_ = function(links) {
  var html = '';
  for (var i = 0; i < links.length; ++i) {
    html += i == 0 ? '[' : '';
    html += '<a title="' + links[i].title + '"';
    html += ' href=' + links[i].href;
    if (links[i].target) html += ' target=_blank';
    html += '>' + links[i].text + '</a>';
    html += i < links.length - 1 ? ' | ' : ']';
  }
  return html;
};


/**
 * Regular expresion of the URL to be trimmed.
 *
 * To be overriden for customization.
 *
 * @type {RegExp}
 */
puppet.trimURL = RegExp();


/**
 * Trims paths about directory prefix, protocol and host, or query
 * parameters of an URL.
 *
 * For example, return puppet/basic/basic.html for
 * http://google.com:6342/puppet/basic/basic.html?time=10,
 *
 * or, return puppet/basic/basic.html:10 for
 * http://google.com:9099/$trimPrefix/puppet/basic/basic.html?close
 *
 * or, return assert(false)@puppet/puppet.js:493 for
 * assert(false)@http://google.com:9099/puppet/puppet.js:493
 * ([object Array])@http://google.com:9099/puppet/puppet.js:695
 *
 * @private
 * @param {string} url the original URL.
 * @return {string} the trimmed URL.
 */
puppet.trim_ = function(url) {
  var prefix = document.location.protocol + '//' + document.location.host + '/';
  return url
      .replace(RegExp(prefix, 'g'), '')
      .replace(puppet.trimURL, '')
      .replace(/@/g, ' @')
      .replace(/\?[^:]*/g, '');  // keep line number after colon
};


/**
 * Test name.
 *
 * E.g. puppet/api/basic.html.
 *
 * This is a function, not a constant, for customization of
 * puppet.trimURL in site.js.
 *
 * @return {string} Trimmed test name from URL.
 */
puppet.name = function() { return puppet.trim_(document.URL); };


/**
 * Prefix of the source code link.
 *
 * To be overriden for customization.
 *
 * @type {string}
 */
puppet.srcPrefix = '';


/**
 * Documentation URL.
 *
 * To be overriden for customization.
 *
 * @type {string}
 */
puppet.doc = 'http://code.google.com/apis/maps';


/**
 * Make the log div and its initial content.
 *
 * @private
 */
puppet.makeLog_ = function() {
  puppet.log_ = document.createElement('div');
  puppet.log_.id = 'log';
  var name = puppet.name().substr(puppet.name().lastIndexOf('/') + 1)
      .replace('.html', '');
  document.title = name + ' - Puppet test: ' + puppet.name();
  var href = document.location.href;

  var html = '<pre>Menu: <a href=' + puppet.doc +
      ' title="Go to the documentation" target=_blank>doc</a>  ';

  html += puppet.menu_([
    { text: 'pause',
      title: 'Pause execution and wait for stepping',
      href: 'javascript:puppet.step_=true;void(0)' },
    { text: 'continue',
      title: 'Continue execution through the rest of commands',
      href: 'javascript:puppet.step_=false;void(0)' },
    { text: 'step',
      title: 'Step through the next command and pause execution, ?step',
      href: 'javascript:puppet.step(1)' },
    { text: 'step 3',
      title: 'Step through the next three commands ' +
          'and pause execution, ?step=3',
      href: 'javascript:puppet.step(3)' },
    { text: 'cmd',
      title: 'Pause at the i-th numbers of commands, ?cmd=1,3',
      href: puppet.add_(href.replace(/[?&]+cmd=[^&]+/, ''), 'cmd=1,3') },
    { text: 'line',
      title: 'Pause at the i-th numbers of source code lines ' +
          '(Firefox only), ?line=10,13',
      href: puppet.add_(href.replace(/[?&]+line=[^&]+/, ''), 'line=10,13') },
    { text: 'delay',
      title: 'Delay for 2 seconds between run() commands, ?delay=2',
      href: puppet.add_(href.replace(/[?&]+delay=[^&]+/, ''), 'delay=2') }]);

  html += '\n  ' + puppet.menu_([
    { text: 'firebug',
      title: 'Firebug lite for debugging, ?firebug',
      href: 'javascript:puppet.firebug()' },
    { text: 'call',
      title: 'Toggle: in Firefox show the evaluated call values ' +
          'of each command, ?call',
      href: puppet.call_ ? href.replace(/[?&]+call/, '') :
          puppet.add_(href, 'call') },
    { text: 'clock',
      title: 'Toggle: show the clock time/the elapsed seconds at each command',
      href: puppet.clock_ ? href.replace(/[?&]+clock/, '') :
          puppet.add_(href, 'clock') },
    { text: 'flash',
      title: 'Flash element in action for 2 seconds (0 to disable), ?flash=2',
      href: puppet.add_(href.replace(/[?&]+flash=[^&]+/, ''), 'flash=2') }]) +
    '\n';

  if (puppet.menu.length > 0) html += '  ' + puppet.menu_(puppet.menu) + '\n';
  html += puppet.html_;  // messages from before puppet.log_ was ready
  var step =
      puppet.firefox || puppet.chrome ? 'Press Control-U in browser' :
      puppet.safari ? 'Press Control-Alt-U in browser' :
      'Open Menu -> View -> Source';  // puppet.explorer
  html += 'Running <a href=' + puppet.srcPrefix +
      puppet.name() + ' target=_blank>' +
      puppet.name() + '</a> (<a href=javascript:alert("' + escape(step) +
      '")>view source</a>)<br>';
  html += '<div id=log2>';  // inner log without menu

  puppet.html_ = html;
  puppet.log_.innerHTML = html;
  document.body.appendChild(puppet.log_);
};


//-- Event handlers.

/**
 * Creates content and control iframes, and starts execution.
 *
 * @private
 */
puppet.init_ = function() {
  // Do not initialize if ?nostart is in the URL, or if the Javascript
  // unit test runner is present, or if the Puppet multi-test runner
  // is present. Check during window.onload (puppet.init_ is called
  // during window.onload) to allow a late definition of
  // window.runner.
  if (puppet.nostart_ || window.runner) return;

  document.body.id = 'puppet';  // for Selenium farm
  if (puppet.firefox) {
    puppet.control_ = document.createElement('iframe');
    puppet.control_.style.display = 'none';
    puppet.addOnLoad_(puppet.control_, puppet.start);
    document.body.appendChild(puppet.control_);
  } else puppet.start();

  puppet.content_ = document.createElement('iframe');
  puppet.content_.width = '100%';
  puppet.content_.height = puppet.height_;
  puppet.content_.style.borderWidth = 1;
  puppet.addOnLoad_(puppet.content_, function() {
    // See the explanation at puppet.url.
    puppet.window().open = function(url) {
      puppet.url = url;
      puppet.echo('-- window.open() is mocked: ' + url,
          '-- window.open() is mocked: <a href=' + url +
          ' target=_blank>' + url + '</a>');
    };
    puppet.initDoc_();
    puppet.setDialog_();
    puppet.ready_ = true;
  });
  document.body.appendChild(puppet.content_);
  // Explicitly clear the iframe to support reloads.  Otherwise, the iframe
  // document will be loaded twice during reloaded.
  // TODO(deboer): Find a reference explaining this behaviour.
  puppet.content_.src = '';
  puppet.makeLog_();

  var seconds = puppet.timeout;
  if (/^7/.test(puppet.explorer)) seconds *= 2;  // slow IE7
  if (/^6/.test(puppet.explorer)) seconds *= 3;  // very slow IE6
  if (seconds > 0) {
    window.setTimeout(function() {
      if (!puppet.step_) {
        puppet.done_('timed out after ' + seconds + ' seconds');
      }
    }, seconds * 1000);
  }

  puppet.status_('loaded', 'cornsilk');
};
puppet.addOnLoad_(window, puppet.init_);


/**
 * Initializes the document for dialogs, Firebug Lite, and onerror events.
 *
 * @private
 * This function will be called again when updating
 * puppet.window().location.href in load() and when submitting form in
 * puppet.submit; hence, skip on subsequent calls.
 */
puppet.initDoc_ = function() {
  if (puppet.window().puppetInit_) return;
  for (var i = 0; i < puppet.oninit.length; i++) puppet.oninit[i]();

  // Must load Firebug Lite inside this onload handler instead of
  // puppet.init(); otherwise, in Firefox with Firebug extension,
  // window.console is defined but not callable. Verify with
  // puppet/api/basic.html?firebug.
  if (puppet.firebug_) puppet.firebug();

  document.onkeypress = function(event) {
    if (puppet.explorer) event = window.event;
    var target = event.target || event.srcElement;

    // Avoid input fields such as Firebug lite.
    if (target != document.documentElement && // in Firefox
      target != document.body) return;  // in Webkit or Internet Explorer

    if (event.altKey || event.ctrlKey) return;
    var code = String.fromCharCode(event.keyCode || event.which);
    switch (code) {
    case 'c': puppet.step_ = false; break;  // c (continiue)
    case 's': puppet.step(1); break;  // s (one step)
    case 'S': puppet.step(3); break;  // S (three steps)
    }
  };

  // Verify with puppet/load.html.
  puppet.window().onerror = function(msg, url, line) {
    // Skip checking 'Error loading script' because clicking to load a
    // new page (such as in textview or mapshop profile) will
    // interrupt script loadings of asynchronous modules. TODO(stse):
    // Disable this check only for clicking or new page loading
    // instead of for all commands.
    if (typeof msg == 'string' && msg.indexOf('Error loading script') == 0) {
      return;
    }
    assert(false, 'error from server: ' + msg + '  @' +
        url + ', line ' + line, false);
  };
  puppet.window().puppetInit_ = true;
};



// Skip setting window.onerror and auto-loading if Javascript unittest
// framework is in place (window.onerror is already set).
if (!window.onerror) {
  /**
   * Stops execution and prints error messages.
   *
   * Safari and Chrome do not support 'window.onerror'.
   *
   * @param {string} msg error message.
   * @param {string} url document URL.
   * @param {string} line line number.
   */
  window.onerror = function(msg, url, line) {
    // Ignore missing scripts from auto-loading (see below).
    if (msg == 'Error loading script' &&
      (url.indexOf('/main.js') > 0 || url.indexOf('/site.js') > 0)) return;
    puppet.ready_ = false;
    var message = 'error from test: ' + msg + '  @' +
        puppet.trim_(url) + ', line ' + line;
    puppet.done_(message);
    throw message;  // Rethrow the same exception.
  };

  // Auto-loading: ../site.js per company domain, ../main.js per
  // project directory, and main.js per feature subdirectory.
//  puppet.load('/history/static/puppet/main_public.js');
}


/**
 * Removes the control frame and thus its associated timer. Otherwise,
 * the browser will not terminate the associated timer that runs
 * puppet.start() and will complain 'puppet' being undefined at the
 * entrance of puppet.start() because its definition in the main
 * document has already been removed.
 *
 * Safari and Chrome do not support 'window.onunload'.
 */
window.onunload = function() {
  // Sometimes Firefox throws unknown errors during document unload.
  try {
    // Skip if document.body is already deleted.
    if (puppet.control_ && document.body) {
      document.body.removeChild(puppet.control_);
    }
  } catch (e) {}

  // Close window to terminate a test early in the multi-test runner.
  // FIXME(stse): conflicts with window.close in run.html.
  // if (puppet.batch_) puppet.done_('window killed');
};


// Safari and Chrome, unlike Firefox or IE, do not automatically
// inserted 'head' and 'body' elements if they are missing. Their
// absence causes Maps API and Firebug Lite, for example, fails to
// initialize elements in the document. Those elements are omitted in
// Puppet tests for convenience and are manually inserted below.
// Verify with api/basic.html and by clicking on 'firebug'.
// - Check for puppet.webkit: IE initializes head/body late.
// - Check for head/body as puppet.js may be included for other runners.

if (puppet.webkit && document.getElementsByTagName('head').length == 0) {
  document.documentElement.insertBefore(
      document.createElement('head'), document.documentElement.firstChild);
}

if (puppet.webkit && !document.body) {
  document.documentElement.appendChild(document.createElement('body'));
}


if (puppet.explorer) {
  /** To export window.install() from xpath.js.
   *
   * @type {Object}
   */
  window.jsxpath = { exportInstaller : true };
  // TODO(stse): Check for updates; the current version is 0.1.11 in 2007.
  // http://coderepos.org/share/wiki/JavaScript-XPath
  puppet.load('/history/static/puppet/xpath.js');
}
