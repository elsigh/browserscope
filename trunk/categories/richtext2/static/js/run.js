/**
 * @fileoverview 
 * Main functions used in running the RTE test suite.
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
 * Info function: returns true if the suite (mainly) tests the result HTML/Text.
 *
 * @return {boolean} Whether the suite main focus is the output HTML/Text
 */
function suiteChecksHTMLOrText() {
  return currentSuiteID[0] != 'S';
}

/**
 * Info function: returns true if the suite checks the result selection.
 *
 * @return {boolean} Whether the suite checks the selection
 */
function suiteChecksSelection() {
  return currentSuiteID[0] != 'Q';
}

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
 * Helper function returning the effective value of a test parameter.
 *
 * @param {String} the test parameter to be checked
 * @return {Any} the effective value of the parameter (can be undefined)
 */
function getTestParameter(param) {
  return (currentTest[param] === undefined) ? currentSuite[param]
                                            : currentTest[param];
}

/**
 * Runs a single test - outputs and sets the result variables.
 * @see variables.js for result values
 */
function runSingleTest() {
  currentResultHTML      = RESULTHTML_SETUP_EXCEPTION;
  currentResultSelection = RESULTSEL_NA; 

  // 1.) Populate the editor element with the initial test setup HTML.
  try {
    initEditorElement();
  } catch(ex) {
    outputSingleTestResult('Setup exception: ' + ex.toString());
    return;
  }

  // 2.) Run the test command, general function or query function.
  var cmd    = undefined;
  var output = SETUP_NOCOMMAND_EXCEPTION;

  try {
    if (cmd = getTestParameter(PARAM_COMMAND)) {
      // Note: "getTestParameter(PARAM_VALUE) || null" doesn't work, since
      // value might be the empty string - e.g., for 'insertText'!
      var value = getTestParameter(PARAM_VALUE);
      if (value === undefined) {
        value = null;
      }
      editorDoc.execCommand(cmd, false, value);
    } else if (cmd = getTestParameter(PARAM_FUNCTION)) {
      eval(cmd);
    } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSUPPORTED)) {
      output = editorDoc.queryCommandSupported(cmd);
    } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDENABLED)) {
      output = editorDoc.queryCommandEnabled(cmd);
    } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDINDETERM)) {
      output = editorDoc.queryCommandIndeterm(cmd);
    } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDSTATE)) {
      output = editorDoc.queryCommandState(cmd);
    } else if (cmd = getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
      output = editorDoc.queryCommandValue(cmd);
    }

    // 3.) Verify test result
    if (cmd) {
      if (getTestParameter(PARAM_COMMAND) || getTestParameter(PARAM_FUNCTION)) {
        try {
          prepareTestResult();
          compareHTMLTestResult();
          output = canonicalizeElementsAndAttributes(currentActualHTML,
                                                     { emitAttrs:         true,
                                                       emitStyle:         true,
                                                       emitClass:         true,
                                                       emitID:            true,
                                                       lowercase:         false,
                                                       canonicalizeUnits: false });
        } catch (ex) {
          output = 'Verification exception: ' + ex.toString();
          currentResultHTML = RESULT_VERIFICATION_EXCEPTION;
        }
      } else {
        if (output === false && getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
          // A return value of boolean 'false' for queryCommandValue means
          // 'not supported'.
          //
          // TODO(rolandsteiner): Color such a result purple? 
          // However, no exception was thrown...
          output = '<i>false</i> (UNSUPPORTED)';
          currentResultHTML = RESULTHTML_UNSUPPORTED;
        } else {
          compareTextTestResult(output);
        }
      }
    }
  } catch (ex) {
    output = ex.toString()
    if (getTestParameter(PARAM_ALLOW_EXCEPTION)) {
      currentResultHTML      = RESULTHTML_EQUAL;
      currentResultSelection = RESULTSEL_EQUAL;
    } else {
      currentResultHTML      = RESULTHTML_EXECUTION_EXCEPTION;
      currentResultSelection = RESULTSEL_NA;
    }
  }
  
  // 4.) Output the result
  try {
    outputSingleTestResult(output);
  } catch (ex) {
    // An exception shouldn't really happen here!
    writeFatalError('Exception on output when running ' + currentClassID + ' tests of the suite "' +
                    currentSuiteID + '" ("' + currentSuite.caption + '"): ' + ex.toString());
  }
}

