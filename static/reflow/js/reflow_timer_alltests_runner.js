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
  for (var i = 0, test; test = ReflowTimer.prototype.unusedTests[i]; i++) {
    allTests.push(test);
  }
  allTests.sort();

  var divEl = document.createElement('div');
  var spanEl = document.createElement('span');
  spanEl.style.marginLeft = '4px';

  var buttonEl = document.createElement('button');
  buttonEl.style.textAlign = 'left';
  buttonEl.style.width = '15em';

  var container = divEl.cloneNode(false);
  var style = container.style;
  style.position = 'absolute';
  style.left = '20px';
  style.top = '20px';
  style.border = '3px solid #333';
  style.padding = '5px 5px 15px 15px';
  style.background = '#eee';
  style.width = '22em';
  style.font = '13px normal Arial, sans';
  style.lineHeight = '1.3';
  style.color = '#111';
  style.textAlign = 'left';
  style.zIndex = '999';
  container.id = 'rt-alltests';

  var header = divEl.cloneNode(false);
  var anchor = document.createElement('a');
  var style = anchor.style;
  style.fontSize = '14px';
  style.fontWeight = 'bold';
  style.textDecoration = 'none';
  style.color = '#333';
  // TODO(elsigh): Insert project name and href here.
  anchor.appendChild(document.createTextNode('Reflow Timer'));
  anchor.target = '_blank';
  anchor.href = '';
  header.appendChild(anchor);
  container.appendChild(header);

  var close = divEl.cloneNode(false);
  close.appendChild(document.createTextNode('close'));
  var style = close.style;
  style.position = 'absolute';
  style.fontSize = '9px';
  style.top = '5px';
  style.right = '5px';
  style.cursor = 'pointer';
  style.color = '#999';
  container.appendChild(close);
  close.onclick = dispose;


  // Stats
  var numElements = document.getElementsByTagName('*').length;
  var rules = goog.cssom.getAllCssStyleRules();
  var numCss = rules.length;
  var ul = document.createElement('ul');
  var style = ul.style
  style.listStyle = 'none';
  style.padding = '0 0 0 1em';
  style.margin = '.2em 0 0 0';

  var li = document.createElement('li');
  li.appendChild(document.createTextNode('#Elements: ' + numElements));
  ul.appendChild(li);

  var li = document.createElement('li');
  li.appendChild(document.createTextNode('#CSS: ' + numCss));
  ul.appendChild(li);

  var li = document.createElement('li');
  li.appendChild(document.createTextNode('Avg Depth: X (min x, max x)'));
  ul.appendChild(li);


  var li = document.createElement('li');
  var reflowElLabel = document.createElement('label');
  reflowElLabel.setAttribute('for', 'bs-el-id');
  reflowElLabel.appendChild(document.createTextNode('ID:'));
  li.appendChild(reflowElLabel);
  var reflowElInput = document.createElement('input');
  reflowElInput.id = reflowElLabel.getAttribute('for');
  reflowElInput.type = 'text';
  reflowElInput.size = '18';
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
    var rt = new ReflowTimer(false, reflowEl);
    rt.tests = [thisButton.test];
    rt.renderResults = false;
    rt.onTestsComplete = function(medianReflowTimes) {
      thisButton.disabled = false;
      var time = medianReflowTimes[this.tests[0]];
      span.innerHTML = '';
      span.appendChild(document.createTextNode(time + ' ms.'));
    };
    rt.run();
  };

  // Clear results button.
  var clearResults = function() {
    for (var i = 0, span; span = resultEls[i]; i++) {
      span.innerHTML = '';
    }
  };
  var buttonContainer = divEl.cloneNode(false);
  buttonContainer.style.marginTop = '5px';
  var button = buttonEl.cloneNode(false);
  button.appendChild(document.createTextNode('clear'));
  button.style.width = '4em';
  button.onclick = clearResults;
  buttonContainer.appendChild(button);
  container.appendChild(buttonContainer);

  var resultEls = [];
  for (var i = 0, test; test = allTests[i]; i++) {
    var buttonContainer = divEl.cloneNode(false);
    buttonContainer.style.marginTop = '5px';

    var button = buttonEl.cloneNode(false);
    button.appendChild(document.createTextNode(test.replace('test', '')));
    button.test = test;
    button.onclick = buttonClickHandler;
    var span = spanEl.cloneNode(false);
    span.style.fontWeight = 'bold';
    resultEls.push(span);

    buttonContainer.appendChild(button);
    buttonContainer.appendChild(span);
    container.appendChild(buttonContainer);
  }
  document.body.appendChild(container);





})();
