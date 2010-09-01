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
 * Runs a single test - outputs and returns the result.
 *
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function runSingleTest() {
  // 1.) Populate the editor element with the initial test setup HTML.
  try {
    initEditorElement();
  } catch(ex) {
    outputSingleTestResult('Setup exception: ' + ex.toString(),
                           RESULT_SETUP_EXCEPTION);
    return RESULT_SETUP_EXCEPTION;
  }

  // 2.) Run the test command, general function or query function.
  var cmd    = undefined;
  var output = SETUP_NOCOMMAND_EXCEPTION;
  var lvl    = RESULT_SETUP_EXCEPTION;

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
      cmd();
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
          lvl = compareHTMLTestResult();
          output = canonicalizeElementsAndAttributes(currentResultHTML,
                                                     { emitAttrs:         true,
                                                       emitStyle:         true,
                                                       emitClass:         true,
                                                       emitID:            true,
                                                       lowercase:         false,
                                                       canonicalizeUnits: false });
        } catch (ex) {
          output = 'Verification exception: ' + ex.toString();
          lvl = RESULT_VERIFICATION_EXCEPTION;
        }
      } else {
        if (output === false && getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
          // A return value of boolean 'false' for queryCommandValue means
          // 'not supported'.
          //
          // TODO(rolandsteiner): Color such a result purple? 
          // However, no exception was thrown...
          lvl = RESULT_UNSUPPORTED;
          output = '<i>false</i> (UNSUPPORTED)';
        } else {
          lvl = compareTextTestResult(output);
        }
      }
    }
  } catch (ex) {
    output = ex.toString()
    lvl = getTestParameter(PARAM_ALLOW_EXCEPTION)
              ? RESULT_EQUAL 
              : RESULT_EXECUTION_EXCEPTION;
  }
  
  // 4.) Output the result
  outputSingleTestResult(output, lvl);
  return lvl;
}

/**
 * Runs a single test suite (such as DELETE tests or INSERT tests).
 *
 * @param {Object} suite as object reference
 */
function runTestSuite(suite) {
  currentSuite = suite;
  currentSuiteScoreID = currentSuite.id + '-score';

  try {
    var classCount = testClassIDs.length;

    // Reset count and score for this suite - set count to 0 for all (!) classes.
    counts[currentSuite.id]        = {total: 0};
    scoresPartial[currentSuite.id] = {total: 0};
    scoresStrict[currentSuite.id]  = {total: 0};
    for (var cls = 0; cls < classCount; ++cls) {
      var testClass = testClassIDs[cls];
      counts[currentSuite.id][testClass]        = 0;
      scoresPartial[currentSuite.id][testClass] = 0;
      scoresStrict[currentSuite.id][testClass]  = 0;
    }
    
    for (var cls = 0; cls < classCount; ++cls) {
      currentClassID = testClassIDs[cls];
      currentClassScoreID = currentSuite.id + '-' + currentClassID + '-score';

      try {
        currentClass = currentSuite[currentClassID];
        if (!currentClass) {
          continue;
        }

        currentBackgroundShade = 'Lo';
        for (testIdx = 0; testIdx < currentClass.length; ++testIdx) {
          currentTest = currentClass[testIdx];
          currentID = commonIDPrefix + '-' + currentSuite.id + '-' + currentTest.id;
          ++counts[currentSuite.id].total;
          ++counts[currentSuite.id][currentClassID];
          var result = runSingleTest();
          switch (result) {
            case RESULT_EQUAL:
              ++scoresStrict[currentSuite.id].total;
              ++scoresStrict[currentSuite.id][currentClassID];
              ++scoresPartial[currentSuite.id].total;
              ++scoresPartial[currentSuite.id][currentClassID];
              beaconStrict.push(currentID + '=1');
              beaconPartial.push(currentID + '=1');
              break;

            case RESULT_SELECTION_DIFFS:
              ++scoresPartial[currentSuite.id].total;
              ++scoresPartial[currentSuite.id][currentClassID];
              beaconStrict.push(currentID + '=0');
              beaconPartial.push(currentID + '=1');
              break;
              
            default:
              beaconStrict.push(currentID + '=0');
              beaconPartial.push(currentID + '=0');
          }
          resetEditorElement();
          currentBackgroundShade = (currentBackgroundShade == 'Lo') ? 'Hi' : 'Lo';
        }

        outputTestClassScores();
      } catch (ex) {
        // An exception shouldn't really happen here!
        alert('Exception when running ' + currentClassID + ' tests of the suite "' +
              currentSuite.id + '" ("' + currentSuite.caption + '"): ' + ex.toString());
      }
    }

    outputTestSuiteScores();
    } catch (ex) {
      // An exception shouldn't really happen here!
     alert('Exception when running the suite "' + currentSuite.id +
          '" ("' + currentSuite.caption + '"): ' + ex.toString());
  }
}

