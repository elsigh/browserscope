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
 * Function to format output according to type
 *
 * @param value {String/Boolean} string or value to format
 * @return {String} HTML-formatted string
 */
function formatValueOrString(value) {
  if (value === undefined)
    return '<i>undefined</i>';
  if (value === null)
    return '<i>null</i>';
  
  switch (typeof value) {
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
 * Function to highlight text nodes
 *
 * @param actual {String} a HTML string containing text nodes with markers
 * @return {String} string with highlighting tags around the text node parts
 */
function formatActualResult(actual) {
  if (typeof actual != 'string')
    return formatValueOrString(actual);

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
  actual = actual.replace(/\x60/g, '<span class="txt">');
  actual = actual.replace(/\xb4/g, '</span>');

  return actual;
}

/**
 * Escape text content for use with .innerHTML.
 *
 * @param str {String} HTML text to displayed
 * @return {String} the escaped HTML
 */
function escapeOutput(str) {
  return str ? str.replace(/\</g, '&lt;').replace(/\>/g, '&gt;') : '';
}

/**
 * Fills in a single output table cell
 *
 * @param id {String} ID suffix of the table column
 * @param val {String} inner HTML to set
 * @param ttl {String, optional} value of the 'title' attribute
 * @param cls {String, optional} class name for the cell
 */
function setTD(id, val, ttl, cls) {
  var td = document.getElementById(currentTestID + id);
  if (td) {
    td.innerHTML = val;
    if (ttl) {
      td.title = ttl;
    }
    if (cls) {
      td.className = cls;
    }
  }
}

/**
 * Fills in a single test line
 *
 * @param actual {String} actual result
 * @see variables.js for success levels
 */
function outputSingleTestResult(actual) {
  var tr = document.getElementById(currentTestID);
  var td;

  var hasSelMarker = /[\[\]\^{}\|]/;
  var classHTML = 'grey';
  var classSel = 'grey';
  var classTR = 'grey';
  var resultStringHTML = '???';
  var resultStringSel = '???';
  var resultTitleHTML = '';
  var resultTitleSel = '';
  
  switch (currentResultHTML) {
    case RESULTHTML_UNSUPPORTED:
      classHTML        = 'unsupported';
      resultStringHTML = 'UNS.';
      resultTitleHTML  = 'Unsupported command or value';
      break;

    case RESULTHTML_DIFFS:
      classHTML        = 'fail';
      resultStringHTML = 'FAIL';
      resultTitleHTML  = 'Test failed';
      break;

    case RESULTHTML_ACCEPT:
      classHTML        = 'accept';
      resultStringHTML = 'ACC.';
      resultTitleHTML  = 'Test only had acceptable result (technically correct, but non-ideal)';
      break;

    case RESULTHTML_EQUAL:
      classHTML        = 'pass';
      resultStringHTML = 'PASS';
      resultTitleHTML  = 'Test passed with ideal result';
      break;

    default:
      classHTML        = 'exception';
      resultStringHTML = 'EXC.';
      resultTitleHTML  = 'Exception was thrown';
      break;
  }
  switch (currentResultSelection) {
    case RESULTSEL_DIFF:
      classSel        = 'fail';
      resultStringSel = 'FAIL';
      resultTitleSel  = 'Selection differs from expectation';
      break;

    case RESULTSEL_ACCEPT:
      classSel        = 'accept';
      resultStringSel = 'ACC.';
      resultTitleSel  = 'Selection is acceptable, but not ideal';
      break;

    case RESULTSEL_EQUAL:
      classSel        = 'pass';
      resultStringSel = 'PASS';
      resultTitleSel  = 'Selection matches expectation';
      break;

    default:
      classSel        = 'na';
      resultStringSel = 'N/A';
      resultTitleSel  = 'Selection cannot be tested';
      break;
  }
  if (suiteChecksHTMLOrText()) {
    classTR = classHTML;
  } else {
    switch (currentResultSelection) {
      case RESULTSEL_DIFF:
      case RESULTSEL_ACCEPT:
      case RESULTSEL_EQUAL:
        classTR = classSel;
        break;

      default:
        classTR = classHTML;
    }
  }
  tr.className = classTR + 'Bk' + currentBackgroundShade;
  
  // Column "ID", with a bookmark to facilitate external references
  // Already filled in
  
  // Column "Command": command being tested
  var usesHTML = false;
  var cmd;
  var value = getTestParameter(PARAM_VALUE);
  if (cmd = getTestParameter(PARAM_COMMAND)) {
    setTD(IDOUT_COMMAND, escapeOutput(cmd));
    usesHTML = true;
  } else if (cmd = getTestParameter(PARAM_FUNCTION)) {
    setTD(IDOUT_COMMAND, '<i>' + escapeOutput(cmd) + '</i>');
    usesHTML = true;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSUPPORTED)) {
    setTD(IDOUT_COMMAND, '<i>queryCommandSupported</i>');
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDENABLED)) {
    setTD(IDOUT_COMMAND, '<i>queryCommandEnabled</i>');
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDINDETERM)) {
    setTD(IDOUT_COMMAND, '<i>queryCommandIndeterm</i>');
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSTATE)) {
    setTD(IDOUT_COMMAND, '<i>queryCommandState</i>');
    value = cmd;
  } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
    setTD(IDOUT_COMMAND, '<i>queryCommandValue</i>');
    value = cmd;
  } else {
    setTD(IDOUT_COMMAND, '<i>(none)</i>');
  }
  
  // Column "Value": value of command (if any)
  if (typeof value == 'string') {
    setTD(IDOUT_VALUE, "'" + escapeOutput(value) + "'");
  }
  
  // Column "Attr.": check Attributes
  if (usesHTML) {
    var checkAttrs = getTestParameter(PARAM_CHECK_ATTRIBUTES);
    setTD(IDOUT_CHECKATTRS, checkAttrs ? OUTSTR_YES : OUTSTR_NO, checkAttrs ? 'attributes must match' : 'attributes are ignored');
  } else {
    setTD(IDOUT_CHECKATTRS, OUTSTR_NA, 'attributes not applicable');
  }

  // Column "Style": check style
  if (usesHTML) {
    var checkStyle = getTestParameter(PARAM_CHECK_STYLE);
    if (checkAttrs && checkStyle) {
      setTD(IDOUT_CHECKSTYLE, OUTSTR_YES, 'style attribute contents must match');
    } else if (checkAttrs) {
      setTD(IDOUT_CHECKSTYLE, OUTSTR_NO, 'style attribute contents is ignored');
    } else {
      setTD(IDOUT_CHECKSTYLE, OUTSTR_NO, 'all attributes (incl. style) are ignored');
    }
  } else {
    setTD(IDOUT_CHECKSTYLE, OUTSTR_NA, 'style not applicable');
  }
  
  // Column "HTML": HTML status ("PASS", "ACC.", "FAIL", "EXC.")
  setTD(IDOUT_STATUSHTML, resultStringHTML, resultTitleHTML, classHTML + 'Bk' + currentBackgroundShade);
  
  // Column "Sel": selection status ("PASS", "N/A", "FAIL", "EXC.")
  setTD(IDOUT_STATUSSEL, resultStringSel, resultTitleSel, classSel + 'Bk' + currentBackgroundShade);
  
  // Column "Initial": original pad specification
  setTD(IDOUT_PAD, highlightSelectionMarkers(escapeOutput(getTestParameter(PARAM_PAD))));
  
  // Column "Expected": expected result(s)
  var expectedOutput = '';
  var expectedArr = getExpectationArray(getTestParameter(PARAM_EXPECTED));
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (expectedOutput) {
      expectedOutput += '\xA0\xA0\xA0<i>or</i><br>';
    }
    expectedOutput += usesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                               : formatValueOrString(expectedArr[idx]);
  }
  var acceptedSpec = getTestParameter(PARAM_ACCEPT);
  if (acceptedSpec) {
    var acceptedArr = getExpectationArray(acceptedSpec);    
    for (var idx = 0; idx < acceptedArr.length; ++idx) {
      expectedOutput += '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br><span class="accexp">';
      expectedOutput += usesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                 : formatValueOrString(acceptedArr[idx]);
      expectedOutput += '</span>';
    }
  }
  setTD(IDOUT_EXPECTED, expectedOutput);
  
  // Column "Actual": actual result
  switch (currentResultHTML) {
    case RESULTHTML_SETUP_EXCEPTION:
      setTD(IDOUT_ACTUAL, escapeOutput(actual));
      break;
    case RESULTHTML_EXECUTION_EXCEPTION:
      setTD(IDOUT_ACTUAL, EXECUTION_EXCEPTION, escapeOutput(actual.toString()));
      break;
    case RESULTHTML_VERIFICATION_EXCEPTION:
      setTD(IDOUT_ACTUAL, VERIFICATION_EXCEPTION, escapeOutput(actual.toString()));
      break;
    case RESULTHTML_UNSUPPORTED:
      setTD(IDOUT_ACTUAL, actual);
      break;
    case RESULTHTML_DIFFS:
    case RESULTHTML_ACCEPT:
    case RESULTHTML_EQUAL:
      setTD(IDOUT_ACTUAL, usesHTML ? formatActualResult(escapeOutput(actual)) : formatValueOrString(actual));
      break;
  }

  // Column "Description": test description
  // Already filled in
}