/**
 * Runs a single test suite (such as DELETE tests or INSERT tests).
 *
 * @param {Object} suite as object reference
 */
function runTestSuite(suite) {
  currentSuite = suite;
  currentSuiteID = suite.id;
  currentSuiteScoreID = currentSuiteID + '-score';
  currentSuiteSelScoreID = currentSuiteID + '-selscore';

  try {
    var classCount = testClassIDs.length;

    // Reset count and score for this suite - set count to 0 for all (!) classes.
    counts[currentSuiteID]          = {total: 0};
    scoresHTML[currentSuiteID]      = {total: 0};
    scoresSelection[currentSuiteID] = {total: 0};
    for (var cls = 0; cls < classCount; ++cls) {
      var testClassID = testClassIDs[cls];
      counts[currentSuiteID][testClassID]          = {total: 0};
      scoresHTML[currentSuiteID][testClassID]      = {total: 0};
      scoresSelection[currentSuiteID][testClassID] = {total: 0};
    }
    
    for (var cls = 0; cls < classCount; ++cls) {
      currentClassID = testClassIDs[cls];
      currentClassScoreID = currentSuiteID + '-' + currentClassID + '-score';
      currentClassSelScoreID = currentSuiteID + '-' + currentClassID + '-selscore';

      try {
        currentClass = currentSuite[currentClassID];
        if (!currentClass) {
          continue;
        }

        currentBackgroundShade = 'Lo';
        for (testIdx = 0; testIdx < currentClass.length; ++testIdx) {
          currentBackgroundShade = (currentBackgroundShade == 'Lo') ? 'Hi' : 'Lo';
          currentTest = currentClass[testIdx];
          currentTestID = generateTestID(currentSuiteID, currentTest.id);
          ++counts[currentSuiteID].total;
          ++counts[currentSuiteID][currentClassID].total;

          runSingleTest();

          switch (currentResultHTML) {
            case RESULTHTML_EQUAL:
              scoresHTML[currentSuiteID][currentClassID][currentTestID] = 1;
              break;

            case RESULTHTML_ACCEPT:
              scoresHTML[currentSuiteID][currentClassID][currentTestID] = 0;
              break;

            default:
              scoresHTML[currentSuiteID][currentClassID][currentTestID] = 0;
              currentResultSelection = RESULTSEL_NA;
          }
          switch (currentResultSelection) {
            case RESULTSEL_EQUAL:
              scoresSelection[currentSuiteID][currentClassID][currentTestID] = 1;
              break;

            default:
              scoresSelection[currentSuiteID][currentClassID][currentTestID] = 0;
          }
          scoresHTML[currentSuiteID].total += scoresHTML[currentSuiteID][currentClassID][currentTestID]
          scoresSelection[currentSuiteID].total += scoresSelection[currentSuiteID][currentClassID][currentTestID]
          scoresHTML[currentSuiteID][currentClassID].total += scoresHTML[currentSuiteID][currentClassID][currentTestID];
          scoresSelection[currentSuiteID][currentClassID].total += scoresSelection[currentSuiteID][currentClassID][currentTestID];
          
          resetEditorElement();
        }

        outputTestClassScores();
      } catch (ex) {
        // An exception shouldn't really happen here!
        writeFatalError('Exception when running ' + currentClassID + ' tests of the suite "' +
                        currentSuiteID + '" ("' + currentSuite.caption + '"): ' + ex.toString());
      }
    }

    outputTestSuiteScores();
    } catch (ex) {
      // An exception shouldn't really happen here!
      writeFatalError('Exception when running the suite "' + currentSuiteID +
                      '" ("' + currentSuite.caption + '"): ' + ex.toString());
  }
}

/**
 * Fills the beacon with the test results of a given suite
 *
 * @param suiteResults {Object} results for a single suite as object reference
 * @param suffix (String, optional} ID suffix 
 */
