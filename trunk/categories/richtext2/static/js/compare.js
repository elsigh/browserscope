/**
 * @fileoverview 
 * Comparison functions used in the RTE test suite.
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
 * constants used only in the compare functions. 
 */
var RESULT_DIFF  = 0;  // actual result doesn't match expectation
var RESULT_SEL   = 1;  // actual result matches expectation in HTML only
var RESULT_EQUAL = 2;  // actual result matches expectation in both HTML and selection

/**
 * Compare a test result to a single expectation string.
 *
 * FIXME: add support for optional elements/attributes.
 *
 * @param expected {String} the already canonicalized (with the exception of selection marks) expectation string
 * @param actual {String} the already canonicalized (with the exception of selection marks) actual result
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareHTMLTestResultToSingleHTMLExpectation(expected, actual) {
  // If the test checks the selection, then the actual string must match the
  // expectation exactly.
  if (expected == actual) {
    return RESULT_EQUAL;
  }

  // Remove selection markers and see if strings match then.
  expected = expected.replace(/ [{}\|]>/g, '>');     // intra-tag
  expected = expected.replace(/[\[\]\^{}\|]/g, '');  // outside tag
  actual = actual.replace(/ [{}\|]>/g, '>');         // intra-tag
  actual = actual.replace(/[\[\]\^{}\|]/g, '');      // outside tag

  return (expected == actual) ? RESULT_SEL : RESULT_DIFF;
}

/**
 * Gets the test expectations as an array from the passed-in field.
 *
 * @param {Array|String} the test expectation(s) as string or array.
 * @return {Array} test expectations as an array.
 */
function getExpectationArray(expected) {
  // Treat a single test expectation string or bool as an array of 1 expectation.
  switch (typeof expected) {
    case 'string':
    case 'boolean':
      return [expected];
  }
  return expected;
}

/**
 * Compare the current HTMLtest result to the expectation string(s).
 *
 * @param {String/Boolean} actual value
 * @param {String/Array} expectation(s)
 * @param {Object} flags to use for canonicalization
 * @return {Integer} one of the RESULT_... return values
 * @see variables.js for return values
 */
function compareHTMLTestResultWith(actual, expected, emitFlags) {
  // Find the most favorable result among the possible expectation strings.
  var expectedArr  = getExpectationArray(expected);
  var count = expectedArr.length;
  var best = RESULT_DIFF;
  for (var idx = 0; idx < count; ++idx) {
    var expected = canonicalizeSpaces(expectedArr[idx]);
    expected = canonicalizeElementsAndAttributes(expected, emitFlags);
    var result = compareHTMLTestResultToSingleHTMLExpectation(expected, actual);
    if (result == RESULT_EQUAL) {
      // Shortcut: it doesn't get any better.
      return RESULT_EQUAL;
    }
    if (result > best) {
      best = result;
    }
  }
  return best;
}

/**
 * Compare the current HTMLtest result to the expectation string(s).
 * Sets the global result variables.
 *
 * @see variables.js for result values
 */
function compareHTMLTestResult() {
  var emitFlags = {emitAttrs:         getTestParameter(PARAM_CHECK_ATTRIBUTES),
                   emitStyle:         getTestParameter(PARAM_CHECK_STYLE),
                   emitClass:         getTestParameter(PARAM_CHECK_CLASS),
                   emitID:            getTestParameter(PARAM_CHECK_ID),
                   lowercase:         true,
                   canonicalizeUnits: true};
  
  var actual = currentActualHTML;
  // Remove closing tags </hr>, </br> for comparison.
  actual = actual.replace(/<\/[hb]r>/g, '');
  // Remove text node markers for comparison.
  actual = actual.replace(/[\x60\xb4]/g, '');
  // Canonicalize result.
  actual = canonicalizeElementsAndAttributes(actual, emitFlags);

  var expected = getTestParameter(PARAM_EXPECTED);
  var bestExpected = compareHTMLTestResultWith(actual, expected, emitFlags);
  if (bestExpected == RESULT_EQUAL) {
    // Shortcut - it doesn't get any better 
    currentResultHTML      = RESULTHTML_EQUAL;
    currentResultSelection = RESULTSEL_EQUAL;
    return;
  }
  var accepted = getTestParameter(PARAM_ACCEPT);
  var bestAccepted = accepted ? compareHTMLTestResultWith(actual, accepted, emitFlags)
                              : RESULT_DIFF;
  switch (bestExpected) {
    case RESULT_SEL:
      switch (bestAccepted) {
        case RESULT_EQUAL:
          // Since the HTML was equal on the/an expected result,
          // it has to be equal with the accepted result as well.
          // Therefore, the difference can only lie in the selection.
          currentResultHTML      = RESULTHTML_EQUAL;
          currentResultSelection = RESULTSEL_ACCEPT;
          break;

        case RESULT_SEL:
          // Since the HTML was equal on the/an expected result,
          // it has to be equal with the accepted result as well.
          // The selection however, matches neither.
          currentResultHTML      = RESULTHTML_EQUAL;
          currentResultSelection = RESULTSEL_DIFF;
          break;

        case RESULT_DIFF:
        default:
          // The acceptable expectations all have different HTML
          // -> stay with the original result.
          currentResultHTML      = RESULTHTML_EQUAL;
          currentResultSelection = RESULTSEL_DIFF;
          break;
      }
      break;

    case RESULT_DIFF:
    default:
      switch (bestAccepted) {
        case RESULT_EQUAL:
          currentResultHTML      = RESULTHTML_ACCEPT;
          currentResultSelection = RESULTSEL_EQUAL;
          break;

        case RESULT_SEL:
          currentResultHTML      = RESULTHTML_ACCEPT;
          currentResultSelection = RESULTSEL_DIFF;
          break;

        default:
          currentResultHTML      = RESULTHTML_DIFFS;
          currentResultSelection = RESULTSEL_NA;
          break;
      }
      break;
  }
}

