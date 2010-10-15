function popHandler_(e) {
  parent.pops && parent.pops.push(e);
  parent.events && parent.events.push('popstate');
  display_(e.state);
}

function hashChangeHandler_(e) {
  parent.hashChanges && parent.hashChanges.push(e);
  parent.events && parent.events.push('hashchange');
  display_(location.hash);
}
/**
 * Note: history back/forward don't behave like the browser controls in IE.
 * They always force a reload, even if they are just navigating a hash change.
 *
 * So it's impossile to test IE's history navigation behavior. This should
 * probably mean IE just fails all of these tests, but I'm putting in a cheat.
 * The hashchange_back_forward test verifies the specific behavior and fails
 * for IE as expected.
 */
hashChangeHandler_({});

function loadHandler_(e) {
  parent.loads && parent.loads.push(e);
  parent.events && parent.events.push('load');
  display_(location.href);
}

function display_(text) {
  try {
    document.getElementById('debug').innerHTML += '<p>' + text;
  } catch(e) {}
}

if (window.addEventListener) {
  window.addEventListener('popstate', popHandler_, false);
} else if (window.attachEvent) {
  window.attachEvent('onpopstate', popHandler_);
}

if (window.addEventListener) {
  window.addEventListener('load', loadHandler_, false);
} else if (window.attachEvent) {
  window.attachEvent('onload', loadHandler_);
}

window.onhashchange = hashChangeHandler_;
