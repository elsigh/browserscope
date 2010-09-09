/**
 * @fileoverview 
 * Functions used to format the test result output.
 *
 * Copyright 2010 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License')
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version 0.1
 * @author rolandsteiner@google.com
 */

/**
 * Generates a unique ID for a given single test out of the suite ID and
 * test ID.
 *
 * @param suiteID {string}
 * @param testID {string}
 * @return {string} globally unique ID
 */
function generateTestID(suiteID, testID) {
  return commonIDPrefix + '-' + suiteID + '_' + testID;
}

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
      node.data = '\x60' + node.data + '\xb4';
      break;
  }
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
 * @param actual {String} a HTML string containing text nodes with markers
 * @return {String} string with highlighting tags around the text node parts
 */
function formatActualResult(actual) {
  // Fade attributes (or just style) if not actually tested for
  if (!getTestParameter(PARAM_CHECK_ATTRIBUTES)) {
    actual = actual.replace(/([^ =]+)=\x22([^\x22]*)\x22/g, '<span class="fade">$1="$2"</span>');
  } else {
    // NOTE: convert 'class="..."' first, before adding other <span class="fade">...</span> !!!
    if (!getTestParameter(PARAM_CHECK_CLASS)) {
      actual = actual.replace(/class=\x22([^\x22]*)\x22/g, '<span class="fade">class="$1"</span>');
    }
    if (!getTestParameter(PARAM_CHECK_STYLE)) {
      actual = actual.replace(/style=\x22([^\x22]*)\x22/g, '<span class="fade">style="$1"</span>');
    }
    if (!getTestParameter(PARAM_CHECK_ID)) {
      actual = actual.replace(/id=\x22([^\x22]*)\x22/g, '<span class="fade">id="$1"</span>');
    }
  }
  // Highlight selection markers and text nodes.
  actual = highlightSelectionMarkers(actual);
  actual = actual.replace(/\x60/g,  '<span class="txt">');
  actual = actual.replace(/\xb4/g,  '</span>');

  return actual;
}

/**
 * Function to format output according to type
 *
 * @param value {String/Boolean} string or value to format
 * @return {String} HTML-formatted string
 */
