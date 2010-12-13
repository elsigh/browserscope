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
 * @param suite {String} the test suite
 * @return {boolean} Whether the suite main focus is the output HTML/Text
 */
function suiteChecksHTMLOrText(suite) {
  return suite.id[0] != 'S';
}

/**
 * Info function: returns true if the suite checks the result selection.
 *
 * @param suite {String} the test suite
 * @return {boolean} Whether the suite checks the selection
 */
function suiteChecksSelection(suite) {
  return suite.id[0] != 'Q';
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
 * @param suite {String} the test suite
 * @param test {String} the test
 * @param param {String} the test parameter to be checked
 * @return {Any} the effective value of the parameter (can be undefined)
 */
function getParameter(suite, test, param) {
  var val = test[param];
  return (val === undefined) ? suite[param] : val;
}

/**
 * Initializes the global variables before any tests are run.
 */
function initVariables() {
  results = {
      count: 0,
      valscore: 0,
      selscore: 0
  };
}

/**
 * Runs a single test - outputs and sets the result variables.
 *
 * @param suite {Object} suite that test originates in as object reference
 * @param test {Object} test to be run as object reference
 * @param container {Object} container descriptor as object reference
 * @see variables.js for RESULT... values
 */
function runSingleTest(suite, test, container) {
  var result = {
    valscore: 0,
    selscore: 0,
    valresult: VALRESULT_NOT_RUN,
    selresult: SELRESULT_NOT_RUN,
    actual: ''
  };

  // 1.) Populate the editor element with the initial test setup HTML.
  try {
    initContainer(suite, test, container);
  } catch(ex) {
    result.valresult = VALRESULT_SETUP_EXCEPTION;
    result.selresult = SELRESULT_NA;
    result.actual = SETUP_EXCEPTION + ex.toString();
    return result;
  }

  // 2.) Run the test command, general function or query function.
  var isHTMLTest = false;

  try {
    var cmd = undefined;

    if (cmd = getParameter(suite, test, PARAM_EXECCOMMAND)) {
      isHTMLTest = true;
      // Note: "getParameter(suite, test, PARAM_VALUE) || null" doesn't work, since
      // value might be the empty string - e.g., for 'insertText'!
      var value = getParameter(suite, test, PARAM_VALUE);
      if (value === undefined) {
        value = null;
      }
      container.doc.execCommand(cmd, false, value);
    } else if (cmd = getParameter(suite, test, PARAM_FUNCTION)) {
      isHTMLTest = true;
      eval(cmd);
    } else if (cmd = getParameter(suite, test, PARAM_QUERYCOMMANDSUPPORTED)) {
      result.actual = container.doc.queryCommandSupported(cmd);
    } else if (cmd = getParameter(suite, test, PARAM_QUERYCOMMANDENABLED)) {
      result.actual = container.doc.queryCommandEnabled(cmd);
    } else if (cmd = getParameter(suite, test, PARAM_QUERYCOMMANDINDETERM)) {
      result.actual = container.doc.queryCommandIndeterm(cmd);
    } else if (cmd = getParameter(suite, test, PARAM_QUERYCOMMANDSTATE)) {
      result.actual = container.doc.queryCommandState(cmd);
    } else if (cmd = getParameter(suite, test, PARAM_QUERYCOMMANDVALUE)) {
      result.actual = container.doc.queryCommandValue(cmd);
      if (result.actual === false) {
        // A return value of boolean 'false' for queryCommandValue means 'not supported'.
        result.valresult = VALRESULT_UNSUPPORTED;
        result.selresult = SELRESULT_NA;
        result.actual = UNSUPPORTED;
        return result;
      }
    } else {
      result.valresult = VALRESULT_SETUP_EXCEPTION;
      result.selresult = SELRESULT_NA;
      result.actual = SETUP_EXCEPTION + SETUP_NOCOMMAND;
      return result;
    }
  } catch (ex) {
    result.valresult = VALRESULT_EXECUTION_EXCEPTION;
    result.selresult = SELRESULT_NA;
    result.actual = EXECUTION_EXCEPTION + ex.toString();
    return result;
  }
  
  // 3.) Get HTML in case of execCommand or function tests
  try {
    if (isHTMLTest) {
      prepareHTMLTestResult(container, result);
    }
  } catch (ex) {
    result.valresult = VALRESULT_VERIFICATION_EXCEPTION;
    result.selresult = SELRESULT_NA;
    result.actual = VERIFICATION_EXCEPTION + ex.toString();
    return result;
  }

  // 4.) Verify test result
  try {
    if (isHTMLTest) {
      // Verify canaries (if any)
      if (result.outer) {
        verifyCanaries(result.outer, container, result);
      }

      // Compare result to expectations
      // Remove text node markers for comparison for this purpose.
      var actual = result.actual.replace(/[\x60\xb4]/g, '');
      var cmp = compareHTMLTestResult(suite, test, actual);

      // Set result values only if they haven't been set by the canary test.
      if (result.valresult === VALRESULT_NOT_RUN) {
        result.valresult = cmp.valresult;
      }
      if (result.selresult === SELRESULT_NOT_RUN) {
        result.selresult = cmp.selresult;
      }
      result.valscore = (result.valresult === VALRESULT_EQUAL) ? 1 : 0;
      result.selscore = (result.selresult === SELRESULT_EQUAL) ? 1 : 0;
    } else {
      result.valresult = compareTextTestResult(suite, test, result.actual);
      result.selresult = SELRESULT_NA;
      result.valscore = (result.valresult === VALRESULT_EQUAL) ? 1 : 0;
    }
  } catch (ex) {
    result.valresult = VALRESULT_VERIFICATION_EXCEPTION;
    result.selresult = SELRESULT_NA;
    result.actual = VERIFICATION_EXCEPTION + ex.toString();
    return result;
  }
  
  return result;
}

/**
 * Initializes the results dictionary for a given test suite.
 * (for all classes -> tests -> containers)
 *
 * @param {Object} suite as object reference
 */
function initTestSuiteResults(suite) {
  var suiteID = suite.id;

  // Initialize results entries for this suite
  results[suiteID] = {
      count: 0,
      valscore: 0,
      selscore: 0,
      time: 0
  };
  var totalTestCount = 0;
  for (var clsIdx = 0; clsIdx < testClassCount; ++clsIdx) {
    var clsID = testClassIDs[clsIdx];
    var cls = suite[clsID];
    if (!cls)
      continue;

    var testCount = cls.length;

    results[suiteID][clsID] = {
        count: testCount,
        valscore: 0,
        selscore: 0
    };
    totalTestCount += testCount;

    for (var testIdx = 0; testIdx < testCount; ++testIdx) {
      var test = cls[testIdx];
      var testID = generateTestID(suiteID, test.id);
      
      results[suiteID][clsID ][testID] = {
          valscore: 0,
          selscore: 0,
          valresult: VALRESULT_NOT_RUN,
          selresult: SELRESULT_NOT_RUN
      };
      for (var cntIdx = 0; cntIdx < containerCount; ++cntIdx) {
        var cntID = containerIDs[cntIdx];

        results[suiteID][clsID][testID][cntID] = {
          valscore: 0,
          selscore: 0,
          valresult: VALRESULT_NOT_RUN,
          selresult: SELRESULT_NOT_RUN,
          actual: ''
        }
      }
    }
  }
  results[suiteID].count = totalTestCount;
}

/**
 * Runs a single test suite (such as DELETE tests or INSERT tests).
 *
 * @param suite {Object} suite as object reference
 */
function runTestSuite(suite) {
  var suiteID = suite.id;
  var suiteStartTime = new Date().getTime();

  initTestSuiteResults(suite);

  for (var clsIdx = 0; clsIdx < testClassCount; ++clsIdx) {
    var clsID = testClassIDs[clsIdx];
    var cls = suite[clsID];
    if (!cls)
      continue;

    var testCount = cls.length;

    for (var testIdx = 0; testIdx < testCount; ++testIdx) {
      var test = cls[testIdx];
      var testID = generateTestID(suiteID, test.id);

      var valscore = 1;
      var selscore = 1;
      var valresult = VALRESULT_EQUAL;
      var selresult = SELRESULT_EQUAL;

      for (var cntIdx = 0; cntIdx < containerCount; ++cntIdx) {
        var cntID = containerIDs[cntIdx];
        var container = containers[cntID];

        var result = runSingleTest(suite, test, container);

        results[suiteID][clsID][testID][cntID] = result;

        valscore = Math.min(valscore, result.valscore);
         selscore = Math.min(selscore, result.selscore);
        valresult = Math.min(valresult, result.valresult);
        selresult = Math.min(selresult, result.selresult);
      }          

      results[suiteID][clsID][testID].valscore = valscore;
      results[suiteID][clsID][testID].selscore = selscore;
      results[suiteID][clsID][testID].valresult = valresult;
      results[suiteID][clsID][testID].selresult = selresult;

      results[suiteID][clsID].valscore += valscore;
      results[suiteID][clsID].selscore += selscore;
      results[suiteID].valscore += valscore;
      results[suiteID].selscore += selscore;
      results.valscore += valscore;
      results.selscore += selscore;
    }
  }

  results[suiteID].time = new Date().getTime() - suiteStartTime;
}

/**
 * Runs a single test suite (such as DELETE tests or INSERT tests)
 * and updates the output HTML.
 *
 * @param {Object} suite as object reference
 */
function runAndOutputTestSuite(suite) {
  runTestSuite(suite);
  outputTestSuiteResults(suite);
}

/**
 * Fills the beacon with the test results.
 */
function fillResults() {
  // Result totals of the individual categories
  categoryTotals = [
    'selection='        + results['S'].selscore,
    'apply='            + results['A'].valscore,
    'applyCSS='         + results['AC'].valscore,
    'change='           + results['C'].valscore,
    'changeCSS='        + results['CC'].valscore,
    'unapply='          + results['U'].valscore,
    'unapplyCSS='       + results['UC'].valscore,
    'delete='           + results['D'].valscore,
    'forwarddelete='    + results['FD'].valscore,
    'insert='           + results['I'].valscore,
    'selectionResult='  + (results['A'].selscore +
                           results['AC'].selscore +
                           results['C'].selscore +
                           results['CC'].selscore +
                           results['U'].selscore +
                           results['UC'].selscore +
                           results['D'].selscore +
                           results['FD'].selscore +
                           results['I'].selscore),
    'querySupported='   + results['Q'].valscore,
    'queryEnabled='     + results['QE'].valscore,
    'queryIndeterm='    + results['QI'].valscore,
    'queryState='       + results['QS'].valscore,
    'queryStateCSS='    + results['QSC'].valscore,
    'queryValue='       + results['QV'].valscore,
    'queryValueCSS='    + results['QVC'].valscore
  ];
  
  // Beacon copies category results
  beacon = categoryTotals.slice(0);
}

