window.pops = [];
window.hashChanges = [];
window.loads = [];
window.events = [];

var ONE = "one.html";
var TWO = "one.html";
var THREE = "one.html";
var AWAY = "one.html";

function lastPop_() {
  return pops[pops.length-1].state;
}

function display_(text) {
  puppet.elems(id("debug"))[0].innerHTML += "<p>" + text;
}

function back_() {
  puppet.window().history.back();
}

function forward_() {
  puppet.window().history.forward();
}

function go_(arg) {
  puppet.window().history.go(arg);
}

function location_(value) {
  try {
    value = new RegExp(value + "$");
    return !!(puppet.window().location.href).match(value);
  } catch(e) {
    return false;
  }
}

function getTestContainer() {
  var opener = window.opener;
  var testContainer = opener ? opener.parent : window.parent;
  if (testContainer != window && testContainer.saveResult) {
    return testContainer;
  }
}

function done() {
  var opener = window.opener;
  if (opener) {
    window.close();
  }
}

function saveResult(key, value) {
  var testContainer = getTestContainer();
  testContainer && testContainer.saveResult(key, value);
  window.DONE=1;
  done();
}

/**
 * Wrap puppet's done_ to ensure we send a beacon on timeout.
 */
if (window.puppet) {
  var done_orig = puppet.done_;
  puppet.done_ = function(msg) {
    if (!window.DONE) {
      saveResult(window.TEST_NAME, 0);
    }
    done_orig.apply(arguments);
  }
}

function assertEq(a, b, opt_comment) {
  if (!(a == b)) {
    puppet.echo(opt_comment);
    puppet.echo("Expected: " + b);
    puppet.echo("Actual: " + a);
    saveResult(TEST_NAME, 0);
    throw(opt_comment);
  }
}

// Override Puppet's assert so we can fail nicely.
function assert(pred, opt_comment) {
  if (!pred) {
    puppet.echo(opt_comment);
    saveResult(TEST_NAME, 0);
    throw(opt_comment);
  }
}