function formatValueOrString(value) {
  switch (typeof value) {
    case 'undefined':
      return '<i>undefined</i>';

    case 'boolean':
      return '<i>' + value.toString() + '</i>';
      
    case 'number':
      return value.toString();
      
    case 'string':
      return "'" + escapeOutput(value.toString()) + "'";
      
    default:
      return '<i>(' + escapeOutput(value.toString()) + ')</i>';
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
 * Fills in a single test line
 *
 * @param actual {String} actual result
 * @param successLevel {Integer} success/failure/exception
 * @see variables.js for success levels
 */
function outputSingleTestResult(actual, successLevel) {
  var tr = currentIDPartial ? document.getElementById(currentIDPartial) : document.getElementById(currentIDStrict);
  var td;

  if (!tr || !tr.cells || tr.cells.length < 12) {
    // This means the output template and this JavaScript code are
    // out of sync. This really shouldn't happen and won't look pretty,
    // but there's not much we can show in this case.
    // At least this won't affect the test scores themselves. 
    return;
  }

  var hasSelMarker = /[\[\]\^{}\|]/;
  var backgroundColorClass;
  var resultString = '';
  var resultTitle = '';
  
  switch (successLevel) {
    case RESULT_UNSUPPORTED:
      backgroundColorClass = 'exception';
      resultString = 'UNS.';
      resultTitle  = 'Unsupported command or value';
      break;
    case RESULT_DIFFS:
      backgroundColorClass = 'fail';
      resultString = 'FAIL';
      resultTitle  = 'Test failed';
      break;
    case RESULT_SELECTION_DIFFS:
      backgroundColorClass = 'seldiff';
      resultString = 'SEL.';
      resultTitle  = 'Test passed, but had selection differences';
      break;
    case RESULT_ACCEPT:
      backgroundColorClass = 'accept';
      resultString = 'ACC.';
      resultTitle  = 'Test passed with acceptable result';
      break;
    case RESULT_EQUAL:
      backgroundColorClass = 'success';
      resultString = 'PASS';
      resultTitle  = 'Test passed with ideal result';
      break;
    default:
      backgroundColorClass = 'exception';
      resultString = 'EXC.';
      resultTitle  = 'Exception was thrown';
      break;
  }

  tr.className = backgroundColorClass + 'Bk' + currentBackgroundShade;
  
  // Column 1: test ID, with a bookmark to facilitate external references
  // Already filled in
  
  // Column 2: command being tested
  td = tr.cells[1];
  var usesHTML = false;
  var cmd;
  var value = getTestParameter(PARAM_VALUE);
  if (cmd = getTestParameter(PARAM_COMMAND)) {
    td.innerHTML = escapeOutput(cmd);
    usesHTML = true;
  } else if (cmd = getTestParameter(PARAM_FUNCTION)) {
    td.innerHTML = '<i>' + escapeOutput(cmd) + '</i>';
    usesHTML = true;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSUPPORTED)) {
    td.innerHTML = '<i>queryCommandSupported</i>';
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDENABLED)) {
    td.innerHTML = '<i>queryCommandEnabled</i>';
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDINDETERM)) {
    td.innerHTML = '<i>queryCommandIndeterm</i>';
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSTATE)) {
    td.innerHTML = '<i>queryCommandState</i>';
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
    td.innerHTML = '<i>queryCommandValue</i>';
    value = cmd;
  } else {
    td.innerHTML = '<i>(none)</i>';
  }
  
  // Column 3: value of command (if any)
  if (typeof value == 'string') {
    td = tr.cells[2];
    td.innerHTML = "'" + escapeOutput(value) + "'";  
  }
  
  // Column 4: styleWithCSS
  td = tr.cells[3];
  var styleWithCSS = getTestParameter(PARAM_STYLE_WITH_CSS);
  td.innerHTML = styleWithCSS ? 'y' : 'n';
  td.title = styleWithCSS ? 'styleWithCSS is set' : 'styleWithCSS is false';
  
  // Column 5: check Attributes
  td = tr.cells[4];
  if (usesHTML) {
    var checkAttrs = getTestParameter(PARAM_CHECK_ATTRIBUTES);
    td.innerHTML = checkAttrs ? 'y' : 'n';
    td.title = checkAttrs ? 'attributes must match' : 'attributes are ignored';
  } else {
    td.innerHTML = '-';
    td.title = 'attributes not applicable';
  }
  
  // Column 6: check Style
  td = tr.cells[5];
  if (usesHTML) {
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
  } else {
    td.innerHTML = '-';
    td.title = 'style not applicable';
  }
  
  // Column 7: check Selection
  td = tr.cells[6];
  var expectedSpec = getTestParameter(PARAM_EXPECTED);
  if (usesHTML) {
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
  } else {
     td.innerHTML = '-';
     td.title = 'selection not applicable';
  }
  
  // Column 8: pass/fail
  td = tr.cells[7];
  td.innerHTML = resultString;
  td.title = resultTitle;
  td.className = backgroundColorClass;
  
  // Column 9: original pad specification
  td = tr.cells[8];
  td.innerHTML = highlightSelectionMarkers(escapeOutput(getTestParameter(PARAM_PAD)));
  
  // Column 10: expected result(s)
  td = tr.cells[9];
  var expectedOutput = '';
  var expectedArr = getExpectationArray(expectedSpec);
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (expectedOutput) {
      expectedOutput = expectedOutput + '\xA0\xA0\xA0<i>or</i><br>';
    }
    expectedOutput = expectedOutput + (usesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                                                : formatValueOrString(expectedArr[idx]));
  }
  var acceptedSpec = getTestParameter(PARAM_ACCEPT);
  if (acceptedSpec) {
    var acceptedArr = getExpectationArray(acceptedSpec);    
    for (var idx = 0; idx < acceptedArr.length; ++idx) {
      expectedOutput = expectedOutput + '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br><span class="accexp">';
      expectedOutput = expectedOutput + (usesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                                  : formatValueOrString(acceptedArr[idx]))
                                      + '</span>';
    }
  }
  td.innerHTML = expectedOutput;
  
  // Column 11: actual result
  td = tr.cells[10];
  switch (successLevel) {
    case RESULT_SETUP_EXCEPTION:
      td.innerHTML = formatValueOrString(actual);
      break;
    case RESULT_EXECUTION_EXCEPTION:
      td.title = escapeOutput(actual.toString());
      td.innerHTML = UNSUPPORTED_COMMAND_EXCEPTION;
      break;
    case RESULT_VERIFICATION_EXCEPTION:
      td.title = escapeOutput(actual.toString());
      td.innerHTML = VERIFICATION_EXCEPTION;
      break;
    case RESULT_UNSUPPORTED:
      td.innerHTML = actual;
      break;
    case RESULT_DIFFS:
    case RESULT_SELECTION_DIFFS:
    case RESULT_ACCEPT:
    case RESULT_EQUAL:
      td.innerHTML = usesHTML ? formatActualResult(escapeOutput(actual)) : formatValueOrString(actual);
      break;
  }
  
  // Column 12: test description
  // Already filled in
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
