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
  buttonEl.style.textAlign = 'left';
  buttonEl.style.width = '12em';
  buttonEl.style.padding = 'auto';
  buttonEl.style.margin = 'auto';
  buttonEl.style.font = 'inherit';
  buttonEl.style.color = 'inherit';
  buttonEl.style.background = 'none';
  buttonEl.style.border = 'auto';

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
  style.color = '#999';
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
