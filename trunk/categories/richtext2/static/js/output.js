/**
 * @fileoverview 
 * Functions used to format the test result output.
 *
 * TODO: license! $$$
 *
 * @version 0.1
 * @author rolandsteiner@google.com
 */

/**
 * Adds quotes around all text nodes to show cases with non-normalized
 * text nodes. Those are not a bug, but may still be usefil in helping to
 * debug erroneous cases.
 *
 * @param node {DOMNode} root node from which to descend
 */
function encloseTextNodesWithQuotes(node) {
  switch (node.nodeType) {
    case DOM_NODE_TYPE_ELEMENT:
      for (var i = 0; i < node.childNodes.length; ++i) {
        encloseTextNodesWithQuotes(node.childNodes[i]);
      }
      break;
      
    case DOM_NODE_TYPE_TEXT:
      node.data = '`' + node.data + '´';
      break;
  }
}

/**
 * Escape text content for use with .innerHTML.
 *
 * @param str {String} HTML text to displayed
 * @return {String} the escaped HTML
 */
function escapeOutput(str) {
  return str.replace(/\</g, '&lt;').replace(/\>/g, '&gt;');
}

/**
 * Outputs the header for the test suite and constructs the HTML table.
 */
function outputTestSuiteHeader() {
  var linkID = currentSuite.id;
  currentSuiteScoreID = linkID + '-score';

  var h1 = document.createElement('H1');
  h1.id = linkID;
  h1.innerHTML = '<A NAME="' + linkID + '" HREF="#' + linkID +'">' +
                 currentSuite.id +
                 '</A> - ' + 
                 currentSuite.caption + 
                 ': <SPAN ID="' + currentSuiteScoreID + '">\xA0</SPAN>';
  document.body.appendChild(h1);
  
  if (currentSuite.comment) {
    var div = document.createElement('DIV');
    div.className = 'comment';
    div.innerHTML = currentSuite.comment;
    document.body.appendChild(div);
  }
}

/**
 * Outputs the header for the test class ('Finalized', 'RFC' or 'Proposed')
 */
function outputTestClassHeader() {
  var linkID = currentSuite.id + '-' + currentClassID;
  currentClassScoreID = linkID + '-score';

  var h2 = document.createElement('H2');
  h2.id = linkID;
  h2.innerHTML = '<A NAME="' + linkID + '" HREF="#' + linkID +'">' + 
                 currentClassID + 
                 ' Tests</A>: <SPAN ID="' + currentClassScoreID +'">\xA0</SPAN>';
  document.body.appendChild(h2);
}

/**
 * Constructs the HTML table header and body.
 */
function outputTestTableHeader() {
  var table = document.createElement('TABLE');
  table.width = '100%';
  var thead = document.createElement('THEAD');
  var tr  = document.createElement('TR');
  tr.className = 'suite-thead';
  var th = document.createElement('TH');
  th.innerHTML = 'ID';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Command';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Value';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.title = 'styleWithCSS set?';
  th.innerHTML = 'C';  // styleWithCSS
  tr.appendChild(th);
  th = document.createElement('TH');
  th.title = 'Check attributes?';
  th.innerHTML = 'A';  // check Attributes
  tr.appendChild(th);
  th = document.createElement('TH');
  th.title = 'Check style?';
  th.innerHTML = 'S';  // check Style
  tr.appendChild(th);
  th = document.createElement('TH');
  th.title = 'Check selection?';
  th.innerHTML = '^';  // check Selection
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Status';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Initial';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Expected';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Actual (lower case, canonicalized, selection marks)';
  tr.appendChild(th);
  th = document.createElement('TH');
  th.innerHTML = 'Test Description';
  tr.appendChild(th);
  thead.appendChild(tr);
  table.appendChild(thead);
  document.body.appendChild(table);
  currentOutputTable = table;
}

/**
 * Function to highlight the selection markers
 *
 * @param str {String} a HTML string containing selection markers
 * @return {String} the HTML string with highlighting tags around the markers
 */
function highlightSelectionMarkers(str) {
  str = str.replace(/\[/g, '<span class="sel">[</span>');
  str = str.replace(/\]/g, '<span class="sel">]</span>');
  str = str.replace(/\^/g, '<span class="sel">^</span>');
  str = str.replace(/{/g,  '<span class="sel">{</span>');
  str = str.replace(/}/g,  '<span class="sel">}</span>');
  str = str.replace(/\|/g, '<b class="sel">|</b>');
  return str;
}

