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
var EXECUTION_EXCEPTION           = 'EXCEPTION';
var VERIFICATION_EXCEPTION        = 'EXCEPTION DURING TEST VERIFICATION';

// Constants for indicating an exception in score handling.
var SCORE_EXCEPTION = 'EXCEPTION WHEN WRITING TEST SCORES';

// Exceptiona to be thrown on unsupported selection operations
var SELMODIFY_UNSUPPORTED      = 'UNSUPPORTED selection.modify()';
var SELALLCHILDREN_UNSUPPORTED = 'UNSUPPORTED selection.selectAllChildren()';

// HTML comparison result contants.
var RESULTHTML_SETUP_EXCEPTION        = 0;
var RESULTHTML_EXECUTION_EXCEPTION    = 1;
var RESULTHTML_VERIFICATION_EXCEPTION = 2;
var RESULTHTML_UNSUPPORTED            = 3;
var RESULTHTML_DIFFS                  = 4;
var RESULTHTML_ACCEPT                 = 6;  // HTML technically correct, but not ideal.
var RESULTHTML_EQUAL                  = 7;

// Selection comparison result contants.
var RESULTSEL_DIFF   = 0;
var RESULTSEL_NA     = 1;
var RESULTSEL_ACCEPT = 2;  // Selection is acceptable, but not ideal.
var RESULTSEL_EQUAL  = 3;

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
var PARAM_ACCEPT                = 'accept';
var PARAM_CHECK_ATTRIBUTES      = 'checkAttrs';
var PARAM_CHECK_STYLE           = 'checkStyle';
var PARAM_CHECK_CLASS           = 'checkClass';
var PARAM_CHECK_ID              = 'checkID';
var PARAM_STYLE_WITH_CSS        = 'styleWithCSS';
var PARAM_ALLOW_EXCEPTION       = 'allowException';

// ID suffixes for the output columns
var IDOUT_COMMAND    = '_:cmd';
var IDOUT_VALUE      = '_:val';
var IDOUT_CHECKATTRS = '_:att';
var IDOUT_CHECKSTYLE = '_:sty';
var IDOUT_STATUSHTML = '_:htm';
var IDOUT_STATUSSEL  = '_:sel';
var IDOUT_PAD        = '_:pad';
var IDOUT_EXPECTED   = '_:exp';
var IDOUT_ACTUAL     = '_:act';

// Output strings to use for yes/no/NA
var OUTSTR_YES = '&#x25CF;'; 
var OUTSTR_NO  = '&#x25CB;'; 
var OUTSTR_NA  = '-'; 

// DOM elements used for the tests.
var editorElem = null;
var editorWin  = null;
var editorDoc  = null;
var contentEditableElem = null;

// Helper variables to use in test functions
var win = null;  // window object to use for test functions
var doc = null;  // document object to use for test functions
var sel = null;  // The current selection after the pad is set up

// Variables holding the current suite and test for simplicity.
var currentSuite           = null;  // object specifiying the current test suite
var currentSuiteID         = '';    // ID of the current suite
var currentSuiteScoreID    = '';    // ID of the element showing the final score for the suite
var currentSuiteSelScoreID = '';    // ID of the element showing the final selection score for the suite
var currentClass           = null;  // sub-object of currentSuite, specifying the current class
var currentClassID         = '';    // ID string of the current class - one of testClasses, below
var currentClassScoreID    = '';    // ID of the element showing the final scores for the class
var currentClassSelScoreID = '';    // ID of the element showing the final selection scores for the class
var currentTest            = null;  // sub-object of currentClass, specifying the current test
var currentTestID          = '';    // ID of the current test
var currentActualHTML      = '';    // HTML string after executing the/all command(s)
var currentResultHTML      = 0;     // Result value (integer) for the actual HTML - see RESULTHTML_... above
var currentResultSelection = 0;     // Result value (integer) for the selection - see RESULTSEL_... above
var currentOutputTable     = null;  // HTML table for the current suite + class
var currentBackgroundShade = 'Hi';  // to facilitate alternating table row shading

// Classes of tests
var testClassIDs = ['Finalized', 'RFC', 'Proposed'];

// Dictionaries storing the numeric results.
var counts          = {};
var scoresHTML      = {};
var scoresSelection = {};

// Results - populated by the fillResults() function.
var categoryResults = [];
var beacon = [];

