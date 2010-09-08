/**
 * @fileoverview 
 * Common constants and variables used in the RTE test suite.
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

// Constant for indicating a test setup is unsupported or incorrect
// (threw exception).
var SETUP_BAD_SELECTION_SPEC  = 'BAD SELECTION SPECIFICATION IN TEST OR EXPECTATION STRING';
var SETUP_HTML_EXCEPTION      = 'EXCEPTION WHEN SETTING TEST HTML';
var SETUP_SELECTION_EXCEPTION = 'EXCEPTION WHEN SETTING SELECTION';
var SETUP_NOCOMMAND_EXCEPTION = 'NO COMMAND, GENERAL FUNCTION OR QUERY FUNCTION GIVEN';

// Constants for indicating a test action is unsupported (threw exception).
var UNSUPPORTED_COMMAND_EXCEPTION = 'UNSUPPORTED COMMAND';
var VERIFICATION_EXCEPTION        = 'EXCEPTION DURING TEST VERIFICATION';

// Constants for indicating an exception in score handling.
var SCORE_EXCEPTION = 'EXCEPTION WHEN WRITING TEST SCORES';

// Selection comparison result contants.
var RESULT_SETUP_EXCEPTION        = 0;
var RESULT_EXECUTION_EXCEPTION    = 1;
var RESULT_VERIFICATION_EXCEPTION = 2;
var RESULT_UNSUPPORTED            = 3;
var RESULT_DIFFS                  = 4;
var RESULT_SELECTION_DIFFS        = 5;
var RESULT_EQUAL                  = 6;

// Special attributes used to mark selections within elements that otherwise
// have no children. Important: attribute name MUST be lower case!
var ATTRNAME_SEL_START = 'bsselstart';
var ATTRNAME_SEL_END   = 'bsselend';

// DOM node type constants.
var DOM_NODE_TYPE_ELEMENT = 1;
var DOM_NODE_TYPE_TEXT    = 3;
var DOM_NODE_TYPE_COMMENT = 8;

// Test parameter names
var PARAM_DESCRIPTION           = 'desc';
var PARAM_PAD                   = 'pad';
var PARAM_COMMAND               = 'command';
var PARAM_FUNCTION              = 'function';
var PARAM_QUERYCOMMANDSUPPORTED = 'qcsupported';
var PARAM_QUERYCOMMANDENABLED   = 'qcenabled';
var PARAM_QUERYCOMMANDINDETERM  = 'qcindeterm';
var PARAM_QUERYCOMMANDSTATE     = 'qcstate';
var PARAM_QUERYCOMMANDVALUE     = 'qcvalue';
var PARAM_VALUE                 = 'value';
var PARAM_EXPECTED              = 'expected';
var PARAM_CHECK_ATTRIBUTES      = 'checkAttrs';
var PARAM_CHECK_STYLE           = 'checkStyle';
var PARAM_CHECK_CLASS           = 'checkClass';
var PARAM_CHECK_ID              = 'checkID';
var PARAM_CHECK_SELECTION       = 'checkSel';
var PARAM_STYLE_WITH_CSS        = 'styleWithCSS';
var PARAM_ALLOW_EXCEPTION       = 'allowException';

// DOM elements used for the tests.
var editorElem = null;
var editorWin  = null;
var editorDoc  = null;
var contentEditableElem = null;

// Variables holding the current suite and test for simplicity.
var currentSuite           = null;  // object specifiying the current test suite
var currentSuiteScoreID    = '';    // ID of the element showing the final scores for the suite
var currentClass           = null;  // sub-object of currentSuite, specifying the current class
var currentClassID         = '';    // ID string of the current class - one of testClasses, below
var currentClassScoreID    = '';    // ID of the element showing the final scores for the class
var currentTest            = null;  // sub-object of currentClass, specifying the current test
var currentIDpartial       = '';    // totally unique ID for non-strict tests
var currentIDStrict        = '';    // totally unique ID for strict tests
var currentResultHTML      = '';    // HTML string after executing the/all command(s)
var currentOutputTable     = null;  // HTML table for the current suite + class
var currentBackgroundShade = 'Lo';  // to facilitate alternating table row shading

// Classes of tests
var testClassIDs = ['Finalized', 'RFC', 'Proposed'];

// Dictionaries storing the numeric results.
var counts        = {};
var scoresStrict  = {};
var scoresPartial = {};

// Beacon results (seed, or the beacon will fail).
var beacon = ['selection=0',
              'apply=0',
              'applySel=0',
              'applyCSS=0',
              'applyCSSSel=0',
              'change=0',
              'changeSel=0',
              'changeCSS=0',
              'changeCSSSel=0',
              'unapply=0',
              'unapplySel=0',
              'unapplyCSS=0',
              'unapplyCSSSel=0',
              'delete=0',
              'deleteSel=0',
              'forwarddelete=0',
              'forwarddeleteSel=0',
              'insert=0',
              'insertSel=0',

              'querySupported=0',
              'queryEnabled=0',
              'queryEnabledCSS=0',
              'queryInd=0',
              'queryIndCSS=0',
              'queryState=0',
              'queryStateCSS=0',
              'queryValue=0',
              'queryValueCSS=0'];