/**
 * Function to highlight text nodes
 *
 * @param str {String} a HTML string containing text nodes with markers
 * @return {String} string with highlighting tags around the text node parts
 */
function formatActualResult(str) {
  // Fade attributes (or just style) if not actually tested for
  if (!getTestParameter(PARAM_CHECK_ATTRIBUTES)) {
    str = str.replace(/([^ =]+)=\"([^\"]*)\"/g, '<span class="fade">$1="$2"</span>');
  } else {
    if (!getTestParameter(PARAM_CHECK_STYLE)) {
      str = str.replace(/style=\"([^\"]*)\"/g, '<span class="fade">style="$1"</span>');
    }
    if (!getTestParameter(PARAM_CHECK_CLASS)) {
      str = str.replace(/class=\"([^\"]*)\"/g, '<span class="fade">class="$1"</span>');
    }
    if (!getTestParameter(PARAM_CHECK_ID)) {
      str = str.replace(/id=\"([^\"]*)\"/g, '<span class="fade">id="$1"</span>');
    }
  }
  // Highlight selection markers and text nodes.
  str = highlightSelectionMarkers(str);
  str = str.replace(/`/g,  '<span class="txt">');
  str = str.replace(/´/g,  '</span>');

  return str;
}

/**
 * Outputs the result of a single test to a table
 *
 * @param actual {String} actual result string
 * @param successLevel {Integer} one of the RESULT_... values
 * @see variables.js for return values
 */
function outputSingleTestResult(actual, successLevel) {
  var hasSelMarker = /[\[\]\^{}\|]/;
  var backgroundColorClass;
  var resultString;

  switch (successLevel) {
    case RESULT_HTML_DIFFS:
      backgroundColorClass = 'fail';
      resultString = 'FAIL';
      break;
    case RESULT_SELECTION_DIFFS:
      backgroundColorClass = 'seldiff';
      resultString = 'SEL.';
      break;
    case RESULT_EQUAL:
      backgroundColorClass = 'success';
      resultString = 'PASS';
      break;
    default:
      backgroundColorClass = 'exception';
      resultString = 'EXC.';
      break;
  }

  // Each command is displayed as a table row with 6 columns
  var tr = document.createElement('TR');
  tr.className = backgroundColorClass + 'Bk' + currentBackgroundShade;
  tr.id = currentID;

  // Column 1: test ID, with a bookmark to facilitate external references
  var a = document.createElement('a');
  a.name = currentID;
  a.href = '#' + currentID;
  a.innerHTML = currentID;
  var td = document.createElement('TD');
  td.appendChild(a);
  tr.appendChild(td);

  // Column 2: command being tested
  td = document.createElement('TD');
  var cmd = getTestParameter(PARAM_COMMAND);
  if (typeof cmd == 'string') {
    td.innerHTML = escapeOutput(cmd);
  } else if (typeof cmd == 'function') {
    td.innerHTML = '(func)';
    td.title = escapeOutput(cmd.toString());
  } else {
    td.innerHTML = '(none)';
  }
  tr.appendChild(td);

  // Column 3: value of command (if any)
  td = document.createElement('TD');
  var value = getTestParameter(PARAM_VALUE);
  if (typeof value == 'string') {
    td.innerHTML = "'" + value + "'";  
  }
  tr.appendChild(td);

  // Column 4: styleWithCSS
  td = document.createElement('TD');
  var styleWithCSS = getTestParameter(PARAM_STYLE_WITH_CSS);
  td.innerHTML = styleWithCSS ? 'y' : 'n';
  td.title = styleWithCSS ? 'styleWithCSS is set' : 'styleWithCSS is false';
  tr.appendChild(td);

  // Column 5: check Attributes
  td = document.createElement('TD');
  var checkAttrs = getTestParameter(PARAM_CHECK_ATTRIBUTES);
  td.innerHTML = checkAttrs ? 'y' : 'n';
  td.title = checkAttrs ? 'attributes must match' : 'attributes are ignored';
  tr.appendChild(td);

  // Column 6: check Style
  td = document.createElement('TD');
  var checkStyle = getTestParameter(PARAM_CHECK_STYLE);
  if (checkAttrs && checkStyle) {
    td.innerHTML = 'y';
    td.title = 'style attribute contents must match';
  } else if (checkAttrs) {
    td.innerHTML = 'n';
    td.title = 'style attribute is ignored';
  } else {
    td.innerHTML = 'n';
    td.title = 'all attributes (incl. style) are ignored';
  }
  tr.appendChild(td);

  // Column 7: check Selection
  td = document.createElement('TD');
  var expectedSpec = getTestParameter(PARAM_EXPECTED);
  var checkSel = getTestParameter(PARAM_CHECK_SELECTION);
  if (checkSel === undefined) {
    if (typeof expectedSpec == 'string') {
      checkSel = hasSelMarker.test(expectedSpec);
    } else {
      var y = false;
      var n = false;
      var count = expectedSpec.length;
      for (var e = 0; e < count; ++e) {
        if (hasSelMarker.test(expectedSpec[e])) {
          y = true;
        } else {
          n = true;
        }
      }
      if (y && !n) {
        checkSel = true;
      } else if (!y && n) {
        checkSel = false;
      }
    }
  }
  if (checkSel === undefined) {
    td.innerHTML = '?';
    td.title = 'selection check depends on individual expectation string';
  } else if (checkSel) {
    td.innerHTML = 'y';
    td.title = 'result selection is being checked';
  } else {
    td.innerHTML = 'n';
    td.title = 'result selection is irrelevant';
  }
  tr.appendChild(td);

  // Column 8: pass/fail
  td = document.createElement('TD');
  td.innerHTML = resultString;
  td.className = backgroundColorClass;
  tr.appendChild(td);

  // Column 9: original pad specification
  td = document.createElement('TD');
  td.innerHTML = highlightSelectionMarkers(escapeOutput(currentTest.pad));
  tr.appendChild(td);

  // Column 10: expected result(s)
  td = document.createElement('TD');
  var expectedOutput = '';
  if (typeof expectedSpec == 'string') {
    expectedOutput = escapeOutput(expectedSpec);
  } else {
    var count = expectedSpec.length;
    for (var idx = 0; idx < count; ++idx) {
      if (idx > 0) {
        expectedOutput = expectedOutput + '\xA0\xA0\xA0<i>or</i><br>';
      }
      expectedOutput = expectedOutput + escapeOutput(expectedSpec[idx]);
    }
  }
  td.innerHTML = highlightSelectionMarkers(expectedOutput);
  tr.appendChild(td);

  // Column 11: resulting html
  td = document.createElement('TD');
  actual = escapeOutput(actual);
  switch (successLevel) {
    case RESULT_SETUP_EXCEPTION:
      td.innerHTML = actual;
      break;
    case RESULT_EXECUTION_EXCEPTION:
      td.title = actual;
      td.innerHTML = UNSUPPORTED_COMMAND_EXCEPTION;
      break;
    case RESULT_VERIFICATION_EXCEPTION:
      td.title = actual;
      td.innerHTML = VERIFICATION_EXCEPTION;
      break;
    case RESULT_HTML_DIFFS:
    case RESULT_SELECTION_DIFFS:
    case RESULT_EQUAL:
      td.innerHTML = formatActualResult(actual);
      break;
  }
  tr.appendChild(td);

  // Column 12: test description
  td = document.createElement('TD');
  td.innerHTML = escapeOutput(getTestParameter(PARAM_DESCRIPTION) || '\xA0');
  tr.appendChild(td);

  currentOutputTable.appendChild(tr);
}

/**
 * Outputs the scores for the current class ('Finalized', 'RFC', 'Proposed')
 * of the current test suite.
 */
function outputTestClassScores() {
  var scoreSpan = document.getElementById(currentClassScoreID);
  if (!scoreSpan) {
    throw SCORE_EXCEPTION;
  }

  scoreSpan.innerHTML = scoresStrict[currentSuite.id][currentClassID] + '/' + 
                        scoresPartial[currentSuite.id][currentClassID] + '/' + 
                        counts[currentSuite.id][currentClassID];
}

/**
 * Outputs the total scores over all test classes for the current suite.
 */
function outputTestSuiteScores() {
  var scoreSpan = document.getElementById(currentSuiteScoreID);
  if (!scoreSpan) {
    throw SCORE_EXCEPTION;
  }

  scoreSpan.innerHTML = scoresStrict[currentSuite.id].total + '/' + 
                        scoresPartial[currentSuite.id].total + '/' + 
                        counts[currentSuite.id].total;
}