/**
 * Outputs the scores for the current class ('Finalized', 'RFC', 'Proposed')
 * of the current test suite.
 */
function outputTestClassScores() {
  var span;

  span = document.getElementById(currentClassScoreID);
  if (span) {
    span.innerHTML = scoresHTML[currentSuiteID][currentClassID].total + '/' + counts[currentSuiteID][currentClassID].total;
  }
  span = document.getElementById(currentClassSelScoreID);
  if (span) {
    span.innerHTML = scoresSelection[currentSuiteID][currentClassID].total + '/' + counts[currentSuiteID][currentClassID].total;
  }
}

/**
 * Outputs the total scores over all test classes for the current suite.
 */
function outputTestSuiteScores() {
  var span;

  span = document.getElementById(currentSuiteScoreID);
  if (span) {
    span.innerHTML = scoresHTML[currentSuiteID].total + '/' + counts[currentSuiteID].total;
  }
  span = document.getElementById(currentSuiteSelScoreID);
  if (span) {
    span.innerHTML = scoresSelection[currentSuiteID].total + '/' + counts[currentSuiteID].total;
  }
}

/**
 * Writes a fatal error to the output (replaces alert box)
 *
 * @param text {String} text to output
 */
function writeFatalError(text) {
  var errorsStart = document.getElementById('errors');
  var divider = document.getElementById('divider');
  if (!errorsStart) {
    errorsStart = document.createElement('hr');
    errorsStart.id = 'errors';
    divider.parentNode.insertBefore(errorsStart, divider);
  }
  var error = document.createElement('div');
  error.className = 'fatalerror';
  error.innerHTML = 'FATAL ERROR: ' + escapeOutput(text);
  errorsStart.parentNode.insertBefore(error, divider);
}
