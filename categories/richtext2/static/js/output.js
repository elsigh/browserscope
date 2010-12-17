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
 * Function to highlight the selection markers
 *
 * @param str {String} a HTML string containing selection markers
 * @return {String} the HTML string with highlighting tags around the markers
 */
function highlightSelectionMarkersAndTextNodes(str) {
  str = highlightSelectionMarkers(str);
  str = str.replace(/\x60/g, '<span class="txt">');
  str = str.replace(/\xb4/g, '</span>');
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
      return "'" + escapeOutput(value) + "'";
      
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
function formatActualResult(suite, test, actual) {
  if (typeof actual != 'string')
    return formatValueOrString(actual);

  actual = escapeOutput(actual);

  // Fade attributes (or just style) if not actually tested for
  if (!getTestParameter(suite, test, PARAM_CHECK_ATTRIBUTES)) {
    actual = actual.replace(/([^ =]+)=\x22([^\x22]*)\x22/g, '<span class="fade">$1="$2"</span>');
  } else {
    // NOTE: convert 'class="..."' first, before adding other <span class="fade">...</span> !!!
    if (!getTestParameter(suite, test, PARAM_CHECK_CLASS)) {
      actual = actual.replace(/class=\x22([^\x22]*)\x22/g, '<span class="fade">class="$1"</span>');
    }
    if (!getTestParameter(suite, test, PARAM_CHECK_STYLE)) {
      actual = actual.replace(/style=\x22([^\x22]*)\x22/g, '<span class="fade">style="$1"</span>');
    }
    if (!getTestParameter(suite, test, PARAM_CHECK_ID)) {
      actual = actual.replace(/id=\x22([^\x22]*)\x22/g, '<span class="fade">id="$1"</span>');
    } else {
      // fade out contenteditable host element's 'editor-<xyz>' ID.
      actual = actual.replace(/id=\x22editor-([^\x22]*)\x22/g, '<span class="fade">id="editor-$1"</span>');
    }
    // grey out 'xmlns' and 'onload'
    actual = actual.replace(/xmlns=\x22([^\x22]*)\x22/g, '<span class="fade">xmlns="$1"</span>');
    actual = actual.replace(/onload=\x22([^\x22]*)\x22/g, '<span class="fade">onload="$1"</span>');
  }
  // Highlight selection markers and text nodes.
  actual = highlightSelectionMarkersAndTextNodes(actual);

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
 * @param id {String} ID of the table cell
 * @param val {String} inner HTML to set
 * @param ttl {String, optional} value of the 'title' attribute
 * @param cls {String, optional} class name for the cell
 */
function setTD(id, val, ttl, cls) {
  var td = document.getElementById(id);
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
 * Outputs the results of a single test suite
 *
 * @param suite {Object} test suite as object reference
 * @param clsID {String} test class ID ('Proposed', 'RFC', 'Final')
 * @param testIdx {Integer} test index
 */
function outputTestResults(suite, clsID, testIdx) {
  var suiteID = suite.id;
  var cls = suite[clsID];
  var test = cls[testIdx];
  var testID = generateTestID(suiteID, test.id);
  var testResult = results[suiteID][clsID][testID];
  var testValOut = VALOUTPUT[testResult.valresult];
  var testSelOut = SELOUTPUT[testResult.selresult];

  var suiteChecksSelOnly = !suiteChecksHTMLOrText(suite);
  var testUsesHTML = !!getTestParameter(suite, test, PARAM_EXECCOMMAND) ||
                     !!getTestParameter(suite, test, PARAM_FUNCTION);

  var shade = colorShades[testIdx % 2];

  // Set background color for test ID
  var td = document.getElementById(testID + IDOUT_TESTID);
  if (td) {
    td.className = ((suiteChecksSelOnly && testResult.selresult != SELRESULT_NA) ? testSelOut.css : testValOut.css) + 'Bk' + shade;
  }

  // Fill in "Command" and "Value" cells
  var cmd;
  var cmdOutput = '&nbsp;';
  var valOutput = '&nbsp;';

  if (cmd = getTestParameter(suite, test, PARAM_EXECCOMMAND)) {
    cmdOutput = escapeOutput(cmd);
    var val = getTestParameter(suite, test, PARAM_VALUE);
    if (val !== undefined) {
      valOutput = formatValueOrString(val);
    }
  } else if (cmd = getTestParameter(suite, test, PARAM_FUNCTION)) {
    cmdOutput = '<i>' + escapeOutput(cmd) + '</i>';
  } else if (cmd = getTestParameter(suite, test, PARAM_QUERYCOMMANDSUPPORTED)) {
    cmdOutput = '<i>queryCommandSupported</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, test, PARAM_QUERYCOMMANDENABLED)) {
    cmdOutput = '<i>queryCommandEnabled</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, test, PARAM_QUERYCOMMANDINDETERM)) {
    cmdOutput = '<i>queryCommandIndeterm</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, test, PARAM_QUERYCOMMANDSTATE)) {
    cmdOutput = '<i>queryCommandState</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, test, PARAM_QUERYCOMMANDVALUE)) {
    cmdOutput = '<i>queryCommandValue</i>';
    valOutput = escapeOutput(cmd);
  } else {
    cmdOutput = '<i>(none)</i>';
  }
  setTD(testID + IDOUT_COMMAND, cmdOutput);
  setTD(testID + IDOUT_VALUE, valOutput);

  // Fill in "Attribute checked?" and "Style checked?" cells
  if (testUsesHTML) {
    var checkAttrs = getTestParameter(suite, test, PARAM_CHECK_ATTRIBUTES);
    var checkStyle = getTestParameter(suite, test, PARAM_CHECK_STYLE);

    setTD(testID + IDOUT_CHECKATTRS,
          checkAttrs ? OUTSTR_YES : OUTSTR_NO,
          checkAttrs ? 'attributes must match' : 'attributes are ignored');

    if (checkAttrs && checkStyle) {
      setTD(testID + IDOUT_CHECKSTYLE, OUTSTR_YES, 'style attribute contents must match');
    } else if (checkAttrs) {
      setTD(testID + IDOUT_CHECKSTYLE, OUTSTR_NO, 'style attribute contents is ignored');
    } else {
      setTD(testID + IDOUT_CHECKSTYLE, OUTSTR_NO, 'all attributes (incl. style) are ignored');
    }
  } else {
    setTD(testID + IDOUT_CHECKATTRS, OUTSTR_NA, 'attributes not applicable');
    setTD(testID + IDOUT_CHECKSTYLE, OUTSTR_NA, 'style not applicable');
  }
  
  // Fill in test pad specification cell (initial HTML + selection markers)
  setTD(testID + IDOUT_PAD, highlightSelectionMarkers(escapeOutput(getTestParameter(suite, test, PARAM_PAD))));

  // Fill in expected result(s) cell
  var expectedOutput = '';
  var expectedArr = getExpectationArray(getTestParameter(suite, test, PARAM_EXPECTED));
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (expectedOutput) {
      expectedOutput += '\xA0\xA0\xA0<i>or</i><br>';
    }
    expectedOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                                   : formatValueOrString(expectedArr[idx]);
  }
  var acceptedArr = getExpectationArray(getTestParameter(suite, test, PARAM_ACCEPT));    
  for (var idx = 0; idx < acceptedArr.length; ++idx) {
    expectedOutput += '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br><span class="accexp">';
    expectedOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                   : formatValueOrString(acceptedArr[idx]);
    expectedOutput += '</span>';
  }
  // TODO(rolandsteiner): THIS IS UGLY, relying on 'div' container being index 2,
  // AND not allowing other containers to have 'outer' results - change!!!
  var outerOutput = '';
  expectedArr = getExpectationArray(getContainerParameter(suite, test, containers[2], PARAM_EXPECTED_OUTER));
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (outerOutput) {
      outerOutput += '\xA0\xA0\xA0<i>or</i><br>';
    }
    outerOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                                : formatValueOrString(expectedArr[idx]);
  }
  acceptedArr = getExpectationArray(getContainerParameter(suite, test, containers[2], PARAM_ACCEPT_OUTER));
  for (var idx = 0; idx < acceptedArr.length; ++idx) {
    if (outerOutput) {
      outerOutput += '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br><span class="accexp">';
    }
    outerOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                : formatValueOrString(acceptedArr[idx]);
    outerOutput += '</span>';
  }
  if (outerOutput) {
    expectedOutput += '<hr>' + outerOutput;
  }
  setTD(testID + IDOUT_EXPECTED, expectedOutput);

  // Iterate over the individual container results
  for (var cntIdx = 0; cntIdx < containers.length; ++cntIdx) {
    var cntID = containers[cntIdx].id;
    var cntTD = document.getElementById(testID + IDOUT_CONTAINER + cntID);
    var cntResult = testResult[cntID];
    var cntValOut = VALOUTPUT[cntResult.valresult];
    var cntSelOut = SELOUTPUT[cntResult.selresult];
    var cssVal = cntValOut.css + 'Bk' + shade;
    var cssSel = (!suiteChecksSelOnly || cntResult.selresult != SELRESULT_NA) ? (cntSelOut.css + 'Bk' + shade) : cssVal;
    var cssCnt = cssVal;

    // Fill in result status cell ("PASS", "ACC.", "FAIL", "EXC.", etc.)
    setTD(testID + IDOUT_STATUSVAL + cntID, cntValOut.output, cntValOut.title, cssVal);
    
    // Fill in selection status cell ("PASS", "ACC.", "FAIL", "N/A")
    setTD(testID + IDOUT_STATUSSEL + cntID, cntSelOut.output, cntSelOut.title, cssSel);

    // Fill in actual result
    switch (cntResult.valresult) {
      case VALRESULT_SETUP_EXCEPTION:
        setTD(testID + IDOUT_ACTUAL + cntID,
              SETUP_EXCEPTION + '(mouseover)',
              escapeOutput(cntResult.output),
              cssVal);
        break;

      case VALRESULT_EXECUTION_EXCEPTION:
        setTD(testID + IDOUT_ACTUAL + cntID,
              EXECUTION_EXCEPTION + '(mouseover)',
              escapeOutput(cntResult.output.toString()),
              cssVal);
        break;

      case VALRESULT_VERIFICATION_EXCEPTION:
        setTD(testID + IDOUT_ACTUAL + cntID,
              VERIFICATION_EXCEPTION + '(mouseover)',
              escapeOutput(cntResult.output.toString()),
              cssVal);
        break;

      case VALRESULT_UNSUPPORTED:
        setTD(testID + IDOUT_ACTUAL + cntID,
              escapeOutput(cntResult.output),
              '',
              cssVal);
        break;

      case VALRESULT_CANARY:
        setTD(testID + IDOUT_ACTUAL + cntID,
              highlightSelectionMarkersAndTextNodes(escapeOutput(cntResult.output)),
              '',
              cssVal);
        break;

      case VALRESULT_DIFF:
      case VALRESULT_ACCEPT:
      case VALRESULT_EQUAL:
        if (!testUsesHTML) {
          setTD(testID + IDOUT_ACTUAL + cntID,
                formatValueOrString(cntResult.output),
                '',
                cssVal);
        } else if (cntResult.selresult == SELRESULT_CANARY) {
          cssCnt = suiteChecksSelOnly ? cssSel : cssVal;
          setTD(testID + IDOUT_ACTUAL + cntID, 
                highlightSelectionMarkersAndTextNodes(escapeOutput(cntResult.output)),
                '',
                cssCnt);
        } else {
          cssCnt = suiteChecksSelOnly ? cssSel : cssVal;
          setTD(testID + IDOUT_ACTUAL + cntID, 
                formatActualResult(suite, test, cntResult.output),
                '',
                cssCnt);
        }
        break;

      default:
        cssCnt = 'exceptionBk' + shade;
        setTD(testID + IDOUT_ACTUAL + cntID,
              INTERNAL_ERR + 'UNKNOWN RESULT VALUE',
              '',
              cssCnt);
    }

    if (cntTD) {
      cntTD.className = cssCnt;
    }
  }          
}

/**
 * Outputs the results of a single test suite
 *
 * @param {Object} suite as object reference
 */
function outputTestSuiteResults(suite) {
  var suiteID = suite.id;
  var span;

  span = document.getElementById(suiteID + '-score');
  if (span) {
    span.innerHTML = results[suiteID].valscore + '/' + results[suiteID].count;
  }
  span = document.getElementById(suiteID + '-selscore');
  if (span) {
    span.innerHTML = results[suiteID].selscore + '/' + results[suiteID].count;
  }
  span = document.getElementById(suiteID + '-time');
  if (span) {
    span.innerHTML = results[suiteID].time;
  }
  span = document.getElementById(suiteID + '-progress');
  if (span) {
    span.style.color = 'green';
  }

  for (var clsIdx = 0; clsIdx < testClassCount; ++clsIdx) {
    var clsID = testClassIDs[clsIdx];
    var cls = suite[clsID];
    if (!cls)
      continue;

    var testCount = cls.length;

    span = document.getElementById(suiteID + '-' + clsID + '-score');
    if (span) {
      span.innerHTML = results[suiteID][clsID].valscore + '/' + results[suiteID][clsID].count;
    }
    span = document.getElementById(suiteID + '-' + clsID + '-selscore');
    if (span) {
      span.innerHTML = results[suiteID][clsID].selscore + '/' + results[suiteID][clsID].count;
    }

    for (var testIdx = 0; testIdx < testCount; ++testIdx) {
      outputTestResults(suite, clsID, testIdx);
    }
  }
}
