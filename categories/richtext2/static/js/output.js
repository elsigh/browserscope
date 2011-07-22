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
 * Generates a unique ID for a given single test out of the suite ID and
 * test ID.
 *
 * @param suiteID {string} ID string of the suite
 * @param testID {string} ID string of the individual tests
 * @return {string} globally unique ID
 */
function generateOutputID(suiteID, testID) {
  return commonIDPrefix + '-' + suiteID + '_' + testID;
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
 * @param suite {Object} the suite the test belongs to
 * @param group {Object} the group within the suite the test belongs to
 * @param test {Object} the test description as object reference
 * @param actual {String} a HTML string containing text nodes with markers
 * @return {String} string with highlighting tags around the text node parts
 */
function formatActualResult(suite, group, test, actual) {
  if (typeof actual != 'string')
    return formatValueOrString(actual);

  actual = escapeOutput(actual);

  // Fade attributes (or just style) if not actually tested for
  if (!getTestParameter(suite, group, test, PARAM_CHECK_ATTRIBUTES)) {
    actual = actual.replace(/([^ =]+)=\x22([^\x22]*)\x22/g, '<span class="fade">$1="$2"</span>');
  } else {
    // NOTE: convert 'class="..."' first, before adding other <span class="fade">...</span> !!!
    if (!getTestParameter(suite, group, test, PARAM_CHECK_CLASS)) {
      actual = actual.replace(/class=\x22([^\x22]*)\x22/g, '<span class="fade">class="$1"</span>');
    }
    if (!getTestParameter(suite, group, test, PARAM_CHECK_STYLE)) {
      actual = actual.replace(/style=\x22([^\x22]*)\x22/g, '<span class="fade">style="$1"</span>');
    }
    if (!getTestParameter(suite, group, test, PARAM_CHECK_ID)) {
      actual = actual.replace(/id=\x22([^\x22]*)\x22/g, '<span class="fade">id="$1"</span>');
    } else {
      // fade out contenteditable host element's 'editor-<xyz>' ID.
      actual = actual.replace(/id=\x22editor-([^\x22]*)\x22/g, '<span class="fade">id="editor-$1"</span>');
    }
    // grey out 'xmlns'
    actual = actual.replace(/xmlns=\x22([^\x22]*)\x22/g, '<span class="fade">xmlns="$1"</span>');
    // remove 'onload'
    actual = actual.replace(/onload=\x22[^\x22]*\x22 ?/g, '');
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
 * @param group {Object} the group of tests within the suite the test belongs to
 * @param testIdx {Object} the test as object reference
 */
function outputTestResults(suite, clsID, group, test) {
  var suiteID = suite.id;
  var cls = suite[clsID];
  var trID = generateOutputID(suiteID, test.id);
  var testResult = results[suiteID][clsID][test.id];
  var testValOut = VALOUTPUT[testResult.valresult];
  var testSelOut = SELOUTPUT[testResult.selresult];

  var suiteChecksSelOnly = !suiteChecksHTMLOrText(suite);
  var testUsesHTML = !!getTestParameter(suite, group, test, PARAM_EXECCOMMAND) ||
                     !!getTestParameter(suite, group, test, PARAM_FUNCTION);

  // Set background color for test ID
  var td = document.getElementById(trID + IDOUT_TESTID);
  if (td) {
    td.className = (suiteChecksSelOnly && testResult.selresult != SELRESULT_NA) ? testSelOut.css : testValOut.css;
  }

  // Fill in "Command" and "Value" cells
  var cmd;
  var cmdOutput = '&nbsp;';
  var valOutput = '&nbsp;';

  if (cmd = getTestParameter(suite, group, test, PARAM_EXECCOMMAND)) {
    cmdOutput = escapeOutput(cmd);
    var val = getTestParameter(suite, group, test, PARAM_VALUE);
    if (val !== undefined) {
      valOutput = formatValueOrString(val);
    }
  } else if (cmd = getTestParameter(suite, group, test, PARAM_FUNCTION)) {
    cmdOutput = '<i>' + escapeOutput(cmd) + '</i>';
  } else if (cmd = getTestParameter(suite, group, test, PARAM_QUERYCOMMANDSUPPORTED)) {
    cmdOutput = '<i>queryCommandSupported</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, group, test, PARAM_QUERYCOMMANDENABLED)) {
    cmdOutput = '<i>queryCommandEnabled</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, group, test, PARAM_QUERYCOMMANDINDETERM)) {
    cmdOutput = '<i>queryCommandIndeterm</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, group, test, PARAM_QUERYCOMMANDSTATE)) {
    cmdOutput = '<i>queryCommandState</i>';
    valOutput = escapeOutput(cmd);
  } else if (cmd = getTestParameter(suite, group, test, PARAM_QUERYCOMMANDVALUE)) {
    cmdOutput = '<i>queryCommandValue</i>';
    valOutput = escapeOutput(cmd);
  } else {
    cmdOutput = '<i>(none)</i>';
  }
  setTD(trID + IDOUT_COMMAND, cmdOutput);
  setTD(trID + IDOUT_VALUE, valOutput);

  // Fill in "Attribute checked?" and "Style checked?" cells
  if (testUsesHTML) {
    var checkAttrs = getTestParameter(suite, group, test, PARAM_CHECK_ATTRIBUTES);
    var checkStyle = getTestParameter(suite, group, test, PARAM_CHECK_STYLE);

    setTD(trID + IDOUT_CHECKATTRS,
          checkAttrs ? OUTSTR_YES : OUTSTR_NO,
          checkAttrs ? 'attributes must match' : 'attributes are ignored');

    if (checkAttrs && checkStyle) {
      setTD(trID + IDOUT_CHECKSTYLE, OUTSTR_YES, 'style attribute contents must match');
    } else if (checkAttrs) {
      setTD(trID + IDOUT_CHECKSTYLE, OUTSTR_NO, 'style attribute contents is ignored');
    } else {
      setTD(trID + IDOUT_CHECKSTYLE, OUTSTR_NO, 'all attributes (incl. style) are ignored');
    }
  } else {
    setTD(trID + IDOUT_CHECKATTRS, OUTSTR_NA, 'attributes not applicable');
    setTD(trID + IDOUT_CHECKSTYLE, OUTSTR_NA, 'style not applicable');
  }
  
  // Fill in test pad specification cell (initial HTML + selection markers)
  setTD(trID + IDOUT_PAD, highlightSelectionMarkers(escapeOutput(getTestParameter(suite, group, test, PARAM_PAD))));

  // Fill in expected result(s) cell
  var expectedOutput = '';
  var expectedArr = getExpectationArray(getTestParameter(suite, group, test, PARAM_EXPECTED));
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (expectedOutput) {
      expectedOutput += '\xA0\xA0\xA0<i>or</i><br>';
    }
    expectedOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                                   : formatValueOrString(expectedArr[idx]);
  }
  var acceptedArr = getExpectationArray(getTestParameter(suite, group, test, PARAM_ACCEPT));    
  for (var idx = 0; idx < acceptedArr.length; ++idx) {
    expectedOutput += '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br><span class="accexp">';
    expectedOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                   : formatValueOrString(acceptedArr[idx]);
    expectedOutput += '</span>';
  }
  // TODO(rolandsteiner): THIS IS UGLY, relying on 'div' container being index 2,
  // AND not allowing other containers to have 'outer' results - change!!!
  var outerOutput = '';
  expectedArr = getExpectationArray(getContainerParameter(suite, group, test, containers[2], PARAM_EXPECTED_OUTER));
  for (var idx = 0; idx < expectedArr.length; ++idx) {
    if (outerOutput) {
      outerOutput += '\xA0\xA0\xA0<i>or</i><br>';
    }
    outerOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(expectedArr[idx]))
                                : formatValueOrString(expectedArr[idx]);
  }
  acceptedArr = getExpectationArray(getContainerParameter(suite, group, test, containers[2], PARAM_ACCEPT_OUTER));
  for (var idx = 0; idx < acceptedArr.length; ++idx) {
    if (outerOutput) {
      outerOutput += '<span class="accexp">\xA0\xA0\xA0<i>or</i></span><br>';
    }
    outerOutput += '<span class="accexp">';
    outerOutput += testUsesHTML ? highlightSelectionMarkers(escapeOutput(acceptedArr[idx]))
                                : formatValueOrString(acceptedArr[idx]);
    outerOutput += '</span>';
  }
  if (outerOutput) {
    expectedOutput += '<hr>' + outerOutput;
  }
  setTD(trID + IDOUT_EXPECTED, expectedOutput);

  // Iterate over the individual container results
  for (var containerIdx = 0; containerIdx < containers.length; ++containerIdx) {
    var containerID = containers[containerIdx].id;
    var containerTD = document.getElementById(trID + IDOUT_CONTAINER + containerID);
    var containerResult = testResult[containerID];
    var containerValOut = VALOUTPUT[containerResult.valresult];
    var containerSelOut = SELOUTPUT[containerResult.selresult];
    var containerValCSS = containerValOut.css;
    var containerSelCSS = (!suiteChecksSelOnly || containerResult.selresult != SELRESULT_NA) ? containerSelOut.css : containerValCSS;
    var containerCSS = containerValCSS;

    switch (containerResult.valresult) {
      case VALRESULT_SETUP_EXCEPTION:
      case VALRESULT_EXECUTION_EXCEPTION:
      case VALRESULT_VERIFICATION_EXCEPTION:
      case VALRESULT_UNSUPPORTED:
      case VALRESULT_CANARY:
        break;

      case VALRESULT_DIFF:
      case VALRESULT_ACCEPT:
      case VALRESULT_EQUAL:
        containerCSS = (testUsesHTML && suiteChecksSelOnly) ? containerSelCSS : containerValCSS;
        break;

      default:
        containerCSS = 'exception';
    }

    // Output results for both unfocused and focused
    for (var focusIdx = 0; focusIdx < focusArr.length; ++focusIdx) {
      var focusID = focusArr[focusIdx];
      var focusTD = document.getElementById(trID + IDOUT_FOCUS + containerID + ':' + focusID);
      var focusResult = containerResult[focusID];
      var focusValOut = VALOUTPUT[focusResult.valresult];
      var focusSelOut = SELOUTPUT[focusResult.selresult];
      var focusValCSS = focusValOut.css;
      var focusSelCSS = (!suiteChecksSelOnly || focusResult.selresult != SELRESULT_NA) ? focusSelOut.css : focusValCSS;
      var focusCSS = focusValCSS;

      // Fill in result status cell ("PASS", "ACC.", "FAIL", "EXC.", etc.)
      setTD(trID + IDOUT_STATUSVAL + containerID + ':' + focusID, focusValOut.output, focusValOut.title, focusValCSS);
      
      // Fill in selection status cell ("PASS", "ACC.", "FAIL", "N/A")
      setTD(trID + IDOUT_STATUSSEL + containerID + ':' + focusID, focusSelOut.output, focusSelOut.title, focusSelCSS);

      // Fill in actual result
      switch (focusResult.valresult) {
        case VALRESULT_SETUP_EXCEPTION:
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                SETUP_EXCEPTION + '(mouseover)',
                escapeOutput(focusResult.output),
                focusValCSS);
          break;
  
        case VALRESULT_EXECUTION_EXCEPTION:
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                EXECUTION_EXCEPTION + '(mouseover)',
                escapeOutput(focusResult.output.toString()),
                focusValCSS);
          break;
  
        case VALRESULT_VERIFICATION_EXCEPTION:
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                VERIFICATION_EXCEPTION + '(mouseover)',
                escapeOutput(focusResult.output.toString()),
                focusValCSS);
          break;
  
        case VALRESULT_UNSUPPORTED:
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                escapeOutput(focusResult.output),
                '',
                focusValCSS);
          break;
  
        case VALRESULT_CANARY:
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                highlightSelectionMarkersAndTextNodes(escapeOutput(focusResult.output)),
                '',
                focusValCSS);
          break;
  
        case VALRESULT_DIFF:
        case VALRESULT_ACCEPT:
        case VALRESULT_EQUAL:
          if (!testUsesHTML) {
            setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
                  formatValueOrString(focusResult.output),
                  '',
                  focusValCSS);
          } else if (focusResult.selresult == SELRESULT_CANARY) {
            focusCSS = suiteChecksSelOnly ? focusSelCSS : focusValCSS;
            setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID, 
                  highlightSelectionMarkersAndTextNodes(escapeOutput(focusResult.output)),
                  '',
                  focusCSS);
          } else {
            focusCSS = suiteChecksSelOnly ? focusSelCSS : focusValCSS;
            setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID, 
                  formatActualResult(suite, group, test, focusResult.output),
                  '',
                  focusCSS);
          }
          break;
  
        default:
          focusCSS = 'exception';
          setTD(trID + IDOUT_ACTUAL + containerID + ':' + focusID,
              INTERNAL_ERR + 'UNKNOWN RESULT VALUE',
              '',
              focusCSS);
      }
      
      if (focusTD) {
        focusTD.className = focusCSS;
      }
    }
    if (containerTD) {
      containerTD.className = containerCSS;
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

    span = document.getElementById(suiteID + '-' + clsID + '-score');
    if (span) {
      span.innerHTML = results[suiteID][clsID].valscore + '/' + results[suiteID][clsID].count;
    }
    span = document.getElementById(suiteID + '-' + clsID + '-selscore');
    if (span) {
      span.innerHTML = results[suiteID][clsID].selscore + '/' + results[suiteID][clsID].count;
    }

    var groupCount = cls.length;
    
    for (var groupIdx = 0; groupIdx < groupCount; ++groupIdx) {
      var group = cls[groupIdx];
      var testCount = group.tests.length;

      for (var testIdx = 0; testIdx < testCount; ++testIdx) {
        var test = group.tests[testIdx];

        outputTestResults(suite, clsID, group, test);
      }
    }
  }
}