/**
 * Compare a text test result to the expectation string(s).
 *
 * @param {String/Boolean} actual value
 * @param {String/Array} expectation(s)
 * @return {Boolean} whether we found a match
 */
function compareTextTestResultWith(actual, expected) {
  var expectedArr = getExpectationArray(expected);
  // Find the most favorable result among the possible expectation strings.
  var count = expectedArr.length;

  // If the value matches the expectation exactly, then we're fine.  
  for (var idx = 0; idx < count; ++idx) {
    if (actual === expectedArr[idx])
      return true;
  }
  
  // Otherwise see if we should canonicalize specific value types.
  //
  // We only need to look at font name, color and size units if the originating
  // test was both a) queryCommandValue and b) querying a font name/color/size
  // specific criterion.
  //
  // TODO(rolandsteiner): This is ugly! Refactor!
  switch (getTestParameter(PARAM_QUERYCOMMANDVALUE)) {
    case 'backcolor':
    case 'forecolor':
    case 'hilitecolor':
      for (var idx = 0; idx < count; ++idx) {
        if (new Color(actual).compare(new Color(expectedArr[idx])))
          return true;
      }
      return false;
    
    case 'fontname':
      for (var idx = 0; idx < count; ++idx) {
        if (new FontName(actual).compare(new FontName(expectedArr[idx])))
          return true;
      }
      return false;
    
    case 'fontsize':
      for (var idx = 0; idx < count; ++idx) {
        if (new FontSize(actual).compare(new FontSize(expectedArr[idx])))
          return true;
      }
      return false;
  }
  
  return false;
}

/**
 * Compare the passed-in text test result to the expectation string(s).
 * Sets the global result variables.
 *
 * @param {String/Boolean} actual value
 * @see variables.js for result values
 */
function compareTextTestResult(actual) {
  var expected = getTestParameter(PARAM_EXPECTED);
  if (compareTextTestResultWith(actual, expected)) {
    currentResultHTML = RESULTHTML_EQUAL;
    return;
  }
  var accepted = getTestParameter(PARAM_ACCEPT);
  if (accepted && compareTextTestResultWith(actual, accepted)) {
    currentResultHTML = RESULTHTML_ACCEPT;
    return;
  }
  currentResultHTML = RESULTHTML_DIFFS;
}

/**
 * Insert a selection position indicator.
 *
 * @param node {DOMNode} the node where to insert the selection indicator
 * @param offs {Integer} the offset of the selection indicator
 * @param textInd {String}  the indicator to use if the node is a text node
 * @param elemInd {String}  the indicator to use if the node is an element node
 */
function insertSelectionIndicator(node, offs, textInd, elemInd) {
  switch (node.nodeType) {
    case DOM_NODE_TYPE_TEXT:
      // Insert selection marker for text node into text content.
      var text = node.data;
      node.data = text.substring(0, offs) + textInd + text.substring(offs);
      break;
      
    case DOM_NODE_TYPE_ELEMENT:
      var child = node.firstChild;
      try {
        // node has other children: insert marker as comment node
        var comment = document.createComment(elemInd);
        while (child && offs) {
          --offs;
          child = child.nextSibling;
        }
        if (child) {
          node.insertBefore(comment, child);
        } else {
          node.appendChild(comment);
        }
      } catch (ex) {
        // can't append child comment -> insert as special attribute(s)
        switch (elemInd) {
          case '|':
            node.setAttribute(ATTRNAME_SEL_START, '1');
            node.setAttribute(ATTRNAME_SEL_END, '1');
            break;

          case '{':
            node.setAttribute(ATTRNAME_SEL_START, '1');
            break;

          case '}':
            node.setAttribute(ATTRNAME_SEL_END, '1');
            break;
        }
      }
      break;
  }
}

/**
 * Retrieve the result of a test run and do some preliminary canonicalization.
 */
function prepareTestResult() {
  // 1.) insert selection markers
  var selRange = createFromWindow(editorWin);
  if (selRange) {
    // save values, since range object gets auto-modified
    var node1 = selRange.getAnchorNode();
    var offs1 = selRange.getAnchorOffset();
    var node2 = selRange.getFocusNode();
    var offs2 = selRange.getFocusOffset();
    // do some sanity checking
    if (node1 != contentEditableElem && !goog.dom.contains(contentEditableElem, node1)) {
      node1 = null;
      offs1 = 0;
    }
    if (node2 != contentEditableElem && !goog.dom.contains(contentEditableElem, node2)) {
      node2 = null;
      offs2 = 0;
    }
    // add markers
    if (node1 && node1 == node2 && offs1 == offs2) {
      // collapsed selection
      insertSelectionIndicator(node1, offs1, '^', '|');
    } else {
      // Start point and end point are different
      if (node1) {
        insertSelectionIndicator(node1, offs1, '[', '{');
      }

      if (node2) {
        if (node1 == node2 && offs1 < offs2) {
          // Anchor indicator was inserted under the same node, so we need
          // to shift the offset by 1
          ++offs2;
        }
        insertSelectionIndicator(node2, offs2, ']', '}');
      }
    }
  }

  // 2.) insert markers for text node boundaries;
  encloseTextNodesWithQuotes(contentEditableElem);
  
  // 3.) retrieve innerHTML, canonicalize spacing
  currentActualHTML = canonicalizeSpaces(contentEditableElem.innerHTML);

  // 4a.) remove comment start and end comment tags, retain only {, } and |
  currentActualHTML = currentActualHTML.replace(/ ?<!-- ?/g, '');
  currentActualHTML = currentActualHTML.replace(/ ?--> ?/g, '');
}

