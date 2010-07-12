/**
 * @fileoverview 
 * Main functions used in running the RTE test suite.
 *
 * TODO: license! $$$
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
  return currentTest[param] === undefined ? currentSuite[param]
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

  // 2.) Run the test command or function.
  var cmd = getTestParameter(PARAM_COMMAND);
  if (cmd) {
    try {
      if (typeof cmd == 'string') {
        // Note: "getTestParameter(PARAM_VALUE) || null" doesn't work, since
        // value might be the empty string - e.g., for 'insertText'!
        var value = getTestParameter(PARAM_VALUE);
        if (value === undefined) {
          value = null;
        }
        editorDoc.execCommand(cmd, false, value);
      } else if (typeof cmd == 'function') {
        cmd();
      }
    } catch (ex) {
      var lvl = getTestParameter(PARAM_ALLOW_EXCEPTION)
                    ? RESULT_EQUAL 
                    : RESULT_EXECUTION_EXCEPTION;
      outputSingleTestResult('Exception: ' + ex.toString(), lvl);
      return lvl;
    }
  }

  // 3.) Verify test result.
  try {
    prepareTestResult();
    var lvl = compareTestResult();
    var output = canonicalizeElementsAndAttributes(currentResultHTML,
                                                   {emitAttrs:         true,
                                                    emitStyle:         true,
                                                    emitClass:         true,
                                                    emitID:            true,
                                                    lowercase:         false,
                                                    canonicalizeUnits: false});
    outputSingleTestResult(output, lvl);
    return lvl;
  } catch (ex) {
    outputSingleTestResult('Verification exception: ' + ex.toString(),
                           RESULT_VERIFICATION_EXCEPTION);
    return RESULT_VERIFICATION_EXCEPTION;
  }
}

/**
 * Runs a single test suite (such as DELETE tests or INSERT tests).
 *
 * @param {Object} suite as object reference
 */
function runTestSuite(suite) {
  currentSuite = suite;

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
    
    outputTestSuiteHeader();
  
    for (var cls = 0; cls < classCount; ++cls) {
      currentClassID = testClassIDs[cls];

      try {
        currentClass = currentSuite['tests' + currentClassID];
        if (!currentClass) {
          continue;
        }

        outputTestClassHeader();
        outputTestTableHeader();

        currentBackgroundShade = 'Lo';
        for (currentTestID in currentClass) {
          currentTest = currentClass[currentTestID];
          currentID = currentSuite.id + '-' + currentTestID;
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

/**
 * Runs all tests in all suites.
 */
function runTests() {
  initEditorDoc();

  // The test suites to be run.
  runTestSuite(SELECTION_TESTS);
  runTestSuite(APPLY_TESTS);
  runTestSuite(APPLY_TESTS_CSS);
  runTestSuite(UNAPPLY_TESTS);
  runTestSuite(UNAPPLY_TESTS_CSS);
  runTestSuite(CHANGE_TESTS);
  runTestSuite(CHANGE_TESTS_CSS);
  runTestSuite(DELETE_TESTS);
  runTestSuite(FORWARDDELETE_TESTS);
  runTestSuite(INSERT_TESTS);

  // Remove testing IFrame once all tests have finished.
  editorElem.parentNode.removeChild(editorElem);
}