function fillBeaconForSuite(suiteResults, suffix) {
  if (!suiteResults) {
    return;
  }
  if (!suffix) {
    suffix = '';
  }
  for (var cls = 0; cls < testClassIDs.length; ++cls) {
    var classID = testClassIDs[cls];
    var classResults = suiteResults[classID];
    if (!classResults) {
      continue;
    }
    for (testID in classResults) {
      if (testID == 'total') {
        continue;
      }
      beacon.push(testID + suffix + '=' + classResults[testID]);
    }
  }
}

/**
 * Fills the beacon with the results for individual tests.
 */
function fillIndividualTestResults() { 
  // selection suite
  fillBeaconForSuite(scoresSelection['S']);
  // DOM modifying suites
  fillBeaconForSuite(scoresHTML['A']);
  fillBeaconForSuite(scoresHTML['AC']);
  fillBeaconForSuite(scoresHTML['C']);
  fillBeaconForSuite(scoresHTML['CC']);
  fillBeaconForSuite(scoresHTML['U']);
  fillBeaconForSuite(scoresHTML['UC']);
  fillBeaconForSuite(scoresHTML['D']);
  fillBeaconForSuite(scoresHTML['FD']);
  fillBeaconForSuite(scoresHTML['I']);
  // selection results for DOM modifying suites
  fillBeaconForSuite(scoresSelection['A'], '_SEL');
  fillBeaconForSuite(scoresSelection['AC'], '_SEL');
  fillBeaconForSuite(scoresSelection['C'], '_SEL');
  fillBeaconForSuite(scoresSelection['CC'], '_SEL');
  fillBeaconForSuite(scoresSelection['U'], '_SEL');
  fillBeaconForSuite(scoresSelection['UC'], '_SEL');
  fillBeaconForSuite(scoresSelection['D'], '_SEL');
  fillBeaconForSuite(scoresSelection['FD'], '_SEL');
  fillBeaconForSuite(scoresSelection['I'], '_SEL');
  // query suites
  fillBeaconForSuite(scoresHTML['Q']);
  fillBeaconForSuite(scoresHTML['QE']);
  fillBeaconForSuite(scoresHTML['QI']);
  fillBeaconForSuite(scoresHTML['QS']);
  fillBeaconForSuite(scoresHTML['QSC']);
  fillBeaconForSuite(scoresHTML['QV']);
  fillBeaconForSuite(scoresHTML['QVC']);
}

/**
 * Fills the beacon with the test results.
 */
function fillResults() {
  // Result totals of the individual categories
  categoryTotals = [
    'selection='        + scoresSelection['S'].total,
    'apply='            + scoresHTML['A'].total,
    'applyCSS='         + scoresHTML['AC'].total,
    'change='           + scoresHTML['C'].total,
    'changeCSS='        + scoresHTML['CC'].total,
    'unapply='          + scoresHTML['U'].total,
    'unapplyCSS='       + scoresHTML['UC'].total,
    'delete='           + scoresHTML['D'].total,
    'forwarddelete='    + scoresHTML['FD'].total,
    'insert='           + scoresHTML['I'].total,
    'selectionResult='  + (scoresSelection['A'].total +
                           scoresSelection['AC'].total +
                           scoresSelection['C'].total +
                           scoresSelection['CC'].total +
                           scoresSelection['U'].total +
                           scoresSelection['UC'].total +
                           scoresSelection['D'].total +
                           scoresSelection['FD'].total +
                           scoresSelection['I'].total),
    'querySupported='   + scoresHTML['Q'].total,
    'queryEnabled='     + scoresHTML['QE'].total,
    'queryIndeterm='    + scoresHTML['QI'].total,
    'queryState='       + scoresHTML['QS'].total,
    'queryStateCSS='    + scoresHTML['QSC'].total,
    'queryValue='       + scoresHTML['QV'].total,
    'queryValueCSS='    + scoresHTML['QVC'].total
  ];
  
  // Beacon copies category results
  beacon = categoryTotals.slice(0);
  // fillIndividualTestResults()
}

